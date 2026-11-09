# Thư mục `outputs/figures`

Nơi lưu biểu đồ EDA, hình trực quan hóa dữ liệu, biểu đồ đánh giá mô hình và các hình ảnh kết quả khác.

## Tệp hiện có

Tám hình sau do [`02_model_training_baseline.ipynb`](../../notebooks/02_model_training_baseline.ipynb) tạo ra. Các hình về sai số đều tính trên dự đoán out-of-fold của 5 fold validation, không dùng test.

| Tệp                                       | Nội dung                                                                                                              |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `baseline_cv_rmse_by_fold.png`           | RMSE validation của Persistence và Linear Regression theo từng fold expanding-window.                               |
| `baseline_error_by_group.png`            | RMSE theo trạm, theo mùa và theo mức PM2.5 thực tế.                                                              |
| `baseline_pred_vs_actual.png`            | Dự đoán so với thực tế (hexbin, thang log; trục giới hạn 0–500 µg/m³ để dễ nhìn).                      |
| `baseline_residuals.png`                 | Phân bố residual (thực tế − dự đoán) và residual trung bình theo mức PM2.5.                                 |
| `baseline_timeseries_example.png`        | Chuỗi thời gian ±72 giờ quanh đỉnh PM2.5 lớn nhất của fold cuối (thực tế, Persistence, Linear Regression). |
| `baseline_rmse_by_month.png`             | RMSE theo tháng trên vùng validation, kèm PM2.5 thực tế trung bình của tháng.                                 |
| `baseline_lr_coefficients.png`           | Hệ số của các feature số trong Linear Regression (đã chuẩn hóa).                                              |
| `baseline_lr_permutation_importance.png` | Permutation importance theo nhóm feature của Linear Regression (một fold, mẫu 30.000 dòng).                       |

- `.gitkeep`: tệp rỗng giúp Git lưu thư mục.

## Lưu ý

- Chạy lại notebook 02 với `SAVE_ARTIFACTS = True` sẽ ghi đè các tệp `baseline_*.png`.
- Hình của các mô hình cây và hình phân tích cuối trên tập test chưa có trong thư mục này.


# Hình Random Forest – Notebook 03

Sau khi chạy [`03_advanced_models_and_tuning.ipynb`](../../notebooks/03_advanced_models_and_tuning.ipynb) với `SAVE_ARTIFACTS = True`, có thêm 5 hình:

| Tệp                                     | Nội dung                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| `random_forest_cv_rmse_by_fold.png`    | RMSE trên validation của từng fold.                                    |
| `random_forest_cv_metrics_by_fold.png` | MAE, RMSE và R² theo từng validation fold.                             |
| `random_forest_feature_importance.png` | Top 20 feature importance từ mô hình cuối fit trên Train/Validation. |
| `random_forest_pred_vs_actual.png`     | Actual vs Predicted trên validation OOF của 5 folds.                    |
| `random_forest_residuals.png`          | Phân bố residual (thực tế − dự đoán) trên validation OOF.        |

Bốn hình đầu tiên liên quan đến kết quả validation OOF (trừ Feature Importance, lấy từ mô hình cuối fit trên Train/Validation); không hình nào sử dụng nhãn Test.

## Lưu ý

- Chạy lại Notebook 02 hoặc 03 với `SAVE_ARTIFACTS = True` sẽ cập nhật các hình có tiền tố tương ứng.
- `.gitkeep` giúp Git lưu thư mục ngay cả khi chưa có hình.
