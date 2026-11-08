# Thư mục `notebooks`

Nơi lưu các Jupyter Notebook dùng để khám phá dữ liệu (EDA), tiền xử lý, thử nghiệm mô hình và tinh chỉnh siêu tham số.

## Các tệp hiện có

- `01_eda_and_preprocessing.ipynb`: EDA 12 CSV PRSA; kiểm tra schema, thời gian, missing, phân bố PM2.5, xu hướng theo tháng/giờ/mùa và tương quan. Cuối notebook có bước xuất bản CSV chuẩn hóa nhưng không impute hoặc tiền xử lý thành dữ liệu model-ready.
- `02_model_training_baseline.ipynb`: huấn luyện và đánh giá hai baseline cho bài toán dự đoán PM2.5 giờ t+1:
  - **Persistence**: dự đoán PM2.5(t+1) = PM2.5(t), không học tham số.
  - **Linear Regression**: pipeline `build_preprocessor(scale=True)` + `LinearRegression`.
  - Dùng lại pipeline trong `src/` (đặc trưng, chia thời gian, 5 fold expanding-window) và đánh giá bằng MAE, RMSE, R².
  - Phân tích sai số theo trạm, mùa, mức PM2.5 và theo tháng; residual; hệ số và permutation importance theo nhóm feature của Linear Regression.
  - Có mục đánh giá trên tập test, điều khiển bằng cờ `RUN_FINAL_TEST`.
  - Mục 13 ghép (`merge`) các bảng kết quả của hai mô hình, ghép thêm với nhật ký `experiment_log.csv`, rồi **xuất file so sánh kết quả thực nghiệm** (Excel và CSV).
- `03_advanced_models_and_tuning.ipynb`: dự kiến thử nghiệm mô hình nâng cao và tinh chỉnh tham số. Notebook này hiện còn rỗng.

## Chạy notebook 02

Điều kiện: đã có `data/processed/beijing_air_quality_standardized.csv` (tạo từ notebook 01) và đã cài các thư viện trong `requirements.txt`; môi trường cần có Jupyter hoặc `ipykernel` để chạy notebook. Để xuất file Excel ở mục 13 cần thêm `openpyxl` (`pip install openpyxl`); nếu thiếu, notebook vẫn chạy, chỉ bỏ qua file Excel và vẫn ghi CSV.

Mở notebook rồi chọn `Restart & Run All`. Chạy từ thư mục gốc hay từ `notebooks/` đều được; thời gian khoảng 1–2 phút. Hai cờ ở mục 1:

- `SAVE_ARTIFACTS`: `True` thì ghi mô hình, bảng và hình ra đĩa; `False` thì chỉ chạy thử.
- `RUN_FINAL_TEST`: `True` thì đánh giá baseline trên tập test (mục 11). Baseline không có siêu tham số nào chọn dựa trên test; không quay lại sửa baseline sau khi xem số test.

## Notebook 02 tạo ra

- `models/baseline_linear_regression.joblib`, `models/baseline_metrics.csv`, `models/baseline_metadata.json`
- `outputs/baseline_error_analysis.csv`
- `outputs/baseline_model_comparison.xlsx` (file so sánh) và `outputs/baseline_comparison_merged.csv` (bảng gộp)
- `outputs/figures/baseline_*.png`
- Các dòng `baseline_*` trong `experiment_log.csv`; mỗi dòng có `experiment_id` cố định nên chạy lại sẽ ghi đè dòng cũ, không tạo dòng trùng.

Notebook 02 và 03 nên dùng cùng các fold, cùng hàm độ đo và cùng định dạng `experiment_id` (`<tên_thí_nghiệm>_cv5` cho validation, `<tên_thí_nghiệm>_test` cho test) để kết quả so sánh được với nhau. Chạy lại mục 13 của notebook 02 sau khi các mô hình khác ghi log theo quy ước này thì sheet `Nhat_ky_thuc_nghiem` tự gom chúng vào bảng xếp hạng.

## Chạy notebook 03

Điều kiện: đã có `<span>data/processed/beijing_air_quality_standardized.csv</span>` (tạo từ notebook 01), đã cài các thư viện trong `<span>requirements.txt</span>` và môi trường có Jupyter hoặc `<span>ipykernel</span>`.

Mở `<span>03_advanced_models_and_tuning.ipynb</span>` rồi chọn `<span>Restart & Run All</span>`. Chạy từ thư mục gốc hay từ `<span>notebooks/</span>` đều được. Notebook sử dụng cùng quy trình chia dữ liệu và 5-Fold Cross-Validation với Notebook 02 để đảm bảo kết quả có thể so sánh.

## Notebook 03 tạo ra

* `<span>models/random_forest.joblib</span>`: mô hình Random Forest đã huấn luyện.
* `<span>models/random_forest_metadata.json</span>`: thông tin cấu hình mô hình.
* `<span>outputs/random_forest_cv_metrics.csv</span>`: kết quả đánh giá 5-Fold Cross-Validation.
* Dòng `<span>random_forest_cv5</span>` trong `<span>experiment_log.csv</span>`; sử dụng `<span>experiment_id</span>` cố định để cập nhật kết quả khi chạy lại, không tạo dòng trùng.

Notebook 02 và Notebook 03 cần sử dụng cùng các fold, cùng hàm tính MAE, RMSE, R² và cùng định dạng `<span>experiment_id</span>` để đảm bảo kết quả thực nghiệm có thể so sánh công bằng.

Không sử dụng tập Test để lựa chọn mô hình hoặc tinh chỉnh siêu tham số.
