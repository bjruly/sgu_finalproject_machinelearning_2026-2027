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

- **EDA:** thống kê mô tả; kiểm tra kiểu dữ liệu, missing theo cột/trạm, bản ghi trùng theo cặp trạm-thời điểm và giá trị bất thường; khảo sát phân bố PM2.5 (kể cả log-scale), biến động theo giờ/tháng/mùa/năm, tự tương quan, tương quan với biến khí tượng/ô nhiễm và quan hệ với tốc độ/hướng gió.
- **Missing và ngoại lệ:** không impute target; bỏ các dòng thiếu target khỏi huấn luyện/đánh giá. Với feature, forward-fill có giới hạn theo từng trạm rồi điền phần còn thiếu bằng median fit trên train, đồng thời tạo cờ missing. Không loại đợt PM2.5 cao nếu có thể là ô nhiễm thực tế; chỉ xử lý giá trị vô lý hoặc nghi lỗi cảm biến sau khi xác minh.
- **Đặc trưng và mã hóa:** dự kiến có PM2.5 lag 1, 2, 3, 6, 12, 24 giờ; rolling mean 6/24 giờ và độ lệch so với rolling mean; lag các biến khí tượng chính; thời gian giờ/tháng/thứ trong tuần/cuối tuần; `station` và `wd`. Mã hóa tuần hoàn sin/cos cho giờ/tháng, One-Hot cho trạm/hướng gió. Tất cả lag/rolling tính riêng theo trạm, chỉ từ quá khứ.
- **Chuẩn hóa:** chỉ dùng `StandardScaler` cho Linear Regression; mô hình cây không cần scaling. Imputer, encoder và scaler phải fit trên phần train của từng fold rồi mới transform validation/test.
- **Chia tập:** theo trình tự thời gian, không shuffle. Dự kiến train + validation từ 03/2013 đến 08/2016, validation bằng `TimeSeriesSplit` expanding-window 5 fold; test từ 09/2016 đến 02/2017, chỉ đánh giá sau khi chốt cấu hình. Các trạm có cùng target timestamp phải cùng phía của mỗi fold. Test chủ yếu rơi vào thu-đông nên cần báo cáo theo tháng/mùa để xem xét khác biệt phân bố.
- **Tuning và đánh giá:** dùng `RandomizedSearchCV` kết hợp `TimeSeriesSplit` để tinh chỉnh ít nhất một mô hình, dự kiến cả hai mô hình cây. Các tham số xem xét gồm `n_estimators`, `max_depth`, `min_samples_leaf`, `max_features` cho Random Forest; `n_estimators`, `learning_rate`, `max_depth`, `subsample` cho Gradient Boosting. Nếu Gradient Boosting của scikit-learn quá chậm trên toàn bộ dữ liệu, proposal cho phép cân nhắc `HistGradientBoostingRegressor` hoặc tập con có kiểm soát và phải ghi rõ. Chọn theo RMSE trung bình validation và độ ổn định giữa folds; báo cáo MAE/RMSE/R² tổng thể, theo trạm, mùa và nhóm PM2.5 cao; so sánh train với validation/test để nhận diện overfit/underfit. Cố định random seed để tái lập.

### Đối chiếu với triển khai hiện tại

- Đã có EDA, tạo target t+1, PM2.5 lag 1/2/3/6/12/24, rolling mean 6/24, đặc trưng thời gian tuần hoàn, `station`/`wd`, forward-fill tối đa 6 giờ, train-fitted median imputation và missing indicators. Dữ liệu được chia theo thời gian và baseline chạy 5 fold expanding-window.
- Chưa có trong pipeline hiện tại một số đặc trưng proposal dự kiến: độ lệch so với rolling mean, lag của các biến khí tượng, và cờ cuối tuần. Các phân tích EDA tự tương quan, phân bố log-scale và quan hệ gió cũng cần được xác nhận có đủ nội dung trước khi kết luận hoàn tất proposal.
- Baseline Persistence/Linear Regression đã chạy và có file so sánh kết quả thực nghiệm (`outputs/baseline_model_comparison.xlsx`). Random Forest (`03_random_forest.ipynb`) và Gradient Boosting (`04_gradient_boosting.ipynb`, dùng `HistGradientBoostingRegressor`) đã chạy 5-fold CV với cấu hình cố định, chưa tuning và chưa dùng test. Notebook `05_tuning.ipynb` đã tinh chỉnh bằng `RandomizedSearchCV` cho cả hai mô hình cây trên cùng 5 fold (Gradient Boosting thử 20 bộ tham số, Random Forest thử 8 bộ), không dùng tập Test. So sánh cuối cùng, đánh giá test và permutation importance cho các mô hình cây chưa hoàn thành.Tuning bằng `RandomizedSearchCV`, so sánh cuối cùng, đánh giá test và permutation importance cho các mô hình cây chưa hoàn thành.
- Proposal dự kiến có thể điều chỉnh mốc chia sau EDA; mốc đang dùng trong baseline là test target từ 01/09/2016. Mọi thay đổi so với proposal cần ghi rõ lý do và thống nhất trong nhóm. Test chỉ dùng để báo cáo cuối, không dùng chọn/tuning cấu hình.

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

## Việc cần làm tiếp theo trong 7 ngày

Đây là checklist đầu việc và đầu ra, không phải phân công nhân sự. Proposal đặt tiến độ dự kiến 5 tuần; mốc 7 ngày dưới đây là kế hoạch rút gọn để hoàn thiện các phần còn lại, không thay đổi yêu cầu phương pháp của proposal.

| Ngày | Việc cần hoàn thành                                                                                                                                                                                                                                                                                                                        | Đầu ra/tiêu chí kiểm tra                                                                                                                                                                                                                                         |
| :---: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1   | Chốt cấu hình thực nghiệm theo proposal; xác nhận bộ feature và cách chia thời gian dùng chung. Rà soát pipeline hiện có để ghi rõ khác biệt so với feature dự kiến trong proposal trước khi so sánh mô hình.                                                                                                     | Ghi nhận target, feature, split, CV folds, metric chính (RMSE), random seed và các khác biệt đã được thống nhất. Các mô hình dùng cùng dữ liệu/folds/preprocessing; mọi transformer chỉ fit trên train của từng fold.                        |
|   2   | Huấn luyện Random Forest trên các fold thời gian dùng chung với baseline.                                                                                                                                                                                                                                                               | Notebook/mã chạy lại được; lưu MAE, RMSE, R² từng fold, cấu hình và thời gian chạy; kết quả không dùng test để chọn cấu hình.                                                                                                                  |
|   3   | Huấn luyện Gradient Boosting Regressor. Thực hiện tuning bằng `RandomizedSearchCV` kết hợp `TimeSeriesSplit` cho ít nhất một mô hình; proposal dự kiến tinh chỉnh cả hai mô hình cây. Nếu Gradient Boosting chuẩn quá chậm, cân nhắc phương án thay thế mà proposal cho phép và ghi rõ lý do/cấu hình. | Log các lượt thử, tham số tìm kiếm, seed, điểm CV và thời gian chạy; chọn cấu hình bằng RMSE validation, có xem xét độ ổn định giữa folds.                                                                                                    |
|   4   | Tổng hợp kết quả CV của Persistence, Linear Regression, Random Forest và Gradient Boosting; chọn cấu hình cuối và khóa cấu hình trước khi dùng test.                                                                                                                                                                          | Bảng so sánh CV trên cùng folds, có MAE/RMSE/R² và độ biến động; ghi rõ mô hình/cấu hình được chọn và lý do. Không điều chỉnh dựa trên test.                                                                                             |
|   5   | Chạy đánh giá cuối trên tập test cho các mô hình/cấu hình đã khóa; baseline test đã có trong kết quả hiện tại nên không dùng lại để tinh chỉnh.                                                                                                                                                                   | Một bộ kết quả test có số mẫu, khoảng thời gian, MAE/RMSE/R² và cấu hình; test chỉ phục vụ báo cáo cuối.                                                                                                                                           |
|   6   | Hoàn thiện phân tích theo proposal: so sánh dự đoán-thực tế, residual theo thời gian, sai số theo trạm/mùa/nhóm PM2.5 cao, train-validation/test để nhận diện overfit/underfit, permutation importance. Tạo workbook Excel từ các kết quả đã kiểm chứng.                                                           | Workbook `outputs/model_comparison.xlsx` tách rõ CV và test, gồm cấu hình và phân tích; số liệu khớp với CSV/log và biểu đồ. Có thể mở rộng từ `outputs/baseline_model_comparison.xlsx` (mục 13 notebook 02) thay vì làm lại từ đầu. |
|   7   | Hoàn thiện báo cáo DOCX và slide PPTX; chạy lại kiểm thử/notebook từ trạng thái sạch; rà citation, README, artifact và khả năng tái lập.                                                                                                                                                                                    | Báo cáo phản ánh đúng tiến độ thực tế; mã nguồn, log, bảng, hình và slide thống nhất; `pytest` và quy trình chạy lại thành công.                                                                                                            |

### Tiến độ thực tế (cập nhật 10/11/2026)

| Ngày | Việc                                                              | Trạng thái                                                                                                                                            |
| :---: | :----------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
|   1   | Chốt cấu hình, rà soát pipeline                               | Đã có pipeline dùng chung; các khác biệt feature so với proposal vẫn còn (xem phần Đối chiếu ở trên)                                    |
|   2   | Random Forest trên 5 fold                                         | Xong (`03_random_forest.ipynb`), `n_estimators=20`, chưa tuning                                                                       |
|   3   | Gradient Boosting + `RandomizedSearchCV`                         | Xong: Gradient Boosting (`04_gradient_boosting.ipynb`, bản Hist) và tinh chỉnh cả hai mô hình cây (`05_tuning.ipynb`, 20 và 8 bộ tham số) |
| 4–7 | Tổng hợp CV, test cuối, phân tích, workbook, báo cáo, slide | Chưa làm                                                                                                                                              |

### Cấu trúc báo cáo tham khảo từ tài liệu TLTK

Khóa luận tham khảo trình bày theo mạch: mở đầu → cơ sở lý thuyết → dữ liệu và tiền xử lý → phân tích xu hướng → phương pháp → thiết lập/kết quả/đánh giá thực nghiệm → kết luận, hạn chế và hướng phát triển → tài liệu tham khảo/phụ lục. Có thể vận dụng cấu trúc đó cho đề tài Beijing, nhưng không cần sao chép nguyên số chương hoặc nội dung chuyên ngành:

1. **Thông tin đề tài và tiến độ:** tên đề tài, thành viên/đóng góp, mục tiêu và trạng thái thực tế.
2. **Giới thiệu bài toán:** bối cảnh, ý nghĩa, Input/Output, target PM2.5 giờ `t+1`, loại bài toán hồi quy.
3. **Dữ liệu và khám phá:** nguồn, số mẫu/thuộc tính, các trạm, phân bố, missing, xu hướng và các biểu đồ EDA.
4. **Tiền xử lý và pipeline:** quy tắc xử lý missing/ngoại lệ, tạo feature, chia thời gian và biện pháp chống leakage.
5. **Phương pháp thực nghiệm:** persistence/Linear Regression, Random Forest, Gradient Boosting; folds, tuning, metric và cấu hình.
6. **Kết quả và thảo luận:** bảng so sánh CV/test, dự đoán-thực tế, sai số theo trạm/mùa/PM2.5 cao, residual, importance; nêu hạn chế và giải thích dựa trên số liệu.
7. **Kết luận, hạn chế, hướng phát triển; tài liệu tham khảo và phụ lục:** đưa bảng/biểu đồ chi tiết theo trạm, cấu hình và kết quả bổ sung vào phụ lục để nội dung chính dễ theo dõi.

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
├── processed/                                Dữ liệu sau khi làm sạch/biến đổi
notebooks/
├── 01_eda_and_preprocessing.ipynb            EDA, so sánh trước/sau pipeline và xuất CSV chuẩn hóa
├── 02_model_training_baseline.ipynb           Baseline Persistence và Linear Regression, merge kết quả và xuất file so sánh
├── 03_random_forest.ipynb        Random Forest, 5 fold CV (chưa tuning, chưa dùng test)
├── 04_gradient_boosting.ipynb                 Gradient Boosting (HistGradientBoosting), 5 fold CV (chưa tuning)
└── 05_tuning.ipynb                            RandomizedSearchCV cho Gradient Boosting và Random Forest               Gradient Boosting (HistGradientBoosting), 5 fold CV (chưa tuning)
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

| STT | Họ và tên        |    MSSV    | Vai trò       | Phần việc phụ trách                                                                                                                                                                                                                                                                                                                                                                   |
| :-: | :------------------ | :--------: | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  1  | Trần Lê Gia Bảo  | 3124411038 | Nhóm trưởng | Tổ chức repository và tài liệu theo proposal; khảo sát và phân tích dữ liệu (EDA); chuẩn hóa, xuất bản dữ liệu và ghi lại kết luận; xây dựng pipeline dữ liệu, tạo đặc trưng, chia tập theo thời gian và kiểm thử pipeline. Phạm vi phụ trách kết thúc ở pipeline dữ liệu, không bao gồm xây dựng, huấn luyện hay đánh giá mô hình. |
|  2  | Tô Thành Nhân    | 3124411198 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                       |
|  3  | Đào Hữu Tài     | 3124411261 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                       |
|  4  | Huỳnh Nhật Quang  | 3124411245 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                       |
|  5  | Nguyễn Thanh Tuấn | 3124411337 | Thành viên   | Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật.                                                                                                                                                                                                                                                                                                                       |

Chi tiết phạm vi công việc của nhóm trưởng được ghi tại [`docs/phan-cong-cong-viec.docx`](docs/phan-cong-cong-viec.docx). Nhật ký EDA để các thành viên đọc lại quy trình và quyết định nằm tại [`outputs/eda/eda_worklog.md`](outputs/eda/eda_worklog.md); bảng kết luận nằm tại [`outputs/eda/eda_conclusions.csv`](outputs/eda/eda_conclusions.csv).

## Nguồn dữ liệu

Chen, S. (2017). *Beijing Multi-Site Air Quality* [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G). Dữ liệu được phát hành theo giấy phép [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Bản tham khảo trên Kaggle

Thành viên có thể tham khảo trang [Beijing Multi-Site Air-Quality Data Set trên Kaggle](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set). Khi sử dụng dữ liệu trong báo cáo, cần kiểm tra nội dung và giấy phép của bản tải xuống; trích dẫn bộ dữ liệu gốc UCI ở trên theo proposal.
