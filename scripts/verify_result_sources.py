"""Verify CSV values against executed notebook outputs and write a source index."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.notebook_evidence import verify_evidence


def main():
    sources = verify_evidence(ROOT, write_index=True)
    if sources.empty or sources.notebook.nunique() != 8:
        raise ValueError("All eight notebooks must have executed evidence cells.")
    tables = ROOT / "outputs/notebooks/tables"
    log = pd.read_csv(ROOT / "experiment_log.csv").set_index("experiment_id")
    baseline = pd.read_csv(tables / "baseline_cv_metrics.csv")
    for model, key in [("Persistence", "persistence"), ("Linear Regression", "linreg")]:
        scores = baseline.loc[baseline.model.eq(model), ["mae", "rmse", "r2"]].mean()
        np.testing.assert_allclose(scores.to_numpy(), log.loc[f"baseline_{key}_cv5", scores.index].to_numpy(dtype=float), atol=1e-6)
    for key in ["random_forest", "gradient_boosting", "mlp",
                "random_forest_tuned", "gradient_boosting_tuned", "mlp_tuned"]:
        scores = pd.read_csv(tables / f"{key}_cv_metrics.csv")[["mae", "rmse", "r2"]].mean()
        np.testing.assert_allclose(scores.to_numpy(), log.loc[f"{key}_cv5", scores.index].to_numpy(dtype=float), atol=1e-6)
    final = pd.read_csv(tables / "final_test_metrics.csv").set_index("experiment_id")
    np.testing.assert_allclose(final[["mae", "rmse", "r2"]],
                               log.loc[final.index, ["mae", "rmse", "r2"]].astype(float), atol=1e-6)
    folder = ROOT / "outputs/experiments/final_test/analysis"
    for group in ["station", "month", "season", "pm25_level"]:
        values = pd.read_csv(folder / f"final_test_error_by_{group}.csv")
        if not values.groupby("model").n.sum().eq(int(final.n_test.iloc[0])).all():
            raise ValueError(f"Group sample counts differ: {group}")
    print(f"PASS: {len(sources)} CSV artifacts linked to 8 notebooks; numerical outputs, hashes, log and group counts verified.")
    print(sources[["notebook", "cell_id", "mode", "csv_path"]].to_string(index=False))


if __name__ == "__main__":
    main()
