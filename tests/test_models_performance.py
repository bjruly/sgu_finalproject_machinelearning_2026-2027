# Unit tests for model performance bounds
import numpy as np

from src.data_loader import cv_folds, load_data, time_split
from src.evaluate import metrics
from src.features import add_features, split_xy
from src.models import make_linreg, persistence


def test_metrics_known_values():
    m = metrics([0.0, 2.0], [1.0, 1.0])
    assert m["mae"] == 1.0 and m["rmse"] == 1.0 and m["r2"] == 0.0


def test_linreg_beats_persistence_on_validation():
    df = add_features(load_data()).dropna(subset=["target"])
    train_val, _test = time_split(df)                  # test để yên, chỉ dùng ở bước đánh giá cuối
    X, y = split_xy(train_val)
    pers, lin = [], []
    for a, b in cv_folds(train_val):
        pers.append(metrics(y.iloc[b], persistence(X.iloc[b], y.iloc[a].median())))
        lin.append(metrics(y.iloc[b], make_linreg().fit(X.iloc[a], y.iloc[a]).predict(X.iloc[b])))
    mean = lambda ms, k: np.mean([m[k] for m in ms])
    assert mean(lin, "rmse") < mean(pers, "rmse")      # LR phải học được hơn việc lặp lại giá trị cuối
    assert mean(lin, "r2") > 0.9