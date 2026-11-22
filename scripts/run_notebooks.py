"""Execute selected existing notebooks with the project's installed Jupyter stack.

--verify-searches executes only the explicitly labeled saved-artifact checks in
05/07. It preserves their historical search outputs and never claims a new search.
"""

import argparse
import asyncio
import json
import os
import runpy
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def notebook_write_target(path, runtime, succeeded):
    """Where to save a notebook after an execution attempt.

    A successful run replaces the notebook in place. A failed run must never
    overwrite the executed evidence in notebooks/, so the partial notebook goes
    to ``<runtime>/<name>.failed.ipynb`` instead.
    """
    path = Path(path)
    if succeeded:
        return path
    return Path(runtime) / f"{path.stem}.failed.ipynb"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="Notebook filenames or two-digit prefixes")
    parser.add_argument("--verify-searches", action="store_true")
    args = parser.parse_args()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    runtime = ROOT / ".notebook_runtime"
    (runtime / "ipython").mkdir(parents=True, exist_ok=True)
    (runtime / "jupyter").mkdir(parents=True, exist_ok=True)
    os.environ["IPYTHONDIR"] = str(runtime / "ipython")
    os.environ["JUPYTER_RUNTIME_DIR"] = str(runtime / "jupyter")
    for name in args.names:
        matches = list((ROOT / "notebooks").glob(name if name.endswith(".ipynb") else name + "_*.ipynb"))
        if len(matches) != 1:
            raise ValueError(f"Ambiguous or missing notebook: {name}")
        path = matches[0]
        notebook = nbformat.read(path, as_version=4)
        search_check = args.verify_searches and path.name.startswith(("05_", "07_"))
        if not search_check:
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None
        def progress(cell, cell_index, **kwargs):
            if cell.cell_type == "code":
                print(f"{path.name}: cell {cell_index + 1} [{cell.get('id', '')}]", flush=True)
        client = NotebookClient(notebook, timeout=2400, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}}, on_cell_start=progress)
        print(f"START {path.name}: {'verify existing search only' if search_check else 'full execution'}", flush=True)
        try:
            if search_check:
                with client.setup_kernel():
                    for index, cell in enumerate(notebook.cells):
                        if cell.cell_type == "code" and cell.get("id", "").startswith("verify-saved-search-"):
                            client.execute_cell(cell, index)
            else:
                client.execute()
        except BaseException:
            # Keep the partial run for debugging, but leave notebooks/ untouched.
            failed = notebook_write_target(path, runtime, succeeded=False)
            nbformat.write(notebook, failed)
            print(f"FAIL {path.name}: partial notebook saved to {failed}; {path} left unchanged", flush=True)
            raise
        nbformat.write(notebook, notebook_write_target(path, runtime, succeeded=True))
        print(f"PASS {path.name}", flush=True)
    runpy.run_path(str(ROOT / "scripts/sync_notebooks.py"), run_name="__main__")


if __name__ == "__main__":
    main()
