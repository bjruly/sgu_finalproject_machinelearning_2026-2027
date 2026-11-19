# Thư mục `tests`

Nơi chứa kiểm thử tự động cho pipeline dữ liệu và tạo đặc trưng. Dự án sử dụng pytest; các test chạy từ thư mục gốc repository bằng `python -m pytest -q`.

## Các tệp hiện có

- `__init__.py`: đánh dấu `tests` là một Python package.
- [`test_data_pipeline.py`](test_data_pipeline.py) kiểm tra đọc dữ liệu, kiểm tra khóa station-hour, chia theo mốc thời gian và tạo expanding-window folds không tách các trạm cùng timestamp.
- [`test_feature_engineering.py`](test_feature_engineering.py) kiểm tra target t+1 theo trạm, target không bị impute, forward-fill có giới hạn, hướng gió `Unknown`, lag/rolling chỉ dùng quá khứ, chọn X/y và median chỉ fit trên dữ liệu train.
- [`test_integration.py`](test_integration.py) chạy pipeline trên CSV PRSA chuẩn hóa, kiểm tra thời điểm chia test và các fold theo timestamp.

Kiểm thử tích hợp dùng [CSV chuẩn hóa](../data/processed/README.md) do notebook 01 tạo. [Notebook 08](../notebooks/08_final_evaluation.ipynb) đo chất lượng dự báo bằng MAE, RMSE và R². Điểm đã lưu nằm trong [hồ sơ đánh giá cuối](../outputs/experiments/final_test/README.md).
