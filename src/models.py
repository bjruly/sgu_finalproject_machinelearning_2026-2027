# Model training module
"""Mô hình baseline: persistence và Linear Regression."""
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

from src.features import build_preprocessor


def persistence(X, fill):
    """Dự đoán PM2.5(t+1) = PM2.5(t). Giờ t còn thiếu sau ffill thì dùng `fill` (median của train)."""
    return X["PM2.5"].fillna(fill)


def make_linreg():
    return make_pipeline(build_preprocessor(scale=True), LinearRegression())