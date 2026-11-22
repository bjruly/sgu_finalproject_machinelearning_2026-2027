"""Write final-test ranking sensitivity to the largest-error rows (report only).

Reads the saved final-test predictions; loads no model and changes no result.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import trimmed_sensitivity

FOLDER = ROOT / "outputs/experiments/final_test/analysis"


def main():
    predictions = pd.read_csv(FOLDER / "final_test_predictions.csv")
    result = trimmed_sensitivity(predictions)
    result.to_csv(FOLDER / "final_test_sensitivity.csv", index=False)
    print(result.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
