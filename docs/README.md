# Tài liệu đồ án

## Tệp hiện hành

- [Proposal](Nhom10_BeijingAirQuality_Proposal.pdf): kế hoạch đã nộp, giữ nguyên để đối chiếu.
- [Báo cáo cập nhật tiến độ](Nhom10_BeijingAirQuality_BaoCaoGiuaKy.docx): đã có kết quả tuning và test; tên tệp giữ theo bản nhóm cung cấp.
- [Slide cập nhật](Nhom10__Slide.pptx): trình bày dữ liệu, phương pháp, validation, tuning và test.
- [Bản rà soát và kế hoạch khắc phục](ra-soat-do-an-va-ke-hoach-khac-phuc.md): phát hiện, checklist và trạng thái khắc phục.
- [Phân công](phan-cong-cong-viec.docx): đối chiếu với đóng góp thực tế.
- TLTK/: tài liệu tham khảo cách trình bày, không dùng số liệu của đề tài khác làm kết quả nhóm.

## Nguồn số liệu cập nhật

- outputs/experiments/experiments01–03/: baseline, mô hình ban đầu và tuning trên validation.
- [Điểm test gốc](../outputs/notebooks/tables/final_test_metrics.csv): các cấu hình đã chốt.
- [Phân tích test bổ sung](../outputs/experiments/final_test/analysis/): predictions, lỗi theo nhóm, bootstrap ghép cặp và manifest.
- [Chẩn đoán validation](../outputs/experiments/validation_diagnostics/): importance của RF, độ ổn định theo seed và hội tụ MLP.
- [EDA có thể tái lập](../outputs/eda/): bảng/hình được tạo từ python -m src.eda và notebook 01.

Báo cáo và slide cần nhận các bảng/hình mới sau khi kiểm chứng. Giữ rõ nguồn tập dữ liệu: baseline OOF, mô hình tuned trên test, hay chẩn đoán validation. Không áp dụng kết luận importance của Linear Regression cho Random Forest.

Dùng môi trường trong requirements.txt và xem hướng dẫn chạy ở [README gốc](../README.md). Các file đề cương/báo cáo lịch sử không được sửa để biến kết quả mới thành kết quả đã biết từ trước.

## Phạm vi sửa tài liệu hiện tại

- [Yêu cầu sửa DOCX và slide](nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md): chỉ áp dụng phần phù hợp với đồ án PM2.5, số liệu lấy từ output notebook.
- [Bảng tra nguồn CSV](../outputs/notebooks/tables/report_sources.csv): notebook, mã ô và trạng thái tính mới/đối chiếu search cũ.
- W&B/MLflow tạm chưa cần; mọi bổ sung công nghệ phải hỏi ý kiến người dùng trước.
- Không chuyển các yêu cầu riêng của bài đầu gối/MRI thành yêu cầu cho đề tài này.
- Chạy scripts/build_report_requirements.py để cập nhật danh sách sửa tài liệu sau khi kiểm chứng notebook/CSV. Script không sửa trực tiếp DOCX hoặc PPTX.
