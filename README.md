# Beijing Multi-Site Air Quality Prediction

Đồ án cuối kỳ môn Máy học, xây dựng hệ thống phân tích và dự đoán nồng độ bụi mịn PM2.5 từ bộ dữ liệu Beijing Multi-Site Air Quality. Đây là bài toán hồi quy chuỗi thời gian đa trạm: dự đoán PM2.5 ở giờ kế tiếp (t+1) cho cùng trạm dựa trên thông tin tại thời điểm hiện tại và các đặc trưng chỉ sử dụng dữ liệu quá khứ.

## Mục tiêu

- Khám phá dữ liệu và xử lý các giá trị khuyết.
- Phân tích mối liên hệ giữa PM2.5, các chất ô nhiễm khác và điều kiện khí tượng.
- Xây dựng và so sánh các mô hình hồi quy:
  - Baseline: persistence và Linear Regression.
  - Mô hình cây: Random Forest Regressor và Gradient Boosting Regressor.
- Chọn mô hình theo RMSE trên validation; đồng thời báo cáo MAE và R².
- Phân tích sai số theo trạm, mùa và mức PM2.5; xem xét residual và permutation importance.
- Tôn trọng thứ tự thời gian khi chia tập dữ liệu và chỉ fit các bước tiền xử lý trên tập huấn luyện để tránh rò rỉ dữ liệu.

## Dữ liệu

Bộ dữ liệu PRSA gồm 12 tệp CSV, mỗi tệp là dữ liệu theo giờ của một trạm trong khoảng 01/03/2013–28/02/2017. Các cột gồm thời gian, PM2.5, PM10, SO2, NO2, CO, O3 và các thông số khí tượng. Giá trị khuyết được ghi là `NA`.

Dữ liệu thô nằm trong [`data/raw/`](data/raw/README.md); dữ liệu sau xử lý dự kiến được lưu trong [`data/processed/`](data/processed/README.md). Thư mục `data/raw/` hiện cũng có `data.csv`, `test.csv` với cấu trúc OHLCV và một ảnh JPG; mục đích của các tệp này trong đồ án chưa được xác định. Chúng không được mô tả ở đây là dữ liệu đầu vào của mô hình PM2.5.

Kế hoạch chính là gộp dữ liệu của 12 trạm thành một bộ dữ liệu đa trạm và mã hóa `station` như một đặc trưng. Mỗi mẫu dự đoán PM2.5 ở giờ t+1 của cùng trạm; mô hình riêng theo trạm hoặc dự đoán chân trời dài hơn là hướng mở rộng.

### Kế hoạch thực nghiệm theo proposal

- Chia theo thời gian, không xáo trộn ngẫu nhiên: train/validation dự kiến từ 03/2013 đến 08/2016; test dự kiến từ 09/2016 đến 02/2017 và chỉ dùng đánh giá cuối sau khi chốt cấu hình.
- Dùng `TimeSeriesSplit` expanding-window với 5 fold trên phần train/validation. Khi gộp nhiều trạm, các bản ghi cùng mốc thời gian cần thuộc cùng một fold để tránh rò rỉ giữa trạm.
- Tạo lag PM2.5 tại 1, 2, 3, 6, 12 và 24 giờ; rolling mean 6 và 24 giờ; thêm đặc trưng khí tượng, thời gian tuần hoàn sin/cos và trạm. Các lag/rolling chỉ được tính từ quá khứ và riêng theo trạm.
- Không điền giá trị target bị thiếu; loại các dòng đó khỏi huấn luyện/đánh giá. Với feature, dự kiến forward-fill có giới hạn theo trạm, sau đó điền phần còn thiếu bằng median chỉ fit trên train và thêm cờ báo thiếu.
- Dùng One-Hot Encoding cho hướng gió và trạm. Chỉ StandardScaler cho Linear Regression; mô hình cây không cần scaling.
- Các mốc chia và chi tiết tiền xử lý là kế hoạch ban đầu trong proposal, có thể điều chỉnh sau EDA; chưa phải kết quả thực nghiệm đã chạy.

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

**Trạng thái hiện tại:** notebook `01_eda_and_preprocessing.ipynb` đã có EDA và xuất bản dữ liệu chuẩn hóa còn giữ missing tại `data/processed/`; bước imputation/model-ready và pipeline huấn luyện chưa được triển khai. Các module trong `src/` và tệp kiểm thử trong `tests/` vẫn là khung; notebook baseline và notebook mô hình nâng cao còn rỗng. Pytest có thể báo `no tests ran` cho đến khi các test được viết.

## Cấu trúc thư mục dự án

Sơ đồ dưới đây thể hiện thư mục và tệp hiện có. Notebook EDA đã có nội dung khảo sát; các module Python, test và notebook mô hình vẫn đang là khung.

```text
data/
├── raw/                                      Dữ liệu PRSA và các tệp bổ sung
│   └── PRSA_Data_20130301-20170228/          CSV theo 12 trạm
├── processed/                                Dữ liệu sau khi làm sạch/biến đổi
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA và xuất CSV chuẩn hóa; imputation chưa triển khai
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

## Phân công công việc

Giảng viên hướng dẫn: TS. Đỗ Như Tài

| STT | Họ và tên | MSSV | Vai trò | Phần việc phụ trách |
| :-: | :--- | :-: | :--- | :--- |
| 1 | Trần Lê Gia Bảo | 3124411038 | Nhóm trưởng | Tổ chức repository và tài liệu theo proposal; khảo sát và phân tích dữ liệu (EDA); chuẩn hóa, xuất bản dữ liệu và ghi lại kết luận; xây dựng pipeline dữ liệu, tạo đặc trưng, chia tập theo thời gian và kiểm thử pipeline. Phạm vi phụ trách kết thúc ở pipeline dữ liệu, không bao gồm xây dựng, huấn luyện hay đánh giá mô hình. |
| 2 | Tô Thành Nhân | 3124411198 | Thành viên | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật. |
| 3 | Đào Hữu Tài | 3124411261 | Thành viên | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật. |
| 4 | Huỳnh Nhật Quang | 3124411245 | Thành viên | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật. |
| 5 | Nguyễn Thanh Tuấn | 3124411337 | Thành viên | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật. |

Chi tiết phạm vi công việc của nhóm trưởng được ghi tại [`docs/phan-cong-cong-viec.docx`](docs/phan-cong-cong-viec.docx). Nhật ký EDA để các thành viên đọc lại quy trình và quyết định nằm tại [`outputs/eda/eda_worklog.md`](outputs/eda/eda_worklog.md); bảng kết luận nằm tại [`outputs/eda/eda_conclusions.csv`](outputs/eda/eda_conclusions.csv).

## Nguồn dữ liệu

Chen, S. (2017). *Beijing Multi-Site Air Quality* [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G). Dữ liệu được phát hành theo giấy phép [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Bản tham khảo trên Kaggle

Thành viên có thể tham khảo trang [Beijing Multi-Site Air-Quality Data Set trên Kaggle](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set). Khi sử dụng dữ liệu trong báo cáo, cần kiểm tra nội dung và giấy phép của bản tải xuống; trích dẫn bộ dữ liệu gốc UCI ở trên theo proposal.
