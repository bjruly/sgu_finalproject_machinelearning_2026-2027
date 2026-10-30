# Data loading and preprocessing module
"""Nạp dữ liệu, chia tập theo thời gian, tạo fold CV theo timestamp."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed" / "beijing_air_quality_standardized.csv"
TEST_START = "2016-09-01"  # proposal: test 09/2016 - 02/2017


def load_data(path=PROCESSED):
    """CSV đã gộp 12 trạm (notebook 01). Giữ nguyên missing; bỏ cột No (chỉ là chỉ số)."""
    df = pd.read_csv(path, na_values=["NA"], parse_dates=["datetime"])
    return df.drop(columns="No").sort_values(["station", "datetime"]).reset_index(drop=True)


def time_split(df, test_start=TEST_START):
    """(train_val, test) theo thời gian, không xáo trộn."""
    is_test = df["datetime"] >= test_start
    return df[~is_test].reset_index(drop=True), df[is_test].reset_index(drop=True)


def cv_folds(df, n_splits=5):
    """TimeSeriesSplit expanding-window trên các timestamp DUY NHẤT:
    12 trạm cùng một giờ luôn nằm chung một fold. Trả list[(train_idx, val_idx)]
    (chỉ số vị trí) để đưa thẳng vào cv= của sklearn."""
    times = np.sort(df["datetime"].unique())
    return [
        (np.flatnonzero(df["datetime"].isin(times[tr])), np.flatnonzero(df["datetime"].isin(times[va])))
        for tr, va in TimeSeriesSplit(n_splits).split(times)
    ]