# Thư mục `data/processed`

Nơi lưu bản dữ liệu đã chuẩn hóa và các dữ liệu được tạo ra sau khi làm sạch/biến đổi. Tệp trong thư mục này không thay thế dữ liệu gốc ở `data/raw/`.

## Tệp hiện có

- [`beijing_air_quality_standardized.csv`](beijing_air_quality_standardized.csv): dữ liệu 12 trạm đã gộp, thêm cột `datetime` và sắp xếp theo trạm/thời gian. Tệp giữ nguyên các missing và điểm PM2.5 cao; chưa phải dữ liệu đã impute hay model-ready. Xem [nhật ký EDA](../../outputs/eda/eda_worklog.md) để hiểu cách tạo và các giới hạn của tệp.
- `.gitkeep`: tệp rỗng giúp Git lưu thư mục.
