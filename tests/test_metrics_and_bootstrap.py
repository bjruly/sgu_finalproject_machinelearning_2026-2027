"""Hermetic checks of metric definitions, residual sign and the paired block bootstrap."""

import itertools
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.artifacts import MODEL_FILES, MODEL_LABELS
from src.evaluation import export_analysis, paired_block_intervals, regression_metrics

PAIR = [("random_forest_tuned", "baseline_persistence")]


def _frame(errors_a, errors_b, stations=2):
    """One row per station per day; per-day errors given for model a and model b."""
    rows = []
    for day, (ea, eb) in enumerate(zip(errors_a, errors_b)):
        for s in range(stations):
            y = 50.0 + 10 * day + s
            row = {"station": f"S{s}", "y_true": y,
                   "datetime": pd.Timestamp("2016-08-31 23:00") + pd.Timedelta(days=day),
                   "target_datetime": pd.Timestamp("2016-09-01 12:00") + pd.Timedelta(days=day)}
            for key in MODEL_LABELS:
                row[f"pred_{key}"] = y + 1.0
            row["pred_random_forest_tuned"] = y + ea
            row["pred_baseline_persistence"] = y + eb
            rows.append(row)
    return pd.DataFrame(rows)


def test_regression_metrics_known_values():
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 3, 2, 6, 4]  # y_true - y_pred = 0, -1, 1, -2, 1
    scores = regression_metrics(y_true, y_pred)
    assert scores["mae"] == pytest.approx(1.0)
    assert scores["rmse"] == pytest.approx(np.sqrt(1.4))
    assert scores["r2"] == pytest.approx(1 - 7 / 10)
    assert scores["mean_residual"] == pytest.approx(-0.2)


def test_residual_sign_positive_means_under_prediction():
    assert regression_metrics([10.0, 12.0], [8.0, 9.0])["mean_residual"] == pytest.approx(2.5)
    assert regression_metrics([10.0, 12.0], [13.0, 15.0])["mean_residual"] == pytest.approx(-3.0)


def test_bootstrap_identical_errors_give_zero_interval():
    frame = _frame([1, -2, 3, 0.5, 2, -1], [1, -2, 3, 0.5, 2, -1])
    result = paired_block_intervals(frame, pairs=PAIR, n_bootstrap=100, block_days=2)
    row = result.iloc[0]
    assert (row.rmse_difference_a_minus_b, row.ci_95_low, row.ci_95_high) == (0.0, 0.0, 0.0)


def test_bootstrap_uniformly_better_model_has_interval_below_zero():
    # Model a errs by 1 every day; model b errs by 2..7 (varying), so resamples vary.
    frame = _frame([1.0] * 8, [2, 3, 4, 5, 6, 7, 2, 3])
    row = paired_block_intervals(frame, pairs=PAIR, n_bootstrap=300, block_days=2).iloc[0]
    assert row.rmse_difference_a_minus_b < 0
    assert row.ci_95_low < row.ci_95_high  # non-degenerate
    assert row.ci_95_high < 0


def test_bootstrap_same_seed_same_result_and_other_seed_differs():
    frame = _frame([1, 4, 2, 5, 1, 3, 6, 2], [3, 1, 5, 2, 4, 1, 2, 6])
    kwargs = dict(pairs=PAIR, n_bootstrap=200, block_days=2)
    first = paired_block_intervals(frame, seed=7, **kwargs)
    pd.testing.assert_frame_equal(first, paired_block_intervals(frame, seed=7, **kwargs))
    other = paired_block_intervals(frame, seed=8, **kwargs)
    assert not np.allclose(first[["ci_95_low", "ci_95_high"]], other[["ci_95_low", "ci_95_high"]])


def test_bootstrap_single_block_spanning_all_days_reproduces_the_estimate():
    # n_days == block_days leaves one possible block (the original series).
    frame = _frame([1, 4, 2, 5], [3, 1, 5, 2])
    row = paired_block_intervals(frame, pairs=PAIR, n_bootstrap=50, block_days=4).iloc[0]
    assert row.ci_95_low == pytest.approx(row.rmse_difference_a_minus_b)
    assert row.ci_95_high == pytest.approx(row.rmse_difference_a_minus_b)


def test_bootstrap_resamples_whole_days_in_blocks_with_stations_together():
    errors_a, errors_b = [1, 4, 2, 5], [3, 1, 5, 2]
    frame = _frame(errors_a, errors_b, stations=3)
    row = paired_block_intervals(frame, pairs=PAIR, n_bootstrap=400, block_days=2).iloc[0]
    # Every resample is two blocks [s, s+1], s in {0,1,2}; enumerate all outcomes.
    # All days have equal station count so day loss = n * error^2.
    outcomes = []
    for s1, s2 in itertools.product(range(3), repeat=2):
        days = [s1, s1 + 1, s2, s2 + 1]
        a = np.sqrt(np.mean([errors_a[d] ** 2 for d in days]))
        b = np.sqrt(np.mean([errors_b[d] ** 2 for d in days]))
        outcomes.append(a - b)
    assert min(outcomes) - 1e-9 <= row.ci_95_low <= row.ci_95_high <= max(outcomes) + 1e-9
    # Row order inside the frame must not matter (stations are never split from their day).
    shuffled = frame.sample(frac=1, random_state=3).reset_index(drop=True)
    again = paired_block_intervals(shuffled, pairs=PAIR, n_bootstrap=400, block_days=2).iloc[0]
    assert again.ci_95_low == pytest.approx(row.ci_95_low)
    assert again.ci_95_high == pytest.approx(row.ci_95_high)


def test_manifest_paths_are_repo_relative_posix(tmp_path):
    import matplotlib
    matplotlib.use("Agg")
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "mod.py").write_text("x = 1\n", encoding="utf-8")
    data_path = root / "data" / "processed" / "d.csv"
    data_path.parent.mkdir(parents=True)
    data_path.write_text("a\n1\n", encoding="utf-8")
    model_paths = {}
    for key, (filename, metadata, _) in MODEL_FILES.items():
        folder = root / "models"
        folder.mkdir(exist_ok=True)
        (folder / filename).write_bytes(b"model")
        (folder / metadata).write_text(json.dumps({"sklearn_version": "0"}), encoding="utf-8")
        model_paths[key] = folder / filename
    frame = _frame([1, 2, 3, 1, 2, 3, 1, 2], [2, 1, 3, 2, 1, 3, 2, 1])
    out = root / "outputs" / "analysis"
    tables = export_analysis(frame, model_paths, out, n_bootstrap=10, block_days=2,
                             project_root=root, data_path=data_path)
    manifest = json.loads((out / "evaluation_manifest.json").read_text(encoding="utf-8"))

    paths = [manifest["dataset"], *manifest["source_sha256"], *manifest["outputs"]]
    for model in manifest["models"].values():
        paths += [model["path"], model["metadata_path"]]
    assert paths
    for value in paths:
        assert "\\" not in value
        assert not Path(value).is_absolute() and not re.match(r"^[A-Za-z]:", value)
        assert not value.startswith("/")
    assert manifest["dataset"] == "data/processed/d.csv"
    assert manifest["models"]["mlp_tuned"]["path"] == "models/mlp_tuned.joblib"
    text = json.dumps(manifest)
    assert str(tmp_path) not in text and tmp_path.as_posix() not in text
    # Residual sign convention is exposed in exported worst cases and the manifest.
    worst = tables["final_test_worst_cases.csv"]
    np.testing.assert_allclose(worst.residual, worst.y_true - worst.y_pred)
    assert manifest["residual_definition"] == "y_true - y_pred"
