# Thư mục `data`

Thư mục này lưu dữ liệu đầu vào và dữ liệu được tạo ra sau khi làm sạch hoặc biến đổi cho đồ án dự đoán PM2.5.

## Thư mục con

- [`raw/`](raw/README.md) chứa dữ liệu gốc Beijing Multi-Site Air Quality theo 12 trạm.
- [`processed/`](processed/README.md): nơi lưu dữ liệu sau xử lý để phân tích và huấn luyện mô hình.

Notebook 01 tạo [`beijing_air_quality_standardized.csv`](processed/beijing_air_quality_standardized.csv) trong `processed/`. Notebook 02–08 dùng CSV này qua `load_data()`.
