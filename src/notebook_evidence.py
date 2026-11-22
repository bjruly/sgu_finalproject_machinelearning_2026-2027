"""Record computed notebook tables using existing JSON/CSV dependencies only.

The JSON is displayed as a notebook output. Verification ties each CSV to the
cell ID, code digest and numerical records in that executed notebook. It is not
an experiment-tracking service and does not claim to recover historical runs.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.artifacts import sha256_file
from src.data_loader import PROJECT_ROOT

MIME_TYPE = "application/vnd.beijing.notebook-evidence+json"


def notebook_code_sha256(notebook):
    cells = [{"cell_type": c["cell_type"], "id": c.get("id"), "source": "".join(c["source"])}
             for c in notebook["cells"]]
    return hashlib.sha256(json.dumps(cells, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def evidence_frame(table):
    result = table.copy().reset_index(drop=True)
    result.columns = result.columns.astype(str)
    if not result.columns.is_unique:
        raise ValueError("Evidence tables must have unique column names.")
    for column in result:
        if pd.api.types.is_datetime64_any_dtype(result[column]):
            result[column] = result[column].astype(str)
        elif isinstance(result[column].dtype, pd.PeriodDtype):
            result[column] = result[column].astype(str)
        elif isinstance(result[column].dtype, pd.CategoricalDtype):
            result[column] = result[column].astype(object)
    return result


def record_tables(notebook_path, cell_id, tables, *, mode="computed", root=PROJECT_ROOT):
    """Export actual DataFrames, return a displayable payload with numerical evidence.

    computed: variables produced by the notebook in this execution.
    verified_saved_search: checks of existing search artifacts, not a fresh search.
    Large row-level artifacts carry a digest; report-sized tables include records.
    """
    if mode not in {"computed", "verified_saved_search"}:
        raise ValueError("Unsupported evidence mode.")
    root = Path(root).resolve()
    notebook_path = (root / notebook_path).resolve()
    notebook_path.relative_to(root)
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    if sum(c.get("id") == cell_id for c in notebook["cells"]) != 1:
        raise ValueError(f"Missing or ambiguous evidence cell: {cell_id}")
    payload = {"notebook": notebook_path.relative_to(root).as_posix(), "cell_id": cell_id,
               "notebook_code_sha256": notebook_code_sha256(notebook), "mode": mode,
               "recorded_at_utc": datetime.now(timezone.utc).isoformat(), "tables": []}
    for relative, table in tables.items():
        path = (root / relative).resolve()
        path.relative_to(root)
        table = evidence_frame(table)
        path.parent.mkdir(parents=True, exist_ok=True)
        if mode == "computed":
            table.to_csv(path, index=False, encoding="utf-8-sig")
        elif not path.is_file():
            raise FileNotFoundError(path)
        actual = pd.read_csv(path, encoding="utf-8-sig")
        pd.testing.assert_frame_equal(actual, table, check_dtype=False, check_exact=False,
                                      rtol=1e-9, atol=1e-10)
        item = {"path": path.relative_to(root).as_posix(), "csv_sha256": sha256_file(path),
                "n_rows": len(table), "columns": list(table.columns)}
        if len(table) <= 2000:
            item["records"] = json.loads(table.to_json(orient="records", double_precision=15))
        payload["tables"].append(item)
    return payload


def display_evidence(payload):
    from IPython.display import display
    display({MIME_TYPE: payload, "text/plain": (
        f"Notebook evidence: {payload['notebook']} / {payload['cell_id']} / "
        f"{payload['mode']} / {len(payload['tables'])} CSV files")}, raw=True)


def verify_evidence(root=PROJECT_ROOT, write_index=False):
    """Fail when a CSV or its producing notebook code differs from saved evidence."""
    root = Path(root).resolve()
    rows = []
    for path in sorted((root / "notebooks").glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        digest = notebook_code_sha256(notebook)
        for index, cell in enumerate(notebook["cells"]):
            for output in cell.get("outputs", []):
                payload = output.get("data", {}).get(MIME_TYPE)
                if not payload:
                    continue
                if payload["notebook_code_sha256"] != digest:
                    raise ValueError(f"Notebook source changed after execution: {path.name}")
                if payload["cell_id"] != cell.get("id") or cell.get("execution_count") is None:
                    raise ValueError(f"Invalid evidence cell in {path.name}")
                for item in payload["tables"]:
                    artifact = root / item["path"]
                    if sha256_file(artifact) != item["csv_sha256"]:
                        raise ValueError(f"CSV differs from notebook evidence: {item['path']}")
                    actual = pd.read_csv(artifact, encoding="utf-8-sig")
                    if len(actual) != item["n_rows"] or list(actual) != item["columns"]:
                        raise ValueError(f"CSV shape differs: {item['path']}")
                    if "records" in item:
                        expected = pd.DataFrame(item["records"], columns=item["columns"])
                        for column in expected:
                            if expected[column].dtype == object:
                                expected[column] = expected[column].where(expected[column].notna(), float("nan"))
                        pd.testing.assert_frame_equal(actual, expected, check_dtype=False,
                                                      check_exact=False, rtol=1e-9, atol=1e-10)
                    rows.append({"csv_path": item["path"], "notebook": payload["notebook"],
                                 "cell_id": payload["cell_id"], "cell_number": index + 1,
                                 "execution_count": cell["execution_count"], "mode": payload["mode"],
                                 "n_rows": item["n_rows"], "csv_sha256": item["csv_sha256"],
                                 "notebook_code_sha256": digest,
                                 "recorded_at_utc": payload["recorded_at_utc"]})
    result = pd.DataFrame(rows)
    if write_index:
        destination = root / "outputs/notebooks/tables/report_sources.csv"
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(destination, index=False, encoding="utf-8-sig")
    return result
