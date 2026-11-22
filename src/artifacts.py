"""Resolve saved artifacts and check estimator compatibility before unpickling."""

import hashlib
import json
from pathlib import Path

import joblib
import sklearn

from src.data_loader import PROJECT_ROOT

MODEL_LABELS = {
    "baseline_persistence": "Persistence",
    "baseline_linreg": "Linear Regression",
    "random_forest_tuned": "Random Forest - tuned",
    "gradient_boosting_tuned": "Gradient Boosting - tuned",
    "mlp_tuned": "MLP - tuned",
}
MODEL_FILES = {
    "baseline_linreg": ("baseline_linear_regression.joblib", "baseline_metadata.json", "experiments01"),
    "random_forest_tuned": ("random_forest_tuned.joblib", "random_forest_tuned_metadata.json", "experiments03"),
    "gradient_boosting_tuned": ("gradient_boosting_tuned.joblib", "gradient_boosting_tuned_metadata.json", "experiments03"),
    "mlp_tuned": ("mlp_tuned.joblib", "mlp_tuned_metadata.json", "experiments03"),
}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_model_paths(root=PROJECT_ROOT, linear_model_path=None):
    """Prefer models/; fall back to the archived artifact without copying it."""
    root = Path(root)
    paths = {}
    for key, (filename, _, experiment) in MODEL_FILES.items():
        if key == "baseline_linreg" and linear_model_path is not None:
            path = Path(linear_model_path)
            path = path if path.is_absolute() else root / path
        else:
            candidates = [
                root / "models" / filename,
                root / "outputs" / "experiments" / experiment / "models" / filename,
            ]
            path = next((p for p in candidates if p.is_file()), candidates[0])
        if not path.is_file():
            raise FileNotFoundError(
                f"Missing model: {path}. Run notebooks 02, 05 and 07 with SAVE_ARTIFACTS=True."
            )
        paths[key] = path
    return paths


def metadata_path(key, model_path):
    return Path(model_path).with_name(MODEL_FILES[key][1])


def load_saved_model(key, path):
    """Reject an incompatible sklearn version rather than patching pickle internals."""
    metadata_file = metadata_path(key, path)
    if not metadata_file.is_file():
        raise FileNotFoundError(f"Missing model metadata: {metadata_file}")
    metadata = json.loads(metadata_file.read_text(encoding="utf-8-sig"))
    expected = metadata.get("sklearn_version")
    if expected and sklearn.__version__ != expected:
        raise RuntimeError(
            f"{Path(path).name} was saved with scikit-learn {expected}; "
            f"running {sklearn.__version__}. Use .venv and requirements.txt "
            "before loading the saved models."
        )
    return joblib.load(path)

