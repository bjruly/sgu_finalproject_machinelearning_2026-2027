"""Load the standardized Beijing air-quality data and create chronological splits."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "beijing_air_quality_standardized.csv"
)
TEST_START = pd.Timestamp("2016-09-01 00:00:00")
REQUIRED_COLUMNS = {"station", "datetime", "PM2.5"}


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the standardized station data from CSV.

    Args:
        path: CSV path. Defaults to the processed dataset in the repository.

    Returns:
        Data sorted by station and timestamp, with ``datetime`` parsed.

    Raises:
        FileNotFoundError: If the requested CSV does not exist.
        ValueError: If required columns or unique station-hour keys are missing.
    """
    csv_path = Path(path) if path is not None else DEFAULT_DATA_PATH
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. Run the EDA notebook to create "
            "data/processed/beijing_air_quality_standardized.csv."
        )

    data = pd.read_csv(csv_path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
    data["datetime"] = pd.to_datetime(data["datetime"], errors="raise")
    if data["datetime"].isna().any():
        raise ValueError("Dataset contains invalid or missing datetime values.")
    if data["station"].isna().any():
        raise ValueError("Dataset contains missing station values.")
    if data.duplicated(["station", "datetime"]).any():
        raise ValueError("Dataset contains duplicate station-hour records.")

    return data.sort_values(["station", "datetime"], kind="stable").reset_index(drop=True)


def time_split(
    data: pd.DataFrame,
    test_start: str | pd.Timestamp = TEST_START,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split rows by target time, keeping all stations at a timestamp together.

    The default test period starts on 2016-09-01. The returned first frame
    contains labels earlier than that boundary and is intended for
    training/validation only. If ``target_datetime`` exists, it is used so a
    t+1 label from the test period cannot enter a training row from t.
    """
    if "datetime" not in data.columns:
        raise ValueError("Data must contain a 'datetime' column before splitting.")

    split_column = "target_datetime" if "target_datetime" in data.columns else "datetime"
    timestamps = pd.to_datetime(data[split_column], errors="raise")
    if timestamps.isna().any():
        raise ValueError(f"Data contains missing values in '{split_column}'.")
    boundary = pd.Timestamp(test_start)
    train_validation = data.loc[timestamps < boundary].copy()
    test = data.loc[timestamps >= boundary].copy()
    return train_validation, test


def cv_folds(
    data: pd.DataFrame,
    n_splits: int = 5,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Return expanding-window folds grouped by target timestamp when present.

    The indices refer to row positions in ``data``. All station records for a
    given timestamp are assigned to the same side of each fold.
    """
    if "datetime" not in data.columns:
        raise ValueError("Data must contain a 'datetime' column before CV splitting.")
    if data.empty:
        raise ValueError("Cannot create time-series folds from an empty dataset.")

    split_column = "target_datetime" if "target_datetime" in data.columns else "datetime"
    timestamps = pd.to_datetime(data[split_column], errors="raise")
    if timestamps.isna().any():
        raise ValueError(f"Data contains missing values in '{split_column}'.")
    unique_timestamps = np.sort(timestamps.unique())
    splitter = TimeSeriesSplit(n_splits=n_splits)
    folds = []

    for train_time_idx, validation_time_idx in splitter.split(unique_timestamps):
        train_times = unique_timestamps[train_time_idx]
        validation_times = unique_timestamps[validation_time_idx]
        train_rows = np.flatnonzero(timestamps.isin(train_times).to_numpy())
        validation_rows = np.flatnonzero(timestamps.isin(validation_times).to_numpy())
        folds.append((train_rows, validation_rows))

    return folds
