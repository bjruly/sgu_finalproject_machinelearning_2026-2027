"""Reproduce fixed-model test scores, grouped errors and paired block intervals.

This module never tunes estimators or selects hyperparameters from test scores.
Run: python -m src.evaluation
"""

import argparse
import importlib.metadata
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from threadpoolctl import threadpool_limits

from src.artifacts import MODEL_LABELS, load_saved_model, metadata_path, resolve_model_paths, sha256_file
from src.analysis_groups import PM25_BINS, PM25_LABELS, pm25_levels
from src.data_loader import DEFAULT_DATA_PATH, PROJECT_ROOT, TEST_START, load_data, time_split
from src.features import FEATURE_COLUMNS, FFILL_LIMIT, add_features, split_xy

SEASONS = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring",
           5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn",
           10: "Autumn", 11: "Autumn"}
PREDICTION_COLUMNS = [f"pred_{key}" for key in MODEL_LABELS]


def regression_metrics(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape or not y_true.size:
        raise ValueError("Targets and predictions must have the same non-empty shape.")
    if not np.isfinite(y_true).all() or not np.isfinite(y_pred).all():
        raise ValueError("Targets and predictions must be finite.")
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)) if y_true.size > 1 else np.nan,
        "mean_residual": float(np.mean(y_true - y_pred)),
    }


def predict_test(test, train_validation, model_paths):
    """Predict the same station-hour keys with every frozen model."""
    test = test.reset_index(drop=True)
    X, y = split_xy(test)
    result = test[["station", "datetime", "target_datetime"]].copy()
    result["y_true"] = y.to_numpy()
    result["pred_baseline_persistence"] = X["PM2.5"].fillna(
        float(train_validation["target"].median())
    ).to_numpy()
    for key, path in model_paths.items():
        with threadpool_limits(limits=1):
            model = load_saved_model(key, path)
            result[f"pred_{key}"] = np.asarray(model.predict(X)).ravel()
    if result.duplicated(["station", "target_datetime"]).any():
        raise ValueError("Duplicate station-target timestamp keys.")
    if not np.isfinite(result[["y_true", *PREDICTION_COLUMNS]].to_numpy()).all():
        raise ValueError("Invalid predictions.")
    return result


def summarize_predictions(predictions):
    rows = []
    for key, label in MODEL_LABELS.items():
        scores = regression_metrics(predictions.y_true, predictions[f"pred_{key}"])
        rows.append({
            "experiment_id": f"{key}_test", "model": label,
            **{k: scores[k] for k in ("mae", "rmse", "r2")}, "n_test": len(predictions),
        })
    metrics = pd.DataFrame(rows).sort_values("rmse", kind="stable", ignore_index=True)
    metrics.insert(0, "rank", metrics.rmse.rank(method="min").astype(int))
    return metrics


def trimmed_sensitivity(predictions, fractions=(0.0, 0.001, 0.005, 0.01)):
    """Sensitivity of the model ranking to the largest-error rows (report only).

    Rule fixed in advance: rank rows by the mean absolute error across all
    models, drop the top ``fraction`` of rows (the same rows for every model),
    and recompute the metrics. It never selects or changes a model.
    """
    pooled = np.mean([(predictions.y_true - predictions[c]).abs() for c in PREDICTION_COLUMNS], axis=0)
    order = np.argsort(-pooled, kind="stable")
    rows = []
    for fraction in fractions:
        if not 0 <= fraction < 1:
            raise ValueError("fractions must be in [0, 1).")
        kept = predictions.iloc[np.sort(order[int(round(len(predictions) * fraction)):])]
        part = []
        for key, label in MODEL_LABELS.items():
            scores = regression_metrics(kept.y_true, kept[f"pred_{key}"])
            part.append({"trimmed_fraction": fraction, "n_removed": len(predictions) - len(kept),
                         "n_kept": len(kept), "model": label, "mae": scores["mae"], "rmse": scores["rmse"]})
        part = pd.DataFrame(part)
        part["rank_by_rmse"] = part.rmse.rank(method="min").astype(int)
        rows.append(part)
    return pd.concat(rows, ignore_index=True)


def grouped_errors(predictions, group):
    """All concentration groups are right-closed, including exact thresholds."""
    frame = predictions.copy()
    times = pd.to_datetime(frame.target_datetime)
    frame["month"] = times.dt.to_period("M").astype(str)
    frame["season"] = times.dt.month.map(SEASONS)
    frame["pm25_level"] = pm25_levels(frame.y_true)
    if group not in {"station", "month", "season", "pm25_level"}:
        raise ValueError(f"Unsupported error group: {group}")
    rows = []
    for value, part in frame.groupby(group, observed=True, sort=True):
        for key, label in MODEL_LABELS.items():
            rows.append({
                "experiment_id": f"{key}_test", "model": label, group: str(value),
                "n": len(part), "mean_pm25": float(part.y_true.mean()),
                **regression_metrics(part.y_true, part[f"pred_{key}"]),
            })
    return pd.DataFrame(rows)


def paired_block_intervals(predictions, pairs=None, n_bootstrap=2000, block_days=7, seed=42):
    """Paired moving-block bootstrap of calendar days; keep all stations together.

    Positive RMSE difference means model_a has larger error than model_b.
    Percentile intervals are conditional on these frozen predictions and this
    period, not estimates of generalization to new stations or all seasons.
    """
    if block_days < 1 or n_bootstrap < 1:
        raise ValueError("block_days and n_bootstrap must be positive.")
    if pairs is None:
        pairs = [("random_forest_tuned", "baseline_persistence"),
                 ("random_forest_tuned", "baseline_linreg"),
                 ("random_forest_tuned", "gradient_boosting_tuned"),
                 ("random_forest_tuned", "mlp_tuned")]
    frame = predictions.copy()
    frame["day"] = pd.to_datetime(frame.target_datetime).dt.normalize()
    days = pd.date_range(frame.day.min(), frame.day.max(), freq="D")
    n_days = len(days)
    if n_days < block_days:
        raise ValueError("Not enough calendar days for the requested block length.")
    daily = pd.DataFrame(index=days)
    daily["n"] = frame.groupby("day").size().reindex(days, fill_value=0)
    for key in MODEL_LABELS:
        loss = (frame.y_true - frame[f"pred_{key}"]) ** 2
        daily[key] = loss.groupby(frame.day).sum().reindex(days, fill_value=0)
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n_days - block_days + 1,
                          size=(n_bootstrap, int(np.ceil(n_days / block_days))))
    indices = (starts[:, :, None] + np.arange(block_days)).reshape(n_bootstrap, -1)[:, :n_days]
    counts = daily["n"].to_numpy()[indices].sum(axis=1)
    rows = []
    for a, b in pairs:
        boot_a = np.sqrt(daily[a].to_numpy()[indices].sum(axis=1) / counts)
        boot_b = np.sqrt(daily[b].to_numpy()[indices].sum(axis=1) / counts)
        differences = boot_a - boot_b
        estimate = (np.sqrt(daily[a].sum() / daily.n.sum())
                    - np.sqrt(daily[b].sum() / daily.n.sum()))
        low, high = np.quantile(differences, [0.025, 0.975])
        rows.append({
            "model_a": MODEL_LABELS[a], "model_b": MODEL_LABELS[b],
            "rmse_difference_a_minus_b": float(estimate),
            "ci_95_low": float(low), "ci_95_high": float(high),
            "n_bootstrap": n_bootstrap, "block_days": block_days, "seed": seed,
            "n_calendar_days": n_days,
            "method": "paired moving calendar-day blocks; all stations together",
        })
    return pd.DataFrame(rows)


def _figures(predictions, metrics, groups, destination):
    import matplotlib.pyplot as plt

    destination.mkdir(parents=True, exist_ok=True)
    figure_paths = []

    def save(fig, name):
        path = destination / name
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        figure_paths.append(path)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.barh(metrics.model, metrics.rmse, color="#39798e")
    ax.invert_yaxis()
    ax.set(xlabel="Test RMSE (µg/m³)", title="Frozen models: final test")
    save(fig, "final_test_rmse.png")
    for group, errors in groups.items():
        pivot = errors.pivot(index=group, columns="model", values="rmse")
        if group == "pm25_level":
            pivot = pivot.reindex(PM25_LABELS)
        elif group == "season":
            pivot = pivot.reindex([s for s in ["Spring", "Summer", "Autumn", "Winter"] if s in pivot.index])
        fig, ax = plt.subplots(figsize=(12, 5))
        pivot.plot.bar(ax=ax)
        ax.set(ylabel="RMSE (µg/m³)", title=f"Final test errors by {group}", xlabel=group)
        ax.legend(fontsize=8)
        save(fig, f"final_test_rmse_by_{group}.png")

    rf_column = "pred_random_forest_tuned"
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.hexbin(predictions.y_true, predictions[rf_column], bins="log", mincnt=1, gridsize=60)
    limits = [min(predictions.y_true.min(), predictions[rf_column].min()),
              max(predictions.y_true.max(), predictions[rf_column].max())]
    ax.plot(limits, limits, "r--")
    ax.set(xlabel="Observed PM2.5 (µg/m³)", ylabel="Predicted PM2.5 (µg/m³)",
           title="RF selected by CV: test predictions")
    save(fig, "final_test_rf_pred_vs_actual.png")

    residual = predictions.y_true - predictions[rf_column]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.hist(residual, bins=100)
    ax.axvline(0, color="black", linestyle="--")
    ax.set(xlabel="Observed - predicted (µg/m³)", title="RF test residual distribution")
    save(fig, "final_test_rf_residuals.png")

    # Deterministic diagnostic: largest absolute RF test error, without retuning.
    worst = predictions.loc[residual.abs().idxmax()]
    time = pd.Timestamp(worst.target_datetime)
    window = predictions.loc[
        predictions.station.eq(worst.station)
        & pd.to_datetime(predictions.target_datetime).between(
            time - pd.Timedelta(hours=48), time + pd.Timedelta(hours=48))
    ].sort_values("target_datetime")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    axes[0].plot(window.target_datetime, window.y_true, label="Observed", color="black")
    for key in MODEL_LABELS:
        axes[0].plot(window.target_datetime, window[f"pred_{key}"], label=MODEL_LABELS[key], alpha=.7)
    axes[0].set(ylabel="PM2.5 (µg/m³)",
                title=f"Diagnostic window around largest RF error: {worst.station}")
    axes[0].legend(fontsize=8, ncol=2)
    axes[1].plot(window.target_datetime, window.y_true - window[rf_column])
    axes[1].axhline(0, color="black", linestyle="--")
    axes[1].set(ylabel="RF residual (µg/m³)", xlabel="Target timestamp")
    fig.autofmt_xdate()
    save(fig, "final_test_worst_event.png")
    return figure_paths


def _manifest_path(path, root):
    """Repo-relative POSIX path for the manifest; never an absolute or backslash path."""
    path, root = Path(path), Path(root)
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        # Outside the repository: keep only the file name rather than leak a local path.
        return path.name


def train_validation_test_table(train_validation, model_paths, experiment_log, test_metrics):
    """Compare in-sample, 5-fold validation and test RMSE of the frozen models.

    Only predicts; nothing is re-trained or re-tuned. In-sample error is computed
    on the rows the final models were fitted on, so it is an optimistic reference
    for judging over/under-fitting, not a score. ``experiment_log`` and
    ``test_metrics`` are indexed by ``experiment_id`` and carry an ``rmse`` column.
    """
    in_sample = predict_test(train_validation, train_validation, model_paths)
    rows = []
    for key, label in MODEL_LABELS.items():
        train = regression_metrics(in_sample.y_true, in_sample[f"pred_{key}"])
        rows.append({
            "model": label, "n_train_validation": len(in_sample),
            "train_mae": train["mae"], "train_rmse": train["rmse"], "train_r2": train["r2"],
            "validation_cv_rmse_mean": float(experiment_log.loc[f"{key}_cv5", "rmse"]),
            "test_rmse": float(test_metrics.loc[f"{key}_test", "rmse"]),
        })
    result = pd.DataFrame(rows)
    result["test_minus_train_rmse"] = result.test_rmse - result.train_rmse
    result["test_over_train_rmse"] = result.test_rmse / result.train_rmse
    return result


def export_analysis(predictions, model_paths, output_dir=None, n_bootstrap=2000, block_days=7,
                    project_root=None, data_path=None, train_validation=None):
    """Save diagnostics separately from the original final_test metric table.

    ``project_root`` and ``data_path`` default to the repository and processed
    dataset; they exist so the manifest can be tested against a temporary tree.
    Every path written to the manifest is repo-relative with forward slashes.
    Pass ``train_validation`` to also export the train/validation/test comparison.
    """
    project_root = Path(project_root or PROJECT_ROOT)
    data_path = Path(data_path or DEFAULT_DATA_PATH)
    output_dir = Path(output_dir or project_root / "outputs" / "experiments" / "final_test" / "analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics = summarize_predictions(predictions)
    tables = {"final_test_predictions.csv": predictions,
              "final_test_metrics_reproduced.csv": metrics}
    groups = {}
    for group in ("station", "month", "season", "pm25_level"):
        groups[group] = grouped_errors(predictions, group)
        tables[f"final_test_error_by_{group}.csv"] = groups[group]
    tables["final_test_sensitivity.csv"] = trimmed_sensitivity(predictions)
    if train_validation is not None:
        log = pd.read_csv(project_root / "experiment_log.csv").set_index("experiment_id")
        tables["train_vs_validation_vs_test.csv"] = train_validation_test_table(
            train_validation, model_paths, log, metrics.set_index("experiment_id"))
    tables["paired_model_uncertainty.csv"] = paired_block_intervals(
        predictions, n_bootstrap=n_bootstrap, block_days=block_days)
    worst_parts = []
    for key in MODEL_LABELS:
        part = predictions[["station", "datetime", "target_datetime", "y_true"]].copy()
        part["model"] = MODEL_LABELS[key]
        part["y_pred"] = predictions[f"pred_{key}"]
        part["residual"] = part.y_true - part.y_pred
        part["absolute_error"] = part.residual.abs()
        worst_parts.append(part.nlargest(100, "absolute_error"))
    tables["final_test_worst_cases.csv"] = pd.concat(worst_parts, ignore_index=True)
    paths = []
    for filename, table in tables.items():
        path = output_dir / filename
        table.to_csv(path, index=False, encoding="utf-8-sig")
        paths.append(path)
    paths.extend(_figures(predictions, metrics, groups, output_dir / "figures"))
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project_root,
                                capture_output=True, text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=project_root,
                                   capture_output=True, text=True, check=True).stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = None, None
    source_files = sorted((project_root / "src").glob("*.py"))
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": datetime.now(timezone.utc).strftime("final-analysis-%Y%m%dT%H%M%S%fZ"),
        "purpose": "diagnostic reevaluation of existing frozen models; no tuning on test",
        "selection_rule": "original mean RMSE over five chronological validation folds",
        "git_commit": commit, "working_tree_dirty": dirty,
        "source_sha256": {_manifest_path(p, project_root): sha256_file(p) for p in source_files},
        "python_version": platform.python_version(),
        "packages": {p: importlib.metadata.version(p) for p in
                     ["numpy", "pandas", "scikit-learn", "scipy", "joblib", "matplotlib", "threadpoolctl"]},
        "dataset": _manifest_path(data_path, project_root),
        "dataset_sha256": sha256_file(data_path),
        "feature_columns": list(FEATURE_COLUMNS), "ffill_limit_hours": FFILL_LIMIT,
        "test_start": str(TEST_START), "n_test": len(predictions),
        "test_target_period": [str(predictions.target_datetime.min()), str(predictions.target_datetime.max())],
        "residual_definition": "y_true - y_pred",
        "pm25_groups": PM25_LABELS, "pm25_intervals": "right-closed; exact boundaries go into lower interval",
        "uncertainty": {"method": "paired moving calendar-day block bootstrap",
                        "block_days": block_days, "n_bootstrap": n_bootstrap, "seed": 42,
                        "limitations": "fixed predictions, autumn/winter and observed stations only"},
        "models": {key: {"path": _manifest_path(path, project_root),
                           "sha256": sha256_file(path),
                          "metadata_path": _manifest_path(metadata_path(key, path), project_root),
                          "metadata_sha256": sha256_file(metadata_path(key, path)),
                          "metadata": json.loads(metadata_path(key, path).read_text(encoding="utf-8-sig"))}
                   for key, path in model_paths.items()},
        "outputs": {p.relative_to(output_dir).as_posix(): sha256_file(p) for p in paths},
    }
    (output_dir / "evaluation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--block-days", type=int, default=7)
    parser.add_argument("--n-bootstrap", type=int, default=2000)
    args = parser.parse_args()
    paths = resolve_model_paths()
    featured = add_features(load_data()).dropna(subset=["target"]).reset_index(drop=True)
    train_validation, test = time_split(featured)
    predictions = predict_test(test, train_validation, paths)
    metrics = summarize_predictions(predictions)
    original = PROJECT_ROOT / "outputs" / "notebooks" / "tables" / "final_test_metrics.csv"
    if original.is_file():
        expected = pd.read_csv(original).set_index("experiment_id")
        actual = metrics.set_index("experiment_id").reindex(expected.index)
        np.testing.assert_allclose(actual[["mae", "rmse", "r2"]], expected[["mae", "rmse", "r2"]],
                                   rtol=1e-9, atol=1e-9)
    export_analysis(predictions, paths, args.output_dir, args.n_bootstrap, args.block_days)
    print(metrics.to_string(index=False))
    print("Original final-test scores reproduced. Diagnostic artifacts exported.")


if __name__ == "__main__":
    main()
