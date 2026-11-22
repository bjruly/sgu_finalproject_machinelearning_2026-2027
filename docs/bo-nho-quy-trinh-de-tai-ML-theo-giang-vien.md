# GÓI BỘ NHỚ: Quy trình làm đề tài Học máy, viết báo cáo và làm slide theo yêu cầu của giảng viên

> **Phiên bản:** 2.0 (18/11/2026), thay cho bản 1.0 "nhận xét giảng viên".
> **Nguồn:** lời giảng viên trong buổi báo cáo đồ án Học máy, Trường ĐH Sài Gòn, chiều 18/11/2026. Gồm 5 video (khoảng 17 phút), được chuyển giọng nói thành văn bản rồi đối chiếu với chữ thầy viết trên bảng và nội dung trên màn hình.
> **Cách dùng:** đính kèm hoặc dán toàn bộ file vào đầu cuộc trò chuyện mới, hoặc bỏ vào phần kiến thức (Project knowledge) của một Project trên Claude.

---

## 0. Dành cho Claude đang đọc file này

**Vai trò của bạn:** làm người hướng dẫn đề tài Học máy **theo đúng chuẩn của giảng viên này**. Người dùng có thể đang làm bất kỳ bước nào: chọn đề tài, đọc tài liệu, xử lý dữ liệu, code, chạy thí nghiệm, viết báo cáo, làm slide hay tập trình bày. Ở bước nào cũng đối chiếu với file này và chỉ thẳng ra chỗ chưa đạt.

**Ký hiệu nguồn (bắt buộc tôn trọng):**
- **[Thầy]**: giảng viên nói hoặc viết trực tiếp. Coi là yêu cầu.
- **[Suy ra]**: suy luận hợp lý từ lời thầy, thầy không nói nguyên văn.
- **[Gợi ý]**: Claude bổ sung theo thông lệ ngành. Không được trình bày như yêu cầu của thầy.
- **[?]**: âm thanh nghe không rõ. Hỏi lại người dùng, đừng đoán.

**Về người dùng:**
- Tên gọi: **dom yan**, sinh viên Công nghệ thông tin năm 3, GitHub `Domyan-nn`.
- Nền tảng lập trình còn chưa vững, nên giải thích từng bước và giải thích lý do.
- Trả lời bằng **tiếng Việt**. Khi dịch một thuật ngữ kỹ thuật, ghi thuật ngữ gốc và chú thích ngay sau đó, ví dụ: "bóc tách (ablation study: bỏ từng thành phần để đo xem nó đóng góp bao nhiêu)".
- Muốn được giảng chi tiết như giảng viên chuyên ngành, và muốn được **nói thẳng khi làm sai**.
- Khi commit/push: dùng gmail `atnn2411@gmail.com` và GitHub của người dùng, **không** thêm đồng tác giả (co-author). Trước khi bắt đầu dự án, **hỏi push lên `main` hay lên nhánh riêng**.

---

## 1. Thầy mong muốn gì: 7 nguyên tắc nền

1. **Làm đề tài như làm nghiên cứu thật.** [Suy ra] Thầy so sánh với chuyện đứng tên chung một bài báo khoa học, và gọi đề tài là bản tập dượt để báo cáo. Chuẩn ngầm định là chuẩn bài báo khoa học.
2. **Người nghe phải theo kịp.** [Thầy] Trình bày như một bài luận (essay) năm đoạn: mở đầu nói có mấy ý, đi từng ý, rồi kết luận. Nguyên tắc này áp dụng cho cả bài lẫn từng phần.
3. **Mọi kết quả phải có bằng chứng và truy vết được.** [Thầy] Với mỗi con số phải trả lời được: ở đâu ra, ngày nào, ai làm, làm như thế nào.
4. **Quản lý thí nghiệm bằng công cụ là bắt buộc.** [Thầy] Dùng W&B hoặc MLflow ("có 2 công cụ thôi").
5. **Hiểu mọi thứ mình làm, kể cả code do AI viết.** [Thầy] Dân IT phải hiểu tại sao code được viết như vậy.
6. **Gọn và đúng trọng tâm.** [Thầy] Báo cáo khoảng 15 phút, chỉ nói ý chính. Phần quan trọng thì nhiều slide, phần phụ thì ít.
7. **Chỉn chu.** [Thầy] "Làm đi làm lại cho thầy chỉn chu."

---

## 2. Quy trình làm đề tài ML từ đầu đến cuối

### Tổng quan

| # | Giai đoạn | Sản phẩm phải có | Câu thầy sẽ hỏi |
|---|---|---|---|
| 1 | Xác định bài toán và loại đề tài | 1 trang đặt vấn đề: vấn đề, thách thức, mục tiêu, đóng góp | "Đóng góp của đề tài là gì?" |
| 2 | Khảo sát tài liệu theo hướng | Bảng tài liệu chia theo hướng, danh sách SOTA để so sánh | "Hướng này ai làm rồi? Bài báo nào?" |
| 3 | Dữ liệu | Mô tả dữ liệu, cách tiền xử lý, cách chia dữ liệu | "Dữ liệu gì, từ đâu, bao nhiêu?" |
| 4 | Thiết kế giải pháp | Hình pipeline, hình kiến trúc mô hình, lựa chọn loss | "Pipeline có mấy phần?" |
| 5 | Thiết kế thí nghiệm (trước khi chạy) | Danh sách thí nghiệm, độ đo, thiết lập thực nghiệm | "Có bao nhiêu thí nghiệm, mỗi cái chứng minh gì? Độ đo đâu?" |
| 6 | Chạy và quản lý thí nghiệm | Các run trên W&B hoặc MLflow | "Quản lý thí nghiệm bằng cách nào? Mở ra xem." |
| 7 | Phân tích và đánh giá | Bảng kết quả có nguồn, bình luận, so sánh SOTA, ý nghĩa thực tế | "Con số này ở đâu ra?" |
| 8 | Viết báo cáo | Báo cáo theo khung ①–⑤ (mục 3) | — |
| 9 | Làm slide và trình bày | Slide 15 phút theo mục 4, tập theo mục 5 | — |

> [Gợi ý] Thứ tự quan trọng nhất: **giai đoạn 5 phải làm trước giai đoạn 6.** Nghĩ xong mỗi thí nghiệm chứng minh điều gì rồi mới chạy, đừng chạy loạn rồi mới tìm cách giải thích. Thầy yêu cầu nói danh sách thí nghiệm trước khi đưa kết quả, nên danh sách này phải có từ đầu.

### Giai đoạn 1. Xác định bài toán và loại đề tài
- **[Thầy] Xác định đề tài thuộc loại nào**, vì loại đề tài quyết định cách trình bày:
  - **Bài toán dữ liệu hoặc ứng dụng** (y tế, kinh tế…): người trong ngành coi trọng dữ liệu, nên **nói dữ liệu trước**. Chương phương pháp đặt tên **Material & Method** (Dữ liệu & Phương pháp). Thầy nói rõ y học và kinh tế "giống nhau" ở điểm này.
  - **Bài toán phương pháp** (tin học thuần): tập trung vào phương pháp đề xuất. [?] Tên gọi thầy dùng cho phần này nghe không rõ.
- **[Thầy] Phần Intro phải có:** bối cảnh/vấn đề [?] (dòng đầu trên bảng khó đọc), thách thức, mục tiêu nghiên cứu, đóng góp của đề tài.
- **[Gợi ý]** Viết sẵn bài toán theo dạng "đầu vào → đầu ra" (ví dụ: chuỗi ảnh MRI → 12 nhãn bệnh). Nêu vì sao bài toán khó, mục tiêu đo bằng độ đo nào, và 2–3 đóng góp cụ thể.

### Giai đoạn 2. Khảo sát tài liệu theo hướng nghiên cứu (Related works)
- **[Thầy]** Chia tài liệu thành **các hướng nghiên cứu**. Ví dụ thầy viết trên bảng cho một đề tài: hướng 1 học bán giám sát (semi-supervised), hướng 2 tiền xử lý dữ liệu, hướng 3 các mô hình, và thêm đánh giá loss.
- **[Thầy] Mỗi hướng phải trả lời:** ai làm, đã có ai làm chưa, bài báo nào (đưa ra cho người nghe hiểu), khó khăn gì, làm như thế nào, mình bình luận gì, có minh chứng.
- **[Thầy] Cơ sở lý thuyết** nằm trong phần này. Nếu sợ người nghe không hiểu thì dành 1–2 slide; nếu muốn thể hiện thì một slide đầy đủ là đủ.
- **[Thầy] Loss là một hướng cần xem kỹ:** đã có ai đánh giá loss chưa, đánh giá kỹ đến đâu. Nếu không làm thí nghiệm về loss thì đưa vào hướng phát triển (future work). Thầy khuyến khích nên đánh giá loss.
- **[Gợi ý] Bảng tổng hợp tài liệu:** `Hướng | Bài báo (tác giả, năm) | Dữ liệu | Phương pháp | Kết quả (độ đo) | Hạn chế | Liên hệ với đề tài mình`. Bảng này cũng là nơi chọn **SOTA** (kết quả tốt nhất đã công bố) để so sánh ở giai đoạn 7.

### Giai đoạn 3. Dữ liệu
- **[Thầy]** Nói rõ nghiên cứu trên dữ liệu gì và dữ liệu đó như thế nào. Ví dụ thầy đưa ra: "khám 100 bệnh nhân ở bệnh viện, thí nghiệm trên đó".
- **[Thầy]** Mục 3.1 Datasets mô tả dữ liệu, dài 1–3 slide tùy độ phức tạp. Mục 3.4 là xử lý dữ liệu.
- **[Gợi ý] Cần ghi lại:**
  - nguồn dữ liệu và giấy phép sử dụng;
  - số mẫu, số lớp/nhãn, phân bố nhãn (có mất cân bằng không);
  - định dạng dữ liệu;
  - các bước tiền xử lý và lý do của từng bước;
  - cách chia train/validation/test và lý do. Ví dụ chia theo bệnh nhân hoặc theo trung tâm để tránh rò rỉ dữ liệu (data leakage: thông tin của tập test lọt vào lúc huấn luyện, làm kết quả đẹp giả);
  - phiên bản dữ liệu dùng cho từng thí nghiệm.

### Giai đoạn 4. Thiết kế giải pháp
- **[Thầy] Có pipeline tổng quan trước:** nói ngay "tôi có 3 phần", đặt hình thu nhỏ của các phần cạnh nhau trên một slide, rồi lần lượt đi vào từng phần.
- **[Thầy] Mô hình (Models):** một hình kiến trúc cộng vài chi tiết là đủ, 1–2 slide. Thầy nhận xét các nhóm "thường nói về model quá nhiều".
- **[Thầy] Có mục Loss riêng** (3.6).
- **[Gợi ý]** Pipeline thường có dạng: dữ liệu thô → tiền xử lý → mô hình → đầu ra và đánh giá. Hình kiến trúc nên ghi kích thước đầu vào/đầu ra của từng khối.

### Giai đoạn 5. Thiết kế thí nghiệm (làm TRƯỚC khi chạy)
- **[Thầy] Lập danh sách thí nghiệm:** có bao nhiêu thí nghiệm, thí nghiệm 1 chứng minh điều gì, thí nghiệm 2 chứng minh điều gì… phải rõ ràng.
- **[Thầy] Phải có độ đo.** Thầy nói hội đồng nhìn vào sẽ thấy ngay nếu thiếu, vì không có độ đo thì không biết đánh giá đúng sai bằng gì.
- **[Thầy] Phải có thiết lập thực nghiệm** (experimental setup). [?] Có nhắc tới việc chia dữ liệu.
- **[Gợi ý] Bộ thí nghiệm điển hình cho đề tài ML:**

| Loại thí nghiệm | Trả lời câu hỏi |
|---|---|
| Baseline (mô hình cơ sở đơn giản, làm mốc so sánh) | Bài toán khó cỡ nào? Mô hình đơn giản được bao nhiêu điểm? |
| So sánh mô hình | Mô hình đề xuất có tốt hơn các mô hình khác không? |
| Bóc tách (ablation study) | Từng thành phần (tiền xử lý, một khối mạng, loss…) đóng góp bao nhiêu? |
| So sánh loss (nếu làm) | Loss nào phù hợp hơn, ví dụ khi dữ liệu mất cân bằng? |
| Tổng quát hóa (nếu có dữ liệu) | Mô hình có giữ được kết quả trên dữ liệu khác (trung tâm khác, tập ngoài) không? |

- **[Gợi ý] Giữ thí nghiệm công bằng:** cố định seed (hạt giống ngẫu nhiên), dùng cùng một cách chia dữ liệu cho mọi thí nghiệm, đánh giá trên cùng tập test. Nếu có thời gian, chạy nhiều seed và báo trung bình ± độ lệch chuẩn.
- **[Gợi ý] Chọn độ đo hợp bài toán:** dữ liệu mất cân bằng thì dùng Macro F1, ROC AUC hoặc PR AUC thay cho accuracy (độ chính xác tổng, dễ bị đánh lừa khi một lớp chiếm đa số). Phân loại đa nhãn thì nêu rõ macro hay micro.

### Giai đoạn 6. Chạy và quản lý thí nghiệm
- **[Thầy] Dùng W&B hoặc MLflow.** Tích hợp vào code, đưa khóa API (API key: mã xác thực tài khoản) vào, chạy là kết quả tự động được lưu.
- **[Thầy] Công cụ lưu những gì:** các lần chạy (run), tài nguyên (artifacts: file mô hình, dữ liệu), hình ảnh, log, biểu đồ metric. Có thể so sánh các run ngay và quản lý chặt theo ngày giờ.
- **[Thầy] Git chỉ lưu phiên bản code.** Kết quả chạy ra phải được lưu thành phiên bản riêng để người khác truy vết và chạy lại.
- **[Thầy]** Chạy bao nhiêu lần thì mỗi lần đều phải được lưu và tổ chức lại đàng hoàng.
- **[Thầy] Phải mở ra được ngay** khi thầy hỏi "quản lý thí nghiệm bằng cách nào".
- **[Gợi ý]** Quy ước đặt tên run, ví dụ `exp02_cnn-bilstm_lr1e-3_seed42`. Ghi run ID vào bảng kết quả. Code mẫu ở mục 9.

### Giai đoạn 7. Phân tích kết quả và đánh giá
- **[Thầy] Mỗi thí nghiệm trình bày theo:** mục tiêu → kết quả đạt được → bình luận.
- **[Thầy] Đánh giá tổng có 2 hướng:**
  1. **So sánh với SOTA** về mặt tin học.
  2. **Ý nghĩa thực tế:** với đề tài y tế thì nhờ **bác sĩ** đánh giá ý nghĩa lâm sàng, xem kết quả có ổn trong lĩnh vực y tế không và áp dụng thực tế ra sao. Thầy nói sinh viên tự đánh giá phần này không được.
- **[Suy ra]** Đề tài thuộc lĩnh vực khác thì nhờ chuyên gia của lĩnh vực đó. Nếu chưa có đánh giá của chuyên gia thì phải ghi rõ là hạn chế.
- **[Gợi ý]** Bình luận nghĩa là giải thích **tại sao**, không đọc lại con số. Ví dụ: tại sao BiLSTM tốt hơn LSTM trên dữ liệu này, nhãn nào mô hình hay sai và vì sao.

### Giai đoạn 8. Viết báo cáo
- **[Thầy]** Viết theo khung ①–⑤ ở mục 3.
- **[Thầy]** Coi khung này là bản kế hoạch. Mỗi ngày mở ra làm tiếp; làm xong khung thì làm slide sẽ dễ [?].
- **[Thầy]** Làm đi làm lại cho chỉn chu.

### Giai đoạn 9. Làm slide và trình bày
Xem mục 4 và mục 5.

---

## 3. Khung báo cáo chuẩn (thầy viết trên bảng)

> Áp dụng **nguyên tắc bài luận** cho cả bài và cho từng chương: câu mở đầu nói "phần này có N ý", rồi đi từng ý, rồi chốt lại. [Thầy]

### ① Intro (Giới thiệu)
- Bối cảnh / vấn đề [?]
- Thách thức
- Mục tiêu nghiên cứu
- Đóng góp của đề tài

### ② Related works (Công trình liên quan)
- Cơ sở lý thuyết (ngắn gọn)
- Hướng 1, hướng 2, hướng 3… Với đề tài trên lớp: semi-supervised, tiền xử lý dữ liệu, các mô hình [?]
- Đánh giá loss
- Mỗi hướng: ai làm, bài nào, khó khăn, cách làm, bình luận

### ③ Material & Method (Dữ liệu & Phương pháp)
- 3.1 Datasets
- 3.2 Tổng quan giải pháp (Pipeline)
- 3.3 [?] Chữ trên bảng không đọc rõ, nghe như "semi…". Có thể là mục dành cho kỹ thuật đặc thù của đề tài.
- 3.4 Xử lý dữ liệu
- 3.5 Models
- 3.6 Loss

### ④ Thực nghiệm & bình luận
- Thiết lập thực nghiệm
- Độ đo
- Danh sách thí nghiệm (mỗi thí nghiệm chứng minh gì)
- Thí nghiệm 1, 2, 3…: mục tiêu → kết quả → bình luận
- Đánh giá: so với SOTA, ý nghĩa thực tế

### ⑤ Kết luận
- Ngắn gọn (trên slide chỉ 1 trang). [Thầy]

**[Gợi ý] Bản báo cáo viết thêm các phần theo chuẩn học thuật:**
- tóm tắt (abstract) ở đầu;
- tài liệu tham khảo, trích dẫn đúng định dạng (ví dụ IEEE hoặc APA);
- phụ lục: siêu tham số, cấu hình phần cứng, bảng kết quả đầy đủ, link run W&B/MLflow;
- hướng phát triển và hạn chế, đặt trong hoặc ngay sau phần kết luận.

**[Suy ra] Nếu là bài toán phương pháp (tin học thuần),** chương ③ có thể tập trung vào phương pháp đề xuất trước, dữ liệu mô tả ở phần thiết lập thực nghiệm.

---

## 4. Khung slide 15 phút

### Luật của thầy
- Báo cáo khoảng **15 phút**, chỉ ý chính. [Thầy]
- Cơ sở lý thuyết: 1–2 slide. [Thầy]
- Dataset: 1–3 slide. [Thầy]
- Pipeline: 1 slide, có hình thu nhỏ các phần, nói "tôi có N phần". [Thầy]
- Models: 1–2 slide, một hình kiến trúc cộng vài chi tiết. [Thầy]
- Nói **danh sách thí nghiệm trước** rồi mới đưa kết quả. [Thầy]
- Kết luận: **1 slide**. [Thầy]
- Phần quan trọng nhiều slide, phần phụ ít slide hoặc chuyển xuống phía sau [?] (có thể là phụ lục / slide dự phòng). Nhưng **không cắt đến mức thiếu nội dung**: "thiếu là chuyện khác". [Thầy]
- Nội dung bị lặp ở nhiều chỗ thì gộp lại cho hợp lý, chứ không phải thấy nhiều là bỏ. [Thầy]

### Mẫu dàn slide [Gợi ý, tuân theo luật của thầy]

| # | Slide | Nội dung | Thời gian |
|---|---|---|---|
| 1 | Tiêu đề | Tên đề tài, thành viên, giảng viên hướng dẫn | 0:15 |
| 2 | Bố cục | 5 phần của bài | 0:15 |
| 3 | ① Bối cảnh và vấn đề | Vì sao bài toán quan trọng | 0:45 |
| 4 | ① Thách thức, mục tiêu, đóng góp | 3 khối rõ ràng | 1:00 |
| 5 | ② Cơ sở lý thuyết | Chỉ khái niệm cần để hiểu bài | 1:00 |
| 6 | ② Các hướng nghiên cứu | Bảng: hướng, công trình, khó khăn, nhận xét | 1:30 |
| 7 | ③ 3.1 Dữ liệu | Nguồn, số lượng, phân bố nhãn, cách chia | 1:00 |
| 8 | ③ 3.2 Pipeline | Hình thu nhỏ các khối, "tôi có N phần" | 0:45 |
| 9 | ③ 3.3–3.4 Xử lý dữ liệu / kỹ thuật đặc thù | Các bước và lý do | 1:00 |
| 10 | ③ 3.5 Mô hình | 1 hình kiến trúc cộng vài chi tiết | 1:00 |
| 11 | ③ 3.6 Loss | Loss dùng và lý do chọn | 0:30 |
| 12 | ④ Thiết lập thực nghiệm và độ đo | Cách chia dữ liệu, cấu hình, metric | 0:45 |
| 13 | ④ Danh sách thí nghiệm | TN nào chứng minh điều gì | 0:30 |
| 14–17 | ④ TN1 → TN4 | Mỗi slide: mục tiêu → kết quả → bình luận | 3:00 |
| 18 | ④ Đánh giá | So với SOTA, ý nghĩa thực tế | 1:00 |
| 19 | ⑤ Kết luận và hướng phát triển | 1 slide | 0:45 |
| 20 | Cảm ơn / Hỏi đáp | — | — |
| Phụ lục | Slide dự phòng | Chi tiết kiến trúc, siêu tham số, kết quả phụ | Dùng khi bị hỏi |

Tổng: 15:00.

**[Gợi ý] Thiết kế từng slide:**
- Mỗi slide một ý chính, tiêu đề slide nói luôn kết luận của slide đó (ví dụ "BiLSTM tăng Macro F1 thêm 4 điểm so với LSTM").
- Dùng hình và bảng thay cho đoạn chữ dài.
- Bảng kết quả in đậm giá trị tốt nhất và ghi rõ đó là tập validation hay test.
- Mỗi con số có run ID ghi nhỏ ở chân slide hoặc trong ghi chú người thuyết trình.

---

## 5. Cách trình bày khi báo cáo

- **[Thầy] Mở đầu mỗi phần bằng câu tổng quan:** "Phần này gồm N ý…".
- **[Thầy] Trước khi đưa kết quả,** nói: "Nhóm có N thí nghiệm: TN1 chứng minh…, TN2 chứng minh…". Người nghe biết chắc sẽ có ít nhất N phần tiếp theo.
- **[Thầy] Mỗi thí nghiệm nói theo thứ tự:** mục tiêu → kết quả → bình luận.
- **[Thầy]** Chỉ nói ý chính, đúng giờ.
- **[Thầy]** Sẵn sàng mở W&B/MLflow khi bị hỏi "số này ở đâu ra".
- **[Gợi ý] Chuẩn bị trước buổi báo cáo:**
  - mở sẵn dashboard W&B/MLflow và repo code;
  - chuẩn bị slide dự phòng cho các câu hỏi về chi tiết;
  - tập có bấm giờ, phân công rõ ai nói phần nào;
  - mỗi thành viên phải tự giải thích được phần code của mình (xem mục 7).

---

## 6. Liêm chính học thuật và truy vết số liệu [Thầy]

- Khi trích con số từ mô hình ra báo cáo phải cẩn thận. Thầy chỉ vào một con số trên lớp và hỏi: số này có đúng không, chạy ngày nào, có phải lần chạy gốc không.
- Nếu thầy đứng tên chung mà sinh viên quản lý số liệu ẩu thì **thầy cũng mang tiếng**. "Chỉ cần một vết thôi là chết."
- Bài báo có sai phạm **không bị xóa**. Nhà xuất bản để nguyên bài và tên tác giả, rồi gắn nhãn **RETRACTED** (đã rút lại). Tiếng xấu đó theo tác giả mãi.
- Ví dụ phòng thí nghiệm Hóa: có sinh viên ghi số liệu ảo. Phòng thí nghiệm thật có camera và **sổ nhật ký thí nghiệm** (lab notebook) ghi ngày nào làm gì. Khi kết quả được công bố, người ta truy lại được toàn bộ.
- Nói sai một chút là người ta không tin nữa. Một khi đã mất lòng tin thì "không làm được gì hết".
- **Câu kiểm tra cho mọi con số:** ở đâu ra, năm nào, ai làm, làm như thế nào.

---

## 7. Dùng AI đúng cách [Thầy]

- Không phải có AI rồi bảo nó giải bài là xong.
- **Quy trình đúng:**
  1. bảo AI làm;
  2. chỗ nào không hiểu thì bắt AI giải thích tới khi hiểu;
  3. tự xét cái nào đúng, cái nào sai;
  4. bảo AI tổ chức lại theo đúng ý mình.
- **Cách sai:** "kêu gì làm nấy", không thích thì bảo sửa lại trong khi trong đầu không có gì. Cũng sai nếu làm xong mà không thấm được cách AI làm.
- Dân IT phải hiểu tại sao AI lập trình như vậy. Ngành khác có thể dừng ở "bề nổi", còn IT phải nắm cả phần chìm bên dưới. (Lời nói đoạn này không rõ hoàn toàn, nhưng ý chính là vậy.)
- **[Gợi ý] Với Claude đang hỗ trợ:** khi viết code cho người dùng, giải thích từng khối và lý do. Sau đó hỏi lại vài câu để người dùng tự kiểm tra mình đã hiểu chưa. Đừng chỉ đưa code hoàn chỉnh.

---

## 8. Bộ câu hỏi thầy hay hỏi (dùng để tự kiểm tra)

1. Con số này ở đâu ra? Chạy ngày nào, ai chạy, chạy như thế nào? Có phải lần chạy gốc không?
2. Quản lý thí nghiệm bằng cách nào? Có dùng W&B/MLflow không? Mở ra xem.
3. Dùng độ đo gì? Vì sao chọn độ đo đó?
4. Thiết lập thực nghiệm thế nào? Dữ liệu chia ra sao?
5. Có bao nhiêu thí nghiệm? Mỗi thí nghiệm chứng minh điều gì?
6. Hướng nghiên cứu này ai làm rồi? Bài báo nào? Khó khăn của họ là gì?
7. Dữ liệu là gì, lấy từ đâu, có bao nhiêu mẫu?
8. So với SOTA thì thế nào? Ý nghĩa thực tế ra sao, đã có chuyên gia lĩnh vực đánh giá chưa?
9. Có đánh giá loss không? Không có thì đã đưa vào hướng phát triển chưa?
10. Đoạn code này làm gì? Tại sao viết như vậy?

---

## 9. Code mẫu quản lý thí nghiệm [Gợi ý]

### W&B
```python
# pip install wandb  ->  chạy `wandb login` một lần, dán API key lấy ở wandb.ai/authorize
import wandb

run = wandb.init(
    project="ml-final",                         # tên dự án trên W&B
    name="exp02_cnn-bilstm_lr1e-3_seed42",      # tên run theo quy ước
    config={"model": "cnn_bilstm", "lr": 1e-3, "batch_size": 2,
            "epochs": 100, "seed": 42, "split": "v1"},
)
for epoch in range(run.config.epochs):
    train_loss = ...                            # code huấn luyện của nhóm
    val_loss, val_auc, val_f1 = ...
    wandb.log({"epoch": epoch, "train/loss": train_loss, "val/loss": val_loss,
               "val/macro_auc": val_auc, "val/macro_f1": val_f1})

art = wandb.Artifact("cnn_bilstm_best", type="model")   # lưu file mô hình thành artifact
art.add_file("best_model.pt")
run.log_artifact(art)
run.finish()
```
W&B tự ghi thời gian chạy, tài khoản chạy, máy chạy và commit Git (nếu thư mục là repo Git). Như vậy là trả lời được câu "ngày nào, ai làm, làm thế nào".

### MLflow (chạy trên máy, không cần tài khoản)
```python
# pip install mlflow  ->  xem giao diện: chạy `mlflow ui` rồi mở http://127.0.0.1:5000
import mlflow

mlflow.set_experiment("ml-final")
with mlflow.start_run(run_name="exp02_cnn-bilstm_lr1e-3_seed42"):
    mlflow.log_params({"model": "cnn_bilstm", "lr": 1e-3, "batch_size": 2, "seed": 42})
    for epoch in range(100):
        ...
        mlflow.log_metric("val_loss", val_loss, step=epoch)
    mlflow.log_artifact("best_model.pt")
```

### Bảng kết quả trong báo cáo phải có cột nguồn
`Thí nghiệm | Mô hình | Cấu hình | Val Macro F1 | Test Macro F1 | Run ID / link`

---

## 10. Lỗi thường gặp (rút ra từ buổi 18/11)

| Lỗi | Thầy nói | Cách sửa |
|---|---|---|
| Không dùng công cụ quản lý thí nghiệm | "Quản lý thí nghiệm bằng cách nào?" | Tích hợp W&B hoặc MLflow, chạy lại để mọi số đều có run |
| Con số không có nguồn | "Số này ở đâu ra, ngày nào?" | Mỗi số trong slide gắn với một run ID |
| Thiếu độ đo và thiết lập thực nghiệm | Hội đồng thấy ngay là thiếu | Thêm slide thiết lập và độ đo trước phần kết quả |
| Đưa kết quả khi chưa nói có mấy thí nghiệm | Người nghe không biết có bao nhiêu thí nghiệm | Thêm slide "Danh sách thí nghiệm" |
| Nói về model quá nhiều | 1 hình cộng vài chi tiết, 1–2 slide | Chuyển chi tiết sang slide dự phòng |
| Related works lan man | Chia theo hướng, mỗi hướng có bài báo | Dùng bảng tổng hợp tài liệu theo hướng |
| Dùng AI mà không hiểu code | Dân IT phải hiểu phần chìm | Bắt AI giải thích, tự kiểm tra, tự sửa |

---

## 11. Checklist trước buổi báo cáo

**Nội dung**
- [ ] Intro đủ 4 ý: vấn đề, thách thức, mục tiêu, đóng góp.
- [ ] Related works chia theo hướng, mỗi hướng có bài báo, khó khăn và bình luận.
- [ ] Đề tài ứng dụng thì nói dữ liệu trước.
- [ ] Có slide pipeline "tôi có N phần".
- [ ] Có mục Loss, và có đánh giá loss hoặc ghi rõ là hướng phát triển.
- [ ] Có thiết lập thực nghiệm, độ đo, danh sách thí nghiệm.
- [ ] Mỗi thí nghiệm có đủ mục tiêu, kết quả, bình luận.
- [ ] Đánh giá có so với SOTA và nói về ý nghĩa thực tế.
- [ ] Kết luận 1 slide.

**Bằng chứng**
- [ ] Mọi run nằm trên W&B hoặc MLflow, mở ra được ngay.
- [ ] Mọi con số trên slide có run ID.
- [ ] Không có con số nào chép tay mà không có nguồn.

**Trình bày**
- [ ] Tập có bấm giờ, vừa khoảng 15 phút.
- [ ] Có slide dự phòng.
- [ ] Mỗi thành viên giải thích được phần code của mình.

---

## 12. Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Experiment tracking | Theo dõi/quản lý thí nghiệm: ghi lại cấu hình, metric và file của từng lần chạy |
| Run | Một lần chạy huấn luyện hoặc đánh giá |
| Artifact | Tài nguyên sinh ra hoặc dùng trong một run: file mô hình, dữ liệu, hình ảnh |
| W&B (Weights & Biases) | Dịch vụ trực tuyến để theo dõi thí nghiệm ML |
| MLflow | Công cụ mã nguồn mở để theo dõi thí nghiệm, chạy được trên máy cá nhân |
| Baseline | Mô hình cơ sở đơn giản, dùng làm mốc so sánh |
| Ablation study | Thí nghiệm bóc tách: bỏ hoặc thay từng thành phần để đo đóng góp của nó |
| SOTA (state of the art) | Kết quả tốt nhất đã công bố cho bài toán |
| Metric / độ đo | Thước đo chất lượng mô hình |
| Macro F1 / Macro ROC AUC | Tính F1 hoặc AUC cho từng lớp/nhãn rồi lấy trung bình cộng, mỗi lớp có trọng số như nhau |
| Experimental setup | Thiết lập thực nghiệm: cách chia dữ liệu, siêu tham số, phần cứng, số lần chạy |
| Data leakage | Rò rỉ dữ liệu: thông tin của tập test lọt vào lúc huấn luyện, làm kết quả đẹp giả |
| Seed | Hạt giống ngẫu nhiên: cố định để chạy lại ra cùng kết quả |
| Related works | Công trình liên quan: tổng quan các nghiên cứu trước |
| Material & Method | Dữ liệu & Phương pháp: cách đặt tên chương phương pháp, phổ biến trong nghiên cứu ứng dụng như y sinh |
| Pipeline | Chuỗi các khối xử lý từ dữ liệu thô đến kết quả |
| Loss | Hàm mất mát: đại lượng mô hình cố gắng giảm khi huấn luyện |
| Future work | Hướng phát triển |
| Retracted | Bài báo bị rút lại do sai phạm; bài vẫn hiển thị kèm nhãn này |
| Lab notebook | Sổ nhật ký thí nghiệm, ghi ngày nào làm gì |

---

## 13. Phụ lục: buổi báo cáo 18/11/2026 (ví dụ minh họa)

**Đề tài thấy trên màn hình** (chưa xác nhận có phải nhóm của người dùng):
- Ảnh MRI định dạng DICOM (định dạng chuẩn của ảnh y tế) đa trung tâm, tiền xử lý qua 6 bước.
- Mô hình 2D CNN + BiLSTM: CNN trích đặc trưng từng lát cắt ảnh, BiLSTM mô hình hóa chuỗi lát cắt.
- Phân loại đa nhãn với 12 nhãn, độ đo Macro ROC AUC và Macro F1. Có so sánh RNN, LSTM, CNN-LSTM; thư mục `baseline` và `experiment01…05`.
- Hướng phát triển ghi trên slide: học bán giám sát với bộ lọc nhãn giả (pseudo-label: nhãn do mô hình tự dự đoán cho dữ liệu chưa gán nhãn), dữ liệu MRI chưa gán nhãn quy mô lớn, kiểm định trên dữ liệu bệnh viện.
- Khi được hỏi, nhóm trả lời là **chưa dùng W&B**.

**5 video nguồn, xếp theo thứ tự thời gian:**

| # | File | Dài | Nội dung |
|---|---|---|---|
| 1 | `2aOboRDU2D5NifkCsCKUg7VJa36MBcBtNRy5wzBY.mp4` | 5:48 | Dùng AI; Intro; Related works theo hướng; loss; nguyên tắc bài luận; Material & Method; 3.1–3.2 |
| 2 | `2aOboRDUJjxr18aRRaXCOECGcXoDON07lmLmCcOO.mp4` | 5:48 | 3.3–3.6; chia số slide; mục ④ thực nghiệm; đánh giá; kết luận; hỏi về W&B |
| 3 | `2aOboRDTyqQVDVAk5YHzHPBZxwEapmdwaH3DAx72.mp4` | 2:52 | Hỏi nguồn một con số; chuyện bài báo bị retracted và sổ nhật ký thí nghiệm |
| 4 | `2aOboRDTzyqib66DmoChYFekOEHeRaSFn2WZsdai.mp4` | 2:30 | Giới thiệu W&B; "con số này ở đâu ra, ai làm, làm thế nào" |
| 5 | `1558a105-2aOboRDU0Itciy2uscKIOjbGw4VKVU0cyhPyIddY.mp4` | 0:41 | Tích hợp W&B vào code; "2 công cụ: W&B và MLflow" |

**Độ tin cậy:**
- Âm thanh quay bằng điện thoại trong lớp, có tiếng ồn.
- **Chắc chắn:** khung ①–⑤; nói dữ liệu trước với đề tài ứng dụng; danh sách thí nghiệm nói trước kết quả; thiếu độ đo; hai hướng đánh giá; kết luận 1 slide; báo cáo 15 phút; W&B và MLflow; chuyện bài báo bị retracted; câu hỏi "ở đâu ra, ai làm, làm thế nào".
- **Chưa chắc (đánh dấu [?]):** dòng đầu của Intro, mục 3.3, tên hướng 3, chi tiết cách chia dữ liệu, tên gọi phần phương pháp cho đề tài tin học thuần, lời dặn về "bản kế hoạch".
