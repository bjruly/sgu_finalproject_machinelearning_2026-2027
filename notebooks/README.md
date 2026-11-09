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


## Chạy Notebook 03

**Điều kiện trước khi chạy:**

- Đã có file `data/processed/beijing_air_quality_standardized.csv` (được tạo từ Notebook 01).
- Đã cài đặt các thư viện trong `requirements.txt`.
- Môi trường đã có Jupyter Notebook hoặc `ipykernel`.

Mở file `03_advanced_models_and_tuning.ipynb`, sau đó chọn **Restart & Run All** để chạy toàn bộ notebook.

Có thể chạy notebook từ thư mục gốc của dự án hoặc thư mục `notebooks/`. Notebook tự xác định đường dẫn dự án và sử dụng cùng quy trình chia dữ liệu theo thời gian, cùng 5-Fold Cross-Validation với Notebook 02 (Baseline), nhằm đảm bảo kết quả đánh giá giữa hai mô hình có thể so sánh công bằng.

## Các đầu ra được tạo bởi Notebook 03

Sau khi chạy thành công, notebook tạo hoặc cập nhật các tệp sau:

**1. Mô hình và thông tin cấu hình**

- `models/random_forest.joblib`: Mô hình Random Forest sau khi huấn luyện trên tập Train + Validation.
- `models/random_forest_metadata.json`: Thông tin cấu hình mô hình, kết quả đánh giá, thời gian chạy và thông tin các Fold.

**2. Kết quả đánh giá**

- `outputs/random_forest_cv_metrics.csv`: Các chỉ số MAE, RMSE, R² và thời gian chạy của từng Fold.
- `outputs/random_forest_cv_summary.csv`: Tổng hợp giá trị trung bình và độ lệch chuẩn của các chỉ số đánh giá.
- `outputs/random_forest_fold_overview.csv`: Thông tin tổng quan về dữ liệu Train và Validation của từng Fold.
- `outputs/random_forest_validation_oof_predictions.csv`: Lưu giá trị PM2.5 thực tế (`y_true`), giá trị dự đoán (`y_pred`) và sai số (`residual`) trên từng Fold Validation. Dữ liệu này được sử dụng để phân tích kết quả dự đoán và vẽ biểu đồ.

**3. Biểu đồ trực quan**

Các biểu đồ được xuất dưới định dạng PNG vào thư mục `outputs/figures/`:

- `random_forest_cv_rmse_by_fold.png`: RMSE theo từng Fold.
- `random_forest_cv_metrics_by_fold.png`: MAE, RMSE và R² theo từng Fold.
- `random_forest_feature_importance.png`: Mức độ quan trọng của các đặc trưng.
- `random_forest_pred_vs_actual.png`: So sánh giá trị PM2.5 thực tế và dự đoán.
- `random_forest_residuals.png`: Phân phối sai số dự đoán.

**4. Ghi nhận thí nghiệm**

Notebook ghi kết quả vào `experiment_log.csv` với `experiment_id` cố định là `random_forest_cv5`. Khi chạy lại, notebook cập nhật kết quả của thí nghiệm này thay vì tạo thêm dòng trùng lặp, đồng thời giữ lại các kết quả thí nghiệm khác.

## Nguyên tắc đảm bảo tính công bằng trong thực nghiệm

- Notebook 02 và Notebook 03 sử dụng cùng cách chia dữ liệu theo thời gian và cùng 5 Fold Cross-Validation.
- Sử dụng cùng cách tính các chỉ số MAE, RMSE và R² để đảm bảo tính nhất quán.
- Không sử dụng tập Test để lựa chọn mô hình hoặc tinh chỉnh siêu tham số.
- Các kết quả Cross-Validation chỉ được tính trên tập Train + Validation.
- Tập Test được giữ riêng để phục vụ đánh giá cuối cùng sau khi hoàn tất quá trình lựa chọn mô hình.

**Lưu ý:** File OOF chỉ lưu dự đoán trên các Fold Validation, không chứa kết quả dự đoán trên tập Test.
