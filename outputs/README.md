# Thư mục `outputs`

Nơi lưu các sản phẩm được tạo ra trong quá trình phân tích, huấn luyện và kiểm thử, không phải mã nguồn đầu vào.

## Thư mục con

- [`eda/`](eda/README.md): kết luận và kết quả khám phá dữ liệu.
- [`figures/`](figures/README.md): biểu đồ và hình ảnh trực quan hóa; hiện có các hình của baseline từ notebook 02.
- `test_reports/`: báo cáo kết quả kiểm thử; hiện chưa có báo cáo nào được sinh ra.

## Tệp ở cấp thư mục

- `baseline_error_analysis.csv`: sai số của hai baseline (Persistence và Linear Regression) trên dự đoán out-of-fold của 5 fold validation, không dùng test. Tạo bởi [`02_model_training_baseline.ipynb`](../notebooks/02_model_training_baseline.ipynb). Mỗi dòng là một nhóm × một mô hình, gồm các cột:
  - `group_type`: loại nhóm, gồm `station` (12 trạm), `season` (Xuân/Hè/Thu/Đông theo tháng) và `pm25_level` (mức PM2.5 thực tế: 0–35, 35–75, 75–115, 115–150, 150–250, >250).
  - `group`, `model`, `n`: tên nhóm, tên mô hình và số dòng trong nhóm.
  - `mae`, `rmse`, `r2`: độ đo của nhóm đó. R² trong nhóm hẹp như `pm25_level` ít ý nghĩa, nên với nhóm này hãy nhìn MAE, RMSE và `mean_residual`.
  - `mean_residual`: trung bình của (thực tế − dự đoán); **dương** nghĩa là mô hình dự đoán thấp hơn thực tế.

Tệp CSV này lưu bằng `utf-8-sig` để Excel hiển thị đúng tiếng Việt. Chạy lại notebook 02 sẽ ghi đè tệp.

Kết luận dạng bảng của EDA nằm trong [`eda/eda_conclusions.csv`](eda/eda_conclusions.csv); diễn giải từng bước, các quyết định và việc còn bỏ ngỏ được ghi trong [`eda/eda_worklog.md`](eda/eda_worklog.md).