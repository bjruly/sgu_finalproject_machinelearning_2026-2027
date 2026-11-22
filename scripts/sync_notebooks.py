"""Create output-free copies with identical source; run after editing notebooks/."""

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    destination = ROOT / "notebooks_unexecuted"
    destination.mkdir(exist_ok=True)
    for source in sorted((ROOT / "notebooks").glob("*.ipynb")):
        notebook = deepcopy(json.loads(source.read_text(encoding="utf-8")))
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
        notebook.get("metadata", {}).pop("widgets", None)
        (destination / source.name).write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(source.name)


if __name__ == "__main__":
    main()

