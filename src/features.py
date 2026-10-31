# Feature engineering module
"""Tạo đặc trưng (lag/rolling/thời gian) và bộ tiền xử lý sklearn."""
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

POLLUTANTS = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
WEATHER = ["TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
NUM = POLLUTANTS + WEATHER
CAT = ["station", "wd"]
LAGS = (1, 2, 3, 6, 12, 24)
FFILL_LIMIT = 6  # ponytail: giờ; chỉnh sau khi xem lại các khoảng missing dài
NOT_FEATURE = ["target", "datetime", "year", "month", "day", "hour"]


def add_features(df):
    """Mọi thứ tính riêng từng trạm, chỉ dùng thông tin <= giờ t. Giả định mỗi trạm đủ giờ liên tục
    (đã kiểm tra ở EDA) nên shift theo dòng = shift theo giờ.
    Gọi TRƯỚC khi bỏ dòng thiếu target, nếu không lag bị lệch."""
    df = df.sort_values(["station", "datetime"]).reset_index(drop=True)
    g = df.groupby("station")
    df["target"] = g["PM2.5"].shift(-1)  # từ PM2.5 GỐC, trước ffill -> không điền target
    df[NUM + ["wd"]] = g[NUM + ["wd"]].ffill(limit=FFILL_LIMIT)

    g = df.groupby("station")  # tạo lại sau khi ffill
    for k in LAGS:
        df[f"pm25_lag{k}"] = g["PM2.5"].shift(k)
    for w in (6, 24):
        df[f"pm25_roll{w}"] = g["PM2.5"].transform(lambda s: s.rolling(w, min_periods=1).mean())
        df[f"pm25_dev{w}"] = df["PM2.5"] - df[f"pm25_roll{w}"]
    for c in ("TEMP", "PRES", "WSPM"):
        df[f"{c}_lag1"] = g[c].shift(1)

    dt = df["datetime"].dt
    df["hour_sin"], df["hour_cos"] = np.sin(2 * np.pi * dt.hour / 24), np.cos(2 * np.pi * dt.hour / 24)
    df["month_sin"], df["month_cos"] = np.sin(2 * np.pi * dt.month / 12), np.cos(2 * np.pi * dt.month / 12)
    df["dayofweek"] = dt.day_of_week
    df["is_weekend"] = (dt.day_of_week >= 5).astype(int)
    return df


def split_xy(df):
    """(X, y). df phải đã bỏ dòng thiếu target (dropna(subset=["target"])) TRƯỚC khi chia tập,
    để vị trí dòng của X khớp với fold từ cv_folds(df)."""
    return df.drop(columns=NOT_FEATURE, errors="ignore"), df["target"]


def build_preprocessor(scale=False):
    """One-Hot cho station/wd; cột số: median (+ cờ thiếu), StandardScaler chỉ khi scale=True (Linear Regression).
    Đặt trong Pipeline cùng model để mỗi fold tự fit lại trên train."""
    steps = [SimpleImputer(strategy="median", add_indicator=True)]
    if scale:
        steps.append(StandardScaler())
    return ColumnTransformer(
        [("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)],
        remainder=make_pipeline(*steps),
    )