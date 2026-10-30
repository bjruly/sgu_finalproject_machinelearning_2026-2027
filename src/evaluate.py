# Evaluation metrics module
"""Độ đo và ghi nhật ký thực nghiệm."""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_loader import ROOT

LOG = ROOT / "experiment_log.csv"


def metrics(y, pred):
    return {
        "mae": mean_absolute_error(y, pred),
        "rmse": float(np.sqrt(mean_squared_error(y, pred))),
        "r2": r2_score(y, pred),
    }


def log_experiment(model_name, dataset_version, m, notes="", path=LOG):
    """Thêm 1 dòng vào experiment_log.csv (cột: experiment_id,model_name,dataset_version,mae,rmse,r2,notes)."""
    n = len(pd.read_csv(path))
    row = pd.DataFrame([[n + 1, model_name, dataset_version, m["mae"], m["rmse"], m["r2"], notes]])
    row.to_csv(path, mode="a", header=False, index=False)