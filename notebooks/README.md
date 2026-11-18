# Thư mục `notebooks`

Nơi lưu các Jupyter Notebook dùng để khám phá dữ liệu (EDA), tiền xử lý, thử nghiệm mô hình tinh chỉnh siêu tham số và đánh giá cuối trên tập test.

## Các tệp hiện có

- `01_eda_and_preprocessing.ipynb`: EDA 12 CSV PRSA; kiểm tra schema, thời gian, missing, phân bố PM2.5, xu hướng theo tháng/giờ/mùa và tương quan. Cuối notebook có bước xuất bản CSV chuẩn hóa nhưng không impute hoặc tiền xử lý thành dữ liệu model-ready.
- `02_model_training_baseline.ipynb`: huấn luyện và đánh giá hai baseline cho bài toán dự đoán PM2.5 giờ t+1:

  - **Persistence**: dự đoán PM2.5(t+1) = PM2.5(t), không học tham số.
  - **Linear Regression**: pipeline `build_preprocessor(scale=True)` + `LinearRegression`.
  - Dùng lại pipeline trong `src/` (đặc trưng, chia thời gian, 5 fold expanding-window) và đánh giá bằng MAE, RMSE, R².
  - Phân tích sai số theo trạm, mùa, mức PM2.5 và theo tháng; residual; hệ số và permutation importance theo nhóm feature của Linear Regression.
  - Có mục đánh giá trên tập test, điều khiển bằng cờ `RUN_FINAL_TEST`.
  - Mục 13 ghép (`merge`) các bảng kết quả của hai mô hình, ghép thêm với nhật ký `experiment_log.csv`, rồi **xuất file so sánh kết quả thực nghiệm** (Excel và CSV).
- `03_random_forest.ipynb`: huấn luyện **Random Forest** (`n_estimators=20`, `max_depth=16`, `min_samples_leaf=5`, `max_features=0.7`) bằng 5-fold CV dùng chung với baseline; lưu mô hình, metrics, dự đoán OOF, hình và dòng `random_forest_cv5` trong `experiment_log.csv`. Cấu hình này dùng để đối chiếu với kết quả tinh chỉnh ở notebook 05.
- `04_gradient_boosting.ipynb`: huấn luyện **Gradient Boosting** bằng `HistGradientBoostingRegressor` (`max_iter=200`, `learning_rate=0.1`, `early_stopping=False`, còn lại mặc định) trên cùng 5 fold. Có so sánh 4 mô hình theo từng fold (kèm trung bình fold 2–5), kiểm tra overfit (`train_rmse` so với `rmse`), sai số theo mùa/mức PM2.5, so sánh với Random Forest; lưu mô hình, metrics, OOF, 4 hình và dòng `gradient_boosting_cv5`. Chưa tuning, không đánh giá trên test.
- `05_tuning.ipynb`: tinh chỉnh tham số bằng `RandomizedSearchCV` cho Gradient Boosting (mặc định thử 20 bộ tham số) và Random Forest (mặc định thử 8 bộ) trên đúng 5 fold dùng chung (`cv=folds`), chọn bộ có RMSE trung bình 5 fold thấp nhất. Sau đó chấm lại bộ tốt nhất (MAE, RMSE, R², `train_rmse`), so sánh trước và sau tinh chỉnh, lưu mô hình `*_tuned`, bảng các lần thử và ghi các dòng `*_tuned_cv5` vào `experiment_log.csv`. Không dùng tập Test.
- `06_mlp_regression.ipynb` — Huấn luyện MLP gốc cấu hình `(64, 32)` và chấm trên 5 fold validation.
- `07_mlp_tuning.ipynb` — Tinh chỉnh 5 siêu tham số của MLP và chọn theo RMSE validation trung bình.
- `08_final_evaluation.ipynb` — Chấm 5 mô hình trên cùng 51.063 mẫu test và xuất bảng điểm, biểu đồ, nhật ký.

## Chạy notebook 02

Điều kiện: đã có `data/processed/beijing_air_quality_standardized.csv` (tạo từ notebook 01) và đã cài các thư viện trong `requirements.txt`; môi trường cần có Jupyter hoặc `ipykernel` để chạy notebook. Để xuất file Excel ở mục 13 cần thêm `openpyxl` (`pip install openpyxl`); nếu thiếu, notebook vẫn chạy, chỉ bỏ qua file Excel và vẫn ghi CSV.

Mở notebook rồi chọn `Restart & Run All`. Chạy từ thư mục gốc hay từ `notebooks/` đều được; thời gian khoảng 1–2 phút. Hai cờ ở mục 1:

- `SAVE_ARTIFACTS`: `True` thì ghi mô hình, bảng và hình ra đĩa; `False` thì chỉ chạy thử.
- `RUN_FINAL_TEST`: `True` thì đánh giá baseline trên tập test (mục 11). Đặt `False` nếu muốn tập trung phần chấm test ở notebook 08. Notebook 02 vẫn xuất bảng điểm validation và lưu mô hình khi `SAVE_ARTIFACTS = True`.

## Notebook 02 tạo ra

- `models/baseline_linear_regression.joblib`, `models/baseline_metrics.csv`, `models/baseline_metadata.json`
- `outputs/baseline_error_analysis.csv`
- `outputs/baseline_model_comparison.xlsx` (file so sánh) và `outputs/baseline_comparison_merged.csv` (bảng gộp)
- `outputs/figures/baseline_*.png`
- Các dòng `baseline_*` trong `experiment_log.csv`; mỗi dòng có `experiment_id` cố định nên chạy lại sẽ ghi đè dòng cũ, không tạo dòng trùng.

Notebook 02 và 03 nên dùng cùng các fold, cùng hàm độ đo và cùng định dạng `experiment_id` (`<tên_thí_nghiệm>_cv5` cho validation, `<tên_thí_nghiệm>_test` cho test) để kết quả so sánh được với nhau. Chạy lại mục 13 của notebook 02 sau khi các mô hình khác ghi log theo quy ước này thì sheet `Nhat_ky_thuc_nghiem` tự gom chúng vào bảng xếp hạng.

## Chạy Notebook 03

**Điều kiện trước khi chạy:**

- Đã có file `data/processed/beijing_air_quality_standardized.csv` (được tạo từ Notebook 01).
- Đã cài đặt các thư viện trong `requirements.txt`.
- Môi trường đã có Jupyter Notebook hoặc `ipykernel`.

Mở file `03_random_forest.ipynb`, sau đó chọn **Restart & Run All** để chạy toàn bộ notebook.

Có thể chạy notebook từ thư mục gốc của dự án hoặc thư mục `notebooks/`. Notebook tự xác định đường dẫn dự án và sử dụng cùng quy trình chia dữ liệu theo thời gian, cùng 5-Fold Cross-Validation với Notebook 02 (Baseline), nhằm đảm bảo kết quả đánh giá giữa hai mô hình có thể so sánh công bằng.

## Các đầu ra được tạo bởi Notebook 03

Sau khi chạy thành công, notebook tạo hoặc cập nhật các tệp sau:

**1. Mô hình và thông tin cấu hình**

- `models/random_forest.joblib`: Mô hình Random Forest sau khi huấn luyện trên tập Train + Validation.
- `models/random_forest_metadata.json`: Thông tin cấu hình mô hình, kết quả đánh giá, thời gian chạy và thông tin các Fold.

**2. Kết quả đánh giá**

- `outputs/random_forest_cv_metrics.csv`: Các chỉ số MAE, RMSE, R² và thời gian chạy của từng Fold.
- `outputs/random_forest_cv_summary.csv`: Tổng hợp giá trị trung bình và độ lệch chuẩn của các chỉ số đánh giá.
- `outputs/random_forest_fold_overview.csv`: Thông tin tổng quan về dữ liệu Train và Validation của từng Fold.
- `outputs/random_forest_validation_oof_predictions.csv`: Lưu giá trị PM2.5 thực tế (`y_true`), giá trị dự đoán (`y_pred`) và sai số (`residual`) trên từng Fold Validation. Dữ liệu này được sử dụng để phân tích kết quả dự đoán và vẽ biểu đồ.

**3. Biểu đồ trực quan**

Các biểu đồ được xuất dưới định dạng PNG vào thư mục `outputs/figures/`:

- `random_forest_cv_rmse_by_fold.png`: RMSE theo từng Fold.
- `random_forest_cv_metrics_by_fold.png`: MAE, RMSE và R² theo từng Fold.
- `random_forest_feature_importance.png`: Mức độ quan trọng của các đặc trưng.
- `random_forest_pred_vs_actual.png`: So sánh giá trị PM2.5 thực tế và dự đoán.
- `random_forest_residuals.png`: Phân phối sai số dự đoán.

**4. Ghi nhận thí nghiệm**

Notebook ghi kết quả vào `experiment_log.csv` với `experiment_id` cố định là `random_forest_cv5`. Khi chạy lại, notebook cập nhật kết quả của thí nghiệm này thay vì tạo thêm dòng trùng lặp, đồng thời giữ lại các kết quả thí nghiệm khác.

## Nguyên tắc đảm bảo tính công bằng trong thực nghiệm

- Notebook 02 và Notebook 03 sử dụng cùng cách chia dữ liệu theo thời gian và cùng 5 Fold Cross-Validation.
- Sử dụng cùng cách tính các chỉ số MAE, RMSE và R² để đảm bảo tính nhất quán.
- Không sử dụng tập Test để lựa chọn mô hình hoặc tinh chỉnh siêu tham số.
- Các kết quả Cross-Validation chỉ được tính trên tập Train + Validation.
- Tập Test được giữ riêng để phục vụ đánh giá cuối cùng sau khi hoàn tất quá trình lựa chọn mô hình.

**Lưu ý:** File OOF chỉ lưu dự đoán trên các Fold Validation, không chứa kết quả dự đoán trên tập Test.

## Chạy Notebook 04

**Điều kiện trước khi chạy:**

- Có `data/processed/beijing_air_quality_standardized.csv` (từ notebook 01) và đã cài `requirements.txt`.
- Có `outputs/baseline_comparison_merged.csv` (notebook 02) và `outputs/random_forest_cv_metrics.csv` (notebook 03); thiếu một trong hai thì mục 8 báo lỗi `assert`. File `outputs/random_forest_validation_oof_predictions.csv` là tùy chọn (để so sánh sai số theo mùa/mức bụi).

Mở `04_gradient_boosting.ipynb` và chọn `Restart & Run All` (khoảng 40 giây cho 5 fold trên máy đã chạy thử). Hai cờ ở mục 1: `SAVE_ARTIFACTS` (ghi file hay chỉ chạy xem) và `SAVE_OOF` (lưu file dự đoán chi tiết khoảng 28 MB; đặt `False` nếu không muốn file nặng trong Git).

## Các đầu ra được tạo bởi Notebook 04

- `models/gradient_boosting.joblib`, `models/gradient_boosting_metadata.json`
- `outputs/gradient_boosting_cv_metrics.csv` (MAE, RMSE, R², `runtime_seconds`, `train_rows`, `validation_rows`, `train_rmse` theo fold), `outputs/gradient_boosting_cv_summary.csv`, `outputs/gradient_boosting_validation_oof_predictions.csv`
- 4 hình `outputs/figures/gradient_boosting_*.png`
- Dòng `gradient_boosting_cv5` trong `experiment_log.csv` (chạy lại thì thay thế dòng cũ, không tạo dòng trùng).

Notebook 04 theo cùng nguyên tắc công bằng như notebook 02 và 03: cùng 5 fold, cùng hàm độ đo, không dùng tập Test để chọn mô hình hay tinh chỉnh. Mục 15 của notebook là phần kết luận phải điền bằng số in ra khi chạy.

## Chạy Notebook 05

**Điều kiện trước khi chạy:**

- Có `data/processed/beijing_air_quality_standardized.csv` (từ notebook 01) và đã cài `requirements.txt`.
- Có `outputs/random_forest_cv_metrics.csv` (notebook 03) và `outputs/gradient_boosting_cv_metrics.csv` (notebook 04) để mục 8 so sánh trước và sau tinh chỉnh. Notebook 05 đọc các kết quả trước đó từ `experiment_log.csv` khi file đã có.

Mở `05_tuning.ipynb` và chọn `Restart & Run All`. Chạy rất lâu (ước tính khoảng 15 phút cho Gradient Boosting và khoảng 30 phút trở lên cho Random Forest với cấu hình mặc định). Các cờ ở mục 1:

- `SAVE_ARTIFACTS`: ghi file hay chỉ chạy xem.
- `SAVE_OOF`: lưu dự đoán từng dòng của mô hình đã tinh chỉnh (khoảng 28 MB mỗi mô hình); mặc định tắt.
- `TUNE_GRADIENT_BOOSTING`, `TUNE_RANDOM_FOREST`: bật/tắt từng mô hình.
- `N_ITER_GB` (mặc định 20), `N_ITER_RF` (mặc định 8): số bộ tham số ngẫu nhiên thử cho mỗi mô hình. Có thể đặt 2 để chạy thử nhanh; kết quả của lần chạy thử không dùng cho báo cáo.

Nếu mục 8 báo thiếu file kết quả, lấy file từ nhánh có notebook 03 hoặc 04, hoặc chạy lại notebook đó.

## Các đầu ra được tạo bởi Notebook 05

- `models/gradient_boosting_tuned.joblib`, `models/random_forest_tuned.joblib`: pipeline của bộ tham số tốt nhất, fit trên toàn bộ Train/Validation (không dùng Test).
- `models/gradient_boosting_tuned_metadata.json`, `models/random_forest_tuned_metadata.json`: tham số tốt nhất, khoảng tìm kiếm, số bộ tham số đã thử (`n_iter`), hạt giống, phiên bản thư viện, `test_evaluated: false`.
- `outputs/gradient_boosting_tuned_cv_metrics.csv`, `outputs/random_forest_tuned_cv_metrics.csv` (MAE, RMSE, R², `runtime_seconds`, `train_rows`, `validation_rows`, `train_rmse` theo fold) và `outputs/*_tuned_cv_summary.csv` (trung bình và độ lệch chuẩn).
- `outputs/tuning_gradient_boosting_search_results.csv`, `outputs/tuning_random_forest_search_results.csv`: bảng toàn bộ các bộ tham số đã thử, gồm RMSE từng fold, RMSE trung bình 5 fold, RMSE trung bình fold 2-5 và thời gian huấn luyện.
- `outputs/*_tuned_validation_oof_predictions.csv`: dự đoán từng dòng trên các fold validation, chỉ có khi `SAVE_OOF = True`.
- `outputs/figures/tuning_rmse_by_fold.png`: RMSE theo fold, trước và sau tinh chỉnh.
- Hai dòng `gradient_boosting_tuned_cv5` và `random_forest_tuned_cv5` trong `experiment_log.csv` (chạy lại thì thay thế dòng cũ, không tạo dòng trùng).

Notebook 05 không ghi đè kết quả "trước tinh chỉnh" của notebook 03 và 04. Mục 11 của notebook là phần kết luận phải điền bằng số in ra khi chạy thật.

## Chạy notebook 06 và 07

- Chạy notebook 06 với CSV chuẩn hóa từ notebook 01 và `experiment_log.csv` đã có. Các bảng điểm từ notebook 02–04 giúp biểu đồ hiển thị thêm các mô hình đối chiếu. Bật `SAVE_ARTIFACTS = True` ở mục 9 để lưu `models/mlp.joblib`, metadata, bảng CV, bảng sai số theo nhóm và các biểu đồ `mlp_*.png`. `SAVE_OOF` điều khiển việc xuất CSV dự đoán chi tiết. Mã nhật ký là `mlp_cv5`.
- Notebook 07 lấy mẫu 8 tổ hợp cho `hidden_layer_sizes`, `learning_rate_init`, `alpha`, `batch_size` và `max_iter`. Mỗi tổ hợp chạy trên cùng 5 fold. Notebook đọc `outputs/mlp_cv_metrics.csv` nếu phù hợp, hoặc tính lại kết quả MLP gốc để so sánh.
- Khi `SAVE_ARTIFACTS = True`, notebook 07 lưu `models/mlp_tuned.joblib`, `models/mlp_tuned_metadata.json`, `outputs/tuning_mlp_search_results.csv`, `outputs/mlp_tuned_cv_metrics.csv`, `outputs/mlp_tuned_cv_summary.csv` và `outputs/figures/mlp_tuning_rmse_by_fold.png`. Tệp `outputs/mlp_tuned_validation_oof_predictions.csv` được xuất khi `SAVE_OOF = True`. Mã nhật ký là `mlp_tuned_cv5`.

## Chạy notebook 08

1. Kiểm tra CSV chuẩn hóa từ notebook 01 và bốn mô hình đã lưu. Linear Regression đến từ notebook 02, hai mô hình cây đã tinh chỉnh đến từ notebook 05, MLP đã tinh chỉnh đến từ notebook 07. Tên file được liệt kê trong [`models/README.md`](../models/README.md).
2. Mở notebook 08 và chạy các ô từ đầu đến cuối. Notebook đọc 27 đặc trưng, nạp mô hình để dự đoán và tính MAE, RMSE, R² trên 51.063 mẫu có nhãn từ 01/09/2016 đến 28/02/2017. Persistence được tính trực tiếp từ PM2.5 giờ hiện tại, dùng trung vị train + validation khi thiếu giá trị.
3. Nếu Linear Regression nằm ở nơi khác, chỉnh `LINEAR_MODEL_PATH` ở ô đầu. Nếu repo mới clone chưa có `models/baseline_linear_regression.joblib`, lưu mô hình từ notebook 02 rồi chạy notebook 08.
4. Với `SAVE_ARTIFACTS = True`, notebook 08 ghi `outputs/final_test_metrics.csv`, `outputs/figures/final_test_rmse.png` và cập nhật 5 mã `*_test` trong `experiment_log.csv` theo `experiment_id`.

## Bộ notebook chưa chạy trong `notebooks_unexecuted/`

Thư mục [`notebooks_unexecuted/`](../notebooks_unexecuted/) nằm ở thư mục gốc của repo. Các file bên dưới đã được xóa output và số thứ tự chạy của các ô.

- [`01_eda_and_preprocessing.ipynb`](../notebooks_unexecuted/01_eda_and_preprocessing.ipynb)
- [`02_model_training_baseline.ipynb`](../notebooks_unexecuted/02_model_training_baseline.ipynb)
- [`03_random_forest.ipynb`](../notebooks_unexecuted/03_random_forest.ipynb)
- [`04_gradient_boosting.ipynb`](../notebooks_unexecuted/04_gradient_boosting.ipynb)
- [`05_tuning.ipynb`](../notebooks_unexecuted/05_tuning.ipynb)
- [`06_mlp_regression.ipynb`](../notebooks_unexecuted/06_mlp_regression.ipynb)
- [`07_mlp_tuning.ipynb`](../notebooks_unexecuted/07_mlp_tuning.ipynb)
- [`08_final_evaluation.ipynb`](../notebooks_unexecuted/08_final_evaluation.ipynb)

Mở repo từ thư mục gốc trong VS Code và chạy lần lượt 01 → 08. Các notebook dùng cùng dữ liệu trong `data/`, cùng pipeline trong `src/` và lưu kết quả vào các thư mục chung `models/`, `outputs/`.
