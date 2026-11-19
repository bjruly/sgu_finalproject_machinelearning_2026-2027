# Thực nghiệm 02 — Các mô hình với cấu hình ban đầu

So sánh Random Forest, Gradient Boosting và MLP khi dự báo PM2.5 trước 1 giờ. Cả ba được đánh giá trên cùng 5 fold validation theo thời gian. Tổng số mẫu validation qua các fold là 300.696 cho mỗi mô hình. Nguồn thực nghiệm gồm [notebook 03](../../../notebooks/03_random_forest.ipynb), [notebook 04](../../../notebooks/04_gradient_boosting.ipynb) và [notebook 06](../../../notebooks/06_mlp_regression.ipynb).

| Tệp hoặc thư mục | Nội dung |
| --- | --- |
| [`danh_gia.xlsx`](danh_gia.xlsx) | Điểm trung bình (`Tong_hop`), điểm từng fold (`Theo_fold`) và đối chiếu baseline (`So_sanh`). |
| `ket_qua_tong_hop.csv` | MAE, RMSE, R² trung bình, độ lệch chuẩn và số mẫu validation. |
| `ket_qua_theo_fold.csv` | Điểm từng fold, số mẫu train và số mẫu validation. |
| `ket_qua_goc/` | CSV gốc về điểm CV, dự đoán từng mẫu validation (OOF), thông tin fold Random Forest và sai số theo nhóm của MLP. |
| `figures/` | Biểu đồ gốc về kết quả theo fold, dự đoán so với thực tế, sai số và độ quan trọng đặc trưng. |
| `models/` | Ba mô hình cấu hình ban đầu đã lưu và metadata. |

Bảng tổng hợp là trung bình cộng điểm của 5 fold từ các tệp `*_cv_metrics.csv`, được đối chiếu với `experiment_log.csv`. [Bảng gốc từ notebook](../../notebooks/tables/) được sao vào `ket_qua_goc/`. Ba file OOF lưu giá trị thực tế và dự đoán của từng mẫu validation.

## So sánh với các thực nghiệm trước

Sheet `So_sanh` đối chiếu ba cấu hình ban đầu với Persistence và Linear Regression từ [thực nghiệm 01](../experiments01/README.md). Các bảng dùng cùng 5 fold validation. Chênh lệch RMSE âm cho biết mô hình có RMSE thấp hơn mốc đối chiếu.
