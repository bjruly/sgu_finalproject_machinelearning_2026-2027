# Kết quả khảo sát dữ liệu (EDA)

Thư mục này lưu các kết luận và kết quả khảo sát dữ liệu khám phá (EDA).

## Tệp hiện có

- [`eda_conclusions.csv`](eda_conclusions.csv): kết luận EDA đã đo từ 12 CSV PRSA, gồm chất lượng dữ liệu, missing, phân bố PM2.5, xu hướng mùa, tương quan và các lưu ý cho bước xử lý tiếp theo. Đây là kết quả mô tả dữ liệu thô, không phải dữ liệu đã làm sạch hoặc đã điền khuyết.
- [`eda_worklog.md`](eda_worklog.md): nhật ký tiếng Việt giải thích phạm vi, quy trình, kết quả, cách hiểu các giá trị đáng ngờ, CSV chuẩn hóa và những quyết định còn cần thực hiện.

[Notebook 01](../../notebooks/01_eda_and_preprocessing.ipynb) hiển thị các biểu đồ EDA và xuất [CSV dữ liệu chuẩn hóa](../../data/processed/README.md). Kết quả đánh giá mô hình được ghi ở [thư mục đầu ra](../README.md).

## Mã tái tạo ACF, log-scale và quan hệ gió

Chạy .venv/Scripts/python.exe -m src.eda hoặc phần bổ sung của notebook 01. tables/ lưu ACF từng trạm và trung bình giữa trạm, số cặp có dữ liệu, thống kê hướng gió và nhóm tốc độ gió. figures/ lưu các hình tương ứng.

ACF dùng số đo gốc và giữ hàng giờ đầy đủ; chỉ bỏ cặp thiếu khi tính tương quan, không nối các khoảng mất giờ thành một chuỗi giả. Các bảng gió dùng quan sát sẵn có, không impute target. Biểu đồ log chỉ dùng giá trị dương; biểu đồ tuyến tính giữ số đo không thiếu.
