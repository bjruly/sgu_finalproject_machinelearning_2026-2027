# Thư mục `src`

Nơi chứa mã nguồn Python của dự án. Phần pipeline dữ liệu và tạo đặc trưng đã được triển khai; các mô hình và đánh giá chưa thuộc phạm vi phần việc hiện tại.

## Các tệp

- `__init__.py`: đánh dấu `src` là một Python package.
- `data_loader.py`:
  - `load_data(path=None)`: đọc CSV chuẩn hóa mặc định trong `data/processed/`, parse `datetime`, kiểm tra schema/khóa duy nhất và sắp xếp theo trạm/thời gian.
  - `time_split(data)`: tách theo `target_datetime` nếu có, để nhãn giờ t+1 thuộc giai đoạn test không rơi vào dòng feature của giờ trước đó; test bắt đầu từ 01/09/2016.
  - `cv_folds(data, n_splits=5)`: tạo expanding-window folds theo timestamp target duy nhất để mọi trạm có cùng giờ nhãn thuộc cùng phía của fold.
- `features.py`:
  - `add_features(data, ffill_limit=6)`: tạo target PM2.5 giờ kế tiếp trong cùng trạm từ giá trị gốc và cột `target_datetime`; forward-fill feature tối đa 6 giờ theo trạm; giữ hướng gió thiếu còn lại thành `Unknown`; tạo lag PM2.5, rolling mean quá khứ và mã hóa chu kỳ giờ/tháng/thứ.
  - `split_xy(data)`: lấy các feature được định nghĩa và target, không đưa `No`, thời gian thô hoặc target vào X.
  - `build_preprocessor(scale=False)`: tạo median imputation và cờ missing cho mọi feature numeric, One-Hot cho `station`/`wd`; scaler chỉ thêm khi `scale=True`. Median được học khi gọi `.fit()` trên dữ liệu train, không phải toàn bộ dataset.
- `models.py`: dành cho mô hình; chưa triển khai trong phạm vi pipeline dữ liệu.
- `evaluate.py`: dành cho metric và đánh giá; chưa triển khai trong phạm vi pipeline dữ liệu.

## Trình tự sử dụng

Từ thư mục gốc repository:

```python
from src.data_loader import cv_folds, load_data, time_split
from src.features import add_features, build_preprocessor, split_xy

featured = add_features(load_data())
labeled = featured.dropna(subset=["target"]).reset_index(drop=True)
train_validation, test = time_split(labeled)
folds = cv_folds(train_validation)
X_train_validation, y_train_validation = split_xy(train_validation)
preprocessor = build_preprocessor()
preprocessor.fit(X_train_validation.iloc[folds[0][0]])
```

`add_features` phải chạy trước khi lọc các target thiếu để các lag vẫn được tính trên chuỗi thời gian đầy đủ. Test chỉ được giữ riêng đến khi nhóm chốt cấu hình; không fit transformer trên test. Xem [`tests/README.md`](../tests/README.md) để biết các bảo đảm được kiểm thử.
