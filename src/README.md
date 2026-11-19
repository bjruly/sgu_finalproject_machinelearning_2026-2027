# Thư mục `src`

Nơi chứa mã nguồn Python của dự án. Pipeline đọc dữ liệu, chia tập theo thời gian và tạo đặc trưng được dùng chung trong các notebook. Phần huấn luyện, tinh chỉnh và đánh giá nằm trong [notebook 02–08](../notebooks/README.md).

## Các tệp

- [`__init__.py`](__init__.py) đánh dấu `src` là một package Python.
- [`data_loader.py`](data_loader.py) cung cấp các hàm đọc và chia dữ liệu.
  - `load_data(path=None)`: đọc CSV chuẩn hóa mặc định trong `data/processed/`, parse `datetime`, kiểm tra schema/khóa duy nhất và sắp xếp theo trạm/thời gian.
  - `time_split(data)`: tách theo `target_datetime` nếu có, để nhãn giờ t+1 thuộc giai đoạn test không rơi vào dòng feature của giờ trước đó; test bắt đầu từ 01/09/2016.
  - `cv_folds(data, n_splits=5)`: tạo expanding-window folds theo timestamp target duy nhất để mọi trạm có cùng giờ nhãn thuộc cùng phía của fold.
- [`features.py`](features.py) cung cấp các hàm tạo nhãn, đặc trưng và bộ tiền xử lý.
  - `add_features(data, ffill_limit=6)`: tạo target PM2.5 giờ kế tiếp trong cùng trạm từ giá trị gốc và cột `target_datetime`; forward-fill feature tối đa 6 giờ theo trạm; giữ hướng gió thiếu còn lại thành `Unknown`; tạo lag PM2.5, rolling mean quá khứ và mã hóa chu kỳ giờ/tháng/thứ.
  - `split_xy(data)`: lấy các feature được định nghĩa và target, không đưa `No`, thời gian thô hoặc target vào X.
  - `build_preprocessor(scale=False)`: tạo median imputation và cờ missing cho mọi feature numeric, One-Hot cho `station`/`wd`; scaler chỉ thêm khi `scale=True`. Median được học khi gọi `.fit()` trên dữ liệu train, không phải toàn bộ dataset.

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

`add_features` phải chạy trước khi lọc các target thiếu để các lag vẫn được tính trên chuỗi thời gian đầy đủ. Sau khi chốt cấu hình từ validation, [notebook 08](../notebooks/08_final_evaluation.ipynb) dùng tập test để đánh giá cuối. Các transformer đã fit trên dữ liệu huấn luyện nằm trong pipeline được nạp lại. Xem [`tests/README.md`](../tests/README.md) để biết các bảo đảm được kiểm thử.

Hai bộ [notebook có kết quả](../notebooks/README.md) và [notebook đã xóa output](../notebooks_unexecuted/) dùng chung các hàm trên.
