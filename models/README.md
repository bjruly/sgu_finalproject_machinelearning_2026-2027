# Thư mục `models`

Nơi lưu các mô hình đã huấn luyện và các thành phần cần thiết để nạp lại mô hình, ví dụ tệp `.joblib`, `.pkl` hoặc `.pt`.

## Tệp hiện có

- `baseline_metrics.csv`: kết quả CV và test cho Persistence, Linear Regression và biến thể dự đoán được chặn dưới tại 0.
- `baseline_metadata.json`: mô tả target, feature, giai đoạn train/test và phiên bản thư viện dùng trong lần huấn luyện baseline.

Notebook [`02_model_training_baseline.ipynb`](../notebooks/02_model_training_baseline.ipynb) có thể tạo tệp `baseline_linear_regression.joblib` tại máy chạy. Tệp nhị phân này không được commit vì phiên bản scikit-learn trong artifact của branch là 1.7.2, trong khi môi trường hiện tại là 1.8.0; thử nạp chéo phiên bản gây lỗi trong `SimpleImputer`. Nếu cần mô hình đã lưu, chạy lại notebook trong môi trường mong muốn để huấn luyện và tạo artifact tương thích với môi trường đó.
