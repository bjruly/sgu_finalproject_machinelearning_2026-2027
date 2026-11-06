# Thư mục `notebooks`

Nơi lưu các Jupyter Notebook dùng để khám phá dữ liệu (EDA), tiền xử lý, thử nghiệm mô hình và tinh chỉnh siêu tham số.

## Các tệp hiện có

- `01_eda_and_preprocessing.ipynb`: EDA 12 CSV PRSA; kiểm tra schema, thời gian, missing, phân bố PM2.5, xu hướng theo tháng/giờ/mùa và tương quan bằng biểu đồ đã chuẩn hóa màu sắc/bố cục. Có hình so sánh missing và phân bố PM2.5 trước/sau pipeline hiện có (`ffill` giới hạn 6 giờ, `wd=Unknown`, median fit trên train/validation trước test); phần này chỉ tạo dữ liệu tạm để vẽ, tắt scaling để giữ đơn vị PM2.5, không impute target, không loại giá trị cao và không ghi đè CSV nguồn. Notebook 02 vẫn áp dụng scaler theo pipeline baseline. Cuối notebook xuất bản CSV chuẩn hóa còn nguyên missing để dùng ở notebook 02.
- `02_model_training_baseline.ipynb`: huấn luyện và đánh giá hai baseline cho bài toán dự đoán PM2.5 giờ t+1:
  - **Persistence**: dự đoán PM2.5(t+1) = PM2.5(t), không học tham số.
  - **Linear Regression**: pipeline `build_preprocessor(scale=True)` + `LinearRegression`.
  - Dùng lại pipeline trong `src/` (đặc trưng, chia thời gian, 5 fold expanding-window) và đánh giá bằng MAE, RMSE, R².
  - Phân tích sai số theo trạm, mùa, mức PM2.5 và theo tháng; residual; hệ số và permutation importance theo nhóm feature của Linear Regression.
  - Có mục đánh giá trên tập test, điều khiển bằng cờ `RUN_FINAL_TEST`.
- `03_advanced_models_and_tuning.ipynb`: dự kiến thử nghiệm mô hình nâng cao và tinh chỉnh tham số. Notebook này hiện còn rỗng.

## Chạy notebook 02

Điều kiện: đã có `data/processed/beijing_air_quality_standardized.csv` (tạo từ notebook 01) và đã cài các thư viện trong `requirements.txt`; môi trường cần có Jupyter hoặc `ipykernel` để chạy notebook.

Mở notebook rồi chọn `Restart & Run All`. Chạy từ thư mục gốc hay từ `notebooks/` đều được; thời gian khoảng 1–2 phút. Hai cờ ở mục 1:

- `SAVE_ARTIFACTS`: `True` thì ghi mô hình, bảng và hình ra đĩa; `False` thì chỉ chạy thử.
- `RUN_FINAL_TEST`: `True` thì đánh giá baseline trên tập test (mục 11). Baseline không có siêu tham số nào chọn dựa trên test; không quay lại sửa baseline sau khi xem số test.

## Notebook 02 tạo ra

- `models/baseline_linear_regression.joblib`, `models/baseline_metrics.csv`, `models/baseline_metadata.json`
- `outputs/baseline_error_analysis.csv`
- `outputs/figures/baseline_*.png`
- Các dòng `baseline_*` trong `experiment_log.csv`; mỗi dòng có `experiment_id` cố định nên chạy lại sẽ ghi đè dòng cũ, không tạo dòng trùng.

Notebook 02 và 03 nên dùng cùng các fold, cùng hàm độ đo và cùng định dạng `experiment_id` để kết quả so sánh được với nhau.