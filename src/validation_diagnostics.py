"""Explain frozen configurations on training/validation only.

Run: python -m src.validation_diagnostics
RF grouped permutation uses an estimator fitted only on fold 5 training rows.
MLP seed and epoch checks are diagnostics, not replacement model selection.
"""

import argparse
import importlib.metadata
import json
import os
import platform
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.exceptions import ConvergenceWarning
from threadpoolctl import threadpool_limits

from src.artifacts import load_saved_model, resolve_model_paths, sha256_file
from src.data_loader import DEFAULT_DATA_PATH, PROJECT_ROOT, TEST_START, cv_folds, load_data, time_split
from src.evaluation import regression_metrics
from src.features import FEATURE_COLUMNS, add_features, split_xy

FEATURE_GROUPS = {
    "current_pm25": ["PM2.5"],
    "pm25_lags_rolling": [c for c in FEATURE_COLUMNS if c.startswith("PM2.5_")],
    "other_pollutants": ["PM10", "SO2", "NO2", "CO", "O3"],
    "weather": ["TEMP", "PRES", "DEWP", "RAIN", "WSPM", "wd"],
    "time": [c for c in FEATURE_COLUMNS if c.endswith(("_sin", "_cos"))],
    "station": ["station"],
}


def group_permutation_importance(model, X, y, groups=FEATURE_GROUPS, n_repeats=5, seed=42):
    if n_repeats < 1:
        raise ValueError("n_repeats must be positive.")
    if sorted(c for cols in groups.values() for c in cols) != sorted(X.columns):
        raise ValueError("Feature groups must partition the input columns.")
    rng = np.random.default_rng(seed)
    with threadpool_limits(limits=1):
        baseline = regression_metrics(y, model.predict(X))["rmse"]
        rows = []
        for group, columns in groups.items():
            increases = []
            for _ in range(n_repeats):
                shuffled = X.copy()
                shuffled.loc[:, columns] = X[columns].iloc[rng.permutation(len(X))].to_numpy()
                increases.append(regression_metrics(y, model.predict(shuffled))["rmse"] - baseline)
            rows.append({
                "feature_group": group, "baseline_sample_rmse": baseline,
                "rmse_increase_mean": float(np.mean(increases)),
                "rmse_increase_std": float(np.std(increases, ddof=0)),
                "n_repeats": n_repeats, "n_validation_sample": len(X), "seed": seed,
            })
    return pd.DataFrame(rows).sort_values("rmse_increase_mean", ascending=False, ignore_index=True)


def _fit_mlp(template, X_train, y_train, X_val, y_val, seed, max_iter):
    model = clone(template).set_params(
        model__regressor__random_state=seed, model__regressor__max_iter=max_iter)
    with threadpool_limits(limits=1), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(X_train, y_train)
        scores = regression_metrics(y_val, model.predict(X_val))
        train_rmse = regression_metrics(y_train, model.predict(X_train))["rmse"]
    for warning in caught:
        if not issubclass(warning.category, ConvergenceWarning):
            warnings.warn(warning.message, warning.category)
    estimator = model.named_steps["model"].regressor_
    return {
        **scores, "train_rmse": train_rmse, "seed": seed, "max_iter": max_iter,
        "epochs": int(estimator.n_iter_),
        "convergence_warning": any(issubclass(w.category, ConvergenceWarning) for w in caught),
    }, list(estimator.loss_curve_)


def run_diagnostics(output_dir=None, seeds=(7, 42, 2026), n_repeats=5, return_tables=False):
    import matplotlib.pyplot as plt

    output_dir = Path(output_dir or PROJECT_ROOT / "outputs" / "experiments" / "validation_diagnostics")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = resolve_model_paths()
    # Preserve full hourly rows for lags; only labeled train/validation enters any fit/score.
    featured = add_features(load_data()).dropna(subset=["target"]).reset_index(drop=True)
    train_validation, _ = time_split(featured)
    train_validation = train_validation.reset_index(drop=True)
    if not train_validation.target_datetime.max() < TEST_START:
        raise ValueError("Test labels must not enter validation diagnostics.")
    X, y = split_xy(train_validation)
    folds = cv_folds(train_validation)
    train_idx, val_idx = folds[-1]
    rf = clone(load_saved_model("random_forest_tuned", paths["random_forest_tuned"]))
    with threadpool_limits(limits=1):
        rf.fit(X.iloc[train_idx], y.iloc[train_idx])
    sample_idx = np.sort(np.random.default_rng(42).choice(
        val_idx, size=min(30000, len(val_idx)), replace=False))
    importance = group_permutation_importance(
        rf, X.iloc[sample_idx].reset_index(drop=True), y.iloc[sample_idx].reset_index(drop=True),
        n_repeats=n_repeats)
    importance.insert(0, "model", "Random Forest - tuned; refitted on fold 5 training only")
    importance.insert(1, "fold", 5)
    importance.to_csv(output_dir / "rf_group_permutation_importance.csv", index=False, encoding="utf-8-sig")
    fig, ax = plt.subplots(figsize=(9, 5))
    view = importance.iloc[::-1]
    ax.barh(view.feature_group, view.rmse_increase_mean, xerr=view.rmse_increase_std)
    ax.set(xlabel="Validation RMSE increase (µg/m³)", title="RF grouped permutation importance, fold 5")
    fig.tight_layout()
    fig.savefig(output_dir / "rf_group_permutation_importance.png", dpi=150)
    plt.close(fig)
    print("RF validation importance complete.", flush=True)

    template = load_saved_model("mlp_tuned", paths["mlp_tuned"])
    configured_limit = template.get_params()["model__regressor__max_iter"]
    rows, curves = [], []
    for seed in seeds:
        for fold, (tr, va) in enumerate(folds, 1):
            scores, losses = _fit_mlp(template, X.iloc[tr], y.iloc[tr], X.iloc[va], y.iloc[va],
                                       seed, configured_limit)
            rows.append({"diagnostic": "seed_stability", "fold": fold, **scores})
            curves.extend({"diagnostic": "seed_stability", "fold": fold, "seed": seed,
                           "max_iter": configured_limit, "epoch": epoch, "loss_scaled_target": loss}
                          for epoch, loss in enumerate(losses, 1))
            print(f"MLP seed={seed}, fold={fold}: RMSE={scores['rmse']:.4f}", flush=True)
    # Check capped folds at the original seed; do not persist or select a new final model.
    for fold, (tr, va) in enumerate(folds[:2], 1):
        scores, losses = _fit_mlp(template, X.iloc[tr], y.iloc[tr], X.iloc[va], y.iloc[va],
                                   42, max(100, configured_limit))
        rows.append({"diagnostic": "epoch_limit_check", "fold": fold, **scores})
        curves.extend({"diagnostic": "epoch_limit_check", "fold": fold, "seed": 42,
                       "max_iter": max(100, configured_limit), "epoch": epoch, "loss_scaled_target": loss}
                      for epoch, loss in enumerate(losses, 1))
    metrics = pd.DataFrame(rows)
    metrics.to_csv(output_dir / "mlp_validation_diagnostics.csv", index=False, encoding="utf-8-sig")
    losses = pd.DataFrame(curves)
    losses.to_csv(output_dir / "mlp_loss_curves.csv", index=False, encoding="utf-8-sig")
    summary = metrics.loc[metrics.diagnostic.eq("seed_stability")].groupby("seed")[
        ["mae", "rmse", "r2"]].mean().reset_index()
    summary.to_csv(output_dir / "mlp_seed_summary.csv", index=False, encoding="utf-8-sig")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for fold, ax in enumerate(axes, 1):
        part = losses.loc[losses.fold.eq(fold) & losses.seed.eq(42)]
        for label, group in part.groupby("diagnostic"):
            ax.plot(group.epoch, group.loss_scaled_target, label=label)
        ax.set(title=f"MLP fold {fold}", xlabel="Epoch", ylabel="Training loss (scaled target)")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "mlp_convergence.png", dpi=150)
    plt.close(fig)
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "operator": os.environ.get("EXPERIMENT_OPERATOR"),
        "operator_note": "Not inferred from account, Git author or machine name.",
        "python_version": platform.python_version(),
        "packages": {p: importlib.metadata.version(p) for p in
                     ["numpy", "pandas", "scikit-learn", "scipy", "joblib", "threadpoolctl"]},
        "scope": "train/validation only; test labels not scored; final joblib files not replaced",
        "feature_columns": list(FEATURE_COLUMNS), "seeds": list(seeds),
        "dataset_sha256": sha256_file(DEFAULT_DATA_PATH),
        "fold_5_train_target_end": str(train_validation.iloc[train_idx].target_datetime.max()),
        "fold_5_validation_target_start": str(train_validation.iloc[val_idx].target_datetime.min()),
        "feature_importance": {"sample_size": len(sample_idx), "n_repeats": n_repeats, "seed": 42,
                               "limitations": "correlated features; model dependence, not causality"},
        "mlp": {"configured_max_iter": configured_limit,
                "epoch_diagnostic_max_iter": max(100, configured_limit),
                "loss_scale": "MLP objective on training-standardized target; not µg/m³ RMSE",
                "model_selection": "no replacement configuration selected by this diagnostic"},
    }
    (output_dir / "diagnostics_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if return_tables:
        return {"rf_group_permutation_importance.csv": importance,
                "mlp_validation_diagnostics.csv": metrics,
                "mlp_seed_summary.csv": summary, "mlp_loss_curves.csv": losses}
    return importance, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    importance, metrics = run_diagnostics(args.output_dir)
    print(importance.to_string(index=False))
    print(metrics.groupby(["diagnostic", "seed"]).rmse.mean().to_string())


if __name__ == "__main__":
    main()
