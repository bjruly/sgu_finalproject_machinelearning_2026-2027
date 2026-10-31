import pandas as pd
import pytest

from src.data_loader import cv_folds, load_data, time_split


def _panel(periods: int = 20) -> pd.DataFrame:
    timestamps = pd.date_range("2016-08-20", periods=periods, freq="h")
    return pd.DataFrame(
        [
            {"station": station, "datetime": timestamp, "PM2.5": hour}
            for station in ("A", "B")
            for hour, timestamp in enumerate(timestamps)
        ]
    )


def test_load_data_parses_sorts_and_rejects_duplicate_station_hours(tmp_path):
    source = pd.DataFrame(
        {
            "station": ["B", "A"],
            "datetime": ["2016-01-01 01:00:00", "2016-01-01 00:00:00"],
            "PM2.5": [2.0, 1.0],
        }
    )
    csv_path = tmp_path / "small.csv"
    source.to_csv(csv_path, index=False)

    loaded = load_data(csv_path)

    assert loaded["station"].tolist() == ["A", "B"]
    assert pd.api.types.is_datetime64_any_dtype(loaded["datetime"])

    duplicated = pd.concat([source, source.iloc[[0]]], ignore_index=True)
    duplicated.to_csv(csv_path, index=False)
    with pytest.raises(ValueError, match="duplicate station-hour"):
        load_data(csv_path)


def test_time_split_keeps_all_stations_on_the_same_side_of_boundary():
    data = _panel()

    train_validation, test = time_split(data, test_start="2016-08-20 10:00:00")

    assert train_validation["datetime"].max() < pd.Timestamp("2016-08-20 10:00:00")
    assert test["datetime"].min() == pd.Timestamp("2016-08-20 10:00:00")
    assert train_validation["datetime"].nunique() == len(train_validation) // 2
    assert test["datetime"].nunique() == len(test) // 2


def test_time_split_uses_label_timestamp_for_one_hour_ahead_target():
    data = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                ["2016-08-31 22:00", "2016-08-31 23:00", "2016-09-01 00:00"]
            ),
            "target_datetime": pd.to_datetime(
                ["2016-08-31 23:00", "2016-09-01 00:00", "2016-09-01 01:00"]
            ),
            "station": ["A", "A", "A"],
        }
    )

    train_validation, test = time_split(data)

    assert train_validation["target_datetime"].max() == pd.Timestamp("2016-08-31 23:00")
    assert test.iloc[0]["datetime"] == pd.Timestamp("2016-08-31 23:00")
    assert test.iloc[0]["target_datetime"] == pd.Timestamp("2016-09-01 00:00")


def test_cv_folds_are_expanding_and_keep_each_timestamp_grouped():
    data = _panel(periods=30)
    folds = cv_folds(data, n_splits=4)

    assert len(folds) == 4
    previous_train_size = 0
    for train_idx, validation_idx in folds:
        train_times = set(data.iloc[train_idx]["datetime"])
        validation_times = set(data.iloc[validation_idx]["datetime"])

        assert train_times.isdisjoint(validation_times)
        assert max(train_times) < min(validation_times)
        assert len(train_idx) == 2 * len(train_times)
        assert len(validation_idx) == 2 * len(validation_times)
        assert len(train_idx) > previous_train_size
        previous_train_size = len(train_idx)


def test_cv_folds_split_on_target_timestamp_when_available():
    data = _panel(periods=12)
    data["target_datetime"] = data["datetime"] + pd.Timedelta(hours=1)

    for train_idx, validation_idx in cv_folds(data, n_splits=3):
        train_times = set(data.iloc[train_idx]["target_datetime"])
        validation_times = set(data.iloc[validation_idx]["target_datetime"])
        assert train_times.isdisjoint(validation_times)
        assert max(train_times) < min(validation_times)


def test_cv_folds_rejects_missing_datetime():
    with pytest.raises(ValueError, match="datetime"):
        cv_folds(pd.DataFrame({"station": ["A"]}))
