import pandas as pd

from src.data_loader import cv_folds, load_data, time_split
from src.features import add_features, split_xy


def test_real_dataset_runs_through_data_pipeline():
    raw = load_data()
    featured = add_features(raw)
    labeled = featured.dropna(subset=["target"]).reset_index(drop=True)
    train_validation, test = time_split(labeled)
    train_x, train_y = split_xy(train_validation)
    folds = cv_folds(train_validation, n_splits=5)

    assert raw["station"].nunique() == 12
    assert len(raw) == 420_768
    assert train_validation["target_datetime"].max() == pd.Timestamp(
        "2016-08-31 23:00:00"
    )
    assert test["target_datetime"].min() == pd.Timestamp("2016-09-01")
    assert test["datetime"].min() == pd.Timestamp("2016-08-31 23:00:00")
    assert train_x.shape[0] == len(train_y)
    assert len(folds) == 5

    for train_idx, validation_idx in folds:
        train_times = set(train_validation.iloc[train_idx]["datetime"])
        validation_times = set(train_validation.iloc[validation_idx]["datetime"])
        assert train_times.isdisjoint(validation_times)
        assert max(train_times) < min(validation_times)
