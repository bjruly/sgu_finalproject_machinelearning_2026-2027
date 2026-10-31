import numpy as np
import pandas as pd

from src.features import (
    FEATURE_COLUMNS,
    add_features,
    build_preprocessor,
    split_xy,
)


def _raw_panel(periods: int = 32) -> pd.DataFrame:
    timestamps = pd.date_range("2016-01-01", periods=periods, freq="h")
    rows = []
    for station_offset, station in enumerate(("A", "B")):
        for hour, timestamp in enumerate(timestamps):
            rows.append(
                {
                    "station": station,
                    "datetime": timestamp,
                    "PM2.5": float(hour + station_offset * 100),
                    "PM10": float(hour + 10),
                    "SO2": float(hour + 20),
                    "NO2": float(hour + 30),
                    "CO": float(hour + 40),
                    "O3": float(hour + 50),
                    "TEMP": float(hour + 60),
                    "PRES": float(hour + 70),
                    "DEWP": float(hour + 80),
                    "RAIN": float(hour + 90),
                    "WSPM": float(hour + 100),
                    "wd": "N",
                    "No": hour,
                }
            )
    return pd.DataFrame(rows)


def test_target_is_next_hour_of_same_station_and_last_hour_is_unlabeled():
    raw = _raw_panel(periods=3)

    featured = add_features(raw)
    station_a = featured.loc[featured["station"].eq("A")]
    station_b = featured.loc[featured["station"].eq("B")]

    assert station_a["target"].tolist()[:2] == [1.0, 2.0]
    assert station_b["target"].tolist()[:2] == [101.0, 102.0]
    assert pd.isna(station_a["target"].iloc[-1])
    assert pd.isna(station_b["target"].iloc[-1])


def test_target_uses_original_pm25_and_is_not_forward_filled():
    raw = _raw_panel(periods=3)
    raw.loc[(raw["station"] == "A") & (raw["datetime"] == raw["datetime"].min() + pd.Timedelta(hours=1)), "PM2.5"] = np.nan

    featured = add_features(raw)
    station_a = featured.loc[featured["station"].eq("A")].reset_index(drop=True)

    assert pd.isna(station_a.loc[0, "target"])
    assert station_a.loc[1, "PM2.5"] == station_a.loc[0, "PM2.5"]


def test_forward_fill_is_limited_and_station_specific():
    raw = _raw_panel(periods=10)
    start = raw["datetime"].min()
    mask = raw["station"].eq("A") & raw["datetime"].between(
        start + pd.Timedelta(hours=1), start + pd.Timedelta(hours=7)
    )
    raw.loc[mask, "TEMP"] = np.nan
    raw.loc[mask, "wd"] = np.nan

    featured = add_features(raw)
    station_a = featured.loc[featured["station"].eq("A")].reset_index(drop=True)
    station_b = featured.loc[featured["station"].eq("B")].reset_index(drop=True)

    assert station_a.loc[1:6, "TEMP"].notna().all()
    assert pd.isna(station_a.loc[7, "TEMP"])
    assert station_a.loc[1:6, "wd"].eq("N").all()
    assert station_a.loc[7, "wd"] == "Unknown"
    assert station_b["TEMP"].notna().all()


def test_zero_forward_fill_limit_leaves_missing_feature_values():
    raw = _raw_panel(periods=3)
    missing_at = raw["datetime"].min() + pd.Timedelta(hours=1)
    raw.loc[(raw["station"] == "A") & raw["datetime"].eq(missing_at), "TEMP"] = np.nan

    featured = add_features(raw, ffill_limit=0)

    assert pd.isna(
        featured.loc[
            featured["station"].eq("A") & featured["datetime"].eq(missing_at), "TEMP"
        ].iloc[0]
    )


def test_lags_and_rolling_features_only_use_past_data():
    raw = _raw_panel(periods=30)
    featured = add_features(raw)
    station_a = featured.loc[featured["station"].eq("A")].reset_index(drop=True)

    assert station_a.loc[24, "PM2.5_lag_1"] == 23
    assert station_a.loc[24, "PM2.5_lag_24"] == 0
    assert station_a.loc[24, "PM2.5_rolling_mean_6"] == np.mean([18, 19, 20, 21, 22, 23])
    assert station_a.loc[24, "PM2.5_rolling_mean_24"] == np.mean(range(24))

    changed_future = raw.copy()
    changed_future.loc[
        (changed_future["station"] == "A")
        & (changed_future["datetime"] >= raw["datetime"].min() + pd.Timedelta(hours=26)),
        "PM2.5",
    ] = 10000
    changed = add_features(changed_future)
    before_change = featured.loc[
        featured["station"].eq("A")
        & featured["datetime"].lt(raw["datetime"].min() + pd.Timedelta(hours=26)),
        ["PM2.5_lag_1", "PM2.5_rolling_mean_6", "PM2.5_rolling_mean_24"],
    ].reset_index(drop=True)
    actual_before_change = changed.loc[
        changed["station"].eq("A")
        & changed["datetime"].lt(raw["datetime"].min() + pd.Timedelta(hours=26)),
        ["PM2.5_lag_1", "PM2.5_rolling_mean_6", "PM2.5_rolling_mean_24"],
    ].reset_index(drop=True)
    pd.testing.assert_frame_equal(before_change, actual_before_change)


def test_split_xy_excludes_identifiers_and_target_from_predictors():
    featured = add_features(_raw_panel(periods=30))

    features, target = split_xy(featured)

    assert tuple(features.columns) == FEATURE_COLUMNS
    assert "target" not in features
    assert "datetime" not in features
    assert "No" not in features
    assert len(features) == len(target)


def test_preprocessor_learns_numeric_median_from_training_rows_only():
    train = add_features(_raw_panel(periods=30))
    train = train.loc[train["datetime"].lt(train["datetime"].min() + pd.Timedelta(hours=25))]
    train.loc[train["station"].eq("A") & train["datetime"].dt.hour.eq(3), "TEMP"] = np.nan
    test = add_features(_raw_panel(periods=30))
    test.loc[test["station"].eq("A"), "TEMP"] = np.nan
    test.loc[test["station"].eq("A"), "RAIN"] = np.nan
    train_x, _ = split_xy(train)
    test_x, _ = split_xy(test)

    preprocessor = build_preprocessor()
    preprocessor.fit(train_x)
    transformed_test = preprocessor.transform(test_x.iloc[:1])

    numeric_imputer = preprocessor.named_transformers_["numeric"].named_steps["imputer"]
    temp_index = list(train_x.select_dtypes(include="number").columns).index("TEMP")
    expected_median = train_x["TEMP"].median()
    assert numeric_imputer.statistics_[temp_index] == expected_median
    assert transformed_test.shape[0] == 1
    output_names = preprocessor.get_feature_names_out()
    rain_indicator_index = list(output_names).index(
        "numeric_missing__missingindicator_RAIN"
    )
    assert transformed_test[0, rain_indicator_index] == 1


def test_preprocessor_encodes_unknown_wind_as_a_category():
    raw = _raw_panel(periods=30)
    start = raw["datetime"].min()
    missing_wind = raw["station"].eq("A") & raw["datetime"].between(
        start + pd.Timedelta(hours=10), start + pd.Timedelta(hours=17)
    )
    raw.loc[missing_wind, "wd"] = np.nan
    featured = add_features(raw)
    features, _ = split_xy(featured)

    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(features)
    wind_categories = preprocessor.named_transformers_["categorical"].named_steps[
        "onehot"
    ].categories_[1]

    assert transformed.shape[0] == len(features)
    assert "Unknown" in wind_categories
