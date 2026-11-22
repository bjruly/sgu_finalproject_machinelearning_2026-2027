# Thư mục `outputs`

| Thư mục | Nội dung |
| --- | --- |
| [`eda/`](eda/README.md) | Kết luận và nhật ký khảo sát dữ liệu 12 trạm |
| [`notebooks/tables/`](notebooks/tables/) | Bảng CSV và Excel do notebook xuất |
| [`notebooks/figures/`](notebooks/figures/README.md) | Biểu đồ PNG do notebook xuất |
| [`experiments/`](experiments/) | Hồ sơ nhóm tổng hợp theo từng đợt, có bảng đánh giá Excel và tệp đối chiếu |

## Bảng kết quả và phân tích

Các bảng dưới đây nằm trong [`notebooks/tables/`](notebooks/tables/).
- `baseline_error_analysis.csv` lưu sai số baseline theo trạm, mùa và mức PM2.5. `baseline_comparison_merged.csv` và `baseline_model_comparison.xlsx` lưu bảng so sánh của notebook 02.
- `random_forest_cv_metrics.csv` và `gradient_boosting_cv_metrics.csv` lưu điểm từng fold của các cấu hình gốc. Các file `*_cv_summary.csv` lưu trung bình và độ lệch chuẩn.
- `random_forest_fold_overview.csv` ghi thông tin các fold. Các tệp `*_validation_oof_predictions.csv`, nếu được xuất, lưu dự đoán theo từng mẫu validation.
- `mlp_cv_metrics.csv`, `mlp_cv_summary.csv` và `mlp_error_by_group.csv` lưu điểm và phân tích sai số của MLP gốc từ notebook 06.
- `tuning_*_search_results.csv` lưu các tổ hợp đã thử. `*_tuned_cv_metrics.csv` và `*_tuned_cv_summary.csv` lưu điểm sau tinh chỉnh từ notebook 05 và 07.

## Hồ sơ thực nghiệm

| Hồ sơ | Notebook nguồn | Đánh giá |
| --- | --- | --- |
| [`experiments01/`](experiments/experiments01/README.md) | 02 | Baseline trên 5 fold validation |
| [`experiments02/`](experiments/experiments02/README.md) | 03, 04, 06 | Cấu hình ban đầu, so với thực nghiệm 01 |
| [`experiments03/`](experiments/experiments03/README.md) | 05, 07 | Cấu hình tinh chỉnh, so với thực nghiệm 01 và 02 |
| [`final_test/`](experiments/final_test/README.md) | 08 | Đánh giá cuối trên 51.063 mẫu test |

Mỗi hồ sơ có `danh_gia.xlsx` và các kết quả kèm theo. Khi chạy lại notebook, các tệp được ghi vào thư mục đầu ra chung và nhật ký ở gốc. Nếu muốn cập nhật hồ sơ, nhóm cần đối chiếu lại các bản sao và bảng Excel của đợt tương ứng.

## Kết quả test

- [`final_test_metrics.csv`](notebooks/tables/final_test_metrics.csv) lưu hạng, MAE, RMSE, R² và số mẫu test cho 5 mô hình. Tập test có 51.063 mẫu, với nhãn từ 01/09/2016 đến 28/02/2017.
- [`notebooks/figures/final_test_rmse.png`](notebooks/figures/final_test_rmse.png) là biểu đồ so sánh RMSE test.
- [`experiment_log.csv`](../experiment_log.csv) nằm ở thư mục gốc. Notebook 08 cập nhật dòng có đuôi `_test` theo mã thí nghiệm.

## Tệp được notebook sau đọc lại

- Notebook 04 đọc `baseline_comparison_merged.csv` và `random_forest_cv_metrics.csv`. Nếu có `random_forest_validation_oof_predictions.csv`, notebook dùng thêm để so sánh sai số theo mùa và mức bụi.
- Notebook 05 đọc `random_forest_cv_metrics.csv` và `gradient_boosting_cv_metrics.csv` để so sánh trước và sau tinh chỉnh.
- Notebook 06 dùng bảng baseline và các bảng điểm Random Forest, Gradient Boosting nếu có để vẽ biểu đồ đối chiếu.
- Notebook 07 ưu tiên đọc `mlp_cv_metrics.csv` để đối chiếu MLP gốc. Mô hình `.joblib` dùng ở notebook 08 nằm trong [`models/`](../models/README.md).
