# Unit tests for data pipeline
import pandas as pd

from src.data_loader import cv_folds, time_split
from tests import toy


def test_time_split_no_overlap():
    tr, te = time_split(toy(100))
    assert len(tr) and len(te)
    assert tr["datetime"].max() < pd.Timestamp("2016-09-01") <= te["datetime"].min()


def test_cv_folds_by_timestamp():
    df = toy(200)
    folds = cv_folds(df, 5)
    assert len(folds) == 5
    for tr, va in folds:
        t_tr, t_va = df["datetime"].iloc[tr], df["datetime"].iloc[va]
        assert t_tr.max() < t_va.min()                 # validation luôn sau train
        assert not set(t_tr) & set(t_va)               # 1 timestamp chỉ ở 1 phía -> các trạm cùng giờ chung fold
        assert (df.iloc[va].groupby("datetime").size() == 2).all()  # đủ 2 trạm mỗi giờ