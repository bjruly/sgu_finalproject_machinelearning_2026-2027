# Thư mục `models`

Nơi lưu các mô hình đã huấn luyện và các thành phần cần thiết để nạp lại mô hình, ví dụ tệp `.joblib`, `.pkl` hoặc `.pt`, cùng bảng tóm tắt kết quả của các mô hình đó.

## Tệp hiện có

- `baseline_linear_regression.joblib`: pipeline Linear Regression (`build_preprocessor(scale=True)` + `LinearRegression`) đã fit trên **toàn bộ** tập train/validation (nhãn từ 01/03/2013 đến 31/08/2016). Tệp được tạo bởi [`02_model_training_baseline.ipynb`](../notebooks/02_model_training_baseline.ipynb).
- `baseline_metrics.csv`: MAE, RMSE, R² của các baseline. Cột `split` có hai giá trị: `cv_validation_mean_5fold` (trung bình 5 fold validation, kèm `*_std` là độ lệch chuẩn giữa các fold) và `test` (tập test từ 01/09/2016, các cột `*_std` để trống). Cột `n_rows` là số dòng dùng để tính.
- `baseline_metadata.json`: thông tin để nạp lại và truy vết mô hình: danh sách feature, khoảng thời gian train, mốc bắt đầu test, cách chia CV và phiên bản scikit-learn đã dùng.
- `.gitkeep`: tệp rỗng giúp Git lưu thư mục.

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
- Các mô hình cây (Random Forest, Gradient Boosting) chưa được huấn luyện và chưa có trong thư mục này.




## Các tệp Random Forest (Notebook 03)

Sau khi chạy [`03_advanced_models_and_tuning.ipynb`](../notebooks/03_advanced_models_and_tuning.ipynb) với `SAVE_ARTIFACTS = True`, thư mục có thêm:

- `random_forest.joblib`: pipeline gồm preprocessing `build_preprocessor(scale=False)` và `RandomForestRegressor`, fit trên toàn bộ Train/Validation. Tệp này không chứa mô hình được fit trên Test.
- `random_forest_metadata.json`: metadata để truy vết, gồm target, dataset version, feature columns, tham số Random Forest, random seed, phiên bản Python/scikit-learn/pandas, thời gian fit, thông tin 5 folds, metrics CV và danh sách artifact đã lưu.

Cấu hình Random Forest hiện tại: `n_estimators=20`, `max_features=0.7`, `max_depth=16`, `min_samples_leaf=5`, `random_state=42`, `n_jobs=-1`.

## Cách nạp lại mô hình

Chạy từ thư mục gốc repository:

```python
import joblib

model = joblib.load("models/random_forest.joblib")
```

Đầu vào `X` khi gọi `model.predict(X)` phải có đúng các cột feature mà pipeline mong đợi, theo `FEATURE_COLUMNS` trong `src/features.py`. Preprocessing đã được đóng gói trong pipeline.

## Lưu ý

- Các tệp `.joblib` phụ thuộc phiên bản scikit-learn; tham khảo metadata tương ứng hoặc dùng lại môi trường đã chạy notebook.
- Chạy lại Notebook 02 sẽ cập nhật các artifact `baseline_*`; chạy lại Notebook 03 sẽ cập nhật `random_forest.*`.
- Notebook 03 chỉ dùng Train/Validation cho CV và fit mô hình cuối. Test được giữ riêng, không dùng để tuning, chọn cấu hình hoặc đánh giá trong notebook này.
- Gradient Boosting và các artifact tuning chưa được tạo bởi Notebook 03 hiện tại.
