# Thư mục `notebooks`

Nơi lưu các Jupyter Notebook dùng để khám phá dữ liệu (EDA), tiền xử lý, thử nghiệm mô hình và tinh chỉnh siêu tham số.

## Các tệp hiện có

- `01_eda_and_preprocessing.ipynb`: EDA 12 CSV PRSA; kiểm tra schema, thời gian, missing, phân bố PM2.5, xu hướng theo tháng/giờ/mùa và tương quan. Cuối notebook có bước xuất bản CSV chuẩn hóa nhưng không impute hoặc tiền xử lý thành dữ liệu model-ready.
- `02_model_training_baseline.ipynb`: huấn luyện Persistence và Linear Regression; đánh giá bằng 5-fold expanding-window validation, phân tích out-of-fold error theo trạm/mùa/mức PM2.5, và báo cáo test cuối cùng. Khi chạy notebook, mặc định các kết quả được lưu trong `models/`, `outputs/` và `experiment_log.csv`.
- `03_advanced_models_and_tuning.ipynb`: dự kiến thử nghiệm mô hình nâng cao và tinh chỉnh tham số.

Notebook 03 hiện còn rỗng. Notebook 01 cần các thư viện trong `requirements.txt` và tìm dữ liệu tại `data/raw/PRSA_Data_20130301-20170228/`; notebook 02 đọc CSV chuẩn hóa trong `data/processed/`. Với kết quả baseline hiện tại, RMSE test là 23,1133 cho Persistence và 21,8027 cho Linear Regression; xem `models/baseline_metrics.csv` và phần diễn giải trong notebook.
