# Beijing Multi-Site Air Quality Prediction

Đồ án cuối kỳ môn Máy học, xây dựng hệ thống phân tích và dự đoán nồng độ bụi mịn PM2.5 từ bộ dữ liệu Beijing Multi-Site Air Quality. Đây là bài toán hồi quy chuỗi thời gian đa trạm: dự đoán PM2.5 ở giờ kế tiếp (t+1) cho cùng trạm dựa trên thông tin tại thời điểm hiện tại và các đặc trưng chỉ sử dụng dữ liệu quá khứ.

## Mục tiêu

Mục tiêu là dự đoán liên tục nồng độ PM2.5 (µg/m³) tại giờ kế tiếp `t+1` cho cùng trạm, từ dữ liệu ô nhiễm, khí tượng và thời gian đến giờ `t`. Các câu hỏi nghiên cứu theo proposal:

1. Random Forest và Gradient Boosting cải thiện bao nhiêu so với baseline Linear Regression?
2. Nhóm đặc trưng nào (PM2.5 trễ, khí tượng, thời gian, trạm) đóng góp vào độ chính xác?
3. Sai số thay đổi thế nào theo trạm, mùa và các đợt PM2.5 cao?

Các phương pháp được đề xuất gồm Linear Regression làm baseline, Random Forest Regressor và Gradient Boosting Regressor để so sánh. Persistence là mốc tham chiếu đơn giản. Thực nghiệm bổ sung MLP cho bài toán hồi quy PM2.5. Chọn cấu hình theo RMSE validation, đồng thời báo cáo MAE và R². Phân tích kết quả gồm sai số theo trạm/mùa/PM2.5 cao, dự đoán so với thực tế, residual theo thời gian và permutation importance. Không dùng Accuracy cho bài toán hồi quy.

## Dữ liệu

Bộ dữ liệu PRSA gồm 12 tệp CSV, mỗi tệp là dữ liệu theo giờ của một trạm trong khoảng 01/03/2013–28/02/2017. Các cột gồm thời gian, PM2.5, PM10, SO2, NO2, CO, O3 và các thông số khí tượng. Giá trị khuyết được ghi là `NA`.

Dữ liệu thô dùng cho đồ án gồm 12 CSV PRSA tại [`data/raw/`](data/raw/README.md). Notebook 01 gộp và chuẩn hóa dữ liệu, rồi ghi [`beijing_air_quality_standardized.csv`](data/processed/beijing_air_quality_standardized.csv) trong `data/processed/`.

Kế hoạch chính là gộp dữ liệu của 12 trạm thành một bộ dữ liệu đa trạm và mã hóa `station` như một đặc trưng. Mỗi mẫu dự đoán PM2.5 ở giờ t+1 của cùng trạm; mô hình riêng theo trạm hoặc dự đoán chân trời dài hơn (ví dụ t+24) là hướng mở rộng nếu còn thời gian.

### Phương pháp theo proposal

- **EDA:** thống kê mô tả; kiểm tra kiểu dữ liệu, missing theo cột/trạm, bản ghi trùng theo cặp trạm-thời điểm và giá trị bất thường; khảo sát phân bố PM2.5 (kể cả log-scale), biến động theo giờ/tháng/mùa/năm, tự tương quan, tương quan với biến khí tượng/ô nhiễm và quan hệ với tốc độ/hướng gió.
- **Missing và ngoại lệ:** không impute target; bỏ các dòng thiếu target khỏi huấn luyện/đánh giá. Với feature, forward-fill có giới hạn theo từng trạm rồi điền phần còn thiếu bằng median fit trên train, đồng thời tạo cờ missing. Không loại đợt PM2.5 cao nếu có thể là ô nhiễm thực tế; chỉ xử lý giá trị vô lý hoặc nghi lỗi cảm biến sau khi xác minh.
- **Đặc trưng và mã hóa:** dự kiến có PM2.5 lag 1, 2, 3, 6, 12, 24 giờ; rolling mean 6/24 giờ và độ lệch so với rolling mean; lag các biến khí tượng chính; thời gian giờ/tháng/thứ trong tuần/cuối tuần; `station` và `wd`. Mã hóa tuần hoàn sin/cos cho giờ/tháng, One-Hot cho trạm/hướng gió. Tất cả lag/rolling tính riêng theo trạm, chỉ từ quá khứ.
- **Chuẩn hóa:** Pipeline thực nghiệm dùng `StandardScaler` cho đặc trưng số của Linear Regression và MLP. MLP còn chuẩn hóa giá trị mục tiêu và đổi dự đoán về µg/m³ trước khi chấm điểm. Random Forest và Gradient Boosting dùng bộ tiền xử lý với `scale=False`. Mỗi bộ tiền xử lý học từ phần train của từng fold.
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

Bộ kiểm thử tự động kiểm tra đọc dữ liệu, chia theo thời gian, tạo đặc trưng và pipeline tích hợp. Điểm đánh giá các mô hình được tính trong các notebook thực nghiệm. Xem [hướng dẫn kiểm thử](tests/README.md).

**Trạng thái hiện tại** — Notebook 01 xuất dữ liệu chuẩn hóa. Notebook 02–04 đánh giá hai baseline và hai mô hình cây. Notebook 05 tinh chỉnh Random Forest và Gradient Boosting. Notebook 06 huấn luyện MLP gốc, notebook 07 tinh chỉnh MLP, và notebook 08 đánh giá cuối cả 5 mô hình trên cùng tập test.

## Chạy notebook baseline

Cần có `data/processed/beijing_air_quality_standardized.csv` (tạo từ notebook 01) và môi trường có Jupyter hoặc `ipykernel`. Mục 13 xuất file Excel bằng thư viện `openpyxl`; nếu `requirements.txt` chưa có thì cài thêm:

```powershell
python -m pip install openpyxl
```

Mở `notebooks/02_model_training_baseline.ipynb`, chọn kernel của đồ án rồi chạy toàn bộ các ô. Đặt `SAVE_ARTIFACTS = True` để lưu mô hình và các đầu ra. Trong quy trình đánh giá tập trung ở notebook 08, đặt `RUN_FINAL_TEST = False` ở notebook 02. Notebook 02 có thể tạo:

- `models/baseline_linear_regression.joblib`, `models/baseline_metrics.csv`, `models/baseline_metadata.json`
- `outputs/baseline_error_analysis.csv`, `outputs/baseline_model_comparison.xlsx`, `outputs/baseline_comparison_merged.csv`
- `outputs/figures/baseline_*.png`
- các dòng `baseline_*` trong `experiment_log.csv` (chạy lại sẽ ghi đè, không tạo dòng trùng)

Nếu thiếu `openpyxl`, notebook vẫn chạy và chỉ bỏ qua file Excel (vẫn ghi CSV). Các mô hình sau nên ghi `experiment_log.csv` theo quy ước `<tên_thí_nghiệm>_cv5` (validation) và `<tên_thí_nghiệm>_test` (test) để sheet `Nhat_ky_thuc_nghiem` ở mục 13 tự gom chúng vào bảng xếp hạng chung. Chi tiết: [`notebooks/README.md`](notebooks/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md).

## Chạy notebook Random Forest và Gradient Boosting

Cần có `data/processed/beijing_air_quality_standardized.csv` và, để mục so sánh chạy được, các file kết quả của notebook trước: `outputs/baseline_comparison_merged.csv` (notebook 02) và `outputs/random_forest_cv_metrics.csv` (notebook 03). Mở `notebooks/03_random_forest.ipynb` hoặc `notebooks/04_gradient_boosting.ipynb` rồi chọn `Restart & Run All`; mỗi notebook chạy khoảng vài chục giây đến vài phút. Chi tiết đầu ra: [`notebooks/README.md`](notebooks/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md).

## Chạy notebook tinh chỉnh, MLP và đánh giá cuối

Mở repo từ thư mục gốc rồi chạy notebook theo thứ tự 01 → 08. Với các notebook tạo mô hình, bật `SAVE_ARTIFACTS` để các bước sau dùng được tệp đã lưu.

1. Chạy **05** để tinh chỉnh Random Forest và Gradient Boosting trên 5 fold theo thời gian. Notebook đọc bảng điểm từng fold từ 03 và 04.
2. Chạy **06** để xây dựng MLP gốc và lưu `outputs/mlp_cv_metrics.csv` khi bật `SAVE_ARTIFACTS` ở mục 9.
3. Chạy **07** để tinh chỉnh MLP. Bản thực nghiệm đã thử 8 tổ hợp trên 5 fold và lưu `models/mlp_tuned.joblib`.
4. Chạy **08** khi đã có `baseline_linear_regression.joblib`, `random_forest_tuned.joblib`, `gradient_boosting_tuned.joblib` và `mlp_tuned.joblib` trong `models/`. Nếu clone repo và thiếu Linear Regression, tạo và lưu mô hình từ notebook 02 vì file này nằm trong `.gitignore`.

Xem mô tả từng notebook và đầu ra trong [`notebooks/README.md`](notebooks/README.md).

### Bộ notebook chưa chạy

[`notebooks_unexecuted/`](notebooks_unexecuted/) nằm cạnh `notebooks/` ở thư mục gốc và chứa đủ 8 notebook từ 01 đến 08. Mỗi bản giữ nội dung Markdown và mã nguồn, với output và số thứ tự chạy của các ô đã được xóa.

Để chạy lại toàn bộ quy trình, mở thư mục gốc của repo trong VS Code, chọn môi trường Python của đồ án và chạy lần lượt các file 01 → 08 trong `notebooks_unexecuted/`. Bật `SAVE_ARTIFACTS` ở các notebook tạo mô hình để notebook 08 có thể nạp mô hình đã lưu.

## Kết quả validation (5 fold theo thời gian)

MAE và RMSE tính bằng µg/m³, càng thấp càng tốt. Nguồn số liệu là `experiment_log.csv` và notebook 04–07. Notebook 05 dùng `RandomizedSearchCV` với 20 tổ hợp cho Gradient Boosting và 8 cho Random Forest. Notebook 07 thử 8 tổ hợp cho MLP.

| Mô hình                                                        |  RMSE TB 5 fold | RMSE TB fold 2–5 | MAE TB 5 fold |
| :--------------------------------------------------------------- | --------------: | ----------------: | ------------: |
| Persistence                                                      |           19,97 |             18,92 |         10,42 |
| Linear Regression | 19,29 | 18,27 | 10,74 |
| Random Forest (`n_estimators=20`)                              |           20,17 |   **17,74** |         10,53 |
| Gradient Boosting (`HistGradientBoostingRegressor`, 200 vòng) |           21,97 |             18,19 |         11,07 |
| Random Forest (đã tinh chỉnh) | **19,18** | 17,74 | **10,13** |
| Gradient Boosting (đã tinh chỉnh) | 20,04 | 18,25 | 10,52 |
| MLP gốc | 20,08 | 18,09 | 11,73 |
| MLP (đã tinh chỉnh) | 19,63 | 18,00 | 11,07 |

Lưu ý khi đọc bảng:

- Fold 1 chỉ train trên 03–09/2013 (chưa có mùa đông) nhưng validation rơi vào mùa đông, nên sai số rất lớn (Gradient Boosting RMSE 37,11; Random Forest 29,89; Linear Regression 23,39) và kéo trung bình 5 fold lên. Vì vậy bảng có thêm cột trung bình fold 2–5.
- Gradient Boosting yếu nhất ở PM2.5 cao: RMSE 80,9 ở mức trên 250 µg/m³ và 37,1 ở mùa Đông (Random Forest: 65,0 và 30,5).
- Tuning cải thiện chủ yếu ở fold 1 (Gradient Boosting RMSE 37,11 → 27,19; Random Forest 29,89 → 24,92); trung bình fold 2–5 gần như không đổi (Gradient Boosting 18,19 → 18,25; Random Forest 17,74 → 17,74). Điểm CV của bộ tham số tốt nhất hơi lạc quan vì được chọn từ nhiều lần thử trên cùng các fold.
- Trong lần chạy notebook 07, RMSE validation của MLP giảm từ 20,0840 xuống 19,6317 µg/m³ (2,25%); riêng fold 2–5 giảm 0,52%. Random Forest đã tinh chỉnh có RMSE trung bình 5 fold thấp nhất trong các cấu hình đã thử.

## Kết quả đánh giá trên tập test

Notebook 08 đánh giá trên **51.063 mẫu**, với nhãn từ **01/09/2016 đến 28/02/2017**. Cấu hình của các mô hình đã được chốt từ validation. Bảng dưới đây xếp theo RMSE test.

| Hạng | Mô hình | MAE (µg/m³) | RMSE (µg/m³) | R² |
| ---: | --- | ---: | ---: | ---: |
| 1 | Random Forest (đã tinh chỉnh) | 10,5906 | **20,9613** | 0,9550 |
| 2 | Gradient Boosting (đã tinh chỉnh) | 10,8195 | 21,2957 | 0,9536 |
| 3 | MLP (đã tinh chỉnh) | 11,1583 | 21,4967 | 0,9527 |
| 4 | Linear Regression | 11,3510 | 21,8027 | 0,9513 |
| 5 | Persistence | 11,5864 | 23,1133 | 0,9453 |

Random Forest đã tinh chỉnh có RMSE thấp nhất, giảm **9,31%** so với Persistence. Bảng điểm và biểu đồ nằm tại [`outputs/final_test_metrics.csv`](outputs/final_test_metrics.csv) và [`outputs/figures/final_test_rmse.png`](outputs/figures/final_test_rmse.png). Các dòng `*_test` nằm trong [`experiment_log.csv`](experiment_log.csv).

## Việc cần làm tiếp theo

- Đưa bảng điểm, hình và nhận xét về validation/test vào báo cáo và slide cuối kỳ. Ghi rõ giới hạn của các lần tuning và phân tích sai số đã thực hiện theo proposal.
- Hoàn thiện workbook kết quả tổng hợp nếu nhóm chọn dùng Excel để đối chiếu. Đối chiếu kết quả với CSV, nhật ký và biểu đồ.
- Rà citation, tài liệu, cách tái lập và thống nhất nội dung báo cáo với kết quả đã lưu.

Tài liệu tham khảo về cách trình bày báo cáo nằm trong [`docs/README.md`](docs/README.md).

### Điều kiện hoàn thành

1. So sánh công bằng Linear Regression, Random Forest, Gradient Boosting và MLP trên cùng target, đặc trưng và fold theo thời gian. Persistence là mốc tham chiếu.
2. Tuning sử dụng validation/CV; test chỉ dùng đánh giá cuối. Không chọn cấu hình theo kết quả test.
3. Kết quả có MAE, RMSE, R²; phân tích theo các nhóm proposal; đơn vị, số mẫu và khoảng thời gian được ghi rõ.
4. Báo cáo, slide, workbook, experiment log, mã nguồn và hình biểu đồ truy vết được và nhất quán.

## Cấu trúc thư mục dự án

Sơ đồ dưới đây tóm tắt mã nguồn, dữ liệu đầu vào và các đầu ra của quy trình 01–08.

```text
data/
├── raw/                                      Dữ liệu PRSA gốc theo 12 trạm
│   └── PRSA_Data_20130301-20170228/          CSV theo 12 trạm
├── processed/                                Bản gộp/chuẩn hóa; giữ missing, chưa phải feature matrix
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA, so sánh trước/sau pipeline và xuất CSV chuẩn hóa
├── 02_model_training_baseline.ipynb           Baseline Persistence và Linear Regression, merge kết quả và xuất file so sánh
├── 03_random_forest.ipynb        Random Forest, 5 fold CV (chưa tuning, chưa dùng test)
├── 04_gradient_boosting.ipynb                 Gradient Boosting (HistGradientBoosting), 5 fold CV (chưa tuning)
├── 05_tuning.ipynb                            Tinh chỉnh Gradient Boosting và Random Forest
├── 06_mlp_regression.ipynb                    MLP gốc và phân tích validation
├── 07_mlp_tuning.ipynb                        Tinh chỉnh MLP trên 5 fold
└── 08_final_evaluation.ipynb                  Đánh giá cuối 5 mô hình trên tập test
notebooks_unexecuted/                          8 notebook đã xóa output để chạy lại
├── 01_eda_and_preprocessing.ipynb
├── 02_model_training_baseline.ipynb
├── 03_random_forest.ipynb
├── 04_gradient_boosting.ipynb
├── 05_tuning.ipynb
├── 06_mlp_regression.ipynb
├── 07_mlp_tuning.ipynb
└── 08_final_evaluation.ipynb
src/
├── data_loader.py                             Nạp dữ liệu, chia thời gian và CV theo timestamp
└── features.py                                Tạo target/đặc trưng và tiền xử lý train-only
tests/
├── test_data_pipeline.py                      Kiểm thử nạp dữ liệu và chia thời gian
├── test_feature_engineering.py                Kiểm thử target, feature và preprocessing
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
├── gradient_boosting_tuned_metadata.json      Thông tin truy vết Gradient Boosting đã tinh chỉnh
├── mlp.joblib                                 MLP gốc
├── mlp_metadata.json                          Thông tin truy vết MLP gốc
├── mlp_tuned.joblib                           MLP đã tinh chỉnh
└── mlp_tuned_metadata.json                    Thông tin truy vết MLP đã tinh chỉnh
outputs/
├── eda/                                       Nhật ký và kết luận EDA
├── figures/                                   Biểu đồ validation, tuning và test
├── baseline_error_analysis.csv                Sai số baseline theo trạm, mùa, mức PM2.5
├── baseline_model_comparison.xlsx             File so sánh kết quả thực nghiệm của baseline
├── baseline_comparison_merged.csv             Các bảng so sánh đã merge, dạng một bảng dài
├── random_forest_*.csv                        Kết quả CV, tổng quan fold và dự đoán OOF của Random Forest
├── gradient_boosting_*.csv                    Kết quả CV và dự đoán OOF của Gradient Boosting
├── mlp_*.csv                                  Kết quả validation và phân tích sai số của MLP
├── *_tuned_cv_*.csv                           Kết quả CV sau tinh chỉnh từ notebook 05 và 07
├── tuning_*_search_results.csv                Các bộ tham số đã thử bằng RandomizedSearchCV
└── final_test_metrics.csv                     MAE, RMSE và R² trên tập test
docs/                                          Tài liệu đồ án
experiment_log.csv                             Nhật ký validation (*_cv5) và test (*_test)
requirements.txt                               Danh sách thư viện Python
pytest.ini                                     Cấu hình pytest
README.md                                      Giới thiệu và hướng dẫn dự án
```

README chi tiết theo thư mục: [`data/README.md`](data/README.md), [`data/raw/README.md`](data/raw/README.md), [`data/processed/README.md`](data/processed/README.md), [`notebooks/README.md`](notebooks/README.md), [`src/README.md`](src/README.md), [`tests/README.md`](tests/README.md), [`models/README.md`](models/README.md), [`outputs/README.md`](outputs/README.md), [`outputs/figures/README.md`](outputs/figures/README.md) và [`docs/README.md`](docs/README.md).

## Phân công công việc

Giảng viên hướng dẫn: TS. Đỗ Như Tài

| STT | Họ và tên        |    MSSV    | Vai trò       | Phần việc phụ trách                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :-: | :------------------ | :--------: | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|  1  | Trần Lê Gia Bảo  | 3124411038 | Nhóm trưởng | Tổ chức repository và tài liệu theo proposal; khảo sát và phân tích dữ liệu (EDA); chuẩn hóa, xuất bản dữ liệu và ghi lại kết luận; xây dựng pipeline dữ liệu, tạo đặc trưng, chia tập theo thời gian và kiểm thử pipeline. Phạm vi phụ trách kết thúc ở pipeline dữ liệu, không bao gồm xây dựng, huấn luyện hay đánh giá mô hình.                                                                                                                                                         |
|  2  | Tô Thành Nhân    | 3124411198 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|  3  | Đào Hữu Tài     | 3124411261 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|  4  | Huỳnh Nhật Quang  | 3124411245 | Thành viên   | Xây dựng và đánh giá mô hình Gradient Boosting (notebook 04, dùng HistGradientBoostingRegressor, 5-fold CV theo thời gian); tinh chỉnh tham số bằng RandomizedSearchCV cho Gradient Boosting và Random Forest (notebook 05, không dùng tập Test); lưu mô hình, kết quả CV và nhật ký thực nghiệm; cập nhật README của các phần này. Bổ sung và tinh chỉnh MLP (notebook 06–07), thực hiện đánh giá cuối cùng theo notebook 08 và ghi nhận kết quả thực nghiệm. |
|  5  | Nguyễn Thanh Tuấn | 3124411337 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Chi tiết phạm vi công việc của nhóm trưởng được ghi tại [`docs/phan-cong-cong-viec.docx`](docs/phan-cong-cong-viec.docx). Nhật ký EDA để các thành viên đọc lại quy trình và quyết định nằm tại [`outputs/eda/eda_worklog.md`](outputs/eda/eda_worklog.md); bảng kết luận nằm tại [`outputs/eda/eda_conclusions.csv`](outputs/eda/eda_conclusions.csv).

## Nguồn dữ liệu

Chen, S. (2017). *Beijing Multi-Site Air Quality* [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G). Dữ liệu được phát hành theo giấy phép [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Bản tham khảo trên Kaggle

Thành viên có thể tham khảo trang [Beijing Multi-Site Air-Quality Data Set trên Kaggle](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set). Khi sử dụng dữ liệu trong báo cáo, cần kiểm tra nội dung và giấy phép của bản tải xuống; trích dẫn bộ dữ liệu gốc UCI ở trên theo proposal.
