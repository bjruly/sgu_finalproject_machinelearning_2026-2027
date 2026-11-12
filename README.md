# Beijing Multi-Site Air Quality Prediction

Đồ án cuối kỳ môn Máy học, xây dựng hệ thống phân tích và dự đoán nồng độ bụi mịn PM2.5 từ bộ dữ liệu Beijing Multi-Site Air Quality. Đây là bài toán hồi quy chuỗi thời gian đa trạm: dự đoán PM2.5 ở giờ kế tiếp (t+1) cho cùng trạm dựa trên thông tin tại thời điểm hiện tại và các đặc trưng chỉ sử dụng dữ liệu quá khứ.

## Mục tiêu

Mục tiêu là dự đoán liên tục nồng độ PM2.5 (µg/m³) tại giờ kế tiếp `t+1` cho cùng trạm, từ dữ liệu ô nhiễm, khí tượng và thời gian đến giờ `t`. Các câu hỏi nghiên cứu theo proposal:

1. Random Forest và Gradient Boosting cải thiện bao nhiêu so với baseline Linear Regression?
2. Nhóm đặc trưng nào (PM2.5 trễ, khí tượng, thời gian, trạm) đóng góp vào độ chính xác?
3. Sai số thay đổi thế nào theo trạm, mùa và các đợt PM2.5 cao?

Các phương pháp được đề xuất gồm Linear Regression làm baseline, Random Forest Regressor và Gradient Boosting Regressor để so sánh; persistence là mốc tham chiếu đơn giản. Chọn cấu hình theo RMSE validation, đồng thời báo cáo MAE và R². Phân tích kết quả gồm sai số theo trạm/mùa/PM2.5 cao, dự đoán so với thực tế, residual theo thời gian và permutation importance. Không dùng Accuracy cho bài toán hồi quy.

## Dữ liệu

Bộ dữ liệu PRSA gồm 12 tệp CSV, mỗi tệp là dữ liệu theo giờ của một trạm trong khoảng 01/03/2013–28/02/2017. Các cột gồm thời gian, PM2.5, PM10, SO2, NO2, CO, O3 và các thông số khí tượng. Giá trị khuyết được ghi là `NA`.

Dữ liệu thô nằm trong [`data/raw/`](data/raw/README.md); dữ liệu sau xử lý dự kiến được lưu trong [`data/processed/`](data/processed/README.md). Thư mục `data/raw/` hiện cũng có `data.csv`, `test.csv` với cấu trúc OHLCV và một ảnh JPG.

Kế hoạch chính là gộp dữ liệu của 12 trạm thành một bộ dữ liệu đa trạm và mã hóa `station` như một đặc trưng. Mỗi mẫu dự đoán PM2.5 ở giờ t+1 của cùng trạm; mô hình riêng theo trạm hoặc dự đoán chân trời dài hơn (ví dụ t+24) là hướng mở rộng nếu còn thời gian.

### Phương pháp theo proposal

- **EDA:** thống kê mô tả; kiểm tra kiểu dữ liệu, missing theo cột/trạm, bản ghi trùng theo cặp trạm-thời điểm và giá trị bất thường; khảo sát phân bố PM2.5 (kể cả log-scale), biến động theo giờ/tháng/mùa/năm, tự tương quan, tương quan với biến khí tượng/ô nhiễm và quan hệ với tốc độ/hướng gió.
- **Missing và ngoại lệ:** không impute target; bỏ các dòng thiếu target khỏi huấn luyện/đánh giá. Với feature, forward-fill có giới hạn theo từng trạm rồi điền phần còn thiếu bằng median fit trên train, đồng thời tạo cờ missing. Không loại đợt PM2.5 cao nếu có thể là ô nhiễm thực tế; chỉ xử lý giá trị vô lý hoặc nghi lỗi cảm biến sau khi xác minh.
- **Đặc trưng và mã hóa:** dự kiến có PM2.5 lag 1, 2, 3, 6, 12, 24 giờ; rolling mean 6/24 giờ và độ lệch so với rolling mean; lag các biến khí tượng chính; thời gian giờ/tháng/thứ trong tuần/cuối tuần; `station` và `wd`. Mã hóa tuần hoàn sin/cos cho giờ/tháng, One-Hot cho trạm/hướng gió. Tất cả lag/rolling tính riêng theo trạm, chỉ từ quá khứ.
- **Chuẩn hóa:** chỉ dùng `StandardScaler` cho Linear Regression; mô hình cây không cần scaling. Imputer, encoder và scaler phải fit trên phần train của từng fold rồi mới transform validation/test.
- **Chia tập:** theo trình tự thời gian, không shuffle. Dự kiến train + validation từ 03/2013 đến 08/2016, validation bằng `TimeSeriesSplit` expanding-window 5 fold; test từ 09/2016 đến 02/2017, chỉ đánh giá sau khi chốt cấu hình. Các trạm có cùng target timestamp phải cùng phía của mỗi fold. Test chủ yếu rơi vào thu-đông nên cần báo cáo theo tháng/mùa để xem xét khác biệt phân bố.
- **Tuning và đánh giá:** dùng `RandomizedSearchCV` kết hợp `TimeSeriesSplit` để tinh chỉnh ít nhất một mô hình, dự kiến cả hai mô hình cây. Các tham số xem xét gồm `n_estimators`, `max_depth`, `min_samples_leaf`, `max_features` cho Random Forest; `n_estimators`, `learning_rate`, `max_depth`, `subsample` cho Gradient Boosting. Nếu Gradient Boosting của scikit-learn quá chậm trên toàn bộ dữ liệu, proposal cho phép cân nhắc `HistGradientBoostingRegressor` hoặc tập con có kiểm soát và phải ghi rõ. Chọn theo RMSE trung bình validation và độ ổn định giữa folds; báo cáo MAE/RMSE/R² tổng thể, theo trạm, mùa và nhóm PM2.5 cao; so sánh train với validation/test để nhận diện overfit/underfit. Cố định random seed để tái lập.

Proposal đầy đủ: [`docs/Nhom10_BeijingAirQuality_Proposal.pdf`](docs/Nhom10_BeijingAirQuality_Proposal.pdf).

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

**Trạng thái hiện tại:** notebook `01_eda_and_preprocessing.ipynb` có EDA và xuất bản dữ liệu chuẩn hóa còn missing; pipeline nạp, chia thời gian, tạo target/đặc trưng và tiền xử lý train-only đã được triển khai trong `src/`. Notebook `02_model_training_baseline.ipynb` đã huấn luyện và đánh giá persistence cùng Linear Regression bằng 5-fold expanding-window validation và báo cáo test; mục 13 của notebook ghép (merge) các bảng kết quả rồi tự xuất file so sánh `outputs/baseline_model_comparison.xlsx` cùng bảng gộp `outputs/baseline_comparison_merged.csv`. Notebook `03_random_forest.ipynb` huấn luyện Random Forest và notebook `04_gradient_boosting.ipynb` huấn luyện Gradient Boosting (`HistGradientBoostingRegressor`); cả hai dùng cùng 5 fold với baseline, cấu hình cố định (chưa tuning) và chưa đụng tới tập test. Notebook `05_tuning.ipynb` thực hiện `RandomizedSearchCV` cho hai mô hình cây trên cùng 5 fold (Gradient Boosting thử 20 bộ, Random Forest thử 8 bộ) và không dùng tập Test. Các phân tích/tổng hợp cuối theo proposal chưa được triển khai.

## Chạy notebook baseline

Cần có `data/processed/beijing_air_quality_standardized.csv` (tạo từ notebook 01) và môi trường có Jupyter hoặc `ipykernel`. Mục 13 xuất file Excel bằng thư viện `openpyxl`; nếu `requirements.txt` chưa có thì cài thêm:

```powershell
python -m pip install openpyxl
```

Mở `notebooks/02_model_training_baseline.ipynb` rồi chọn `Restart & Run All` (khoảng 1–2 phút). Chạy từ thư mục gốc hay từ `notebooks/` đều được. Notebook ghi:

- `models/baseline_linear_regression.joblib`, `models/baseline_metrics.csv`, `models/baseline_metadata.json`
- `outputs/baseline_error_analysis.csv`, `outputs/baseline_model_comparison.xlsx`, `outputs/baseline_comparison_merged.csv`
- `outputs/figures/baseline_*.png`
- các dòng `baseline_*` trong `experiment_log.csv` (chạy lại sẽ ghi đè, không tạo dòng trùng)

Nếu thiếu `openpyxl`, notebook vẫn chạy và chỉ bỏ qua file Excel (vẫn ghi CSV). Các mô hình sau nên ghi `experiment_log.csv` theo quy ước `<tên_thí_nghiệm>_cv5` (validation) và `<tên_thí_nghiệm>_test` (test) để sheet `Nhat_ky_thuc_nghiem` ở mục 13 tự gom chúng vào bảng xếp hạng chung. Chi tiết: [`notebooks/README.md`](notebooks/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md).

## Chạy notebook Random Forest và Gradient Boosting

Cần có `data/processed/beijing_air_quality_standardized.csv` và, để mục so sánh chạy được, các file kết quả của notebook trước: `outputs/baseline_comparison_merged.csv` (notebook 02) và `outputs/random_forest_cv_metrics.csv` (notebook 03). Mở `notebooks/03_random_forest.ipynb` hoặc `notebooks/04_gradient_boosting.ipynb` rồi chọn `Restart & Run All`; mỗi notebook chạy khoảng vài chục giây đến vài phút. Chi tiết đầu ra: [`notebooks/README.md`](notebooks/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md).

## Kết quả hiện tại (validation, chưa dùng test)

RMSE/MAE tính trên dự đoán validation của 5 fold expanding-window, đơn vị µg/m³, càng thấp càng tốt. Nguồn: `experiment_log.csv` và mục 8 của `04_gradient_boosting.ipynb`. Hai mô hình cây có hai phiên bản: cấu hình cố định (Notebook 03 và 04) và sau khi tinh chỉnh bằng `RandomizedSearchCV` (Notebook 05: Gradient Boosting thử 20 bộ tham số, Random Forest thử 8 bộ).

| Mô hình                                                        |  RMSE TB 5 fold | RMSE TB fold 2–5 | MAE TB 5 fold |
| :--------------------------------------------------------------- | --------------: | ----------------: | ------------: |
| Persistence                                                      |           19,97 |             18,92 |         10,42 |
| Linear Regression                                                | **19,29** |             18,27 |         10,74 |
| Random Forest (`n_estimators=20`)                              |           20,17 |   **17,74** |         10,53 |
| Gradient Boosting (`HistGradientBoostingRegressor`, 200 vòng) |           21,97 |             18,19 |         11,07 |
| Random Forest (đã tuning)                                      |           19,18 |             17,74 |         10,13 |
| Gradient Boosting (đã tuning)                                  |           20,04 |             18,25 |         10,52 |

Lưu ý khi đọc bảng:

- Fold 1 chỉ train trên 03–09/2013 (chưa có mùa đông) nhưng validation rơi vào mùa đông, nên sai số rất lớn (Gradient Boosting RMSE 37,11; Random Forest 29,89; Linear Regression 23,39) và kéo trung bình 5 fold lên. Vì vậy bảng có thêm cột trung bình fold 2–5.
- Gradient Boosting yếu nhất ở PM2.5 cao: RMSE 80,9 ở mức trên 250 µg/m³ và 37,1 ở mùa Đông (Random Forest: 65,0 và 30,5).
- Tuning cải thiện chủ yếu ở fold 1 (Gradient Boosting RMSE 37,11 → 27,19; Random Forest 29,89 → 24,92); trung bình fold 2–5 gần như không đổi (Gradient Boosting 18,19 → 18,25; Random Forest 17,74 → 17,74). Điểm CV của bộ tham số tốt nhất hơi lạc quan vì được chọn từ nhiều lần thử trên cùng các fold.
- Chưa chốt mô hình cuối: Random Forest đã tuning có RMSE trung bình 5 fold thấp nhất (19,18) nhưng chỉ hơn Linear Regression (19,29) rất ít, và số liệu test chưa được dùng.

## Việc cần làm tiếp theo



| Việc cần hoàn thành                                                                                                                                                                                                                                                                                                                        | Đầu ra/tiêu chí kiểm tra                                                                                                                                                                                                                                         |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chốt cấu hình thực nghiệm theo proposal; xác nhận bộ feature và cách chia thời gian dùng chung. Rà soát pipeline hiện có để ghi rõ khác biệt so với feature dự kiến trong proposal trước khi so sánh mô hình.                                                                                                     | Ghi nhận target, feature, split, CV folds, metric chính (RMSE), random seed và các khác biệt đã được thống nhất. Các mô hình dùng cùng dữ liệu/folds/preprocessing; mọi transformer chỉ fit trên train của từng fold.                        |
| Huấn luyện Random Forest trên các fold thời gian dùng chung với baseline.                                                                                                                                                                                                                                                               | Notebook/mã chạy lại được; lưu MAE, RMSE, R² từng fold, cấu hình và thời gian chạy; kết quả không dùng test để chọn cấu hình.                                                                                                                  |
| Huấn luyện Gradient Boosting Regressor. Thực hiện tuning bằng `RandomizedSearchCV` kết hợp `TimeSeriesSplit` cho ít nhất một mô hình; proposal dự kiến tinh chỉnh cả hai mô hình cây. Nếu Gradient Boosting chuẩn quá chậm, cân nhắc phương án thay thế mà proposal cho phép và ghi rõ lý do/cấu hình. | Log các lượt thử, tham số tìm kiếm, seed, điểm CV và thời gian chạy; chọn cấu hình bằng RMSE validation, có xem xét độ ổn định giữa folds.                                                                                                    |
| Tổng hợp kết quả CV của Persistence, Linear Regression, Random Forest và Gradient Boosting; chọn cấu hình cuối và khóa cấu hình trước khi dùng test.                                                                                                                                                                          | Bảng so sánh CV trên cùng folds, có MAE/RMSE/R² và độ biến động; ghi rõ mô hình/cấu hình được chọn và lý do. Không điều chỉnh dựa trên test.                                                                                             |
| Chạy đánh giá cuối trên tập test cho các mô hình/cấu hình đã khóa; baseline test đã có trong kết quả hiện tại nên không dùng lại để tinh chỉnh.                                                                                                                                                                   | Một bộ kết quả test có số mẫu, khoảng thời gian, MAE/RMSE/R² và cấu hình; test chỉ phục vụ báo cáo cuối.                                                                                                                                           |
| Hoàn thiện phân tích theo proposal: so sánh dự đoán-thực tế, residual theo thời gian, sai số theo trạm/mùa/nhóm PM2.5 cao, train-validation/test để nhận diện overfit/underfit, permutation importance. Tạo workbook Excel từ các kết quả đã kiểm chứng.                                                           | Workbook `outputs/model_comparison.xlsx` tách rõ CV và test, gồm cấu hình và phân tích; số liệu khớp với CSV/log và biểu đồ. Có thể mở rộng từ `outputs/baseline_model_comparison.xlsx` (mục 13 notebook 02) thay vì làm lại từ đầu. |
| Hoàn thiện báo cáo DOCX và slide PPTX; chạy lại kiểm thử/notebook từ trạng thái sạch; rà citation, README, artifact và khả năng tái lập.                                                                                                                                                                 | Báo cáo phản ánh đúng tiến độ thực tế; mã nguồn, log, bảng, hình và slide thống nhất; `pytest` và quy trình chạy lại thành công.

1. **Thông tin đề tài và tiến độ:** tên đề tài, thành viên/đóng góp, mục tiêu và trạng thái thực tế.

Tài liệu tham khảo: [KLTN_bao_cao_sau_hoi_dong.pdf](docs/TLTK/KLTN_bao_cao_sau_hoi_dong.pdf). Đây là khóa luận về dự đoán Pb/Zn trong bụi PM10 tại Hàn Quốc, khác dữ liệu và bài toán của nhóm. Chỉ tham khảo cách tổ chức và trình bày; không sử dụng số liệu/kết quả của khóa luận làm kết quả dự án Beijing. Xem thêm mô tả trong [`docs/README.md`](docs/README.md).

### Điều kiện hoàn thành

1. Ba phương pháp theo proposal (Linear Regression, Random Forest, Gradient Boosting) được so sánh công bằng trên cùng target, feature set, folds và quy tắc tiền xử lý; persistence được giữ làm mốc tham chiếu.
2. Tuning sử dụng validation/CV; test chỉ dùng đánh giá cuối. Không chọn cấu hình theo kết quả test.
3. Kết quả có MAE, RMSE, R²; phân tích theo các nhóm proposal; đơn vị, số mẫu và khoảng thời gian được ghi rõ.
4. Báo cáo, slide, workbook, experiment log, mã nguồn và hình biểu đồ truy vết được và nhất quán.

## Cấu trúc thư mục dự án

Sơ đồ dưới đây thể hiện thư mục và tệp hiện có. Notebook EDA, pipeline dữ liệu và baseline đã có nội dung; hai mô hình cây đã chạy 5-fold CV với cấu hình cố định; tuning đã chạy xong; đánh giá test và phân tích cuối vẫn đang chờ triển khai.tuning theo proposal, đánh giá test và phân tích cuối vẫn đang chờ triển khai.

```text
data/
├── raw/                                      Dữ liệu PRSA và các tệp bổ sung
│   └── PRSA_Data_20130301-20170228/          CSV theo 12 trạm
├── processed/                                Bản gộp/chuẩn hóa; giữ missing, chưa phải feature matrix
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA, so sánh trước/sau pipeline và xuất CSV chuẩn hóa
├── 02_model_training_baseline.ipynb           Baseline Persistence và Linear Regression, merge kết quả và xuất file so sánh
├── 03_random_forest.ipynb        Random Forest, 5 fold CV (chưa tuning, chưa dùng test)
├── 04_gradient_boosting.ipynb                 Gradient Boosting (HistGradientBoosting), 5 fold CV (chưa tuning)
└── 05_tuning.ipynb                            RandomizedSearchCV cho Gradient Boosting và Random Forest               Gradient Boosting (HistGradientBoosting), 5 fold CV (chưa tuning)
src/
├── data_loader.py                             Nạp dữ liệu, chia thời gian và CV theo timestamp
├── features.py                                Tạo target/đặc trưng và tiền xử lý train-only
├── models.py                                  Vị trí dự kiến cho triển khai mô hình (chưa triển khai)
└── evaluate.py                                Vị trí dự kiến cho metric/đánh giá dùng chung
tests/
├── test_data_pipeline.py                      Kiểm thử nạp dữ liệu và chia thời gian
├── test_feature_engineering.py                Kiểm thử target, feature và preprocessing
├── test_models_performance.py                 Chưa có test mô hình
└── test_integration.py                        Kiểm thử tích hợp pipeline dữ liệu
models/                                        Nơi lưu mô hình đã huấn luyện
├── baseline_linear_regression.joblib          Pipeline Linear Regression (baseline)
├── baseline_metrics.csv                       MAE/RMSE/R² của các baseline (CV và test)
├── baseline_metadata.json                     Thông tin nạp lại và truy vết mô hình
├── random_forest.joblib                       Pipeline Random Forest (fit trên Train/Validation)
├── random_forest_metadata.json                Thông tin truy vết Random Forest
├── gradient_boosting.joblib                   Pipeline Gradient Boosting (fit trên Train/Validation)
├── gradient_boosting_metadata.json            Thông tin truy vết Gradient Boosting
├── random_forest_tuned.joblib                 Pipeline Random Forest đã tinh chỉnh
├── random_forest_tuned_metadata.json          Thông tin truy vết Random Forest đã tinh chỉnh
├── gradient_boosting_tuned.joblib             Pipeline Gradient Boosting đã tinh chỉnh
└── gradient_boosting_tuned_metadata.json      Thông tin truy vết Gradient Boosting đã tinh chỉnh
outputs/
├── eda/                                       Nhật ký và kết luận EDA
├── figures/                                   Biểu đồ và hình ảnh kết quả (baseline_*, random_forest_*, gradient_boosting_*)
├── test_reports/                              Báo cáo kiểm thử
├── baseline_error_analysis.csv                Sai số baseline theo trạm, mùa, mức PM2.5
├── baseline_model_comparison.xlsx             File so sánh kết quả thực nghiệm của baseline
├── baseline_comparison_merged.csv             Các bảng so sánh đã merge, dạng một bảng dài
├── random_forest_*.csv                        Kết quả CV, tổng quan fold và dự đoán OOF của Random Forest
├── gradient_boosting_*.csv                    Kết quả CV và dự đoán OOF của Gradient Boosting
├── *_tuned_cv_*.csv                           Kết quả CV của hai mô hình đã tinh chỉnh (Notebook 05)
└── tuning_*_search_results.csv                Các bộ tham số đã thử bằng RandomizedSearchCV
docs/                                          Tài liệu đồ án
experiment_log.csv                             Nhật ký thực nghiệm (baseline, các bản ghi *_cv5 và *_tuned_cv5)
requirements.txt                               Danh sách thư viện Python
pytest.ini                                     Cấu hình pytest
README.md                                      Giới thiệu và hướng dẫn dự án
```

README chi tiết theo thư mục: [`data/README.md`](data/README.md), [`data/raw/README.md`](data/raw/README.md), [`data/processed/README.md`](data/processed/README.md), [`notebooks/README.md`](notebooks/README.md), [`src/README.md`](src/README.md), [`tests/README.md`](tests/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md), [`outputs/figures/README.md`](outputs/figures/README.md), [`outputs/test_reports/README.md`](outputs/test_reports/README.md) và [`docs/README.md`](docs/README.md).

## Phân công công việc

Giảng viên hướng dẫn: TS. Đỗ Như Tài

| STT | Họ và tên        |    MSSV    | Vai trò       | Phần việc phụ trách                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :-: | :------------------ | :--------: | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|  1  | Trần Lê Gia Bảo  | 3124411038 | Nhóm trưởng | Tổ chức repository và tài liệu theo proposal; khảo sát và phân tích dữ liệu (EDA); chuẩn hóa, xuất bản dữ liệu và ghi lại kết luận; xây dựng pipeline dữ liệu, tạo đặc trưng, chia tập theo thời gian và kiểm thử pipeline. Phạm vi phụ trách kết thúc ở pipeline dữ liệu, không bao gồm xây dựng, huấn luyện hay đánh giá mô hình.                                                                                                                                                         |
|  2  | Tô Thành Nhân    | 3124411198 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|  3  | Đào Hữu Tài     | 3124411261 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|  4  | Huỳnh Nhật Quang  | 3124411245 | Thành viên   | Xây dựng và đánh giá mô hình Gradient Boosting (notebook 04, dùng HistGradientBoostingRegressor, 5-fold CV theo thời gian); tinh chỉnh tham số bằng RandomizedSearchCV cho Gradient Boosting và Random Forest (notebook 05, không dùng tập Test); lưu mô hình, kết quả CV và nhật ký thực nghiệm; cập nhật README của các phần này. Phạm vi phụ trách chưa bao gồm đánh giá cuối trên tập Test, phân tích sai số và báo cáo.Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật. |
|  5  | Nguyễn Thanh Tuấn | 3124411337 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Chi tiết phạm vi công việc của nhóm trưởng được ghi tại [`docs/phan-cong-cong-viec.docx`](docs/phan-cong-cong-viec.docx). Nhật ký EDA để các thành viên đọc lại quy trình và quyết định nằm tại [`outputs/eda/eda_worklog.md`](outputs/eda/eda_worklog.md); bảng kết luận nằm tại [`outputs/eda/eda_conclusions.csv`](outputs/eda/eda_conclusions.csv).

## Nguồn dữ liệu

Chen, S. (2017). *Beijing Multi-Site Air Quality* [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G). Dữ liệu được phát hành theo giấy phép [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Bản tham khảo trên Kaggle

Thành viên có thể tham khảo trang [Beijing Multi-Site Air-Quality Data Set trên Kaggle](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set). Khi sử dụng dữ liệu trong báo cáo, cần kiểm tra nội dung và giấy phép của bản tải xuống; trích dẫn bộ dữ liệu gốc UCI ở trên theo proposal.