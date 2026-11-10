# Thư mục `outputs`

Nơi lưu các sản phẩm được tạo ra trong quá trình phân tích, huấn luyện và kiểm thử, không phải mã nguồn đầu vào.

## Thư mục con

- [`eda/`](eda/README.md): kết luận và kết quả khám phá dữ liệu.
- [`figures/`](figures/README.md): biểu đồ và hình ảnh trực quan hóa; hiện có hình của baseline (notebook 02), Random Forest (notebook 03) và Gradient Boosting (notebook 04).
- `test_reports/`: báo cáo kết quả kiểm thử; hiện chưa có báo cáo nào được sinh ra.

## Tệp ở cấp thư mục

- `baseline_error_analysis.csv`: sai số của hai baseline (Persistence và Linear Regression) trên dự đoán out-of-fold của 5 fold validation, không dùng test. Tạo bởi [`02_model_training_baseline.ipynb`](../notebooks/02_model_training_baseline.ipynb). Mỗi dòng là một nhóm × một mô hình, gồm các cột:

  - `group_type`: loại nhóm, gồm `station` (12 trạm), `season` (Xuân/Hè/Thu/Đông theo tháng) và `pm25_level` (mức PM2.5 thực tế: 0–35, 35–75, 75–115, 115–150, 150–250, >250).
  - `group`, `model`, `n`: tên nhóm, tên mô hình và số dòng trong nhóm.
  - `mae`, `rmse`, `r2`: độ đo của nhóm đó. R² trong nhóm hẹp như `pm25_level` ít ý nghĩa, nên với nhóm này hãy nhìn MAE, RMSE và `mean_residual`.
  - `mean_residual`: trung bình của (thực tế − dự đoán); **dương** nghĩa là mô hình dự đoán thấp hơn thực tế.
- `baseline_model_comparison.xlsx`: file Excel **so sánh kết quả thực nghiệm** của Persistence và Linear Regression để đưa vào báo cáo, do mục 13 của notebook 02 tạo ra bằng các phép `merge`. Gồm các sheet `Tong_quan` (validation và test, kèm kết luận tự động), `Theo_fold`, `Theo_tram`, `Theo_mua`, `Theo_muc_PM25`, `Test_theo_thang` (chỉ có khi `RUN_FINAL_TEST = True`), `Nhat_ky_thuc_nghiem` (bảng xếp hạng gộp từ `experiment_log.csv`) và `Ghi_chu`; có biểu đồ. Cần `openpyxl` để tạo. Không sửa tay vì chạy lại notebook sẽ ghi đè.
- `baseline_comparison_merged.csv`: toàn bộ các bảng đã merge trong một bảng dài (cột `scope`, `group`, `n` và các cột `mae_*`, `rmse_*`, `r2_*`; `_P` là Persistence, `_LR` là Linear Regression, `_diff` = LR − P, `_rel` là chênh lệch tương đối, `_better` là mô hình tốt hơn). Lưu bằng `utf-8-sig`.

Tệp CSV `baseline_error_analysis.csv` lưu bằng `utf-8-sig` để Excel hiển thị đúng tiếng Việt. Chạy lại notebook 02 sẽ ghi đè tệp.

Kết luận dạng bảng của EDA nằm trong [`eda/eda_conclusions.csv`](eda/eda_conclusions.csv); diễn giải từng bước, các quyết định và việc còn bỏ ngỏ được ghi trong [`eda/eda_worklog.md`](eda/eda_worklog.md).


## Kết quả Random Forest (Notebook 03)

Sau khi chạy [`03_advanced_models_and_tuning.ipynb`](../notebooks/03_advanced_models_and_tuning.ipynb) với `SAVE_ARTIFACTS = True`, các tệp sau được tạo/cập nhật ở cấp `outputs/`:

| Tệp                                             | Nội dung                                                                                                                |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `random_forest_cv_metrics.csv`                 | MAE, RMSE, R², runtime_seconds, train_rows và validation_rows cho từng fold.                                          |
| `random_forest_cv_summary.csv`                 | Trung bình và độ lệch chuẩn của MAE, RMSE, R² qua 5 folds.                                                       |
| `random_forest_fold_overview.csv`              | Khoảng thời gian và số dòng train/validation của từng fold.                                                       |
| `random_forest_validation_oof_predictions.csv` | Dự đoán OOF validation gồm fold, station, datetime, target_datetime, y_true, y_pred và residual. Không chứa Test. |

Các CSV được ghi bằng `utf-8-sig` để thuận tiện mở bằng Excel. Chạy lại Notebook 03 sẽ cập nhật các tệp cùng tên.

## Nhật ký thực nghiệm

Notebook 03 cập nhật `experiment_log.csv` ở thư mục gốc repository bằng bản ghi `random_forest_cv5`, sử dụng trung bình metrics của 5 validation folds. Nếu bản ghi cùng `experiment_id` đã tồn tại, notebook thay thế bản ghi đó và giữ nguyên các dòng baseline khác.

Sau khi Notebook 03 ghi log, có thể chạy lại mục 13 của Notebook 02 để workbook so sánh baseline tổng hợp thêm kết quả Random Forest từ `experiment_log.csv`. Workbook baseline hiện tại không tự cập nhật chỉ vì Notebook 03 chạy.

## Nguyên tắc sử dụng kết quả

- OOF predictions chỉ là dự đoán trên các validation folds, dùng cho phân tích sai số và trực quan hóa.
- Notebook 03 không dự đoán hoặc đánh giá Test; không dùng Test để chọn cấu hình hay tuning.
- Hình PNG do Notebook 03 tạo được mô tả tại [`figures/README.md`](figures/README.md).

## Kết quả Gradient Boosting (Notebook 04)

Sau khi chạy [`04_gradient_boosting.ipynb`](../notebooks/04_gradient_boosting.ipynb) với `SAVE_ARTIFACTS = True`, các tệp sau được tạo/cập nhật ở cấp `outputs/`:

| Tệp | Nội dung |
| --- | --- |
| `gradient_boosting_cv_metrics.csv` | MAE, RMSE, R², `runtime_seconds`, `train_rows`, `validation_rows` và `train_rmse` (RMSE trên chính phần train, dùng kiểm tra overfit) cho từng fold. |
| `gradient_boosting_cv_summary.csv` | Trung bình và độ lệch chuẩn của MAE, RMSE, R² qua 5 fold. |
| `gradient_boosting_validation_oof_predictions.csv` | Dự đoán OOF validation: fold, station, datetime, target_datetime, y_true, y_pred, residual. Không chứa Test. Khoảng 28 MB; đặt `SAVE_OOF = False` để không ghi. |

Notebook 04 ghi bản ghi `gradient_boosting_cv5` vào `experiment_log.csv` (thay thế bản ghi cùng `experiment_id`, giữ nguyên các dòng khác). Workbook baseline không tự cập nhật; muốn đưa Random Forest và Gradient Boosting vào bảng xếp hạng, chạy lại mục 13 của Notebook 02.

Như Random Forest, notebook 04 không dự đoán hoặc đánh giá Test, và không dùng Test để chọn cấu hình.
