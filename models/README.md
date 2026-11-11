# Thư mục `models`

Nơi lưu các mô hình đã huấn luyện và các thành phần cần thiết để nạp lại mô hình, ví dụ tệp `.joblib`, `.pkl` hoặc `.pt`.

## Tệp hiện có

- `.gitkeep`: tệp rỗng giúp Git lưu thư mục khi chưa có mô hình.

Baseline **Persistence** (dự đoán PM2.5 giờ t+1 bằng PM2.5 giờ t) không có tham số nào học từ dữ liệu nên không có tệp mô hình; cách tính nằm trong hàm `predict_persistence` của notebook 02. Kết quả của nó vẫn có trong `baseline_metrics.csv`.

## Kết quả baseline ở lần chạy gần nhất

RMSE (µg/m³). Đây là số ghi lại tại thời điểm viết; nếu chạy lại notebook, `baseline_metrics.csv` là nguồn chính xác.

| Mô hình         | CV 5 fold (validation) |  Test |
| ----------------- | ---------------------: | ----: |
| Persistence       |                  19.97 | 23.11 |
| Linear Regression |                  19.30 | 21.80 |

Mô hình `Linear Regression (clip at 0)` trong `baseline_metrics.csv` là cùng mô hình nhưng cắt các dự đoán âm về 0 khi tính độ đo; tệp `.joblib` lưu mô hình gốc không cắt.

## Cách nạp lại mô hình

Chạy từ thư mục gốc repository, sau khi đã có CSV chuẩn hóa trong `data/processed/`:

```python
import joblib
from src.data_loader import load_data
from src.features import add_features, split_xy

model = joblib.load("models/baseline_linear_regression.joblib")
featured = add_features(load_data())
labeled = featured.dropna(subset=["target"])
X, y = split_xy(labeled)
predictions = model.predict(X)
```

`X` phải có đúng các cột `FEATURE_COLUMNS` trong `src/features.py`. Tiền xử lý (median, scaler, One-Hot) đã nằm trong pipeline và được fit trên train.

## Lưu ý

- Tệp `.joblib` phụ thuộc phiên bản scikit-learn; nếu nạp lỗi hoặc cảnh báo, hãy dùng phiên bản ghi trong `baseline_metadata.json` hoặc chạy lại notebook 02 để tạo lại.
- Chạy lại notebook 02 sẽ **ghi đè** các tệp `baseline_*` trong thư mục này.
- Random Forest và Gradient Boosting có các tệp riêng, xem các phần bên dưới.

## Các tệp Random Forest (Notebook 03)

Sau khi chạy [`03_random_forest.ipynb`](../notebooks/03_random_forest.ipynb) với `SAVE_ARTIFACTS = True`, thư mục có thêm:

- `random_forest.joblib`: pipeline gồm preprocessing `build_preprocessor(scale=False)` và `RandomForestRegressor`, fit trên toàn bộ Train/Validation. Tệp này không chứa mô hình được fit trên Test.
- `random_forest_metadata.json`: metadata để truy vết, gồm target, dataset version, feature columns, tham số Random Forest, random seed, phiên bản Python/scikit-learn/pandas, thời gian fit, thông tin 5 folds, metrics CV và danh sách artifact đã lưu.

Cấu hình Random Forest hiện tại: `n_estimators=20`, `max_features=0.7`, `max_depth=16`, `min_samples_leaf=5`, `random_state=42`, `n_jobs=-1`.

## Cách nạp lại mô hình Random Forest

Chạy từ thư mục gốc repository:

```python
import joblib

model = joblib.load("models/random_forest.joblib")
```

Đầu vào `X` khi gọi `model.predict(X)` phải có đúng các cột feature mà pipeline mong đợi, theo `FEATURE_COLUMNS` trong `src/features.py`. Preprocessing đã được đóng gói trong pipeline.

## Lưu ý về Random Forest

- Các tệp `.joblib` phụ thuộc phiên bản scikit-learn; tham khảo metadata tương ứng hoặc dùng lại môi trường đã chạy notebook.
- Chạy lại Notebook 02 sẽ cập nhật các artifact `baseline_*`; chạy lại Notebook 03 sẽ cập nhật `random_forest.*`.
- Notebook 03 chỉ dùng Train/Validation cho CV và fit mô hình cuối. Test được giữ riêng, không dùng để tuning, chọn cấu hình hoặc đánh giá trong notebook này.
- Gradient Boosting do Notebook 04 tạo (xem phần bên dưới); các mô hình đã tinh chỉnh (`*_tuned`) do Notebook 05 tạo, xem phần cuối file.

## Các tệp Gradient Boosting (Notebook 04)

Sau khi chạy [`04_gradient_boosting.ipynb`](../notebooks/04_gradient_boosting.ipynb) với `SAVE_ARTIFACTS = True`, thư mục có thêm:

- `gradient_boosting.joblib`: pipeline gồm `build_preprocessor(scale=False)` và `HistGradientBoostingRegressor`, fit trên toàn bộ Train/Validation (360.954 dòng, nhãn đến 31/08/2016). Không chứa mô hình fit trên Test.
- `gradient_boosting_metadata.json`: truy vết gồm target, feature, tham số, seed, phiên bản Python/scikit-learn/pandas, thông tin 5 fold, metrics CV, thời gian chạy và `test_evaluated: false`.

Cấu hình hiện tại: `max_iter=200`, `learning_rate=0.1`, `early_stopping=False`, `random_state=42`; các tham số khác để mặc định của thư viện (ví dụ `max_leaf_nodes=31`, `min_samples_leaf=20`). Dùng bản `HistGradientBoostingRegressor` thay cho `GradientBoostingRegressor` vì chạy nhanh hơn trên khoảng 361 nghìn dòng; proposal cho phép phương án này nhưng cần ghi rõ lý do trong báo cáo.

### Nạp lại mô hình Gradient Boosting

```python
import joblib

model = joblib.load("models/gradient_boosting.joblib")
```

`X` đưa vào `model.predict(X)` phải có đúng các cột `FEATURE_COLUMNS` trong `src/features.py`; tiền xử lý đã nằm trong pipeline.

### Lưu ý về Gradient Boosting

- Tệp `.joblib` phụ thuộc phiên bản scikit-learn (lần chạy ghi nhận: 1.7.2).
- Chạy lại Notebook 04 sẽ ghi đè `gradient_boosting.*`.
- Đây là cấu hình chưa tuning; Test chưa được dùng.

## Các tệp đã tinh chỉnh (Notebook 05)

Sau khi chạy [`05_tuning.ipynb`](../notebooks/05_tuning.ipynb) với `SAVE_ARTIFACTS = True`, thư mục có thêm:

- `gradient_boosting_tuned.joblib`, `random_forest_tuned.joblib`: pipeline của bộ tham số tốt nhất (chọn bằng `RandomizedSearchCV`, RMSE trung bình 5 fold thấp nhất), fit trên toàn bộ Train/Validation. Không chứa mô hình fit trên Test.
- `gradient_boosting_tuned_metadata.json`, `random_forest_tuned_metadata.json`: truy vết gồm tham số tốt nhất, khoảng tìm kiếm, số bộ tham số đã thử (`n_iter`), cấu hình trước tinh chỉnh, hạt giống, phiên bản Python/scikit-learn/pandas, metrics CV và `test_evaluated: false`.

Các tệp `gradient_boosting.*` (Notebook 04) và `random_forest.*` (Notebook 03) là cấu hình **trước** tinh chỉnh và không bị Notebook 05 ghi đè.

### Nạp lại mô hình đã tinh chỉnh

```python
import joblib

gb_tuned = joblib.load("models/gradient_boosting_tuned.joblib")
rf_tuned = joblib.load("models/random_forest_tuned.joblib")
```

`X` đưa vào `predict` phải có đúng các cột `FEATURE_COLUMNS` trong `src/features.py`; tiền xử lý đã nằm trong pipeline.

### Lưu ý về các mô hình đã tinh chỉnh

- Trước khi dùng kết quả, mở file `*_tuned_metadata.json` kiểm tra `tuning.n_iter` (mặc định 20 cho Gradient Boosting, 8 cho Random Forest). Nếu là 2 thì đó là lần chạy thử.
- Chạy lại Notebook 05 sẽ ghi đè `*_tuned.*`.
- Test chưa được dùng; cần chốt cấu hình rồi mới đánh giá Test đúng một lần.
