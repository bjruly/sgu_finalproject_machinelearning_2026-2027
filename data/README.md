# Thư mục `data`

Thư mục này lưu dữ liệu PRSA gốc và bản CSV đã gộp, chuẩn hóa cho đồ án dự báo PM2.5.

## Thư mục con

- [`raw/`](raw/README.md) chứa dữ liệu gốc Beijing Multi-Site Air Quality theo 12 trạm.
- [`processed/`](processed/README.md) chứa dữ liệu đã chuẩn hóa, vẫn giữ các ô thiếu và giá trị PM2.5 cao.

[Notebook 01](../notebooks/01_eda_and_preprocessing.ipynb) tạo [`beijing_air_quality_standardized.csv`](processed/beijing_air_quality_standardized.csv) trong `processed/`. Notebook 02–08 dùng CSV này qua `load_data()`.

[Pipeline dữ liệu](../src/README.md) tạo nhãn và đặc trưng trong bộ nhớ. Các bảng kết quả được lưu tại [thư mục đầu ra](../outputs/README.md).
