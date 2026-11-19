# Thư mục `data/processed`

Nơi lưu bản dữ liệu đã chuẩn hóa và các dữ liệu được tạo ra sau khi làm sạch/biến đổi. Tệp trong thư mục này không thay thế dữ liệu gốc ở `data/raw/`.

## Tệp hiện có

- [`beijing_air_quality_standardized.csv`](beijing_air_quality_standardized.csv): dữ liệu 12 trạm đã gộp, thêm cột `datetime` và sắp xếp theo trạm/thời gian. Tệp nguồn này giữ nguyên các missing và điểm PM2.5 cao; chưa được impute và chưa phải ma trận feature model-ready. Pipeline trong `src/` tạo target/feature trong bộ nhớ và fit bộ tiền xử lý riêng trên train, không ghi đè CSV này. Xem [nhật ký EDA](../../outputs/eda/eda_worklog.md) để hiểu cách tạo và các giới hạn của tệp.
- `.gitkeep`: tệp rỗng giúp Git lưu thư mục.

## Sử dụng trong notebook

[Notebook 01](../../notebooks/01_eda_and_preprocessing.ipynb) tạo lại CSV từ 12 tệp PRSA. Notebook 02–08 dùng `load_data()` để đọc CSV và gọi `time_split()` sau khi tạo nhãn. [Notebook 08](../../notebooks/08_final_evaluation.ipynb) chấm trên 51.063 mẫu có nhãn từ 01/09/2016 đến 28/02/2017. [Bảng kết quả test](../../outputs/notebooks/tables/final_test_metrics.csv) nằm trong thư mục đầu ra.
