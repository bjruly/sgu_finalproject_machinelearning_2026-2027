"""Hermetic checks: feature groups, grouped permutation importance, loader error branches,
fold-level fit-only-on-train, and the (guarded) real-data / evidence integrity constants."""

import hashlib
import importlib.util

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from src.data_loader import DEFAULT_DATA_PATH, PROJECT_ROOT, cv_folds, load_data, time_split
from src.features import (FEATURE_COLUMNS, NUMERIC_FEATURES, add_features,
                          build_preprocessor, split_xy)
from src.validation_diagnostics import FEATURE_GROUPS, group_permutation_importance
from tests.test_feature_engineering import _raw_panel


# ---- c. feature groups and grouped permutation importance -------------------------------
def test_feature_groups_partition_all_feature_columns_exactly_once():
    flat = [c for cols in FEATURE_GROUPS.values() for c in cols]
    assert len(flat) == len(set(flat)), "a column appears in more than one group"
    assert set(flat) == set(FEATURE_COLUMNS)
    assert len(flat) == len(FEATURE_COLUMNS)


class _UsesPm25:
    def predict(self, X):
        return X["PM2.5"].to_numpy(dtype=float)


def _synthetic_xy(n=200, seed=0):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({c: rng.normal(size=n) for c in NUMERIC_FEATURES})
    X["station"] = rng.choice(["A", "B", "C"], n)
    X["wd"] = rng.choice(["N", "S"], n)
    X = X[list(FEATURE_COLUMNS)]
    return X, pd.Series(X["PM2.5"].to_numpy() + rng.normal(scale=0.1, size=n))


def test_group_permutation_importance_ranks_only_informative_group_first():
    X, y = _synthetic_xy()
    before = X.copy(deep=True)
    result = group_permutation_importance(_UsesPm25(), X, y, n_repeats=3, seed=1)
    pd.testing.assert_frame_equal(X, before)  # input frame not mutated
    assert result.feature_group.iloc[0] == "current_pm25"
    assert result.rmse_increase_mean.iloc[0] > 0.5
    noise = result.loc[result.feature_group.ne("current_pm25")]
    assert (noise.rmse_increase_mean >= -1e-9).all()
    assert noise.rmse_increase_mean.abs().max() < 1e-9


def test_group_permutation_importance_rejects_non_partition():
    X, y = _synthetic_xy(20)
    with pytest.raises(ValueError, match="partition"):
        group_permutation_importance(_UsesPm25(), X, y, groups={"only": ["PM2.5"]})
    with pytest.raises(ValueError):
        group_permutation_importance(_UsesPm25(), X, y, n_repeats=0)


# ---- d. loader / feature error branches (actual behaviour) -------------------------------
def test_load_data_missing_column_raises(tmp_path):
    path = tmp_path / "d.csv"
    pd.DataFrame({"station": ["A"], "datetime": ["2016-01-01"]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing required columns"):
        load_data(path)


def test_load_data_missing_file_and_missing_station_raise(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "nope.csv")
    path = tmp_path / "d.csv"
    pd.DataFrame({"station": [None], "datetime": ["2016-01-01"], "PM2.5": [1.0]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing station"):
        load_data(path)


def test_load_data_unparseable_datetime_raises(tmp_path):
    path = tmp_path / "d.csv"
    pd.DataFrame({"station": ["A"], "datetime": ["not a date"], "PM2.5": [1.0]}).to_csv(path, index=False)
    with pytest.raises(Exception):
        load_data(path)


def test_load_data_header_only_file_currently_returns_empty_frame(tmp_path):
    # Documents actual behaviour: load_data does NOT reject an empty (header-only) file.
    path = tmp_path / "d.csv"
    pd.DataFrame({"station": [], "datetime": [], "PM2.5": []}).to_csv(path, index=False)
    assert load_data(path).empty


def test_cv_folds_rejects_empty_frame_and_split_rejects_missing_values():
    empty = pd.DataFrame({"station": [], "datetime": pd.to_datetime([])})
    with pytest.raises(ValueError, match="empty"):
        cv_folds(empty)
    with pytest.raises(ValueError, match="missing values"):
        time_split(pd.DataFrame({"datetime": [pd.Timestamp("2016-01-01"), pd.NaT]}))
    with pytest.raises(ValueError, match="datetime"):
        time_split(pd.DataFrame({"x": [1]}))


def test_add_features_error_branches():
    base = _raw_panel(10)
    with pytest.raises(ValueError, match="missing required columns"):
        add_features(base.drop(columns=["PM10"]))
    with pytest.raises(ValueError, match="duplicate"):
        add_features(pd.concat([base, base.iloc[:1]], ignore_index=True))
    with pytest.raises(ValueError, match="continuous hourly"):
        add_features(base.drop(index=[4]).reset_index(drop=True))
    with pytest.raises(ValueError, match="ffill_limit"):
        add_features(base, ffill_limit=-1)
    nan_station = base.copy()
    nan_station.loc[0, "station"] = None
    with pytest.raises(ValueError, match="must not be missing"):
        add_features(nan_station)
    with pytest.raises(ValueError, match="missing columns"):
        split_xy(base)


def test_add_features_empty_frame_behaviour_is_documented():
    empty = _raw_panel(10).iloc[:0]
    try:
        result = add_features(empty)
    except ValueError:
        return  # rejecting an empty frame is acceptable
    assert result.empty


def test_time_split_without_target_datetime_falls_back_to_datetime():
    # Documents the current fallback (see data_loader.time_split); existing tests rely on it.
    data = pd.DataFrame({"datetime": pd.to_datetime(["2016-08-31 23:00", "2016-09-01 00:00"])})
    train, test = time_split(data)
    assert len(train) == 1 and len(test) == 1


# ---- e. every fitted statistic comes from the training fold only -------------------------
def test_preprocessing_pipeline_fits_only_on_train_fold_statistics():
    rng = np.random.default_rng(0)
    n = 200
    frame = pd.DataFrame({c: rng.normal(size=n) for c in NUMERIC_FEATURES})
    frame["station"] = "A"
    frame["wd"] = "N"
    half = n // 2
    shift = np.where(np.arange(n) < half, 0.0, 1000.0)  # validation distribution is far away
    frame.loc[:, list(NUMERIC_FEATURES)] += shift[:, None]
    frame.loc[::7, "TEMP"] = np.nan  # make imputation matter
    y = pd.Series(rng.normal(size=n))
    train_idx = np.arange(half)
    pipe = Pipeline([("prep", build_preprocessor(scale=True)), ("model", LinearRegression())])
    pipe.fit(frame.iloc[train_idx][list(FEATURE_COLUMNS)], y.iloc[train_idx])
    numeric = pipe.named_steps["prep"].named_transformers_["numeric"]
    train = frame.iloc[train_idx][list(NUMERIC_FEATURES)]
    full = frame[list(NUMERIC_FEATURES)]
    np.testing.assert_allclose(numeric.named_steps["imputer"].statistics_, train.median().to_numpy())
    assert not np.allclose(numeric.named_steps["imputer"].statistics_, full.median().to_numpy())
    imputed_train = train.fillna(train.median())
    np.testing.assert_allclose(numeric.named_steps["scaler"].mean_, imputed_train.mean().to_numpy())
    np.testing.assert_allclose(numeric.named_steps["scaler"].scale_, imputed_train.std(ddof=0).to_numpy())
    assert numeric.named_steps["scaler"].mean_.max() < 10  # nowhere near validation (~1000)


# ---- f. documented constants on the real dataset ----------------------------------------
@pytest.mark.skipif(not DEFAULT_DATA_PATH.is_file(), reason="processed dataset not present")
def test_real_dataset_matches_constants_quoted_in_report():
    raw = load_data()
    assert len(raw) == 420_768 and raw.station.nunique() == 12
    labeled = add_features(raw).dropna(subset=["target"]).reset_index(drop=True)
    assert len(labeled) == 412_017
    train_validation, test = time_split(labeled)
    assert (len(train_validation), len(test)) == (360_954, 51_063)
    sizes = [(len(a), len(b)) for a, b in cv_folds(train_validation, n_splits=5)]
    assert sizes == [(60_258, 60_595), (120_853, 59_958), (180_811, 59_858),
                     (240_669, 60_217), (300_886, 60_068)]


# ---- g. read-only evidence integrity ------------------------------------------------------
SOURCES = PROJECT_ROOT / "outputs" / "notebooks" / "tables" / "report_sources.csv"


@pytest.mark.skipif(not SOURCES.is_file(), reason="report_sources.csv not present")
def test_report_source_csv_hashes_match_recorded_values():
    index = pd.read_csv(SOURCES, encoding="utf-8-sig")
    checked = 0
    for row in index.itertuples():
        path = PROJECT_ROOT / row.csv_path
        if not path.is_file():
            continue
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row.csv_sha256, row.csv_path
        checked += 1
    assert checked > 0


# ---- 1. run_notebooks write decision (pure function, no kernel) --------------------------
def test_failed_notebook_run_never_targets_the_executed_notebook(tmp_path):
    script = PROJECT_ROOT / "scripts" / "run_notebooks.py"
    if not script.is_file():
        pytest.skip("scripts/run_notebooks.py not present")
    spec = importlib.util.spec_from_file_location("run_notebooks_under_test", script)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError:
        pytest.skip("nbformat/nbclient not installed")
    path = tmp_path / "notebooks" / "05_tuning.ipynb"
    runtime = tmp_path / ".notebook_runtime"
    assert module.notebook_write_target(path, runtime, succeeded=True) == path
    failed = module.notebook_write_target(path, runtime, succeeded=False)
    assert failed == runtime / "05_tuning.failed.ipynb" and failed != path
