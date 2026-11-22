"""Rebuild current summary CSV/XLSX from notebook-produced tables, not hand-entered values.

Experimental Log/ and historical model copies are intentionally not rewritten.
"""

import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.notebook_evidence import verify_evidence

TABLES = ROOT / "outputs/notebooks/tables"
EXPERIMENTS = ROOT / "outputs/experiments"
LABELS = {"random_forest": "Random Forest", "gradient_boosting": "Gradient Boosting", "mlp": "MLP"}


def model_tables(kinds):
    summary, parts = [], []
    for kind, tuned in kinds:
        key = kind + ("_tuned" if tuned else "")
        frame = pd.read_csv(TABLES / f"{key}_cv_metrics.csv")
        stage = "Sau tinh chỉnh" if tuned else "Ban đầu"
        rows = frame[["fold", "train_rows", "validation_rows", "mae", "rmse", "r2"]].copy()
        rows.insert(0, "stage", stage)
        rows.insert(0, "model", LABELS[kind])
        rows.insert(0, "experiment_id", key + "_cv5")
        parts.append(rows)
        summary.append({"experiment_id": key + "_cv5", "model": LABELS[kind], "stage": stage,
                        **{m: frame[m].mean() for m in ["mae", "rmse", "r2"]},
                        **{m + "_std": frame[m].std(ddof=1) for m in ["mae", "rmse", "r2"]},
                        "n_folds": len(frame), "n_validation": int(frame.validation_rows.sum())})
    return pd.DataFrame(summary), pd.concat(parts, ignore_index=True)


def save(folder, sheets, csvs):
    folder.mkdir(parents=True, exist_ok=True)
    for name, table in csvs.items():
        table.to_csv(folder / name, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(folder / "danh_gia.xlsx", engine="openpyxl") as writer:
        for name, table in sheets.items():
            table.to_excel(writer, sheet_name=name, index=False)
            sheet = writer.sheets[name]
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            for column in sheet.columns:
                letter = column[0].column_letter
                sheet.column_dimensions[letter].width = min(70, max(14, max(len(str(c.value or "")) for c in column) + 2))
            for row in sheet.iter_rows(min_row=2):
                for cell in row:
                    if isinstance(cell.value, float):
                        cell.number_format = "0.0000"


def main():
    sources = verify_evidence(ROOT, write_index=True)
    if sources.notebook.nunique() != 8:
        raise ValueError("Execute/verify all notebooks before refreshing summaries.")
    base = pd.read_csv(TABLES / "baseline_cv_metrics.csv")
    baseline_metrics = pd.read_csv(TABLES / "baseline_metrics.csv")
    log = pd.read_csv(ROOT / "experiment_log.csv").set_index("experiment_id")
    groups = pd.read_csv(TABLES / "baseline_error_analysis.csv")
    summary = []
    for model, key in [("Persistence", "persistence"), ("Linear Regression", "linreg")]:
        frame = base.loc[base.model.eq(model)]
        summary.append({"experiment_id": f"baseline_{key}_cv5", "model": model,
                        "split": "cv_validation_mean_5fold",
                        **{m: frame[m].mean() for m in ["mae", "rmse", "r2"]},
                        **{m + "_std": frame[m].std(ddof=1) for m in ["mae", "rmse", "r2"]},
                        "n_rows": int(baseline_metrics.loc[
                            baseline_metrics.model.eq(model) &
                            baseline_metrics.split.eq("cv_validation_mean_5fold"), "n_rows"].iloc[0]),
                        "dataset_version": log.loc[f"baseline_{key}_cv5", "dataset_version"]})
    summary = pd.DataFrame(summary)
    merged = pd.read_csv(TABLES / "baseline_comparison_merged.csv")
    per_fold = merged.loc[merged.scope.eq("cv_fold")].reset_index(drop=True)
    folder = EXPERIMENTS / "experiments01"
    save(folder, {"Tong_hop": summary, "Theo_fold": per_fold, "Sai_so_nhom": groups},
         {"ket_qua_tong_hop.csv": summary, "ket_qua_theo_fold.csv": per_fold,
          "baseline_error_analysis.csv": groups})
    for name, kinds in [
        ("experiments02", [(kind, False) for kind in LABELS]),
        ("experiments03", [(kind, tuned) for kind in LABELS for tuned in [False, True]])]:
        summary, folds = model_tables(kinds)
        folder = EXPERIMENTS / name
        save(folder, {"Tong_hop": summary, "Theo_fold": folds, "Nguon_notebook": sources},
             {"ket_qua_tong_hop.csv": summary, "ket_qua_theo_fold.csv": folds})
        raw_folder = folder / "ket_qua_goc"
        raw_folder.mkdir(exist_ok=True)
        for kind, tuned in kinds:
            key = kind + ("_tuned" if tuned else "")
            for suffix in ["cv_metrics.csv", "cv_summary.csv"]:
                shutil.copyfile(TABLES / f"{key}_{suffix}", raw_folder / f"{key}_{suffix}")
            search = TABLES / f"tuning_{kind}_search_results.csv"
            if tuned and search.is_file():
                shutil.copyfile(search, raw_folder / search.name)
        if name == "experiments02":
            for source in TABLES.glob("*_validation_oof_predictions.csv"):
                if not source.name.startswith("baseline") and "tuned" not in source.name:
                    shutil.copyfile(source, raw_folder / source.name)
            for filename in ["mlp_error_by_group.csv", "random_forest_fold_overview.csv"]:
                shutil.copyfile(TABLES / filename, raw_folder / filename)
    folder = EXPERIMENTS / "final_test"
    final = pd.read_csv(TABLES / "final_test_metrics.csv")
    analysis = folder / "analysis"
    sheets = {"Tong_hop": final, **{g: pd.read_csv(analysis / f"final_test_error_by_{g}.csv")
                                    for g in ["station", "month", "season", "pm25_level"]},
              "Bootstrap": pd.read_csv(analysis / "paired_model_uncertainty.csv"),
              "Nguon_notebook": sources}
    save(folder, sheets, {"final_test_metrics.csv": final})
    for experiment, prefixes in {
        "experiments01": ["baseline_"],
        "experiments02": ["random_forest_", "gradient_boosting_", "mlp_"],
        "experiments03": ["tuning_", "mlp_tuning_"],
        "final_test": ["final_test_rmse"],
    }.items():
        destination = EXPERIMENTS / experiment / "figures"
        destination.mkdir(exist_ok=True)
        for prefix in prefixes:
            for source in (ROOT / "outputs/notebooks/figures").glob(prefix + "*.png"):
                if experiment == "experiments02" and source.name.startswith("mlp_tuning_"):
                    continue
                shutil.copyfile(source, destination / source.name)
    print("Current experiment summaries regenerated from verified notebook tables. Historical experiment logs/model copies were not rewritten.")


if __name__ == "__main__":
    main()
