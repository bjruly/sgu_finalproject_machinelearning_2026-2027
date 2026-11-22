# Đánh giá cuối trên tập test

So sánh 5 mô hình trên cùng 51.063 mẫu test, từ tháng 09/2016 đến tháng 02/2017. [Notebook 08](../../../notebooks/08_final_evaluation.ipynb) dùng Persistence, Linear Regression và các cấu hình đã tinh chỉnh của Random Forest, Gradient Boosting và MLP. Bảng xếp hạng theo RMSE test.

| Tệp hoặc thư mục | Nội dung |
| --- | --- |
| [`danh_gia.xlsx`](danh_gia.xlsx) | Sheet `Tong_hop` lưu bảng xếp hạng, MAE, RMSE, R², số mẫu và mức giảm RMSE của mô hình đứng đầu so với Persistence. |
| [`final_test_metrics.csv`](final_test_metrics.csv) | Bản sao [bảng kết quả gốc](../../notebooks/tables/final_test_metrics.csv) của notebook 08. |
| [`figures/final_test_rmse.png`](figures/final_test_rmse.png) | Bản sao [biểu đồ gốc](../../notebooks/figures/final_test_rmse.png) so sánh RMSE test của 5 mô hình. |

Random Forest đã tinh chỉnh đứng đầu với RMSE 20,9613 µg/m³, giảm 9,31% so với Persistence. Notebook 08 nạp pipeline từ [`models/` tại gốc đồ án](../../../models/README.md). Các bản sao của Linear Regression và ba cấu hình đã tinh chỉnh được lưu lần lượt ở [thực nghiệm 01](../experiments01/models/) và [thực nghiệm 03](../experiments03/models/). Persistence được tính từ PM2.5 giờ hiện tại. Các dòng có đuôi `_test` được ghi trong [nhật ký thực nghiệm](../../../experiment_log.csv).

## Phân tích bổ sung có thể tái lập

Chạy python -m src.evaluation hoặc phần phân tích mới của notebook 08. Thư mục analysis/ lưu predictions từng mẫu, lỗi theo trạm/tháng/mùa/mức PM2.5, worst cases, hình và manifest. final_test_metrics_reproduced.csv được đối chiếu với bảng điểm gốc; không thay đổi cấu hình mô hình theo test.

paired_model_uncertainty.csv ghi chênh lệch RMSE model_a - model_b và khoảng percentile 95% từ bootstrap ghép cặp, khối 7 ngày, giữ toàn bộ trạm cùng thời điểm trong cùng khối. Số âm nghĩa model_a có RMSE thấp hơn. Khoảng này không khái quát hóa sang mọi mùa hoặc trạm mới.

Nhóm nồng độ đóng bên phải; residual = y_true - y_pred. Giữ quy tắc phân nhóm khi so sánh bảng, đặc biệt với các bảng notebook cũ có thể dùng quy tắc biên khác.

## Đồng bộ từ nguồn notebook

CSV/XLSX tổng hợp hiện hành được tạo bằng scripts/refresh_experiment_tables.py sau khi scripts/verify_result_sources.py kiểm tra nguồn. Các bản sao ket_qua_goc và figures được đồng bộ từ outputs/notebooks; nguồn gốc tra trong outputs/notebooks/tables/report_sources.csv.

Các model lưu theo đợt và thư mục Experimental Log là hồ sơ trước đó, không bị đổi thành lần huấn luyện mới. Khi viết báo cáo, dùng bảng hiện hành có mã ô notebook; không trộn số nhóm cũ khác quy tắc biên.
