# Đánh giá cuối trên tập test

So sánh 5 mô hình trên cùng 51.063 mẫu test, từ tháng 09/2016 đến tháng 02/2017. [Notebook 08](../../../notebooks/08_final_evaluation.ipynb) dùng Persistence, Linear Regression và các cấu hình đã tinh chỉnh của Random Forest, Gradient Boosting và MLP. Bảng xếp hạng theo RMSE test.

| Tệp hoặc thư mục | Nội dung |
| --- | --- |
| [`danh_gia.xlsx`](danh_gia.xlsx) | Sheet `Tong_hop` lưu bảng xếp hạng, MAE, RMSE, R², số mẫu và mức giảm RMSE của mô hình đứng đầu so với Persistence. |
| [`final_test_metrics.csv`](final_test_metrics.csv) | Bản sao [bảng kết quả gốc](../../notebooks/tables/final_test_metrics.csv) của notebook 08. |
| [`figures/final_test_rmse.png`](figures/final_test_rmse.png) | Bản sao [biểu đồ gốc](../../notebooks/figures/final_test_rmse.png) so sánh RMSE test của 5 mô hình. |

Random Forest đã tinh chỉnh đứng đầu với RMSE 20,9613 µg/m³, giảm 9,31% so với Persistence. Notebook 08 nạp pipeline từ [`models/` tại gốc đồ án](../../../models/README.md). Các bản sao của Linear Regression và ba cấu hình đã tinh chỉnh được lưu lần lượt ở [thực nghiệm 01](../experiments01/models/) và [thực nghiệm 03](../experiments03/models/). Persistence được tính từ PM2.5 giờ hiện tại. Các dòng có đuôi `_test` được ghi trong [nhật ký thực nghiệm](../../../experiment_log.csv).
