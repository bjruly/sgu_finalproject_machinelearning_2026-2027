# Thư mục `tests`

Nơi chứa kiểm thử tự động cho các thành phần xử lý dữ liệu, tạo đặc trưng, mô hình và luồng tích hợp. Dự án sử dụng pytest; các test là tệp `.py` thuần, thư mục này không dùng notebook (`.ipynb`).

## Các tệp hiện có

- `__init__.py`: đánh dấu `tests` là một Python package và định nghĩa `toy()`, tạo dữ liệu giả gồm 2 trạm × n giờ liên tục (PM2.5 = 0, 1, 2, ...) dùng chung cho các test.
- `test_data_pipeline.py`: kiểm thử chia dữ liệu.
  - `time_split`: train và test không chồng lấn, test bắt đầu từ 01/09/2016.
  - `cv_folds`: validation luôn nằm sau train, một timestamp chỉ thuộc một phía, mỗi giờ validation có đủ các trạm.
- `test_feature_engineering.py`: kiểm thử tạo đặc trưng.
  - Target là PM2.5 giờ kế tiếp của cùng trạm; giờ cuối của mỗi trạm là NaN.
  - Lag không mượn dữ liệu của trạm khác.
  - Không rò rỉ tương lai: đổi dữ liệu sau một mốc thì đặc trưng trước mốc đó không đổi.
  - Target không bị điền khi PM2.5 thiếu, còn đặc trưng thì được forward-fill.
- `test_integration.py`: chạy toàn bộ luồng trên dữ liệu thật trong `data/processed/` (nạp, tạo đặc trưng, chia tập, fit Linear Regression trên fold đầu); chỉ kiểm cấu trúc, không chấm điểm trên tập test.
- `test_models_performance.py`: kiểm tra công thức MAE/RMSE/R² với giá trị biết trước; kiểm tra Linear Regression có RMSE thấp hơn persistence (và R² > 0,9) trên 5 fold validation. Người làm mô hình cây có thể thêm test tương tự vào đây.

## Chạy kiểm thử

Từ thư mục gốc repository:

```powershell
python -m pytest -q
```

Toàn bộ mất khoảng 20 giây. Hai test dùng dữ liệu thật cần có `data/processed/beijing_air_quality_standardized.csv`, và vì kiểm tra điều kiện số nên cần xem lại nếu đổi bộ đặc trưng.