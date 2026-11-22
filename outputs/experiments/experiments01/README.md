# Thực nghiệm 01 — Các mô hình cơ bản

So sánh Persistence và Linear Regression khi dự báo PM2.5 trước 1 giờ. Hai mô hình được đánh giá trên cùng 5 fold validation theo thời gian, với tổng cộng 300.696 mẫu validation qua các fold. Số liệu lấy từ [notebook 02](../../../notebooks/02_model_training_baseline.ipynb) và các tệp đã xuất trong đồ án.

## Các tệp trong thư mục

| Tệp hoặc thư mục              | Nội dung                                                                                                                                                               | Nguồn                                                                                                                               |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [`danh_gia.xlsx`](danh_gia.xlsx) | Sheet `Tong_hop` lưu điểm trung bình, sheet `Theo_fold` lưu điểm từng fold.                                                                                 | Tổng hợp từ các bảng CSV của đồ án.                                                                                         |
| `ket_qua_tong_hop.csv`          | MAE, RMSE, R² trung bình 5 fold, độ lệch chuẩn và số mẫu của mỗi mô hình.                                                                                  | Điểm trung bình từ `experiment_log.csv`. Độ lệch chuẩn và số mẫu từ `outputs/notebooks/tables/baseline_metrics.csv`. |
| `ket_qua_theo_fold.csv`         | Điểm và chênh lệch giữa hai mô hình ở từng fold.                                                                                                              | Các dòng `scope=cv_fold` từ `outputs/notebooks/tables/baseline_comparison_merged.csv`.                                        |
| `baseline_error_analysis.csv`   | Sai số validation theo trạm, mùa và mức PM2.5.                                                                                                                     | [Bảng gốc từ notebook 02](../../notebooks/tables/baseline_error_analysis.csv).                                                     |
| `figures/`                      | 8 biểu đồ về RMSE theo fold và theo tháng, sai số theo nhóm, dự đoán so với thực tế, residual, chuỗi ví dụ, hệ số và độ quan trọng đặc trưng. | Các PNG gốc của notebook 02 trong `outputs/notebooks/figures/`.                                                                 |
| `models/`                       | Pipeline Linear Regression đã lưu và metadata của mô hình.                                                                                                       | Các tệp gốc trong `models/`.                                                                                                    |

Persistence là quy tắc lấy PM2.5 hiện tại làm giá trị dự báo, với trung vị nhãn train làm giá trị dự phòng. Pipeline Linear Regression được fit trên train + validation để lưu lại. Điểm trong bảng là kết quả validation tính từ các lần fit riêng theo từng fold.

Notebook 02 dùng các dự đoán từng mẫu trong bộ nhớ để tính sai số và vẽ hình. Bản nguồn chỉ xuất các bảng tổng hợp và biểu đồ từ những dự đoán đó.

Hai baseline là mốc đối chiếu của [thực nghiệm 02](../experiments02/README.md) và [thực nghiệm 03](../experiments03/README.md). Điểm trên tập test được ghi riêng trong [hồ sơ đánh giá cuối](../final_test/README.md).

## Đồng bộ từ nguồn notebook

CSV/XLSX tổng hợp hiện hành được tạo bằng scripts/refresh_experiment_tables.py sau khi scripts/verify_result_sources.py kiểm tra nguồn. Các bản sao ket_qua_goc và figures được đồng bộ từ outputs/notebooks; nguồn gốc tra trong outputs/notebooks/tables/report_sources.csv.

Các model lưu theo đợt và thư mục Experimental Log là hồ sơ trước đó, không bị đổi thành lần huấn luyện mới. Khi viết báo cáo, dùng bảng hiện hành có mã ô notebook; không trộn số nhóm cũ khác quy tắc biên.
