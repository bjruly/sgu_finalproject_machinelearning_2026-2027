"""Compare in-sample (train+validation), 5-fold validation and test error (report only).

Loads the frozen models and only predicts; nothing is re-trained or re-tuned.
In-sample error is computed on the same 360,954 rows the final models were fitted on,
so it is an optimistic reference used to judge over/under-fitting, not a score.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.artifacts import MODEL_LABELS, resolve_model_paths
from src.data_loader import load_data, time_split
from src.evaluation import predict_test, regression_metrics
from src.features import add_features

FOLDER = ROOT / "outputs/experiments/final_test/analysis"


def main():
    labeled = add_features(load_data()).dropna(subset=["target"]).reset_index(drop=True)
    train_validation, _ = time_split(labeled)
    paths = resolve_model_paths(ROOT)
    predictions = predict_test(train_validation, train_validation, paths)
    log = pd.read_csv(ROOT / "experiment_log.csv").set_index("experiment_id")
    test = pd.read_csv(ROOT / "outputs/notebooks/tables/final_test_metrics.csv").set_index("experiment_id")
    rows = []
    for key, label in MODEL_LABELS.items():
        train = regression_metrics(predictions.y_true, predictions[f"pred_{key}"])
        cv_id = key.replace("baseline_linreg", "baseline_linreg") + "_cv5"
        rows.append({
            "model": label, "n_train_validation": len(predictions),
            "train_mae": train["mae"], "train_rmse": train["rmse"], "train_r2": train["r2"],
            "validation_cv_rmse_mean": float(log.loc[cv_id, "rmse"]),
            "test_rmse": float(test.loc[f"{key}_test", "rmse"]),
        })
    result = pd.DataFrame(rows)
    result["test_minus_train_rmse"] = result.test_rmse - result.train_rmse
    result["test_over_train_rmse"] = result.test_rmse / result.train_rmse
    result.to_csv(FOLDER / "train_vs_validation_vs_test.csv", index=False)
    print(result.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
