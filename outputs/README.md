# Thư mục `outputs`

Nơi lưu bảng kết quả, phân tích sai số, nhật ký EDA và biểu đồ. Danh sách ảnh nằm trong [`figures/README.md`](figures/README.md).

## Bảng kết quả và phân tích

- [`eda/`](eda/README.md) chứa nhật ký và kết luận khảo sát dữ liệu của 12 trạm.
- `baseline_error_analysis.csv` lưu sai số baseline theo trạm, mùa và mức PM2.5. `baseline_comparison_merged.csv` và `baseline_model_comparison.xlsx` lưu bảng so sánh của notebook 02.
- `random_forest_cv_metrics.csv` và `gradient_boosting_cv_metrics.csv` lưu điểm từng fold của các cấu hình gốc. Các file `*_cv_summary.csv` lưu trung bình và độ lệch chuẩn.
- `random_forest_fold_overview.csv` ghi thông tin các fold. Các tệp `*_validation_oof_predictions.csv`, nếu được xuất, lưu dự đoán theo từng mẫu validation.
- `mlp_cv_metrics.csv`, `mlp_cv_summary.csv` và `mlp_error_by_group.csv` lưu điểm và phân tích sai số của MLP gốc từ notebook 06.
- `tuning_*_search_results.csv` lưu các tổ hợp đã thử. `*_tuned_cv_metrics.csv` và `*_tuned_cv_summary.csv` lưu điểm sau tinh chỉnh từ notebook 05 và 07.

## Kết quả test

- [`final_test_metrics.csv`](final_test_metrics.csv) lưu hạng, MAE, RMSE, R² và số mẫu test cho 5 mô hình. Tập test có 51.063 mẫu, với nhãn từ 01/09/2016 đến 28/02/2017.
- [`figures/final_test_rmse.png`](figures/final_test_rmse.png) là biểu đồ so sánh RMSE test.
- [`experiment_log.csv`](../experiment_log.csv) nằm ở thư mục gốc. Notebook 08 cập nhật dòng có đuôi `_test` theo mã thí nghiệm.

## Tệp được notebook sau đọc lại

- Notebook 04 đọc `baseline_comparison_merged.csv` và `random_forest_cv_metrics.csv`. Nếu có `random_forest_validation_oof_predictions.csv`, notebook dùng thêm để so sánh sai số theo mùa và mức bụi.
- Notebook 05 đọc `random_forest_cv_metrics.csv` và `gradient_boosting_cv_metrics.csv` để so sánh trước và sau tinh chỉnh.
- Notebook 06 dùng bảng baseline và các bảng điểm Random Forest, Gradient Boosting nếu có để vẽ biểu đồ đối chiếu.
- Notebook 07 ưu tiên đọc `mlp_cv_metrics.csv` để đối chiếu MLP gốc. Mô hình `.joblib` dùng ở notebook 08 nằm trong [`models/`](../models/README.md).
