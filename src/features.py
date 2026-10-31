"""Create leakage-safe time-series features and preprocessing transformers."""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import MissingIndicator, SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "target"
FFILL_LIMIT = 6
PM25_LAGS = (1, 2, 3, 6, 12, 24)
ROLLING_WINDOWS = (6, 24)
NUMERIC_SOURCE_FEATURES = (
    "PM2.5",
    "PM10",
    "SO2",
    "NO2",
    "CO",
    "O3",
    "TEMP",
    "PRES",
    "DEWP",
    "RAIN",
    "WSPM",
)
CATEGORICAL_FEATURES = ("station", "wd")
NUMERIC_FEATURES = (
    *NUMERIC_SOURCE_FEATURES,
    *(f"PM2.5_lag_{lag}" for lag in PM25_LAGS),
    *(f"PM2.5_rolling_mean_{window}" for window in ROLLING_WINDOWS),
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
    "day_of_week_sin",
    "day_of_week_cos",
)
FEATURE_COLUMNS = (*NUMERIC_FEATURES, *CATEGORICAL_FEATURES)
REQUIRED_FEATURE_COLUMNS = {
    *NUMERIC_SOURCE_FEATURES,
    *CATEGORICAL_FEATURES,
    "datetime",
}


def add_features(data: pd.DataFrame, ffill_limit: int = FFILL_LIMIT) -> pd.DataFrame:
    """Create the same-station next-hour target and past-only predictors.

    The target is shifted from the original PM2.5 values before any
    forward-fill. Predictor values are forward-filled independently within
    each station for at most ``ffill_limit`` hourly rows. Unresolved wind
    direction values are represented by the explicit ``Unknown`` category.
    """
    if ffill_limit < 0:
        raise ValueError("ffill_limit must be zero or a positive number of hours.")

    missing_columns = REQUIRED_FEATURE_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Data is missing required columns: {sorted(missing_columns)}")
    if data["station"].isna().any() or data["datetime"].isna().any():
        raise ValueError("Station and datetime values must not be missing.")
    if data.duplicated(["station", "datetime"]).any():
        raise ValueError("Data contains duplicate station-hour records.")

    result = data.copy()
    result["datetime"] = pd.to_datetime(result["datetime"], errors="raise")
    result = result.sort_values(["station", "datetime"], kind="stable").reset_index(drop=True)

    hour_differences = result.groupby("station", sort=False)["datetime"].diff()
    invalid_steps = hour_differences.notna() & hour_differences.ne(pd.Timedelta(hours=1))
    if invalid_steps.any():
        raise ValueError(
            "Each station must have continuous hourly timestamps before "
            "creating time-based lags."
        )

    grouped = result.groupby("station", sort=False)
    next_pm25 = grouped["PM2.5"].shift(-1)
    next_datetime = grouped["datetime"].shift(-1)
    next_is_one_hour_later = next_datetime.sub(result["datetime"]).eq(pd.Timedelta(hours=1))
    result["target_datetime"] = next_datetime.where(next_is_one_hour_later)
    result[TARGET_COLUMN] = next_pm25.where(next_is_one_hour_later)

    predictor_columns = [*NUMERIC_SOURCE_FEATURES, "wd"]
    if ffill_limit:
        result[predictor_columns] = result.groupby("station", sort=False)[
            predictor_columns
        ].ffill(limit=ffill_limit)
    result["wd"] = result["wd"].fillna("Unknown")

    pm25 = result.groupby("station", sort=False)["PM2.5"]
    for lag in PM25_LAGS:
        result[f"PM2.5_lag_{lag}"] = pm25.shift(lag)
    for window in ROLLING_WINDOWS:
        result[f"PM2.5_rolling_mean_{window}"] = pm25.transform(
            lambda values: values.shift(1).rolling(window=window, min_periods=window).mean()
        )

    hour = result["datetime"].dt.hour
    month = result["datetime"].dt.month
    day_of_week = result["datetime"].dt.day_of_week
    result["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    result["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    result["month_sin"] = np.sin(2 * np.pi * (month - 1) / 12)
    result["month_cos"] = np.cos(2 * np.pi * (month - 1) / 12)
    result["day_of_week_sin"] = np.sin(2 * np.pi * day_of_week / 7)
    result["day_of_week_cos"] = np.cos(2 * np.pi * day_of_week / 7)

    return result


def split_xy(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return predictor columns and the one-hour-ahead PM2.5 target."""
    missing_columns = set(FEATURE_COLUMNS).union({TARGET_COLUMN}).difference(data.columns)
    if missing_columns:
        raise ValueError(f"Featured data is missing columns: {sorted(missing_columns)}")

    features = data.loc[:, FEATURE_COLUMNS].copy()
    target = data[TARGET_COLUMN].copy()
    return features, target


def build_preprocessor(scale: bool = False) -> ColumnTransformer:
    """Build a train-fitted imputation/encoding transformer.

    Numeric medians are learned when the returned transformer is fitted, and
    missingness indicators are emitted for every numeric feature. Categorical
    missing values are represented by ``Unknown`` and one-hot encoded. Scaling
    is optional for linear models.
    """
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(steps=numeric_steps)
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(NUMERIC_FEATURES)),
            (
                "numeric_missing",
                MissingIndicator(features="all", error_on_new=False),
                list(NUMERIC_FEATURES),
            ),
            ("categorical", categorical_pipeline, list(CATEGORICAL_FEATURES)),
        ],
        remainder="drop",
    )
