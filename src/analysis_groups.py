"""Shared, explicit concentration boundaries for every current experiment."""

import numpy as np
import pandas as pd

PM25_BINS = [-np.inf, 35, 75, 115, 150, 250, np.inf]
PM25_LABELS = ["<=35", "(35,75]", "(75,115]", "(115,150]", "(150,250]", ">250"]


def pm25_levels(values):
    """Right-closed intervals: exactly 35 belongs to <=35, exactly 250 to (150,250]."""
    return pd.cut(values, PM25_BINS, labels=PM25_LABELS, right=True, include_lowest=True)
