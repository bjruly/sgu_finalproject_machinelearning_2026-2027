import json

import pandas as pd
import pytest

from src.analysis_groups import PM25_LABELS, pm25_levels
from src.notebook_evidence import MIME_TYPE, record_tables, verify_evidence


def test_shared_concentration_groups_assign_exact_edges_once():
    result = pm25_levels(pd.Series([0, 35, 35.1, 75, 115, 150, 250, 250.1]))
    assert result.astype(str).tolist() == ["<=35", "<=35", "(35,75]", "(35,75]",
                                         "(75,115]", "(115,150]", "(150,250]", ">250"]
    assert list(result.cat.categories) == PM25_LABELS


def _notebook(tmp_path):
    folder = tmp_path / "notebooks"
    folder.mkdir()
    path = folder / "test.ipynb"
    notebook = {"cells": [{"cell_type": "code", "id": "evidence", "source": ["value = 2\n"],
                            "execution_count": 1, "outputs": []}]}
    path.write_text(json.dumps(notebook), encoding="utf-8")
    return path, notebook


def test_csv_tampering_is_detected_by_notebook_evidence(tmp_path):
    path, notebook = _notebook(tmp_path)
    payload = record_tables("notebooks/test.ipynb", "evidence",
                            {"outputs/metrics.csv": pd.DataFrame({"rmse": [2.5]})}, root=tmp_path)
    notebook["cells"][0]["outputs"] = [{"data": {MIME_TYPE: payload}}]
    path.write_text(json.dumps(notebook), encoding="utf-8")
    assert len(verify_evidence(tmp_path)) == 1
    (tmp_path / "outputs/metrics.csv").write_text("rmse\n1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="CSV differs"):
        verify_evidence(tmp_path)


def test_source_changes_invalidate_saved_numeric_evidence(tmp_path):
    path, notebook = _notebook(tmp_path)
    payload = record_tables("notebooks/test.ipynb", "evidence",
                            {"outputs/metrics.csv": pd.DataFrame({"rmse": [2.5]})}, root=tmp_path)
    notebook["cells"][0]["outputs"] = [{"data": {MIME_TYPE: payload}}]
    notebook["cells"][0]["source"] = ["value = 3\n"]
    path.write_text(json.dumps(notebook), encoding="utf-8")
    with pytest.raises(ValueError, match="source changed"):
        verify_evidence(tmp_path)


def test_saved_search_mode_does_not_synthesize_or_overwrite_csv(tmp_path):
    _notebook(tmp_path)
    with pytest.raises(FileNotFoundError):
        record_tables("notebooks/test.ipynb", "evidence",
                      {"outputs/metrics.csv": pd.DataFrame({"rmse": [2.5]})},
                      mode="verified_saved_search", root=tmp_path)
