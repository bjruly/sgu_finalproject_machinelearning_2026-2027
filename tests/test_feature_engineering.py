# Unit tests for feature engineering
import numpy as np

from src.features import NOT_FEATURE, add_features, split_xy
from tests import toy


def test_target_is_next_hour_same_station():
    out = add_features(toy(50))
    for _, g in out.groupby("station"):
        assert (g["target"].iloc[:-1].to_numpy() == g["PM2.5"].iloc[1:].to_numpy()).all()
        assert np.isnan(g["target"].iloc[-1])          # giờ cuối không có t+1, không tràn sang trạm khác


def test_lag_within_station():
    out = add_features(toy(50))
    for _, g in out.groupby("station"):
        assert g["pm25_lag3"].iloc[:3].isna().all()    # không mượn dữ liệu của trạm trước
        assert (g["pm25_lag3"].iloc[3:] == g["PM2.5"].iloc[3:] - 3).all()


def test_no_future_leak():
    df = toy(100)
    cut = df["datetime"].iloc[50]
    df2 = df.copy()
    df2.loc[df2["datetime"] > cut, ["PM2.5", "TEMP", "CO"]] += 1000
    a, b = add_features(df), add_features(df2)
    past = a["datetime"] <= cut
    cols = [c for c in a.columns if c not in NOT_FEATURE]
    assert a.loc[past, cols].equals(b.loc[past, cols])  # feature quá khứ không đổi khi tương lai đổi


def test_target_never_filled_but_features_ffilled():
    df = toy(50)
    df.loc[10, "PM2.5"] = np.nan                       # thủng 1 giờ ở trạm A
    out = add_features(df)
    assert np.isnan(out.loc[9, "target"])              # target (PM2.5 giờ 10) không được điền
    assert out.loc[10, "PM2.5"] == 9                   # feature thì ffill từ giờ 9
    X, y = split_xy(out.dropna(subset=["target"]))
    assert len(X) == len(y) == out["target"].notna().sum() and "target" not in X