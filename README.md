# Beijing Multi-Site Air Quality Prediction

Đồ án cuối kỳ môn Máy học, xây dựng hệ thống phân tích và dự đoán nồng độ bụi mịn PM2.5 từ bộ dữ liệu Beijing Multi-Site Air Quality. Đây là bài toán hồi quy trên dữ liệu quan trắc theo thời gian tại nhiều trạm ở Bắc Kinh.

## Mục tiêu

- Khám phá dữ liệu và xử lý các giá trị khuyết.
- Phân tích mối liên hệ giữa PM2.5, các chất ô nhiễm khác và điều kiện khí tượng.
- Xây dựng và so sánh các mô hình hồi quy:
  - Baseline: Linear Regression hoặc Ridge Regression.
  - Ensemble: Random Forest Regressor và XGBoost Regressor.
  - Neural network: Multi-Layer Perceptron (MLP).
- Đánh giá mô hình bằng MAE, RMSE và R².
- Tôn trọng thứ tự thời gian khi chia tập dữ liệu; chỉ fit scaler trên tập huấn luyện để hạn chế rò rỉ dữ liệu.

## Dữ liệu

Bộ dữ liệu PRSA gồm 12 tệp CSV, mỗi tệp là dữ liệu theo giờ của một trạm trong khoảng 01/03/2013–28/02/2017. Các cột gồm thời gian, PM2.5, PM10, SO2, NO2, CO, O3 và các thông số khí tượng. Giá trị khuyết được ghi là `NA`.

Dữ liệu thô nằm trong [`data/raw/`](data/raw/README.md); dữ liệu sau xử lý dự kiến được lưu trong [`data/processed/`](data/processed/README.md). Thư mục `data/raw/` hiện cũng có `data.csv`, `test.csv` với cấu trúc OHLCV và một ảnh JPG; mục đích của các tệp này trong đồ án chưa được xác định. Chúng không được mô tả ở đây là dữ liệu đầu vào của mô hình PM2.5.

Phạm vi sử dụng 12 trạm (gộp dữ liệu hay huấn luyện riêng theo trạm) và thời điểm dự đoán cụ thể sẽ được chốt trong quá trình thiết kế thực nghiệm.

## Thiết lập môi trường

Các lệnh sau dành cho PowerShell trên Windows, chạy từ thư mục gốc của repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu PowerShell không cho phép kích hoạt môi trường ảo, có thể gọi Python trong môi trường trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Chạy kiểm thử

Sau khi cài dependencies và kích hoạt môi trường:

```powershell
python -m pytest -q
```

**Trạng thái hiện tại:** các module trong `src/` và tệp kiểm thử trong `tests/` mới là khung, chưa có chức năng hoặc test case được triển khai; các notebook trong `notebooks/` cũng đang rỗng. Vì vậy hiện chưa thể chạy pipeline huấn luyện hay tái tạo kết quả mô hình. Pytest có thể báo `no tests ran` cho đến khi các test được viết.

## Cấu trúc thư mục dự án

Sơ đồ dưới đây thể hiện thư mục và tệp hiện có. Các module Python, notebook và test đã có tên nhưng hiện vẫn là khung, chưa được triển khai.

```text
data/
├── raw/                                      Dữ liệu PRSA và các tệp bổ sung
│   └── PRSA_Data_20130301-20170228/          CSV theo 12 trạm
├── processed/                                Dữ liệu sau khi làm sạch/biến đổi
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA và tiền xử lý (chưa triển khai)
├── 02_model_training_baseline.ipynb           Mô hình baseline (chưa triển khai)
└── 03_advanced_models_and_tuning.ipynb        Mô hình nâng cao (chưa triển khai)
src/
├── data_loader.py                             Nạp và xử lý dữ liệu (khung)
├── features.py                                Tạo đặc trưng (khung)
├── models.py                                  Huấn luyện mô hình (khung)
└── evaluate.py                                Đánh giá mô hình (khung)
tests/
├── test_data_pipeline.py                      Kiểm thử pipeline dữ liệu (khung)
├── test_feature_engineering.py                Kiểm thử tạo đặc trưng (khung)
├── test_models_performance.py                 Kiểm thử hiệu năng mô hình (khung)
└── test_integration.py                        Kiểm thử tích hợp (khung)
models/                                        Nơi lưu mô hình đã huấn luyện
outputs/
├── figures/                                   Biểu đồ và hình ảnh kết quả
└── test_reports/                              Báo cáo kiểm thử
docs/                                          Tài liệu đồ án
experiment_log.csv                             Nhật ký thực nghiệm
requirements.txt                               Danh sách thư viện Python
pytest.ini                                     Cấu hình pytest
README.md                                      Giới thiệu và hướng dẫn dự án
```

README chi tiết theo thư mục: [`data/README.md`](data/README.md), [`data/raw/README.md`](data/raw/README.md), [`data/processed/README.md`](data/processed/README.md), [`notebooks/README.md`](notebooks/README.md), [`src/README.md`](src/README.md), [`tests/README.md`](tests/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md), [`outputs/figures/README.md`](outputs/figures/README.md), [`outputs/test_reports/README.md`](outputs/test_reports/README.md) và [`docs/README.md`](docs/README.md).

## Thành viên

Giảng viên hướng dẫn: TS. Đỗ Như Tài

| STT | Họ và tên | MSSV | Vai trò | Đóng góp |
| :-: | :--- | :-: | :--- | :-: |
| 1 | Trần Lê Gia Bảo | 3124411038 | Nhóm trưởng | 20% |
| 2 | Tô Thành Nhân | 3124411198 | Thành viên | 20% |
| 3 | Đào Hữu Tài | 3124411261 | Thành viên | 20% |
| 4 | Huỳnh Nhật Quang | 3124411245 | Thành viên | 20% |
| 5 | Nguyễn Thanh Tuấn | 3124411337 | Thành viên | 20% |
