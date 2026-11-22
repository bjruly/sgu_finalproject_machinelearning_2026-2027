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

from src.artifacts import resolve_model_paths
from src.data_loader import load_data, time_split
from src.evaluation import train_validation_test_table
from src.features import add_features

FOLDER = ROOT / "outputs/experiments/final_test/analysis"


def main():
    labeled = add_features(load_data()).dropna(subset=["target"]).reset_index(drop=True)
    train_validation, _ = time_split(labeled)
    log = pd.read_csv(ROOT / "experiment_log.csv").set_index("experiment_id")
    test = pd.read_csv(ROOT / "outputs/notebooks/tables/final_test_metrics.csv").set_index("experiment_id")
    result = train_validation_test_table(train_validation, resolve_model_paths(ROOT), log, test)
    result.to_csv(FOLDER / "train_vs_validation_vs_test.csv", index=False)
    print(result.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
