import numpy as np
import pandas as pd
import pytest

from src.evaluation import PREDICTION_COLUMNS, trimmed_sensitivity


def _frame():
    y = np.arange(1.0, 101.0)
    data = {"y_true": y}
    for index, column in enumerate(PREDICTION_COLUMNS):
        data[column] = y + 1.0 + index  # constant offsets
    data[PREDICTION_COLUMNS[0]] = data[PREDICTION_COLUMNS[0]].copy()
    frame = pd.DataFrame(data)
    frame.loc[0, PREDICTION_COLUMNS] = 1000.0  # one extreme row for every model
    return frame


def test_zero_fraction_keeps_all_rows_and_trimming_removes_same_rows():
    result = trimmed_sensitivity(_frame(), fractions=(0.0, 0.01))
    assert result[result.trimmed_fraction == 0.0].n_removed.eq(0).all()
    trimmed = result[result.trimmed_fraction == 0.01]
    assert trimmed.n_removed.eq(1).all() and trimmed.n_kept.eq(99).all()
    # the extreme row dominates RMSE; removing it leaves only the constant offsets
    assert (trimmed.rmse.to_numpy() < result[result.trimmed_fraction == 0.0].rmse.to_numpy()).all()
    assert np.allclose(sorted(trimmed.rmse), [1, 2, 3, 4, 5])


def test_rejects_invalid_fraction():
    with pytest.raises(ValueError):
        trimmed_sensitivity(_frame(), fractions=(1.0,))
