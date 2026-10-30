# Thư mục `notebooks`

Nơi lưu các Jupyter Notebook dùng để khám phá dữ liệu (EDA), tiền xử lý, thử nghiệm mô hình và tinh chỉnh siêu tham số.

## Các tệp hiện có

- `01_eda_and_preprocessing.ipynb`: EDA 12 CSV PRSA; kiểm tra schema, thời gian, missing, phân bố PM2.5, xu hướng theo tháng/giờ/mùa và tương quan. Cuối notebook có bước xuất bản CSV chuẩn hóa nhưng không impute hoặc tiền xử lý thành dữ liệu model-ready.
- `02_model_training_baseline.ipynb`: dự kiến huấn luyện và đánh giá các mô hình baseline.
- `03_advanced_models_and_tuning.ipynb`: dự kiến thử nghiệm mô hình nâng cao và tinh chỉnh tham số.

Notebook 02 và 03 hiện còn rỗng. Notebook 01 cần các thư viện trong `requirements.txt` và tìm dữ liệu tại `data/raw/PRSA_Data_20130301-20170228/`.
