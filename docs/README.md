# Tài liệu đồ án

## Tệp hiện hành

- [Proposal](Nhom10_BeijingAirQuality_Proposal.pdf): kế hoạch đã nộp, giữ nguyên để đối chiếu.
- [Báo cáo cuối kỳ](Nhom10_BeijingAirQuality_BaoCaoCuoiKy.docx): dữ liệu, phương pháp, thiết lập thực nghiệm, kết quả validation/test, phân tích sai số, độ chắc chắn và phân công thành viên.
- [Slide trình bày](Nhom10_Slide.pptx): trình bày dữ liệu, phương pháp, validation, tuning và test.
- [Phân công](phan-cong-cong-viec.docx): vai trò, công việc đã thực hiện và tỷ lệ đóng góp, tổng bằng 100%; đối chiếu với Bảng 1 và Mục 8 của báo cáo.

## Nguồn số liệu cập nhật

- outputs/experiments/experiments01–03/: baseline, mô hình ban đầu và tuning trên validation.
- [Điểm test gốc](../outputs/notebooks/tables/final_test_metrics.csv): các cấu hình đã chốt.
- [Phân tích test bổ sung](../outputs/experiments/final_test/analysis/): predictions, lỗi theo nhóm, bootstrap ghép cặp và manifest.
- [Chẩn đoán validation](../outputs/experiments/validation_diagnostics/): importance của RF, độ ổn định theo seed và hội tụ MLP.
- [EDA có thể tái lập](../outputs/eda/): bảng/hình được tạo từ python -m src.eda và notebook 01.

Các bảng/hình phân biệt rõ nguồn tập dữ liệu: baseline OOF, mô hình tuned trên test, hay chẩn đoán validation. Importance của Linear Regression và Random Forest được báo cáo riêng.

Dùng môi trường trong [requirements.txt](../requirements.txt) và xem hướng dẫn chạy ở [README gốc](../README.md). [Nhật ký thực nghiệm](../Experimental%20Log/README.md) lưu các phiên bản và ghi chú lịch sử của quá trình làm đồ án.

## Truy vết và kiểm chứng

- [Bảng tra nguồn CSV](../outputs/notebooks/tables/report_sources.csv): notebook, mã ô và trạng thái tính mới/đối chiếu search cũ.
- [Kiểm tra nguồn kết quả](../scripts/verify_result_sources.py): đối chiếu CSV với bằng chứng trong notebook đã thực thi; mặc định chỉ đọc.
- [Bộ kiểm thử](../tests/README.md): kiểm tra dữ liệu, đặc trưng, mô hình và các phân tích thống kê.

## Tài liệu tham khảo và yêu cầu môn học

- [Seng và cộng sự (2021)](TLTK/1-s2.0-S1110016820306438-main.pdf): dự báo chất lượng không khí bằng LSTM.
- [Bekkar và cộng sự (2021)](TLTK/40537_2021_Article_548.pdf): dự báo ô nhiễm không khí bằng học sâu.
- [Wei và cộng sự (2025)](TLTK/sustainability-17-09211.pdf): so sánh mô hình học máy dự báo PM2.5 và O3.
- [Yêu cầu đề tài cuối kỳ](TLTK/ML%20-%20De%20tai%20cuoi%20ky%20-%20Final.pdf): tài liệu môn học.
- [Khóa luận về PM10](TLTK/KLTN_bao_cao_sau_hoi_dong.pdf): tài liệu tham khảo cùng lĩnh vực chất lượng không khí; không phải kết quả thực nghiệm của nhóm.

Danh mục trích dẫn đầy đủ được trình bày trong báo cáo. Số liệu thực nghiệm của nhóm lấy từ notebook và CSV trong kho mã nguồn.
