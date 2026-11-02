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

- Chia theo thời gian, không xáo trộn ngẫu nhiên: train/validation có target đến 08/2016; test có target từ 09/2016 đến 02/2017 và chỉ dùng đánh giá cuối sau khi chốt cấu hình. Pipeline chia theo thời điểm của target t+1 để nhãn đầu tiên của test không lọt vào train.
- Dùng `TimeSeriesSplit` expanding-window với 5 fold trên phần train/validation. Khi gộp nhiều trạm, các bản ghi cùng mốc thời gian cần thuộc cùng một fold để tránh rò rỉ giữa trạm.
- Tạo lag PM2.5 tại 1, 2, 3, 6, 12 và 24 giờ; rolling mean 6 và 24 giờ; thêm đặc trưng khí tượng, thời gian tuần hoàn sin/cos và trạm. Các lag/rolling chỉ được tính từ quá khứ và riêng theo trạm.
- Không điền giá trị target bị thiếu; loại các dòng đó khỏi huấn luyện/đánh giá sau khi tạo lag/feature. Với feature, pipeline forward-fill tối đa 6 giờ theo trạm; numeric còn thiếu được median-impute cùng missing indicators khi transformer được fit trên train; `wd` còn thiếu dùng category `Unknown` rồi One-Hot.
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

**Trạng thái hiện tại:** notebook `01_eda_and_preprocessing.ipynb` đã có EDA và xuất dữ liệu chuẩn hóa; pipeline nạp, chia dữ liệu theo thời gian, tạo target/đặc trưng và tiền xử lý train-only đã được triển khai trong `src/`. Notebook `02_model_training_baseline.ipynb` đã huấn luyện và đánh giá Persistence cùng Linear Regression bằng 5-fold expanding-window validation, sau đó báo cáo kết quả test. Mô hình nâng cao và tuning chưa được triển khai.

## Kế hoạch hoàn thiện đồ án trong 7 ngày

Kế hoạch dưới đây bắt đầu từ ngày nhóm thống nhất triển khai. Hãy điền người phụ trách vào cột cuối trước khi bắt đầu; các nhãn **Thành viên A–D** là vai trò gợi ý, không phải phân công đã chốt. Phần EDA, pipeline dữ liệu và baseline đã có; trọng tâm còn lại là mô hình cây, so sánh kết quả, workbook Excel, báo cáo và kiểm tra bàn giao.

| Ngày | Công việc và thứ tự | Đầu ra/tiêu chí hoàn thành | Người phụ trách |
| :-: | :--- | :--- | :--- |
| 1 | Họp phân công; mọi người đồng bộ môi trường và chạy `python -m pytest -q`. Chạy lại notebook baseline để xác nhận Persistence/Linear Regression và kiểm tra vị trí các kết quả đã lưu. Chốt phạm vi thử nghiệm Random Forest và Gradient Boosting, metric chính (RMSE), random seed và giới hạn thời gian chạy. | Test hiện có xanh; ghi rõ cấu hình và người nhận từng việc. Baseline đối chiếu được với [`models/baseline_metrics.csv`](models/baseline_metrics.csv). | Nhóm trưởng điều phối; cả nhóm xác nhận |
| 2 | Thành viên A triển khai Random Forest; thành viên B triển khai Gradient Boosting. Dùng cùng feature, cùng 5 fold thời gian và cùng pipeline tiền xử lý; chỉ fit transformer trên train của từng fold. Bắt đầu bằng cấu hình nhỏ, giới hạn số tổ hợp để kịp lịch. | Có code/notebook tái chạy được; kết quả RMSE/MAE/R² cho từng fold; cấu hình, seed và thời gian chạy được ghi lại. | Thành viên A: Random Forest; Thành viên B: Gradient Boosting |
| 3 | Hoàn tất các lượt thử nghiệm có giới hạn cho hai mô hình. Thành viên C kiểm tra việc tính metric, ghép kết quả với baseline và phát hiện lỗi leakage/khác biệt dữ liệu giữa các mô hình. Chọn cấu hình cuối chỉ bằng validation/CV. | Bảng CV đủ các mô hình và 5 fold; cấu hình cuối được chọn theo RMSE validation; không dùng test để chọn tham số. | A, B chạy mô hình; C rà soát kết quả |
| 4 | Đóng băng cấu hình. Chạy đánh giá cuối trên test cho các mô hình đã chọn; tổng hợp Persistence, Linear Regression, Random Forest và Gradient Boosting trên cùng tập test. Phân tích sai số theo trạm, mùa và mức PM2.5. | Một lần chạy test cuối có metric, số mẫu và cấu hình rõ ràng; kết quả phân nhóm và biểu đồ có thể tái tạo. Không quay lại tinh chỉnh dựa trên kết quả test. | Thành viên C; nhóm trưởng kiểm tra quy trình |
| 5 | Tạo workbook `outputs/model_comparison.xlsx` để nhóm và giảng viên xem kết quả. Gợi ý các sheet: `Summary` (CV và test tách rõ), `CV Folds`, `Test by Group`, `Configurations`, `Notes`. Định dạng đơn vị, làm rõ RMSE là metric chọn mô hình; kiểm tra số liệu Excel khớp với CSV nguồn. | Workbook mở được; có đủ bốn phương pháp, metrics MAE/RMSE/R², mean/std CV, số dòng, cấu hình và ghi chú phân biệt validation/test. Không nhập nhầm test vào bảng CV. | Thành viên C |
| 6 | Hoàn thiện báo cáo và slide: bài toán/target t+1, nguồn dữ liệu, EDA, chia thời gian, chống leakage, xử lý missing, mô hình, cách chọn cấu hình, bảng so sánh và hạn chế. Thành viên D đối chiếu mọi con số với CSV/workbook và kiểm tra citation. | Báo cáo/slide có phương pháp và kết quả khớp artifact; nêu rõ hạn chế, không tuyên bố tương quan là nhân quả. | Thành viên D; A–C cung cấp nội dung phần mình |
| 7 | Chạy lại toàn bộ test và notebook cần thiết từ trạng thái sạch; xác nhận workbook/biểu đồ/metrics được tái tạo; rà README, tên file, commit và repository trước khi nộp. Tập dượt trình bày và thống nhất câu trả lời cho câu hỏi về leakage, missing và lý do chọn mô hình. | `pytest` xanh; artifact đầy đủ và nhất quán; repository không chứa cache hoặc file môi trường; cả nhóm có thể giải thích kết quả. | Nhóm trưởng điều phối QA; cả nhóm nghiệm thu |

### Gợi ý chia việc song song

- **Nhóm trưởng — Trần Lê Gia Bảo:** điều phối tiến độ, hỗ trợ pipeline dữ liệu đã triển khai, rà soát chia tập/leakage, tích hợp nhánh và nghiệm thu; không mặc định nhận phần huấn luyện mô hình.
- **Thành viên A:** Random Forest, ghi cấu hình và kết quả CV.
- **Thành viên B:** Gradient Boosting, ghi cấu hình và kết quả CV.
- **Thành viên C:** kiểm tra tính so sánh công bằng, tổng hợp metrics/error analysis và tạo workbook Excel.
- **Thành viên D:** báo cáo, slide, citation và chuẩn bị trình bày; phối hợp với A–C để xác nhận số liệu.

Nhóm có thể đổi người theo kỹ năng/thời gian, nhưng mỗi đầu việc cần một người chịu trách nhiệm chính và một người review. Công việc A/B có thể làm song song sau khi thống nhất giao diện dữ liệu và cách ghi kết quả; workbook chỉ chốt sau khi đã chọn cấu hình bằng CV và chạy đánh giá cuối. Nếu thời gian chạy vượt kế hoạch, giảm phạm vi tuning trước; không bỏ kiểm tra leakage, không thay đổi test để làm đẹp kết quả.

### Điều kiện nghiệm thu cuối

1. Baseline và hai mô hình cây được so sánh trên cùng target, feature set, folds thời gian và quy tắc tiền xử lý.
2. Tất cả imputer/encoder/scaler được fit bên trong từng fold; các trạm cùng target timestamp không bị tách qua train/validation.
3. Cấu hình được chọn bằng validation/CV; test chỉ dùng cho báo cáo đánh giá cuối. Baseline test đã được xem và ghi nhận, vì vậy không dùng test để điều chỉnh mô hình hoặc chọn cấu hình.
4. Bảng trong workbook khớp với các CSV kết quả; nêu rõ đơn vị PM2.5 (µg/m³), số mẫu, metric và split.
5. Notebook, báo cáo và slide có thể truy ngược kết quả về dữ liệu, cấu hình và nhật ký thực nghiệm trong repository.

## Cấu trúc thư mục dự án

Sơ đồ dưới đây thể hiện thư mục và tệp hiện có. Notebook EDA, pipeline dữ liệu và baseline đã có nội dung; mô hình nâng cao/tuning vẫn đang chờ triển khai.

```text
data/
├── raw/                                      Dữ liệu PRSA và các tệp bổ sung
│   └── PRSA_Data_20130301-20170228/          CSV theo 12 trạm
├── processed/                                Dữ liệu sau khi làm sạch/biến đổi
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA và xuất CSV chuẩn hóa; imputation chưa triển khai
├── 02_model_training_baseline.ipynb           Baseline Persistence và Linear Regression
└── 03_advanced_models_and_tuning.ipynb        Mô hình nâng cao (chưa triển khai)
src/
├── data_loader.py                             Nạp dữ liệu, chia thời gian và CV theo timestamp
├── features.py                                Tạo target/đặc trưng và tiền xử lý train-only
├── models.py                                  Huấn luyện mô hình (chưa triển khai)
└── evaluate.py                                Đánh giá mô hình (chưa triển khai)
tests/
├── test_data_pipeline.py                      Kiểm thử nạp dữ liệu và chia thời gian
├── test_feature_engineering.py                Kiểm thử target, feature và preprocessing
├── test_models_performance.py                 Chưa có test mô hình
└── test_integration.py                        Kiểm thử tích hợp pipeline dữ liệu
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
