# Rà soát proposal và định hướng báo cáo cuối kỳ

Tài liệu này đối chiếu proposal của Nhóm 10 với cấu trúc và cách trình bày trong báo cáo Nhóm 11. Báo cáo Nhóm 11 được dùng làm tài liệu tham khảo về tổ chức nội dung; đề tài, dữ liệu, mô hình, số liệu và kết luận của nhóm đó không được chuyển sang đồ án Beijing PM2.5.

Proposal PDF hiện có được giữ nguyên như tài liệu đã nộp. Ghi chú này không thay thế proposal và không khẳng định các phần dự kiến đã được hoàn thành.

## 1. Nhận xét tổng quan

Proposal của Nhóm 10 đã có những thành phần chính cần cho một đề cương môn học: bối cảnh và ý nghĩa, mục tiêu/câu hỏi nghiên cứu, đầu vào và đầu ra, mô tả dữ liệu, EDA và tiền xử lý dự kiến, mô hình, kế hoạch thực nghiệm, sản phẩm bàn giao, tiến độ và tài liệu tham khảo.

Vì vậy, không cần kéo dài proposal chỉ để giống độ dài hoặc nội dung chuyên ngành trong báo cáo Nhóm 11. Đóng góp hữu ích nhất từ bài tham khảo là cách tách mạch nội dung thành phần mở đầu, nền tảng cần thiết, dữ liệu và EDA, phương pháp, thiết lập/kết quả thực nghiệm, rồi kết luận, hạn chế và hướng phát triển.

Đối với đề tài Beijing, tài liệu cần được hoàn thiện tiếp theo chủ yếu là **báo cáo cuối kỳ phản ánh tiến độ và bằng chứng thực tế**, chứ không phải viết lại proposal như thể các kết quả hiện tại đã được biết từ đầu.

## 2. Đối chiếu cấu trúc với báo cáo Nhóm 11

| Thành phần trong báo cáo Nhóm 11 | Đối chiếu với proposal Nhóm 10 | Hướng áp dụng cho báo cáo Beijing |
|---|---|---|
| Bìa, lời mở đầu và các danh mục | Proposal có trang bìa và thông tin nhóm, nhưng đây không phải phần cần mở rộng để sửa nội dung phương pháp. | Áp dụng theo mẫu giảng viên yêu cầu; chỉ thêm lời cam đoan, lời cảm ơn, mục lục, danh mục bảng/hình nếu đúng quy định nộp bài. |
| Mở đầu: lý do, tổng quan nghiên cứu, khoảng trống, mục tiêu, phạm vi và phương pháp | Proposal đã có bối cảnh, ý nghĩa và câu hỏi nghiên cứu; phần tổng quan nghiên cứu/khoảng trống chưa được trình bày thành mục riêng rõ ràng. | Báo cáo cuối nên bổ sung tài liệu liên quan đến dự báo chất lượng không khí và giải thích câu hỏi mà thí nghiệm của nhóm trả lời. Chỉ nêu khoảng trống có dẫn chứng, không tự nhận là nghiên cứu đầu tiên. |
| Mô tả dữ liệu và tiền xử lý | Proposal mô tả nguồn, trường dữ liệu, missing và quy trình dự kiến. | Trình bày thống kê thực tế trước/sau từng bước, quy tắc xử lý, số dòng giữ/bỏ và các giới hạn; không chỉ chép lại kế hoạch. |
| Phân tích dữ liệu/EDA | Proposal liệt kê nhiều câu hỏi EDA, nhưng báo cáo cần chứng minh bằng bảng, hình và nhận xét. | Chọn các hình trả lời câu hỏi nghiên cứu: missing, phân bố PM2.5 (có thể dùng thang log để xem đuôi phân bố), biến động thời gian/trạm, tương quan/tự tương quan và quan hệ gió nếu đã thực hiện. |
| Phương pháp và mô hình | Proposal có Linear Regression, Random Forest, Gradient Boosting, persistence và nguyên tắc đánh giá. | Mô tả đúng pipeline thực tế, tham số, folds và quy trình chọn mô hình. Đánh dấu rõ mô hình/tính năng nào đã chạy, đang làm hoặc chưa triển khai. |
| Thiết lập và kết quả thực nghiệm | Proposal chỉ đưa kết quả dự kiến, không có kết quả chạy. | Báo cáo môi trường, cấu hình, số mẫu từng fold, MAE/RMSE/R², bảng/biểu đồ so sánh, phân tích sai số và diễn giải cả kết quả không tốt. |
| Kết luận, hạn chế, hướng phát triển và tài liệu tham khảo | Proposal có giả thuyết, sản phẩm và tài liệu tham khảo nhưng chưa thể thay cho tổng kết dựa trên thực nghiệm. | Kết luận theo số liệu đã chạy; nêu giới hạn của tập test theo thời gian/mùa, mô hình chưa thử, feature chưa có và những gì cần kiểm chứng thêm. |

Không nên sao chép các phần chuyên biệt của Nhóm 11 như kiến trúc MRI/CNN/RNN, cách chia tập cho bài toán ảnh, số liệu, hoặc lập luận y khoa. Bài đó là tài liệu tham khảo về cấu trúc trình bày, không phải khuôn nội dung hay bằng chứng cho dự án PM2.5.

## 3. Các điểm phương pháp nên đính chính hoặc làm rõ

### 3.1. Không dùng tập test để chọn cấu hình

Trong phần tinh chỉnh, proposal hiện nói so sánh trước và sau tuning trên cùng tập kiểm thử. Cách viết này có thể dẫn tới việc chọn cấu hình dựa vào test và làm mất vai trò đánh giá cuối cùng độc lập của tập test.

**Cách diễn đạt đề xuất cho bản cập nhật hoặc báo cáo phương pháp:**

> Siêu tham số và cấu hình mô hình được lựa chọn chỉ dựa trên các fold validation theo thời gian. Sau khi khóa quy trình và cấu hình, nhóm đánh giá trên tập test một lần để báo cáo khả năng tổng quát hóa; kết quả test không được dùng để chọn mô hình, điều chỉnh feature hoặc tuning.

So sánh trước/sau tuning nên thực hiện trên cùng các folds validation. Nếu báo cáo cả hai kết quả test sau khi đã thử nhiều cấu hình, không được dùng kết quả test để quyết định cấu hình tốt hơn.

### 3.2. Chia fold phải giữ các trạm cùng timestamp ở cùng một phía

Proposal đã nêu đúng yêu cầu rằng các trạm có cùng target timestamp không được tách khác phía trong fold. Khi mô tả RandomizedSearchCV, cần nhắc lại rằng folds phải được tạo theo các timestamp mục tiêu duy nhất và truyền vào quá trình tìm kiếm. Không nên dùng mặc định `TimeSeriesSplit` trên các dòng đã xếp chồng nhiều trạm nếu điều đó có thể chia cùng một timestamp qua train và validation.

### 3.3. Phân biệt feature dự kiến với feature đã triển khai

Proposal dự kiến có PM2.5 lags/rolling, độ lệch so với rolling mean, lag khí tượng và đặc trưng cuối tuần. Trong pipeline `src/features.py` hiện có PM2.5 lag 1/2/3/6/12/24, rolling mean 6/24, đặc trưng thời gian tuần hoàn, station/wind direction và xử lý missing train-only; lag khí tượng, rolling deviation và cờ cuối tuần chưa được triển khai.

Không nên bỏ âm thầm các feature này khỏi lịch sử đề tài hoặc viết trong báo cáo rằng chúng đã được dùng. Hãy đưa vào bảng đối chiếu proposal–thực hiện ở báo cáo cuối, ghi rõ lý do hoãn/bỏ hoặc mô tả kết quả sau khi bổ sung và đánh giá đúng quy trình.

### 3.4. Cập nhật trạng thái mô hình theo bằng chứng hiện có

Tại thời điểm rà soát:

| Mô hình | Bằng chứng hiện có | Cách trình bày trung thực |
|---|---|---|
| Persistence | Có kết quả validation 5 folds và test trong baseline. | Baseline tham chiếu không học tham số. |
| Linear Regression | Có kết quả validation 5 folds và test trong baseline. | Baseline học được; dùng cùng pipeline tiền xử lý. |
| Random Forest | Đã chạy 5-fold validation, chưa dùng test. RMSE trung bình CV khoảng **20.17** (độ lệch chuẩn khoảng **5.56**). | Kết quả hiện tại chưa vượt Linear Regression về RMSE validation (khoảng **19.30**). Không tuyên bố mô hình cây tốt hơn baseline khi chưa có bằng chứng. |
| Linear Regression cắt dự đoán âm về 0 | Có thêm dòng metrics như một biến thể phân tích. | Nêu đây là biến thể bổ sung, mô tả quy tắc clipping và xác định có/không đưa vào bảng xếp hạng chính; không làm lẫn với mô hình Linear Regression gốc. |
| Gradient Boosting và tuning | Chưa có bằng chứng đã triển khai trong các artifacts hiện tại. | Ghi là công việc còn lại hoặc cập nhật sau khi chạy thực nghiệm. |

Các con số trên là kết quả hiện được lưu trong artifacts của repository; nếu chạy lại notebook, dùng artifacts mới nhất và ghi lại cấu hình/môi trường để tránh báo cáo số đã lỗi thời.

## 4. Dàn ý báo cáo cuối kỳ phù hợp với dự án

Có thể áp dụng logic tổ chức của Nhóm 11 theo hướng ngắn gọn, phù hợp với đồ án hồi quy chuỗi thời gian đa trạm:

1. **Mở đầu:** bối cảnh PM2.5, mục tiêu, câu hỏi nghiên cứu, phạm vi và đóng góp trong phạm vi môn học.
2. **Dữ liệu và tiền xử lý:** nguồn/licence, cấu trúc 12 trạm, số mẫu/cột thực tế, missing, kiểm tra dữ liệu, quy tắc tạo target và cách tránh rò rỉ.
3. **EDA:** kết quả có liên quan trực tiếp đến lựa chọn feature/model; so sánh trước/sau xử lý khi biểu đồ và thống kê hỗ trợ điều đó.
4. **Phương pháp:** temporal split, grouped expanding-window CV, feature engineering, pipeline fit trên train, các mô hình và metrics.
5. **Thiết lập và kết quả:** môi trường, cấu hình, kết quả theo fold và tổng hợp, so sánh mô hình, sai số theo trạm/mùa/mức PM2.5, residual và feature importance khi có.
6. **Thảo luận:** ý nghĩa kết quả, trường hợp mô hình thua baseline, hạn chế, sai khác với proposal và nguy cơ khái quát hóa.
7. **Kết luận và hướng phát triển:** trả lời từng câu hỏi nghiên cứu bằng số liệu; liệt kê việc chưa hoàn thành.
8. **Tài liệu tham khảo/phụ lục:** nguồn dữ liệu, bài báo/phương pháp đã trích dẫn, cấu hình và liên kết artifacts.

Tùy yêu cầu giảng viên, có thể gộp chương dữ liệu với EDA hoặc tách thành chương riêng. Không cần hướng tới cùng độ dài với báo cáo Nhóm 11; ưu tiên mạch lập luận và khả năng kiểm chứng.

## 5. Hình ảnh, bảng và mã nguồn

- Dùng hình/biểu đồ được xuất từ notebook và bảng số liệu có nguồn trong `outputs/`; ưu tiên hình có câu hỏi, đơn vị, chú thích và nhận xét trong văn bản.
- Không cần chụp màn hình mã nguồn để thay cho việc bàn giao code. Liên kết repository/notebook và nêu file, hàm, cấu hình liên quan; chỉ đưa đoạn mã ngắn vào phụ lục nếu cần giải thích một quyết định phương pháp.
- Với bảng kết quả, ghi rõ split/fold, số mẫu, metric, mô hình và cấu hình. Không trình bày test như validation hoặc chọn mô hình dựa vào test.
- Đảm bảo số liệu trong báo cáo khớp với CSV/workbook/log và ghi nguồn dữ liệu cùng trích dẫn tài liệu.

## 6. Khuyến nghị về tài liệu gốc

Giữ nguyên [proposal PDF đã nộp](./Nhom10_BeijingAirQuality_Proposal.pdf) để bảo toàn hồ sơ và tránh sửa hồi tố kế hoạch ban đầu. Nếu giảng viên yêu cầu cập nhật proposal, tạo phiên bản có ngày/số phiên bản hoặc phụ lục điều chỉnh riêng; đồng thời vẫn trình bày bảng đối chiếu kế hoạch ban đầu với việc thực hiện trong báo cáo cuối.

Tài liệu tham khảo đối chiếu: [báo cáo Nhóm 11](<./TLTK/11_Phát hiện bất thường khớp gối trên ảnh cộng hưởng từ _NguyenTanDai_3122411035.docx>). Tài liệu này chỉ được dùng để tham khảo cấu trúc và cách trình bày.
