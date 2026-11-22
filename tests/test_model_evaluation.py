"""Exercise model persistence and statistical diagnostics beyond data-only tests."""

import json
import warnings

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from src.artifacts import MODEL_FILES, load_saved_model, resolve_model_paths
from src.data_loader import load_data, time_split
from src.eda import eda_tables
from src.evaluation import MODEL_LABELS, grouped_errors, paired_block_intervals, regression_metrics
from src.features import add_features, build_preprocessor, split_xy
from tests.test_feature_engineering import _raw_panel


@pytest.mark.parametrize("estimator", [
    LinearRegression(),
    RandomForestRegressor(n_estimators=3, max_depth=3, random_state=42, n_jobs=1),
    HistGradientBoostingRegressor(max_iter=5, min_samples_leaf=3, early_stopping=False, random_state=42),
    TransformedTargetRegressor(
        regressor=MLPRegressor(hidden_layer_sizes=(4,), max_iter=5, random_state=42),
        transformer=StandardScaler()),
])
def test_model_fit_save_reload_predict(estimator, tmp_path):
    featured = add_features(_raw_panel(periods=48)).dropna(subset=["target"])
    training = featured.loc[featured.datetime < featured.datetime.min() + pd.Timedelta(hours=36)]
    validation = featured.loc[featured.datetime >= featured.datetime.min() + pd.Timedelta(hours=36)]
    X_train, y_train = split_xy(training)
    X_val, _ = split_xy(validation)
    model = Pipeline([("prep", build_preprocessor(scale=True)), ("model", estimator)])
    with threadpool_limits(limits=1), warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        model.fit(X_train, y_train)
        before = model.predict(X_val)
        path = tmp_path / "model.joblib"
        joblib.dump(model, path)
        after = joblib.load(path).predict(X_val)
    assert before.shape == (len(X_val),)
    assert np.isfinite(before).all()
    np.testing.assert_allclose(before, after, rtol=1e-12, atol=1e-12)


def test_model_resolution_falls_back_to_archived_baseline(tmp_path):
    for key, (filename, _, experiment) in MODEL_FILES.items():
        directory = tmp_path / ("outputs/experiments/" + experiment + "/models" if key == "baseline_linreg" else "models")
        directory.mkdir(parents=True, exist_ok=True)
        (directory / filename).touch()
    paths = resolve_model_paths(tmp_path)
    assert "experiments01" in str(paths["baseline_linreg"])
    with pytest.raises(FileNotFoundError, match="Missing model"):
        resolve_model_paths(tmp_path, linear_model_path="not-present.joblib")


def test_incompatible_metadata_is_rejected_before_unpickling(tmp_path):
    path = tmp_path / "baseline_linear_regression.joblib"
    path.write_bytes(b"not a pickle")
    (tmp_path / "baseline_metadata.json").write_text(
        json.dumps({"sklearn_version": "0.0.0"}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="requirements.txt"):
        load_saved_model("baseline_linreg", path)


def _predictions():
    rows = []
    # Unequal sample counts by calendar day catch accidental weighting of daily means.
    for day, n in enumerate([1, 2, 3, 2, 1, 3, 2, 1], start=1):
        for station in range(n):
            y = float(day * 10 + station)
            row = {"station": f"S{station}",
                   "datetime": pd.Timestamp("2016-08-31 23:00") + pd.Timedelta(days=day-1),
                   "target_datetime": pd.Timestamp("2016-09-01") + pd.Timedelta(days=day-1),
                   "y_true": y}
            for key in MODEL_LABELS:
                row[f"pred_{key}"] = y if key == "random_forest_tuned" else y + 2
            rows.append(row)
    return pd.DataFrame(rows)


def test_error_groups_use_target_time_and_right_closed_thresholds():
    frame = _predictions().iloc[:6].copy()
    frame["y_true"] = [35, 75, 115, 150, 250, 251]
    for key in MODEL_LABELS:
        frame[f"pred_{key}"] = frame.y_true
    errors = grouped_errors(frame, "pm25_level")
    selected = errors.loc[errors.model.eq("Persistence")]
    assert selected.n.tolist() == [1] * 6
    assert selected.rmse.eq(0).all()
    month = grouped_errors(frame.iloc[:1], "month")
    assert month.month.eq("2016-09").all()


def test_paired_bootstrap_keeps_pairing_and_is_reproducible():
    frame = _predictions()
    first = paired_block_intervals(frame, n_bootstrap=50, block_days=2)
    second = paired_block_intervals(frame, n_bootstrap=50, block_days=2)
    pd.testing.assert_frame_equal(first, second)
    np.testing.assert_allclose(first[["rmse_difference_a_minus_b", "ci_95_low", "ci_95_high"]], -2)
    with pytest.raises(ValueError, match="Not enough"):
        paired_block_intervals(frame, n_bootstrap=10, block_days=20)


def test_metrics_reject_nonfinite_or_misaligned_predictions():
    with pytest.raises(ValueError):
        regression_metrics([1, 2], [1])
    with pytest.raises(ValueError):
        regression_metrics([1, 2], [1, np.nan])


def test_eda_acf_respects_station_and_hourly_gaps():
    raw = _raw_panel(periods=32)
    tables = eda_tables(raw, max_lag=3)
    np.testing.assert_allclose(tables["pm25_acf"].mean_station_correlation, 1)
    assert tables["pm25_acf"].n_stations.eq(2).all()
    with pytest.raises(ValueError, match="continuous hourly"):
        eda_tables(raw.drop(index=1), max_lag=3)


def test_saved_final_models_predict_in_supported_environment():
    featured = add_features(load_data()).dropna(subset=["target"]).reset_index(drop=True)
    _, test = time_split(featured)
    X, _ = split_xy(test.groupby("station", sort=False).head(2))
    for key, path in resolve_model_paths().items():
        with threadpool_limits(limits=1):
            predictions = load_saved_model(key, path).predict(X)
        assert predictions.shape == (len(X),)
        assert np.isfinite(predictions).all()


def test_unexecuted_notebooks_have_identical_source_and_no_outputs():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    for path in (root / "notebooks").glob("*.ipynb"):
        main = json.loads(path.read_text(encoding="utf-8"))
        clean = json.loads((root / "notebooks_unexecuted" / path.name).read_text(encoding="utf-8"))
        assert [c["source"] for c in main["cells"]] == [c["source"] for c in clean["cells"]]
        assert all(not c.get("outputs") and c.get("execution_count") is None
                   for c in clean["cells"] if c["cell_type"] == "code")

