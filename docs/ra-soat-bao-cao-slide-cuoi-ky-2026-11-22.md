# Rà soát báo cáo và slide cuối kỳ — 22/11/2026

## Cập nhật sau khi nhóm chỉnh DOCX ngày 22/11/2026

**Bản mới được kiểm tra:** `Nhom10_BeijingAirQuality_BaoCaoCuoiKy.docx`, SHA-256 `6a1f86438925e4d43e52f33a661873078d15c67605d197b0737b2fc1fb73043b`. Đã đối chiếu thay đổi văn bản/bảng với bản trước và mở lại ảnh pipeline trong DOCX. Lượt này chỉ kết luận cho DOCX, không rà lại slide.

**Kết luận cập nhật:** phần thực nghiệm đã sửa đúng các lỗi diễn giải quan trọng. Bảng thành viên đã có tỷ lệ 30% / 15% / 20% / 20% / 15%, tổng 100%, khớp tài liệu phân công. Hai bảng train–validation–test và độ nhạy đã có output/bằng chứng trong notebook 08. Chạy lại `verify_result_sources.py` đạt **52 CSV / 8 notebook**; đối chiếu lại **338 ô số** trong DOCX và tính lại bảng độ nhạy từ dự đoán cố định đều khớp. Không chạy lại pytest trong lượt kiểm tra DOCX này.

Các mục đã khắc phục trên DOCX: bỏ phân rã “một nửa” nguyên nhân chênh lệch train–test; không gán mức overfitting/underfitting khi chưa đủ bằng chứng; sửa diễn giải thứ tự theo seed và epoch; sửa chiều tốt/xấu của R² và đơn vị; phân biệt người commit với người chạy; bỏ lời hướng dẫn biên tập; sửa tham chiếu Bảng 19/20/B1 và Bảng 26/27; ghi đúng độ nhạy là hậu kiểm; ảnh Hình 7 đã sửa chữ tràn/cắt và ghi rõ importance dùng validation fold 5.

**Những chỗ còn cần đồng bộ:**

| Ưu tiên | Vị trí DOCX | Phát hiện còn lại và cách sửa |
| --- | --- | --- |
| Cao | Phụ lục A, Bảng A3 | Dòng notebook 08 vẫn ghi **15 CSV, 20/11/2026 16:20:04 UTC**. Chỉ mục hiện ghi **17 CSV, 22/11/2026 13:31:45 UTC**, mã ô `evidence-nb-08`, execution count 9. Tổng các dòng hiện in trong Bảng A3 là 50, trong khi Bảng 33/Phụ lục C đã ghi đúng tổng mới 52. Cập nhật dòng 08; giữ nguyên dữ liệu lịch sử của 01–07. |
| Cao | Mục 5.4, đoạn “Nguồn gốc số liệu”; đoạn ngay sau Bảng A3 | Phần kể thời điểm chạy vẫn ghi notebook 08 ngày 20/11 và manifest cũ. Hiện `evaluation_manifest.json` có `created_at_utc = 2026-11-22T13:28:59.916299+00:00`, commit nền `581ca53ef03395f94cb23a91abef00fdfea51149`, `working_tree_dirty = true`; `diagnostics_manifest.json` có `created_at_utc = 2026-11-22T13:31:44.978616+00:00`. Cập nhật câu trích manifest hiện hành, không tiếp tục dẫn `ceacd7b` và các giờ cũ như thông tin của tệp hiện tại. |
| Vừa | Phụ lục A, Bảng A2 | Danh sách phân tích bổ sung chưa thêm `train_vs_validation_vs_test.csv` và `final_test_sensitivity.csv`, dù hai tệp đã được dùng ở Bảng 15/25 và đã có nguồn notebook. Thêm hai dòng, nguồn notebook 08 / `evidence-nb-08`. |
| Nhỏ | Mục 7.3, Bảng 33, dòng “Phân công và nguồn số liệu” | Câu “Phân công phần việc **và tỷ lệ đóng góp theo lịch sử commit**” dễ mâu thuẫn với đoạn sau Bảng 1 nói tỷ lệ dựa trên khối lượng gói công việc. Đổi thành “Phân công phần việc có đối chiếu lịch sử commit; tỷ lệ đóng góp theo khối lượng công việc”. |
| Nhỏ | Mục 5.1, đoạn liệt kê bảy khối ngay sau Hình 7 | Đoạn mở đầu và hình đã phân biệt đúng tập dữ liệu; nhưng câu liệt kê khối (7) vẫn gom “permutation importance” vào đánh giá test. Bỏ cụm đó khỏi khối (7), hoặc thêm ngay tại đó rằng importance dùng validation fold 5. |

Hai điểm hoàn thiện câu chữ có thể làm cùng lúc: Mục 6.9 nên nói chính xác hai cặp **RF–GB và RF–MLP** chưa tách khỏi 0, thay vì để người đọc hiểu đã tính cả cặp GB–MLP; chỉ xác nhận ngắt trang và mục lục sau khi xuất PDF. Chưa render toàn bộ DOCX trong lần kiểm tra này.

**Trạng thái xử lý các điểm trên (sau lượt sửa tiếp theo):** đã sửa dòng notebook 08 ở Bảng A3 (17 CSV, 22/11/2026 13:31:45 UTC; tổng 52); cập nhật Mục 5.4 và đoạn manifest (13:28:59 và 13:31:44 UTC, commit nền 581ca53); thêm hai dòng vào Bảng A2; đổi câu ở Bảng 33 thành "tỷ lệ đóng góp theo khối lượng công việc"; bỏ permutation importance khỏi khối (7) ở Mục 5.1; Mục 6.9 nêu rõ hai cặp RF–GB và RF–MLP, chưa tính GB–MLP. Mục lục và số trang đã tính lại từ PDF.

**Không cần huấn luyện thêm để sửa các điểm còn lại trên. Không sửa trực tiếp DOCX trong lượt rà soát.** Các mục R01–R12 và số 50 CSV ở phần bên dưới là hồ sơ của lần kiểm tra trước; dùng cập nhật này làm trạng thái hiện hành cho DOCX mới, không tiếp tục coi các lỗi đã khắc phục là còn tồn đọng.

## 1. Bản được kiểm tra và kết luận

Đã đọc bản đang lưu trên đĩa, không dùng danh sách lỗi của bản giữa kỳ để kết luận cho bản mới:

- [Báo cáo cuối kỳ](Nhom10_BeijingAirQuality_BaoCaoCuoiKy.docx), SHA-256 bắt đầu `9c38a20f8d73`.
- [Slide](Nhom10__Slide.pptx), SHA-256 bắt đầu `cf3f02b635c5`: 34 slide theo thứ tự trình chiếu, 34 slide có ghi chú; slide 25–34 là phụ lục.
- [Phân công công việc](phan-cong-cong-viec.docx), SHA-256 bắt đầu `09c36327d44b`.
- Quy định nộp cuối kỳ người dùng cung cấp và các nhận xét phù hợp với bài PM2.5 trong [ghi chú giảng viên](bo-nho-quy-trinh-de-tai-ML-theo-giang-vien.md). Không áp dụng yêu cầu riêng cho MRI; không yêu cầu W&B/MLflow hoặc bổ sung công nghệ.

**Bản mới đã có phần lớn nội dung từng thiếu. Chưa nên chốt nộp vì vẫn có lỗi diễn giải thực nghiệm, thiếu tỷ lệ đóng góp và một số lỗi biên tập.** Trong phạm vi các bảng được kiểm tra, chưa thấy sai số liệu gốc. Cần sửa lời bình và truy vết trước khi bổ sung thí nghiệm khác.

Ở bản cuối kỳ này **không còn** nhãn `[CẦN NHÓM XÁC NHẬN]` hoặc `[nhóm xác nhận]`. Nhận xét trước về những nhãn đó thuộc bản `BaoCaoGiuaKy.docx`, không còn áp dụng cho tệp hiện tại.

## 2. Những phần đã đạt, không cần làm lại

| Nội dung | DOCX hiện tại | Slide hiện tại |
| --- | --- | --- |
| Bối cảnh, thách thức, mục tiêu, đóng góp | Mục 2.1–2.5 | 3–5 |
| Công trình liên quan, nhận xét và giới hạn so sánh | Mục 2.6, 6.9; ba bài có bản gốc trong TLTK | 6, 21 |
| Dữ liệu, nhãn, đặc trưng, tiền xử lý | Mục 3–4 | 4, 7–10 |
| Mô hình, kiến trúc MLP, loss và độ đo | Mục 5.2–5.3 | 11–12 |
| Thiết lập và danh sách thí nghiệm trước kết quả | Mục 5.4–5.5, TN1–TN8 | 13–14 |
| Validation, tuning, test, lỗi theo nhóm | Mục 6.1–6.5 | 15–18; phụ lục 28–32 |
| Importance của LR và RF, giới hạn diễn giải | Mục 6.6 | 19 |
| Bootstrap ghép cặp, seed và epoch MLP | Mục 6.7 | 20; phụ lục 33 |
| Đánh giá tổng thể, hạn chế và hướng phát triển | Mục 6.8–7 | 21–22 |
| Ghi chú trình bày | Không áp dụng | Đã có ở cả 34 slide |

Các lỗi số liệu cũ đã được sửa: bảng baseline theo nhóm PM2.5 dùng số mẫu 115.085 / 72.055 / 45.799 / 24.358 / 30.226 / 13.173; importance khí tượng của LR là 1,37. Không còn đúng khi nói DOCX và slide không có tài liệu tham khảo chung: cả hai đã dùng UCI, WHO và ba bài Seng/Bekkar/Wei.

## 3. Các sửa đổi cần ưu tiên

### R01 — Diễn giải overfitting đang vượt bằng chứng

**Vị trí:** DOCX Mục 6.4, sau Bảng 15; slide 17 và ghi chú; kết luận slide 22 và ghi chú.

Các câu cần sửa:

- “khoảng một nửa mức tăng ... đến từ việc giai đoạn test khó hơn”.
- “phần còn lại gợi ý overfitting mức vừa”.
- “Không thấy overfitting nặng: RMSE validation ... nằm giữa RMSE train và RMSE test”.
- “Linear Regression ... nên mô hình không overfit”, rồi kết luận “underfitting nhẹ”.

**Bằng chứng:** [train_vs_validation_vs_test.csv](../outputs/experiments/final_test/analysis/train_vs_validation_vs_test.csv) ghi khoảng cách train–test. Tuy nhiên, train ở đây là sai số trong mẫu của mô hình cuối trên toàn bộ train/validation, còn validation là điểm của những mô hình khác được fit trên từng fold. Các tập khác nhau về thời kỳ, phân phối và kích thước huấn luyện. Persistence tăng sai số dù không học tham số cho thấy chênh lệch giữa các giai đoạn cần được lưu ý; không cho phép phân rã định lượng nguyên nhân của chênh lệch ở RF/GB/MLP.

Không có thí nghiệm kiểm soát để quy “một nửa” cho thay đổi dữ liệu, phần còn lại cho overfitting. Sai số train cao hơn mô hình khác cũng chưa đủ chẩn đoán underfitting.

**Đoạn thay thế đề xuất:**

> Sai số test cao hơn sai số trong mẫu ở cả năm mô hình, kể cả Persistence không học tham số. Sự khác nhau giữa các giai đoạn và sai số khái quát hóa đều có thể góp phần tạo khoảng cách này; phép so sánh hiện có chưa tách được ảnh hưởng của từng yếu tố. RF, GB và MLP có khoảng cách train–test lớn hơn hai baseline. Đây là mô tả cần lưu ý, chưa đủ để phân loại mức overfitting. Linear Regression có sai số trong mẫu cao hơn ba mô hình phi tuyến, nhưng chưa có thí nghiệm riêng để kết luận underfitting.

Giữ các số trong Bảng 15; sửa diễn giải ở cả báo cáo, slide và ghi chú. Không cần thay mô hình hoặc tinh chỉnh theo test.

### R02 — Hai bảng mới chưa có bằng chứng thực thi trong notebook

**Vị trí:** DOCX Bảng 15, Bảng 25, Mục 5.5/TN4, Phụ lục A và C; slide 14, 17.

Hai tệp mới:

- [train_vs_validation_vs_test.csv](../outputs/experiments/final_test/analysis/train_vs_validation_vs_test.csv), nguồn hiện ghi là `scripts/export_train_vs_test.py`.
- [final_test_sensitivity.csv](../outputs/experiments/final_test/analysis/final_test_sensitivity.csv), nguồn hiện ghi là `scripts/export_sensitivity.py`.

**Phát hiện:** cả hai chưa có trong [report_sources.csv](../outputs/notebooks/tables/report_sources.csv). Mã nguồn tám notebook hiện không gọi các bước xuất này. Vì vậy, câu “mọi số liệu lấy từ CSV do notebook 01–08 xuất” chưa bao quát đúng hai bảng mới. PASS của bộ kiểm tra 50 CSV không chứng nhận hai bảng này.

Đã tính lại `final_test_sensitivity.csv` từ dự đoán test cố định và đối chiếu: khớp. Đây là vấn đề truy vết theo quy tắc của người dùng, không phải bằng chứng bảng độ nhạy tính sai. Bảng train trong lần rà soát này được đối chiếu nội dung CSV; chưa chạy lại dự đoán toàn bộ train để chứng nhận riêng tệp đó.

**Cần làm trước khi chốt:** đưa hai phép tính vào ô chẩn đoán của notebook 08, thực thi với mô hình đã khóa, lưu output và bằng chứng cho hai CSV; sau đó cập nhật chỉ mục nguồn, số lượng CSV và bảng truy vết trong phụ lục. Không cần chạy lại tìm kiếm siêu tham số. Phụ lục C cũng cần hướng dẫn tái lập hai bảng này; quy trình hiện tại chưa có hai lệnh xuất tương ứng.

### R03 — Chưa đáp ứng bảng thành viên theo quy định nộp cuối kỳ

**Vị trí:** DOCX Bảng 1, Mục 8/Bảng 34; `phan-cong-cong-viec.docx`; slide 23.

Đã có tên, MSSV, vai trò, phần việc và sản phẩm. **Chưa có tỷ lệ đóng góp (%)**, nên chưa chứng minh được tổng bằng 100% theo quy định mới người dùng cung cấp.

**Cần sửa:** ít nhất một bảng chính thức của hồ sơ phải có `Họ tên | MSSV | Vai trò/nhiệm vụ | Công việc đã thực hiện | Đóng góp (%)`. Nhóm tự chốt phần việc và tỷ lệ; không suy phần trăm từ số commit, không tự chia đều. Slide có thể dẫn về bảng chính thức thay vì lặp toàn bộ.

### R04 — Phân công theo commit chưa thay thế thông tin người chạy thực nghiệm

**Vị trí:** DOCX Mục 1.2, 5.4 (Nguồn gốc số liệu), 7.2, 8, Phụ lục A; slide 23; tài liệu phân công.

Bản mới đã bỏ nhãn chờ xác nhận và ghi phân công theo tên/email commit. Không có căn cứ trong lần rà soát này để kết luận bảng phân công đó sai; nhóm có thể dùng Git làm minh chứng tham gia như thầy cho phép.

Tuy nhiên, manifest vẫn ghi `operator = null`. Người viết/commit mô-đun và người thực thi một lượt chạy là hai thông tin khác nhau. Không dùng câu “người thực hiện từng phần việc ... theo lịch sử commit” để coi yêu cầu truy vết người chạy đã hoàn tất.

**Cần sửa:** phân biệt rõ phần việc nhóm đã chốt với nhật ký người chạy. Chỉ điền người chạy nếu có xác nhận thực tế; với lượt cũ không biết thì ghi chưa ghi nhận, không hồi suy từ commit. Hàng “Phân công và truy vết — Hoàn thành” ở Bảng 33 cần giới hạn phạm vi cho đúng. Không cần thêm nền tảng quản lý thí nghiệm.

### R05 — DOCX còn chứa lời hướng dẫn sửa bản thảo

**Vị trí và nội dung nguyên văn:**

- Mục 5.1: `Thêm đoạn dẫn nhập: "Pipeline gồm bảy khối..." (Nguyên tắc của giảng viên...)`.
- Sau Bảng 8: `Chú thích dưới bảng: "Cấu hình ban đầu..."`, kèm lựa chọn “hoặc chuyển thành Phụ lục A2”.
- Ngay sau đó: `Mô tả ngắn của Bảng 8: cần nêu rõ...`.

**Cần sửa:** viết thành văn bản báo cáo hoàn chỉnh, bỏ mệnh lệnh biên tập và lựa chọn chưa chốt. Ví dụ Mục 5.1 bắt đầu thẳng bằng “Pipeline gồm bảy khối...”. Các nguồn sau Bảng 8 viết dưới nhãn “Nguồn”, còn phần giải thích viết thành đoạn bình thường.

### R06 — Một số tham chiếu bảng/hình vẫn mang số cũ

| Vị trí | Hiện tại | Cần sửa |
| --- | --- | --- |
| DOCX Mục 6.1, đoạn phân biệt trung bình fold và OOF | “Các Bảng 19, 14 và B1 dùng cách gộp OOF theo nhóm” | Bảng 14 hiện là kết quả test. Các bảng baseline OOF theo nhóm là **19, 20 và B1**. |
| DOCX Mục 6.6, đoạn giới hạn importance | “Bảng 26 và 15b” | Đổi thành **Bảng 26 và 27**. Không có Bảng 15b hiện hành. |
| Slide 13, chú thích sơ đồ chia tập | “báo cáo, Hình 8” | Sơ đồ chia tập hiện là **Hình 9**; Hình 8 là kiến trúc MLP. |

Sau khi sửa, cập nhật mục lục, số hình/bảng và tham chiếu trong Word. Số trang trong mục lục chưa được xác nhận bằng bản PDF xuất cuối.

### R07 — Kết luận về thứ tự MLP và LR theo seed chưa đúng dữ liệu đã chạy

**Vị trí:** DOCX Mục 6.7, đoạn sau Bảng 30: “Vì vậy thứ tự giữa MLP và Linear Regression trên validation phụ thuộc vào seed.”

**Bằng chứng:** [mlp_seed_summary.csv](../outputs/experiments/validation_diagnostics/mlp_seed_summary.csv) và [baseline_cv_summary.csv](../outputs/notebooks/tables/baseline_cv_summary.csv). RMSE của MLP ở cả ba seed đều cao hơn LR; seed 2026 gần như bằng LR nhưng chưa thấp hơn. Chưa quan sát được đảo thứ tự trong ba lần đã chạy.

**Đổi thành:**

> Khoảng cách giữa MLP và Linear Regression thay đổi theo seed. Ở seed 2026, hai điểm gần như bằng nhau; trong cả ba seed đã kiểm tra, RMSE trung bình của MLP vẫn cao hơn Linear Regression.

Không chọn seed 2026 để thay mô hình cuối sau khi đã xem test.

### R08 — Một số câu về độ đo và mức kết luận cần sửa

| Vị trí | Vấn đề | Cách sửa |
| --- | --- | --- |
| DOCX Mục 6.8, CH1 | “thấp nhất ... ở cả ba độ đo”, trong khi R² càng cao càng tốt | “MAE và RMSE thấp nhất, R² cao nhất”. |
| DOCX Mục 5.3, đoạn đầu sau Bảng 9; slide 13 | Gộp MAE, RMSE, R² dưới đơn vị µg/m³, dù chỗ khác đã ghi R² không đơn vị | Tách nhất quán: MAE/RMSE dùng µg/m³; R² không đơn vị. |
| DOCX Mục 6.7, đoạn epoch | “giới hạn 40 epoch không phải nguyên nhân gây sai số cao” | Chỉ kết luận “tăng giới hạn lên 100 epoch không cải thiện RMSE trên hai fold đã kiểm tra”. Chưa loại trừ mọi nguyên nhân của sai số cao. |
| Một số câu kết luận, ghi chú slide 20–22 | Có thể hiểu cả ba cặp RF/GB/MLP đều đã có kiểm định | Nêu đúng hai cặp có khoảng chứa 0: RF–GB và RF–MLP. Chưa tính khoảng GB–MLP. |

### R09 — Bảng độ nhạy là hậu kiểm; chưa có minh chứng đăng ký quy tắc trước

**Vị trí:** DOCX Mục 6.5, trước Bảng 25: “nhóm đặt quy tắc từ trước”.

Hàm `src.evaluation.trimmed_sensitivity` có quy tắc rõ: xếp theo trung bình sai số tuyệt đối của năm mô hình, cùng bỏ một tập hàng, tính lại độ đo. Nhưng hiện chưa có bằng chứng trong hồ sơ rằng quy tắc được chốt trước khi xem kết quả test. Câu trong docstring không chứng minh lịch sử thiết kế.

**Đổi thành:** “Trong phân tích độ nhạy hậu kiểm, nhóm áp dụng cùng quy tắc ...”. Giữ kết quả trên toàn bộ 51.063 mẫu là kết quả chính. Các hàng đã loại không mặc nhiên là dữ liệu sai; không dùng điểm sau loại để tuyên bố mô hình tốt hơn trên bài toán gốc. Không đánh đồng phép bỏ hàng test với việc xác minh hai điểm 999/844 ở train.

### R10 — Sơ đồ pipeline bị cắt chữ và chưa thống nhất cách mô tả

**Vị trí:** DOCX Hình 7, ảnh nhúng `word/media/image15.png`; Mục 5.1; slide 10.

Đã mở trực tiếp ảnh pipeline: tiêu đề các khối 2/3 bị cắt ở mép hộp; nội dung khối 1/3/6 tràn qua biên. Đây là lỗi có trong ảnh nguồn, không chỉ do cách Word hiển thị.

Báo cáo dùng bảy khối, slide dùng sáu khối do gộp các bước. Việc gộp có thể chấp nhận, nhưng cần giải thích hoặc thống nhất để tránh trả lời mâu thuẫn khi thầy hỏi pipeline có mấy phần. Mục 5.1/Hình 7 đang gom importance vào bước “đánh giá cuối”; cần ghi rõ importance chạy trên **validation fold 5**, còn bảng lỗi cuối và bootstrap chạy trên **test**.

**Cần sửa:** chỉnh sơ đồ theo định dạng hiện có, cho chữ nằm trong hộp; giữ thống nhất tên bước và nguồn dữ liệu của từng chẩn đoán. Không cần thêm công nghệ.

### R11 — Slide đã đủ ý nhưng phần thực nghiệm còn quá nhiều chữ nhỏ

**Bằng chứng trực tiếp từ cấu hình chữ trong PPTX:**

- Slide 14: bảng tám thí nghiệm dùng chữ **10,5 pt**.
- Slide 16: bảng validation dùng chữ **11,5 pt**.
- Slide 17: phần thân bảng kết quả **12,5 pt**, nhiều lời bình ngay dưới.
- Slide 20: bảng bootstrap **10,5–11 pt**, đồng thời chứa seed và epoch.
- Slide 6: bảng ba công trình dùng chữ **13 pt**.

Đây là nhận xét về khả năng đọc khi trình chiếu; chưa kết luận có tràn chữ trên từng trang vì chưa render toàn bộ PPTX trong PowerPoint. Chữ nguồn 9 pt không nên bị đánh đồng với chữ nội dung chính, nhưng bảng chính 10,5 pt cần ưu tiên rút gọn.

**Đề nghị sửa:**

1. Slide 14 giữ tám thí nghiệm nhưng rút mỗi câu hỏi còn một ý; đường dẫn tệp dài đưa vào ghi chú/phụ lục.
2. Slide 16 chỉ giữ RMSE và mức cải thiện cần nói; bảng ba metric đầy đủ chuyển dự phòng.
3. Slide 17 giữ bảng test chính, chuyển bảng train/validation và diễn giải chẩn đoán sang dự phòng sau khi sửa R01.
4. Slide 20 ưu tiên bootstrap; chi tiết epoch đã có slide 33. Seed có thể nói một câu kèm phạm vi validation.
5. Luyện bài với slide chính 1–24; 25–34 là dự phòng. Việc dành khoảng 15 phút là yêu cầu từ ghi chú thầy; số slide tối đa không phải quy định cứng. Có thể đặt 25–34 ở chế độ ẩn hoặc thêm chỉ dẫn rõ để tránh trình chiếu nối tiếp sau trang cảm ơn.

Ghi chú đã có đủ; cần sửa lời bình R01/R08 trong ghi chú cùng lúc với mặt slide.

### R12 — Tài liệu checklist cũ chưa phản ánh bản cuối kỳ

**Vị trí:** [bản tổng hợp cũ](phan-con-thieu-docx-slide/00_tong-hop.md) và các file rà soát trước.

Bản tổng hợp cũ vẫn nói thiếu loss, importance RF, ghi chú; nhắc 54 test, 22 notes trống và các số bảng của bản cũ. Những nhận định này không mô tả đúng cặp tệp được rà soát lần này.

**Cần sửa khi đóng gói:** đánh dấu các checklist cũ là lịch sử hoặc cập nhật trạng thái đã khắc phục; dùng tài liệu này làm danh sách tồn đọng cho bản có hash ở Mục 1. Không để người xem hiểu báo cáo cuối còn thiếu các mục đã hoàn thành.

## 4. Hồ sơ nộp cuối kỳ ngoài hai tệp

- Chưa tìm thấy poster PM2.5 của nhóm trong repo. Poster trong `docs/TLTK/` là mẫu tham khảo.
- Chưa có tỷ lệ đóng góp được nhóm chốt, như R03.
- Cần chỉ rõ GitHub cá nhân của từng thành viên và repo chính trong hồ sơ; chia sẻ tài khoản/repo với giảng viên là việc chưa thể xác nhận chỉ từ file trên đĩa.
- Tên ZIP theo mẫu của thầy, nhóm trưởng nộp đại diện; chuẩn bị một cuốn báo cáo hoàn chỉnh, slide và poster theo quy định bản nộp trực tiếp.
- Chưa tìm thấy video demo riêng của PM2.5. Đoạn quy định người dùng gửi xếp video vào tài nguyên “nếu có”; không coi đây là lý do bắt buộc xây giao diện hoặc thêm thư viện mới.

## 5. Bằng chứng kiểm tra lần này

| Kiểm tra | Kết quả và giới hạn |
| --- | --- |
| `scripts/verify_result_sources.py` | PASS: 50 CSV liên kết với tám notebook; output, hash, nhật ký và tổng số mẫu nhóm khớp. Không bao gồm hai tệp ở R02. |
| `pytest -q -p no:cacheprovider` trong `.venv`, Python chạy với `-B` | **56 passed in 12.11s**. Test đạt không phải chứng minh tuyệt đối rằng mọi khả năng rò rỉ đã được loại trừ. |
| Đối chiếu bảng DOCX | **338 ô số** ở các bảng test tổng thể, tháng, mức PM2.5, trạm, seed và độ nhạy khớp CSV theo độ chính xác hiển thị. Không tuyên bố đã tự động đối chiếu mọi ô của tài liệu. |
| Độ nhạy | Tính lại từ `final_test_predictions.csv`, so với `final_test_sensitivity.csv`: khớp số và thứ hạng. Không fit lại hoặc thay mô hình. |
| Tài liệu liên quan | Đọc bản PDF Seng, Bekkar, Wei trong `docs/TLTK/`. Các mô tả chính về dữ liệu/phương pháp phù hợp. Khi làm rõ khác biệt với Bekkar, có thể bổ sung rằng phần phân tích không gian của bài lấy Aotizhongxin làm trạm đích, thay vì diễn đạt như cùng giao thức đánh giá đủ 12 trạm của nhóm. |
| Kiểm tra Office | Đọc văn bản, bảng, quan hệ và ghi chú trong DOCX/PPTX theo đúng thứ tự slide; mở trực tiếp ảnh pipeline, kiến trúc MLP và sơ đồ chia tập. Chưa render toàn bộ tài liệu thành PDF/ảnh, nên chưa xác nhận ngắt trang, mục lục và mọi trường hợp tràn chữ. |

**Không sửa DOCX/PPTX, không chỉnh số liệu thực nghiệm, không huấn luyện lại và không thêm công nghệ trong lần rà soát này.**

## 6. Thứ tự hoàn thiện

1. Sửa các kết luận vượt bằng chứng: R01, R07, R08, R09, trên cả mặt slide và ghi chú.
2. Bổ sung truy vết notebook cho hai bảng mới theo R02; chốt bảng thành viên và phần người chạy theo R03–R04.
3. Dọn lời biên tập, số tham chiếu, sơ đồ và kích thước chữ theo R05–R06, R10–R11.
4. Xuất PDF từ Word/PowerPoint để kiểm tra hình thức cuối; cập nhật checklist cũ và hoàn thiện poster/hồ sơ nộp.

Các hướng mở rộng đã ghi như loss khác, dữ liệu trạm lân cận, seed RF/GB, trạm giữ ngoài hoặc mùa khác không bắt buộc phải triển khai thêm chỉ để sửa các vấn đề trên.

## 7. Trạng thái xử lý (cập nhật sau rà soát)

| Mã | Trạng thái | Ghi chú |
| --- | --- | --- |
| R01 | Đã sửa | Báo cáo (Mục 6.4), slide 17, 22 và ghi chú không còn quy "một nửa" cho giai đoạn test; nêu rõ không tách được hai nguyên nhân và không kết luận underfitting. |
| R02 | Đã sửa | Hai bảng được xuất từ `export_analysis` trong notebook 08 và có trong `report_sources.csv` (52 CSV, PASS); notebook 08 đã chạy lại, số liệu không đổi. Hai script độc lập vẫn dùng cùng hàm. |
| R03 | Đã sửa, cần nhóm chốt | Bảng 1 có cột Đóng góp (%), tổng 100%: Bảo 30, Tài 20, Quang 20, Nhân 15, Tuấn 15. Đây là ước lượng theo khối lượng gói công việc, không tính theo commit; nhóm có thể điều chỉnh. |
| R04 | Đã sửa | Phân biệt phân công phần việc (theo commit) với nhật ký người chạy (chưa ghi, `operator = null`); thêm hạng mục hướng phát triển. |
| R05 | Đã sửa | Ba đoạn hướng dẫn biên tập ở Mục 5.1 và sau Bảng 8 viết lại thành văn bản báo cáo. |
| R06 | Đã sửa | Bảng 19, 20 và B1; Bảng 26 và 27; slide 13 dùng Hình 9. |
| R07 | Đã sửa | Linear Regression thấp hơn MLP ở cả ba seed; chênh lệch thay đổi theo seed nhưng thứ tự không đảo. |
| R08 | Đã sửa | R² cao nhất, MAE/RMSE thấp nhất; R² không đơn vị; kết luận epoch giới hạn ở hai fold đã kiểm tra; chỉ hai cặp RF–GB, RF–MLP có khoảng, chưa tính GB–MLP. |
| R09 | Đã sửa | Gọi là phân tích hậu kiểm; nêu kết quả chính là toàn bộ 51.063 mẫu. |
| R10 | Đã sửa | Hình 7 vẽ lại không tràn chữ, ghi importance chạy trên validation fold 5; báo cáo và slide giải thích bảy khối so với sáu phần. |
| R11 | Đã sửa | Bảng ở slide chính dùng chữ 14 pt, bảng phụ lục 13–14 pt; rút gọn nội dung bảng; slide 25–34 là dự phòng. |
| R12 | Đã sửa | Ba checklist cũ có chú thích là tài liệu lịch sử. |

Việc còn lại ngoài hai tệp: poster PM2.5, GitHub cá nhân của từng thành viên, hồ sơ nộp theo quy định của giảng viên.
