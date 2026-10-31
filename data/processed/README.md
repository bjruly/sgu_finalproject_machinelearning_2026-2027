# Thư mục `data/processed`

Nơi lưu bản dữ liệu đã chuẩn hóa và các dữ liệu được tạo ra sau khi làm sạch/biến đổi. Tệp trong thư mục này không thay thế dữ liệu gốc ở `data/raw/`.

## Tệp hiện có

- [`beijing_air_quality_standardized.csv`](beijing_air_quality_standardized.csv): dữ liệu 12 trạm đã gộp, thêm cột `datetime` và sắp xếp theo trạm/thời gian. Tệp nguồn này giữ nguyên các missing và điểm PM2.5 cao; chưa được impute và chưa phải ma trận feature model-ready. Pipeline trong `src/` tạo target/feature trong bộ nhớ và fit bộ tiền xử lý riêng trên train, không ghi đè CSV này. Xem [nhật ký EDA](../../outputs/eda/eda_worklog.md) để hiểu cách tạo và các giới hạn của tệp.
- `.gitkeep`: tệp rỗng giúp Git lưu thư mục.
