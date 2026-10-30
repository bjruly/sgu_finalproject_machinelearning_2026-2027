# Tests package init
import numpy as np
import pandas as pd

from src.features import NUM


def toy(n=100, stations=("A", "B"), start="2016-08-30"):
    """2 trạm × n giờ liên tục; PM2.5 = 0..n-1 để dễ kiểm lag."""
    t = pd.date_range(start, periods=n, freq="h")
    frames = []
    for s in stations:
        d = pd.DataFrame({c: np.arange(n, dtype=float) for c in NUM})
        d["station"], d["datetime"], d["wd"] = s, t, "N"
        frames.append(d)
    return pd.concat(frames, ignore_index=True)