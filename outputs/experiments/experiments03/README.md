# Thực nghiệm 03 — So sánh trước và sau tinh chỉnh

So sánh cấu hình ban đầu và cấu hình đã tinh chỉnh của Random Forest, Gradient Boosting và MLP trên cùng 5 fold validation theo thời gian. [Notebook 05](../../../notebooks/05_tuning.ipynb) thực hiện tìm kiếm cho hai mô hình cây. [Notebook 07](../../../notebooks/07_mlp_tuning.ipynb) thực hiện tìm kiếm cho MLP. RandomizedSearchCV thử lần lượt 8 tổ hợp cho Random Forest, 20 tổ hợp cho Gradient Boosting và 8 tổ hợp cho MLP. Tiêu chí chọn cấu hình là RMSE trung bình thấp nhất qua 5 fold.

| Tệp hoặc thư mục | Nội dung |
| --- | --- |
| [`danh_gia.xlsx`](danh_gia.xlsx) | Điểm trước và sau tinh chỉnh (`Tong_hop`), điểm từng fold (`Theo_fold`) và so sánh với các đợt trước (`So_sanh`). |
| `ket_qua_tong_hop.csv` | Điểm trung bình, độ lệch chuẩn và số mẫu của cả 6 cấu hình. |
| `ket_qua_theo_fold.csv` | Điểm của từng cấu hình theo fold, số mẫu train và validation. |
| `ket_qua_goc/` | CSV gốc về điểm CV sau tinh chỉnh và toàn bộ điểm của các tổ hợp đã thử. |
| `figures/` | Hai biểu đồ gốc so sánh RMSE trước và sau tinh chỉnh. |
| `models/` | Ba mô hình đã tinh chỉnh được lưu và metadata đầy đủ. |

Số liệu cấu hình ban đầu lấy từ notebook 03, 04 và 06. Số liệu sau tinh chỉnh lấy từ notebook 05 và 07. Các bản xuất dự đoán từng mẫu của cấu hình ban đầu nằm ở [`experiments02/ket_qua_goc/`](../experiments02/ket_qua_goc/). Các đầu ra gốc của cấu hình đã tinh chỉnh gồm điểm theo fold, bảng điểm tìm kiếm và biểu đồ.

## So sánh với các thực nghiệm trước

Sheet `So_sanh` đối chiếu từng cấu hình đã tinh chỉnh với cấu hình ban đầu tương ứng ở [thực nghiệm 02](../experiments02/README.md) và hai baseline ở [thực nghiệm 01](../experiments01/README.md). Các bảng dùng cùng 5 fold validation. Chênh lệch RMSE âm cho biết mô hình có RMSE thấp hơn mốc đối chiếu.

Sau khi chốt cấu hình từ validation, notebook 08 dùng các pipeline đã lưu để chấm [tập test](../final_test/README.md).
