# Integration tests for end-to-end flow
import numpy as np

from src.data_loader import cv_folds, load_data, time_split
from src.features import add_features, split_xy
from src.models import make_linreg


def test_pipeline_end_to_end():
    df = add_features(load_data()).dropna(subset=["target"])
    tr, te = time_split(df)
    X, y = split_xy(tr)
    Xt, _ = split_xy(te)                               # chỉ kiểm cấu trúc, không chấm điểm trên test
    assert not any(c in X for c in ("target", "datetime", "No"))
    assert X.columns.equals(Xt.columns)

    a, b = cv_folds(tr)[0]
    assert tr["datetime"].iloc[a].max() < tr["datetime"].iloc[b].min()
    pred = make_linreg().fit(X.iloc[a], y.iloc[a]).predict(X.iloc[b])
    assert len(pred) == len(b) and not np.isnan(pred).any()