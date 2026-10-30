# Thư mục `src`

Nơi chứa mã nguồn Python của pipeline học máy: nạp dữ liệu, tạo đặc trưng, huấn luyện mô hình baseline và đánh giá kết quả. Các module import theo dạng `from src.xxx import ...`, nên cần chạy từ thư mục gốc của repository (hoặc thêm thư mục gốc vào `sys.path`, như notebook 02 đang làm).

## Các tệp hiện có

- `__init__.py`: đánh dấu `src` là một Python package.
- `data_loader.py`: nạp và chia dữ liệu.
  - `load_data()`: đọc `data/processed/beijing_air_quality_standardized.csv`, giữ nguyên missing, bỏ cột `No`.
  - `time_split(df)`: chia train/validation và test theo thời gian; test bắt đầu từ 01/09/2016.
  - `cv_folds(df, n_splits=5)`: `TimeSeriesSplit` expanding-window trên các timestamp duy nhất, nên 12 trạm cùng một giờ luôn nằm chung một fold. Trả về danh sách `(train_idx, val_idx)` để dùng trực tiếp cho tham số `cv=` của scikit-learn.
- `features.py`: tạo đặc trưng và bộ tiền xử lý.
  - `add_features(df)`: tạo target PM2.5 giờ t+1 theo từng trạm, forward-fill có giới hạn theo trạm, lag PM2.5 (1, 2, 3, 6, 12, 24 giờ), rolling mean 6/24 giờ và độ lệch so với rolling mean, lag khí tượng (TEMP, PRES, WSPM), sin/cos của giờ và tháng, thứ trong tuần, cờ cuối tuần.
  - `split_xy(df)`: tách `(X, y)`, bỏ các cột không phải đặc trưng (`target`, `datetime`, `year`, `month`, `day`, `hour`).
  - `build_preprocessor(scale)`: One-Hot cho `station` và `wd`; các cột số điền median kèm cờ báo thiếu; `StandardScaler` chỉ bật khi `scale=True` (dành cho Linear Regression).
- `models.py`: mô hình baseline.
  - `persistence(X, fill)`: dự đoán PM2.5(t+1) bằng PM2.5(t); giờ t còn thiếu thì dùng `fill` (median của train).
  - `make_linreg()`: Pipeline gồm `build_preprocessor(scale=True)` và `LinearRegression`.
- `evaluate.py`: đánh giá và ghi nhật ký.
  - `metrics(y, pred)`: trả về MAE, RMSE và R².
  - `log_experiment(...)`: thêm một dòng vào `experiment_log.csv`.

## Cách dùng

```python
from src.data_loader import cv_folds, load_data, time_split
from src.evaluate import metrics
from src.features import add_features, split_xy
from src.models import make_linreg

df = add_features(load_data()).dropna(subset=["target"])
train_val, test = time_split(df)       # test chỉ dùng cho đánh giá cuối
folds = cv_folds(train_val)
X, y = split_xy(train_val)

a, b = folds[0]
pred = make_linreg().fit(X.iloc[a], y.iloc[a]).predict(X.iloc[b])
print(metrics(y.iloc[b], pred))
```

Mô hình cây có thể dùng chung pipeline này: `make_pipeline(build_preprocessor(scale=False), RandomForestRegressor(...))`.

## Quy ước chống rò rỉ dữ liệu

- Target được tạo từ PM2.5 gốc trước khi forward-fill, nên không bao giờ bị điền.
- Mọi lag, rolling và forward-fill đều tính riêng theo trạm và chỉ dùng dữ liệu đến giờ t.
- Gọi `add_features` trước, rồi mới `dropna(subset=["target"])`; làm ngược lại sẽ làm lag bị lệch.
- Phải bỏ dòng thiếu target trước khi `time_split` và `cv_folds`, để vị trí dòng của `X` khớp với chỉ số fold.
- Imputer, scaler và encoder nằm trong Pipeline cùng mô hình, nên được fit lại trên train của từng fold.

## Giả định và điểm cần chốt

- Mỗi trạm có đủ giờ liên tục (đã kiểm tra ở EDA), nên shift theo dòng tương đương shift theo giờ.
- `FFILL_LIMIT = 6` giờ trong `features.py` là giá trị tạm, cần chốt lại sau khi xem các khoảng missing dài.

## Kiểm thử

Các test tương ứng nằm trong [`../tests/`](../tests/README.md); chạy bằng `python -m pytest -q` từ thư mục gốc repository.