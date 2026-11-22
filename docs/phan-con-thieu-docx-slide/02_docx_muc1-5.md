# DOCX phần 1 (bìa, Mục 1 đến Mục 5): nội dung đề xuất, sẵn dán

Phạm vi: dòng 1-213 của docx_clean.txt (bản gốc docs/Nhom10_BeijingAirQuality_BaoCaoGiuaKy.docx). Mọi số liệu dưới đây đã đối chiếu với CSV/JSON/joblib trong repo (nguồn ghi ngay sau từng khối). Chỗ có `[kiểm tra bản gốc]` hoặc `[nhóm xác nhận]` là chỗ chưa thể xác nhận từ repo.

Số liệu thể hiện theo kiểu Việt Nam (dấu phẩy thập phân, dấu chấm phân cách nghìn). Giá trị trong CSV dùng dấu chấm thập phân.

---

## 0. Cấu trúc đề xuất theo khung của giảng viên

Hiện tại docx có 9 mục theo kiểu báo cáo tiến độ. Khung giảng viên (bài luận): (1) Giới thiệu, (2) Công trình liên quan, (3) Dữ liệu và phương pháp, (4) Thực nghiệm, (5) Kết luận. Đề xuất ánh xạ (Word tự cập nhật mục lục, nên chỉ cần đổi heading):

| Mục mới | Nội dung | Lấy từ mục cũ |
|---|---|---|
| Tóm tắt | 1 đoạn (xem 1.A) | 1.3 (viết lại) |
| 1. Giới thiệu | 1.1 Bối cảnh; 1.2 Thách thức; 1.3 Mục tiêu và câu hỏi nghiên cứu; 1.4 Đóng góp; 1.5 Input, Output | 2.1 đến 2.3 + mới |
| 2. Công trình liên quan | 2.1 Cơ sở lý thuyết ngắn; 2.2 Ba hướng nghiên cứu; 2.3 Nhận xét và vị trí của đề tài | mới |
| 3. Dữ liệu và phương pháp | 3.1 Dữ liệu; 3.2 EDA; 3.3 Tổng quan pipeline; 3.4 Tiền xử lý, đặc trưng, chống rò rỉ; 3.5 Mô hình; 3.6 Hàm mất mát | 3, 4, 5.1, 5.2 + mới |
| 4. Thực nghiệm | 4.1 Thiết lập; 4.2 Độ đo; 4.3 Danh sách thí nghiệm; 4.4 trở đi: kết quả từng thí nghiệm (mục tiêu, kết quả, bình luận); 4.x Đánh giá tổng thể và hạn chế | 5.3 + mới + 6 |
| 5. Kết luận | Kết luận, hạn chế, hướng phát triển | 6.7, 7.2, 7.3 |
| Tài liệu tham khảo | giữ, bổ sung (xem 2.D) | 9 |
| Phụ lục A đến C | giữ | giữ |
| Phụ lục D (mới) | Thông tin đề tài, thành viên, tiến độ, phân công | 1.1 đến 1.3, 7.1, 8 |

Phương án tối thiểu nếu không kịp đánh lại số mục: giữ nguyên số mục 1 đến 9, rút Mục 1 còn bảng 1.1 và đoạn Tóm tắt, chuyển Bảng 1 và Bảng 2 xuống phụ lục, chèn các tiểu mục mới (Thách thức, Đóng góp, Công trình liên quan, Loss, Danh sách thí nghiệm) vào đúng vị trí.

---

## 1. Bìa, mục lục, Mục 1 (Thông tin đề tài)

### 1.A. Đoạn Tóm tắt (thay cho 1.3, đặt ngay sau bìa hoặc đầu Mục 1)

> **Tóm tắt.** Đề tài xây dựng và so sánh năm mô hình hồi quy (Persistence, Linear Regression, Random Forest, Gradient Boosting dạng histogram và MLP) để dự báo nồng độ PM2.5 ở giờ kế tiếp cho 12 trạm quan trắc tại Bắc Kinh (03/2013 đến 02/2017; 412.017 mẫu có nhãn). Dữ liệu được chia theo thời điểm của nhãn: 360.954 mẫu cho huấn luyện và validation 5 fold expanding-window, 51.063 mẫu (09/2016 đến 02/2017) cho test. Siêu tham số của ba mô hình học máy được chọn bằng RMSE trung bình trên 5 fold validation, sau đó năm mô hình được chấm trên cùng tập test. Random Forest tinh chỉnh có RMSE test thấp nhất (20,9613 µg/m³; MAE 10,5906; R² 0,9550), thấp hơn Persistence 9,31% và Linear Regression 3,86%. Khoảng bootstrap 95% theo khối 7 ngày của chênh lệch RMSE giữa Random Forest và Gradient Boosting hoặc MLP tinh chỉnh chứa giá trị 0, nên chưa kết luận chắc chắn Random Forest tốt hơn hai mô hình này. Ở nhóm PM2.5 trên 250 µg/m³, Gradient Boosting và MLP tinh chỉnh có RMSE cao hơn Persistence. Kết quả chỉ áp dụng cho giai đoạn test thu-đông và các trạm đã quan sát.

Nguồn: outputs/notebooks/tables/final_test_metrics.csv (cột mae, rmse, r2, n_test); final_test_relative_improvements.csv (rmse_reduction_percent 9,3107 và 3,8593); outputs/experiments/final_test/analysis/paired_model_uncertainty.csv (ci_95_low/high); final_test_error_by_pm25_level.csv (nhóm >250, n = 3.685).

### 1.B. Bìa

- Tiêu đề "BÁO CÁO CẬP NHẬT TIẾN ĐỘ ĐỒ ÁN" không còn khớp nội dung (đã có kết quả đánh giá cuối). Nếu đây là bản nộp chính thức, đổi thành "BÁO CÁO ĐỒ ÁN MÔN MÁY HỌC" [nhóm xác nhận loại báo cáo]. Tên tệp "BaoCaoGiuaKy" cũng nên thống nhất.
- Mục lục: cập nhật sau khi chèn mục mới.

### 1.C. Mục 1.1 giữ lại dạng bảng ngắn; Bảng 1 và Bảng 2 chuyển sang Phụ lục D

Chỉnh các ô lỗi thời trong Bảng 2 khi chuyển (dòng "Tuần 5"):

> **Tuần 5.** Đã nhóm kết quả theo từng thực nghiệm; có danh sách phiên bản thư viện cố định (requirements-lock.txt, scikit-learn 1.7.2), bảng liên kết CSV với notebook sinh ra nó (outputs/notebooks/tables/report_sources.csv) và bộ kiểm thử tự động (54 test đạt khi chạy ngày 22/11/2026 trong .venv [cần xác nhận số cuối: chạy lại pytest ngay trước khi nộp]).

Nguồn: requirements-lock.txt; report_sources.csv (cột csv_path, notebook, cell_id, csv_sha256, recorded_at_utc); lệnh `.venv\Scripts\python.exe -X utf8 -B -m pytest -q -p no:cacheprovider` cho kết quả "54 passed in 17.83s" (chạy lại ngày 22/11/2026 trong lần kiểm tra này; trước đó là 31 test, nay tests/ có thêm test_diagnostics_and_validation.py và test_metrics_and_bootstrap.py).

---

## 2. Mục 2 Giới thiệu

### 2.1 Bối cảnh (giữ nguyên hai đoạn hiện có, thêm đoạn nêu vấn đề)

> Bài toán của đề tài: với mỗi trạm s và giờ t, dùng các số đo đến giờ t để dự báo nồng độ PM2.5 tại chính trạm đó ở giờ t+1. Đây là hồi quy chuỗi thời gian nhiều trạm; mô hình nhận một bảng đặc trưng (số đo hiện tại, giá trị trễ, trung bình trượt, thời gian, trạm, hướng gió) và trả về một số thực theo µg/m³.

Lưu ý đồng bộ: slide 3 trích "WHO Global Air Quality Guidelines (2021)" nhưng danh sách tài liệu tham khảo của docx không có mục này. Hoặc thêm vào tài liệu tham khảo (kiểm tra bản gốc), hoặc bỏ khỏi slide.

### 2.2 Thách thức (mục mới, đặt trước mục tiêu)

> **Thách thức.** Bài toán dự báo PM2.5 một giờ tới trên dữ liệu này có năm khó khăn, mỗi khó khăn đều quan sát được trong dữ liệu của nhóm.
>
> 1. **Mốc đơn giản đã rất mạnh.** Tự tương quan của PM2.5 là 0,969 ở độ trễ 1 giờ (trung bình 12 trạm), nên chỉ cần lặp lại giá trị hiện tại (Persistence) đã đạt R² 0,9453 trên tập test. Phần cải thiện mà mô hình học được là nhỏ: tốt nhất là giảm 9,31% RMSE so với Persistence.
> 2. **Phân phối lệch phải, đuôi dài.** Trung bình 79,79 cao hơn trung vị 55 µg/m³; phân vị 99% là 370 µg/m³; có 953 quan sát từ 500 µg/m³ trở lên. Sai số tập trung ở các đợt ô nhiễm nặng: RMSE test ở nhóm trên 250 µg/m³ là 44,59 đến 48,83 µg/m³, cao hơn nhiều so với 20,96 đến 23,11 µg/m³ trên toàn tập test.
> 3. **Dữ liệu thiếu và gián đoạn dài.** Có 74.027 ô thiếu; PM2.5 thiếu 8.739 giá trị (2,08%); có khoảng thiếu liên tục 343 giờ (PM2.5, Aotizhongxin) và 1.517 giờ (CO, Dongsi). Nhãn thiếu không được điền, đặc trưng chỉ được forward-fill tối đa 6 giờ.
> 4. **Thay đổi theo mùa và theo thời gian.** Trung bình PM2.5 theo mùa từ 64,67 (hè) đến 95,48 µg/m³ (đông); tập test chỉ gồm thu-đông (trung bình 92,18 so với 78,04 µg/m³ ở train/validation). Ở fold đầu tiên, mô hình chỉ được huấn luyện trên 03 đến 09/2013, còn validation kéo dài từ 30/09/2013 đến 01/05/2014 (qua thu, đông và đầu xuân), nên RMSE fold 1 là 23,39 µg/m³ (Linear Regression) đến 37,11 µg/m³ (Gradient Boosting ban đầu), cao hơn các fold sau của cùng mô hình (ví dụ Linear Regression 16,81 đến 20,06 ở fold 2 đến 4). Nguyên nhân (ít dữ liệu huấn luyện, khác mùa) là giải thích của nhóm, chưa được kiểm chứng bằng thí nghiệm riêng.
> 5. **Nguy cơ rò rỉ dữ liệu trong chuỗi thời gian đa trạm.** Đặc trưng trễ, trung bình trượt, forward-fill và việc nhiều trạm có cùng mốc thời gian đều có thể làm lộ thông tin tương lai nếu tạo nhãn, chia tập hoặc fit tiền xử lý sai thứ tự.

Nguồn: outputs/eda/tables/pm25_acf.csv (lag 1: 0,96862); outputs/notebooks/tables/final_test_metrics.csv (R² Persistence 0,94532); outputs/eda/tables/raw_pm25_summary.csv (mean 79,793; 50% = 55; 99% = 370); eda_conclusions.csv (953 giá trị >= 500; 74.027 ô thiếu; mùa 95,48/82,33/76,97/64,67); final_test_error_by_pm25_level.csv (rmse nhóm >250 của 5 mô hình); outputs/eda/tables/target_split_summary.csv (mean_pm25 78,044 và 92,177); random_forest_cv_metrics.csv hoặc docx Bảng 9 (RMSE fold 1: LR 23,39; RF ban đầu 29,89; GB ban đầu 37,11). Tôi đã tính lại độc lập từ data/processed: trung bình mùa, khoảng thiếu 343 và 1.517 giờ, tỷ lệ thiếu theo cột.

### 2.3 Mục tiêu và câu hỏi nghiên cứu (thay Mục 2.2)

> Mục tiêu của đề tài là xây dựng và so sánh các mô hình hồi quy dự báo nồng độ PM2.5 (µg/m³) tại cùng trạm ở giờ kế tiếp, dựa trên số liệu ô nhiễm, khí tượng và thời gian đến giờ hiện tại, đồng thời đánh giá trung thực mô hình sai ở đâu và các kết luận chắc chắn đến mức nào. Nhóm đặt ra ba câu hỏi nghiên cứu (và một câu hỏi bổ sung về mức chắc chắn).
>
> **CH1.** Random Forest, Gradient Boosting và MLP sau tinh chỉnh đạt MAE, RMSE và R² như thế nào so với Persistence và Linear Regression trên tập test theo thời gian?
>
> **CH2.** Các nhóm đặc trưng (PM2.5 hiện tại, PM2.5 trễ và trung bình trượt, chất ô nhiễm khác, khí tượng, thời gian, trạm) ảnh hưởng đến dự báo của Linear Regression và của Random Forest tinh chỉnh ở mức nào trong phép đo permutation importance theo nhóm, và hai mô hình khác nhau ra sao?
>
> **CH3.** Sai số thay đổi thế nào theo trạm, tháng, mùa và mức PM2.5 thực tế? Nhóm tách thành hai phần: (a) phân tích trên validation (300.696 dự đoán ngoài mẫu) cho hai baseline và các mô hình ban đầu; (b) phân tích trên tập test (51.063 mẫu) cho cả năm mô hình cuối, theo 12 trạm, 6 tháng, 2 mùa (thu, đông) và 6 nhóm mức PM2.5.
>
> **CH4 (tùy chọn, nếu đồng ý thêm).** Chênh lệch giữa các mô hình trên tập test và giữa các seed của MLP có đủ chắc chắn để kết luận thứ hạng không? (Bootstrap ghép cặp theo khối 7 ngày; MLP với seed 7, 42, 2026.)

Nếu thêm CH4, phải sửa slide 8 ("ba câu hỏi") và Mục 6.7 cho khớp. Nếu không thêm, đưa nội dung độ chắc chắn vào bình luận của CH1.

Nguồn các phần mở rộng: baseline_lr_group_permutation_importance.csv (notebook 02, cell evidence-nb-02); outputs/experiments/validation_diagnostics/rf_group_permutation_importance.csv (src.validation_diagnostics, hiển thị ở notebook 08, cell evidence-nb-08); outputs/experiments/final_test/analysis/final_test_error_by_{station,month,season,pm25_level}.csv; paired_model_uncertainty.csv; mlp_seed_summary.csv. Nhóm đặc trưng của LR và RF cùng một cách chia (PM2.5 hiện tại; lag và rolling; chất ô nhiễm khác; khí tượng gồm hướng gió; thời gian; trạm), xem FEATURE_GROUPS trong notebook 02 và src/validation_diagnostics.py.

### 2.4 Đóng góp của đề tài (mục mới)

> **Đóng góp.** Đề tài là một đồ án ứng dụng; nhóm không đề xuất thuật toán mới và không so sánh để tuyên bố vượt các công trình đã công bố. Các đóng góp dưới đây đều có mã nguồn và kết quả trong kho mã.
>
> 1. **Pipeline dự báo đa trạm chống rò rỉ dữ liệu.** Nhãn PM2.5(t+1) được tạo theo từng trạm trước khi forward-fill; lag và trung bình trượt chỉ dùng quá khứ; chia tập theo thời điểm của nhãn, các trạm cùng mốc thời gian luôn cùng phía của mỗi fold; imputer, encoder và scaler nằm trong pipeline và chỉ fit trên phần train của từng fold. Bộ kiểm thử pytest (54 test đạt khi chạy ngày 22/11/2026) kiểm tra các điểm này và cả vòng đời mô hình (fit, lưu, nạp, dự đoán).
> 2. **So sánh có kiểm soát năm mô hình.** Cùng 27 đặc trưng đầu vào, cùng 5 fold expanding-window, cùng tập test 51.063 mẫu; có hai mốc tham chiếu (Persistence, Linear Regression) và ba mô hình học máy ở cả cấu hình ban đầu lẫn sau tinh chỉnh. Random Forest tinh chỉnh có RMSE test thấp nhất (20,9613 µg/m³).
> 3. **Phân tích sai số và độ chắc chắn.** Sai số theo 12 trạm, 6 tháng, 2 mùa và 6 nhóm mức PM2.5 cho năm mô hình cuối; khoảng bootstrap 95% theo khối 7 ngày cho chênh lệch RMSE; kiểm tra seed và số epoch của MLP. Kết quả cho thấy Random Forest tốt nhất về tổng thể nhưng không phải ở mọi nơi: xét RMSE test theo trạm (làm tròn 2 chữ số), Random Forest thấp nhất ở 7/12 trạm, Gradient Boosting ở 3 trạm, MLP ở 2 trạm; theo tháng, Random Forest thấp nhất chỉ ở 01/2017; ở nhóm trên 250 µg/m³, Gradient Boosting và MLP kém cả Persistence.
> 4. **Đo mức phụ thuộc của mô hình vào từng nhóm đặc trưng.** Permutation importance theo nhóm cho Linear Regression và cho Random Forest tinh chỉnh; kết quả được diễn giải là mức phụ thuộc của mô hình, không phải quan hệ nhân quả.
> 5. **Khả năng truy vết.** Mỗi bảng số liên kết tới notebook, mã ô, thời điểm ghi và hash của CSV (report_sources.csv, scripts/verify_result_sources.py); môi trường phiên bản cố định (requirements-lock.txt); manifest đánh giá cuối (evaluation_manifest.json) ghi hash dữ liệu, mô hình và mã nguồn.

Nguồn: final_test_metrics.csv; final_test_error_by_station.csv (pivot rmse, 12 trạm; RF thấp nhất ở Aotizhongxin, Dongsi, Gucheng, Nongzhanguan, Tiantan, Wanliu, Wanshouxigong; GB ở Changping, Dingling, Guanyuan; MLP ở Huairou, Shunyi); final_test_error_by_month.csv (thấp nhất: 09/2016 MLP 11,10; 10/2016 GB 14,09; 11/2016 GB 18,86; 12/2016 MLP 25,94; 01/2017 RF 29,57; 02/2017 MLP 17,78); evaluation_manifest.json (run_id final-analysis-20261120T161623317892Z, dataset_sha256, git_commit ceacd7b với working_tree_dirty = true); pytest chạy lại ngày 22/11/2026 (54 passed).

### 2.5 Input, Output (giữ Bảng 2.3 cũ) và thêm hai câu phân biệt hàm mất mát với độ đo

> Hàm mất mát (loss) là đại lượng mô hình giảm khi huấn luyện; độ đo (MAE, RMSE, R²) là thước đo chất lượng dự báo trên dữ liệu đánh giá, tính bằng µg/m³ (R² không có đơn vị). Phân biệt này được trình bày chi tiết ở Mục 3.6.

---

## 3. Mục "Công trình liên quan" (mục mới, bản nháp)

Quy tắc dùng: chỉ dựa vào ba công trình ở slide 9 (Seng 2021, Bekkar 2021, Wei 2025) và các tài liệu đã có trong danh sách của docx (Chen 2017; Zhang và cộng sự 2017; Breiman 2001; Friedman 2001; Pedregosa 2011). Mô tả dưới đây lấy đúng nội dung slide 9; mọi chi tiết khác phải xác nhận từ bài gốc bởi người kiểm tra (đã đánh dấu).

### 3.A. Đoạn mở đầu

> Phần này gồm ba ý: (1) các hướng nghiên cứu dự báo chất lượng không khí liên quan trực tiếp đến dữ liệu và phương pháp của đề tài, (2) khó khăn và nhận xét của nhóm với từng hướng, (3) vị trí của đề tài so với các hướng đó.

### 3.B. Cơ sở lý thuyết (ngắn)

> Đề tài dùng bốn họ mô hình hồi quy trên bảng đặc trưng. Hồi quy tuyến tính khớp tổ hợp tuyến tính của đặc trưng bằng cách giảm tổng bình phương sai số. Random Forest (Breiman, 2001) trung bình kết quả của nhiều cây quyết định huấn luyện trên các mẫu bootstrap. Gradient Boosting (Friedman, 2001) xây các cây tuần tự, mỗi cây khớp phần sai số còn lại của tổ hợp hiện tại; đề tài dùng bản dựa trên histogram của scikit-learn (Pedregosa và cộng sự, 2011). MLP là mạng nơ-ron truyền thẳng nhiều lớp ẩn. Persistence không có tham số và dùng giá trị hiện tại làm dự báo cho giờ kế tiếp.

### 3.C. Bảng tổng hợp theo hướng nghiên cứu

| Hướng | Công trình | Dữ liệu và phạm vi (theo slide 9) | Cách làm | Khó khăn hoặc hạn chế | Nhận xét của nhóm |
|---|---|---|---|---|---|
| (i) Bộ dữ liệu Bắc Kinh và phân tích thống kê về chất lượng không khí [cần xác nhận: nhãn hướng nghiên cứu do nhóm đặt, chưa kiểm tra bản gốc] | Chen (2017): bộ dữ liệu; Zhang và cộng sự (2017) | Beijing Multi-Site Air Quality, 12 trạm, 03/2013 đến 02/2017, theo giờ (số liệu về bộ dữ liệu kiểm tra trên dữ liệu của repo); Zhang và cộng sự: [kiểm tra bản gốc: dữ liệu nào, giai đoạn nào] | Chen (2017) công bố dữ liệu. Zhang và cộng sự (2017) phân tích thống kê về cải thiện chất lượng không khí tại Bắc Kinh [kiểm tra bản gốc: phương pháp, kết luận] | Dữ liệu thiếu và gián đoạn dài; ô nhiễm phụ thuộc mạnh vào khí tượng và mùa [kiểm tra bản gốc nếu muốn nêu như hạn chế của công trình] | Đề tài dùng cùng nguồn dữ liệu nhưng làm bài toán dự báo một giờ tới; các thống kê EDA (thiếu dữ liệu, mùa, gió) của nhóm đặt cơ sở cho thiết kế đặc trưng và chia tập. |
| (ii) Học sâu chuỗi thời gian (LSTM, CNN-LSTM) | Seng và cộng sự (2021); Bekkar và cộng sự (2021) | Seng: 35 trạm Bắc Kinh, 2016 đến 2017, PM2.5, khí tượng và dữ liệu trạm lân cận (số của bài gốc theo slide 9, chưa kiểm tra bản gốc, không so sánh trực tiếp). Bekkar: dự báo PM2.5 theo giờ tại Bắc Kinh [kiểm tra bản gốc: dữ liệu, tầm dự báo, độ đo] | Seng: LSTM không gian-thời gian, kết hợp lịch sử và liên hệ giữa các trạm. Bekkar: so sánh LSTM, GRU, CNN và mô hình lai CNN-LSTM | [cần xác nhận: nhận định chung của nhóm (cần dữ liệu nhiều trạm lân cận hoặc chuỗi dài, chi phí huấn luyện cao, khó giải thích), chưa kiểm tra bản gốc; kiểm tra hạn chế chính các tác giả nêu] | Nhóm không cài đặt các kiến trúc này. Thay vào đó dùng đặc trưng trễ và trung bình trượt cho các mô hình bảng và một MLP làm đại diện nơ-ron. Kết quả của nhóm không so sánh trực tiếp với các bài này vì khác dữ liệu, thời kỳ, tầm dự báo và độ đo. |
| (iii) Mô hình cây tập hợp và mạng nơ-ron trong dự báo khu vực | Wei và cộng sự (2025) | Vùng Bắc Kinh-Thiên Tân-Hà Bắc, 2019 đến 2023, PM2.5 và O3 (số của bài gốc theo slide 9, chưa kiểm tra bản gốc, không so sánh trực tiếp) | So sánh RF, XGBoost, FCNN | [kiểm tra bản gốc: khó khăn, kết quả định lượng] | Hướng này gần nhất với thiết kế của nhóm (RF, boosting, mạng nơ-ron truyền thẳng). Khác biệt: nhóm dùng HistGradientBoostingRegressor của scikit-learn, không dùng XGBoost; dữ liệu và giai đoạn khác. |

### 3.D. Nhận xét tổng hợp và vị trí của đề tài (đoạn dán được)

> Các công trình trên dùng dữ liệu, thời kỳ, tầm dự báo và độ đo khác nhau, nên nhóm không đối chiếu RMSE hay R² trực tiếp và không nêu kết luận rằng kết quả của nhóm tốt hơn hay kém hơn các bài này. Các bài học nhóm rút ra là: (1) dữ liệu chuỗi thời gian cần đánh giá theo thứ tự thời gian, (2) cần một mốc tham chiếu đơn giản đủ mạnh để biết mô hình học được gì hơn việc lặp lại giá trị gần nhất, (3) việc dùng thông tin các trạm lân cận (Seng và cộng sự, 2021) và kiến trúc học sâu (Bekkar và cộng sự, 2021) là hướng mở rộng ngoài phạm vi của đề tài. Đề tài chọn bài toán hồi quy bảng đặc trưng trên 12 trạm với Persistence, Linear Regression, Random Forest, Gradient Boosting dạng histogram và MLP, tập trung vào đánh giá không rò rỉ, phân tích sai số và độ chắc chắn.

Hướng phát triển nên đưa vào Kết luận (chỉ liên quan trực tiếp đến phạm vi hiện tại, không thêm công nghệ mới): dùng thông tin trạm lân cận, dự báo nhiều chân trời, kiểm tra trên trạm chưa quan sát. So sánh các hàm mất mát khác (ví dụ MAE hoặc Huber) cũng là hướng phát triển, vì nhóm chưa làm thí nghiệm này.

### 3.E. Tài liệu tham khảo cần bổ sung (đúng DOI theo slide 9; các trường còn lại cần kiểm tra)

- Seng, D., và cộng sự (2021). [tiêu đề, tạp chí, tập, trang: kiểm tra bản gốc]. https://doi.org/10.1016/j.aej.2020.12.009
- Bekkar, A., và cộng sự (2021). [tiêu đề, tạp chí, tập, trang: kiểm tra bản gốc]. https://doi.org/10.1186/s40537-021-00548-1
- Wei, và cộng sự (2025). [tác giả đầy đủ, tiêu đề, tạp chí, tập, trang: kiểm tra bản gốc]. https://doi.org/10.3390/su17209211

Lỗi tham chiếu hiện có: Zhang và cộng sự (2017), Breiman (2001), Friedman (2001) và Pedregosa và cộng sự (2011) nằm trong Mục 9 nhưng không được trích dẫn ở nội dung các Mục 1 đến 8 (chỉ có Chen 2017 được trích ở 3.1). Thêm trích dẫn đúng chỗ: Breiman và Friedman ở Mục 3.B hoặc 5.2; Pedregosa ở 5.2 và 5.3 (môi trường); Zhang ở Mục "Công trình liên quan".

---

## 4. Mục 3 Mô tả dữ liệu (rà soát)

Các số liệu trong 3.1 đến 3.3 đều khớp: 12 trạm, 35.064 dòng mỗi trạm, 420.768 dòng, 19 cột sau chuẩn hóa (dataset shape 420768 x 19), 412.017 mẫu có nhãn, 360.954 và 51.063; trung bình 79,79, trung vị 55, phân vị 95% = 242, 99% = 370, 953 quan sát >= 500, tỷ lệ thiếu PM2.5 theo trạm 1,089% đến 2,718%.

Điều cần sửa hoặc thêm:

1. **Xóa đoạn cuối Mục 3.3** ("Pipeline nạp 12 tệp PRSA. Hai CSV có cấu trúc OHLCV ... nằm ngoài phạm vi"). Đây là ghi chú về đóng gói kho mã, không phải đặc điểm biến mục tiêu. Chuyển sang Phụ lục C hoặc README (data/raw/ hiện vẫn còn data.csv và test.csv ngoài phạm vi).
2. **Thêm một câu giải thích 8.751 dòng không có nhãn:**

> Tổng 420.768 dòng gốc cho 412.017 mẫu có nhãn; 8.751 dòng còn lại gồm 12 dòng giờ cuối của 12 trạm (không có giờ t+1) và 8.739 dòng mà PM2.5 ở giờ t+1 bị thiếu.

Nguồn: outputs/eda/tables/dataset_counts.csv (raw_rows 420768; labeled_rows 412017; raw_missing_pm25 8739); tôi đã chạy add_features trên dữ liệu: 8.751 dòng không có target, trong đó 12 dòng không có target_datetime.

3. **Gắn nguồn dưới Bảng 3 và đoạn 3.2:** "Notebook 01, ô evidence-nb-01; outputs/eda/tables/dataset_counts.csv, target_split_summary.csv" (xem report_sources.csv, ghi lúc 2026-11-20T16:09:52 UTC).

---

## 5. Mục 4 Khám phá và tiền xử lý

### 4.1 EDA: rút gọn và gắn nguồn

Toàn bộ số liệu trong 4.1.1 đến 4.1.6 đã được đối chiếu và đúng: 74.027 ô thiếu; CO 4,92%, O3 3,16%, NO2 2,88%, SO2 2,14%, PM2.5 2,08%; khí tượng 0,08% đến 0,10%; khoảng thiếu 1.517 giờ (CO, Dongsi, 11/06 đến 13/08/2013) và 343 giờ (PM2.5, Aotizhongxin, 17/12 đến 31/12/2014); mùa 95,48/82,33/76,97/64,67; trạm Dingling 65,99, Huairou 69,63, Changping 71,10, các trạm còn lại 79,49 đến 86,19; Pearson PM10 0,884, CO 0,790, NO2 0,667, WSPM -0,272; ACF 0,969/0,926/0,883/0,767/0,596/0,404 tại lag 1/2/3/6/12/24; bảng gió (Bảng 4) và các hướng gió. Không phải sửa số.

Đề xuất chỉnh:

1. **Rút gọn theo yêu cầu "gọn, ít lặp".** Giữ Hình 2 (phân bố, tuyến tính và log), Hình 4 (trung bình theo tháng, mốc test) và Hình 6 (ACF) trong thân bài. Chuyển Hình 1 (tỷ lệ thiếu), Hình 3 (theo giờ/tháng/trạm) và Hình 5 (ma trận tương quan) xuống phụ lục hoặc bỏ nếu đã có bảng số. Mỗi tiểu mục 4.1.x chỉ giữ 2 đến 3 câu kết luận kèm "Điều này ảnh hưởng thiết kế như thế nào" (ví dụ: ACF cao giải thích lag 1, 2, 3, 6, 12, 24 và sức mạnh của Persistence; gió/mùa giải thích test chỉ thu-đông cần báo cáo theo tháng).
2. **Thêm dòng nguồn mỗi hình/bảng**, ví dụ: "Nguồn: notebook 01, ô evidence-nb-01; outputs/eda/tables/pm25_acf.csv (trung bình 12 trạm, hàng mean_station_correlation); sinh lại bằng `python -m src.eda`." Với Bảng 4: pm25_by_wind_speed.csv (mean_pm25: 103,49; 100,97; 84,65; 59,22; 37,46; 26,02).
3. **Lưu ý truy vết:** các số về mùa, Pearson, khoảng thiếu liên tục và tỷ lệ thiếu nằm trong outputs/eda/eda_conclusions.csv (không nằm trong report_sources.csv nên không có hash). Tôi đã tính lại chúng từ data/processed/beijing_air_quality_standardized.csv và khớp; nhóm nên ghi "nguồn: eda_conclusions.csv, đã tính lại từ CSV chuẩn hóa".
4. Hình 1 đến 6 "được vẽ lại từ file dữ liệu chuẩn hóa" (đúng, outputs/eda/figures/ có pm25_autocorrelation.png, pm25_distribution_linear_log.png, pm25_wind_relationships.png); nên nêu lệnh tạo lại.

### 4.2 Tiền xử lý: bổ sung chi tiết bảng 5 (đã đúng, thêm hai ý)

Thêm dòng vào Bảng 5 hoặc chú thích:

| Vấn đề | Cách xử lý đã triển khai (bổ sung) |
|---|---|
| Lag và trung bình trượt khi có giá trị thiếu | Lag và trung bình trượt của PM2.5 tính từ PM2.5 đã forward-fill (tối đa 6 giờ, theo từng trạm); trung bình trượt cần đủ cửa sổ (6 hoặc 24 giờ trước t), nếu thiếu thì để trống rồi điền trung vị fit trên train và có cột cờ thiếu. |
| Thứ tự thao tác | Tạo nhãn t+1 (dịch theo trạm) trước, sau đó forward-fill đặc trưng, sau đó tạo lag/rolling; chỉ khi đó mới chia tập. Việc forward-fill chỉ dùng giá trị quá khứ của cùng trạm nên không làm lộ thông tin tương lai. |

Nguồn: src/features.py (hàm add_features: dòng tạo target trước khối `ffill(limit=ffill_limit)`; `values.shift(1).rolling(window, min_periods=window)`).

### 4.3 Xây dựng đặc trưng: phân biệt trước và sau tiền xử lý, bổ sung bảng đối chiếu

Thêm đoạn sau (ngay sau đoạn "Pipeline hiện tạo 27 đặc trưng"):

> **Từ 27 đặc trưng đến 79 cột.** 27 là số cột đầu vào thô trước khi qua bộ tiền xử lý. Sau tiền xử lý, mô hình nhận 79 cột: 25 đặc trưng số (đã điền trung vị; có chuẩn hóa StandardScaler với Linear Regression và MLP), 25 cột cờ báo thiếu (một cột cho mỗi đặc trưng số), 12 cột One-Hot của station và 17 cột One-Hot của wd (16 hướng gió và nhãn Unknown). Số 79 là kích thước của pipeline đã fit, không phải hằng số cho mọi dữ liệu.

Bảng 3.x (thay Bảng 6, thêm cột Lý do/ghi chú):

| Đặc trưng theo proposal | Trạng thái | Ghi chú |
|---|---|---|
| PM2.5 lag 1, 2, 3, 6, 12, 24 giờ | Đã có (6 cột) | Tính theo từng trạm |
| Trung bình trượt 6 và 24 giờ | Đã có (2 cột) | Cửa sổ lấy các giờ trước t |
| Độ lệch so với trung bình trượt | Chưa đưa vào | Chưa thử, chưa có bằng chứng về tác động |
| Lag của các biến khí tượng chính | Chưa đưa vào | Chưa thử, chưa có bằng chứng về tác động |
| Giờ, tháng, thứ trong tuần | Đã có dưới dạng sin/cos (6 cột) | |
| Cờ cuối tuần | Chưa có | Thứ trong tuần đã có dạng sin/cos |
| station, wd (One-Hot) | Đã có | 12 và 17 cột sau One-Hot |

Câu giải thích hoãn: "Nhóm giữ nguyên một bộ 27 đặc trưng cho mọi mô hình để so sánh công bằng; các đặc trưng chưa đưa vào là hướng mở rộng và chưa được đánh giá." (Cơ sở: README mục R13 "Giữ bộ 27 đầu vào để so sánh công bằng".) Tránh mô tả các đặc trưng này như đã dùng.

Nguồn: src/features.py (NUMERIC_FEATURES: 25 cột; CATEGORICAL_FEATURES: station, wd); pipeline đã lưu models/random_forest_tuned.joblib nạp bằng scikit-learn 1.7.2: get_feature_names_out cho ra 79 tên = 25 numeric + 25 numeric_missing + 29 categorical (12 station + 17 wd gồm wd_Unknown); outputs/notebooks/tables/final_model_configuration.csv (raw_input_columns 27; transformed_columns 79).

### 4.4 Chống rò rỉ: sửa bullet cuối, thêm hai bullet

Thay bullet "Bộ kiểm thử tự động ...":

> Bộ kiểm thử tự động (tests/, 54 test đạt khi chạy ngày 22/11/2026 bằng pytest trong .venv) kiểm tra nạp dữ liệu, chia thời gian, tạo nhãn và đặc trưng, tiền xử lý, vòng đời mô hình (fit, lưu, nạp, dự đoán cho bốn họ mô hình), quy tắc biên nhóm PM2.5, bootstrap ghép cặp, ACF theo trạm và bằng chứng nguồn của notebook.

Thêm:

> Siêu tham số được chọn chỉ bằng RMSE trên 5 fold validation; các fold được tạo từ phần train/validation (nhãn trước 01/09/2016) và không chứa mẫu test.
>
> Điểm validation của cấu hình tốt nhất hơi lạc quan vì cấu hình được chọn trên chính các fold đó; bảng test là phép đánh giá trên dữ liệu giữ riêng.

Nguồn: src/data_loader.py (time_split dùng target_datetime; cv_folds nhóm theo target_datetime); tests/test_model_evaluation.py (test_model_fit_save_reload_predict, test_saved_final_models_predict_in_supported_environment, test_error_groups_use_target_time_and_right_closed_thresholds, test_paired_bootstrap_keeps_pairing_and_is_reproducible, test_eda_acf_respects_station_and_hourly_gaps).

---

## 6. Mục 5 Phương pháp và mô hình

### 5.1 Pipeline: mô tả bằng lời và sửa Hình 7

Hình 7 là ảnh nên nội dung không đọc được từ văn bản docx; theo mô tả của bản nháp trước nó có 6 khối [cần xác nhận khi mở file docx]: "Dữ liệu gốc, Chuẩn hóa, Nhãn và đặc trưng, Chia theo thời gian, Đánh giá validation, Đánh giá cuối", chú thích dưới hình nói về điền khuyết và chuẩn hóa từ train. Vấn đề: (a) khối 2 "Chuẩn hóa" gây nhầm với StandardScaler, thực chất là chuẩn hóa cấu trúc (ghép datetime); (b) không có khối tiền xử lý fit theo fold, khối mô hình và khối tinh chỉnh; (c) khác Hình pipeline ở slide 14 (Dữ liệu, Mục tiêu, Chia dữ liệu, Tiền xử lý, Dự báo, Đánh giá). Đề xuất vẽ lại thành 7 khối dưới đây và dùng cùng một hình cho docx và slide 14.

> **Hình 7 (vẽ lại). Pipeline của đề tài gồm bảy khối.** (1) Nạp 12 CSV PRSA, ghép datetime, giữ NA (420.768 dòng, 19 cột). (2) Tạo nhãn PM2.5(t+1) theo trạm, rồi forward-fill đặc trưng tối đa 6 giờ, rồi tạo 27 đặc trưng (lag, rolling, sin/cos); chỉ dùng thông tin đến giờ t. (3) Chia theo thời điểm của nhãn: train/validation 360.954 mẫu và test 51.063 mẫu; 5 fold expanding-window trên train/validation. (4) Tiền xử lý trong pipeline, fit trên train của từng fold: điền trung vị, cờ thiếu, One-Hot, StandardScaler (chỉ Linear Regression, MLP; MLP còn chuẩn hóa nhãn). (5) Năm mô hình: Persistence, Linear Regression, Random Forest, Gradient Boosting dạng histogram, MLP; tinh chỉnh RandomizedSearchCV cho ba mô hình học máy. (6) Đánh giá validation (MAE, RMSE, R² trung bình 5 fold) và chọn cấu hình theo RMSE. (7) Đánh giá test cho năm mô hình đã chốt; phân tích sai số, permutation importance, bootstrap.

Thêm đoạn dẫn nhập: "Pipeline gồm bảy khối; ba khối đầu xử lý dữ liệu, khối 4 đến 6 là mô hình và chọn cấu hình trên validation, khối 7 là đánh giá cuối và phân tích." (Nguyên tắc của giảng viên: nói "có N phần" rồi đi từng phần.)

### 5.2 Các mô hình (thay Bảng 7)

Bảng 7 hiện đúng với cấu hình ban đầu nhưng thiếu tham số quan trọng và hoàn toàn không có cấu hình tinh chỉnh dù Mục 6.3 và test dùng chúng. Bản thay thế (đã đối chiếu với notebook 03, 04, 06, models/*_metadata.json, bộ pipeline lưu trong models/*.joblib nạp bằng scikit-learn 1.7.2 và final_model_configuration.csv):

**Bảng 7. Mô hình, cấu hình ban đầu và cấu hình sau tinh chỉnh**

| Mô hình | Cấu hình ban đầu (validation) | Cấu hình sau tinh chỉnh (khóa trước khi chấm test) | Đầu vào của mô hình |
|---|---|---|---|
| Persistence | Dự báo PM2.5(t+1) = PM2.5(t) đã forward-fill; nếu còn thiếu dùng trung vị nhãn tập huấn luyện. Không có tham số. | Không áp dụng | PM2.5(t) |
| Linear Regression | LinearRegression (bình phương tối thiểu, có hệ số chặn) sau StandardScaler; notebook 02 kiểm tra thêm biến thể cắt dự báo âm về 0 (RMSE validation 19,2227 so với 19,2950). | Không có siêu tham số để chọn | 79 cột sau tiền xử lý |
| Random Forest | RandomForestRegressor: n_estimators=20, max_depth=16, min_samples_leaf=5, max_features=0,7, bootstrap, criterion=squared_error, random_state=42. | n_estimators=50, max_depth=None, min_samples_leaf=20, max_features=0,7 | 79 cột (không chuẩn hóa) |
| Gradient Boosting | HistGradientBoostingRegressor (không phải GradientBoostingRegressor chuẩn và không phải XGBoost): max_iter=200, learning_rate=0,1, early_stopping=False, các tham số còn lại mặc định (max_leaf_nodes=31, min_samples_leaf=20, l2_regularization=0), loss=squared_error, random_state=42. | learning_rate=0,06937 (0,0693663), max_iter=100, max_leaf_nodes=127, min_samples_leaf=200, l2_regularization=1,0 | 79 cột (không chuẩn hóa) |
| MLP | MLPRegressor, hai lớp ẩn (64, 32), ReLU, Adam, alpha=0,001, batch_size=512, learning_rate_init=0,001, max_iter=60, n_iter_no_change=8, early_stopping=False, random_state=42; đầu vào và nhãn đều chuẩn hóa. | hidden_layer_sizes=(32, 16), learning_rate_init=0,003, alpha=0,0001, batch_size=256, max_iter=40; lần fit cuối dừng sau 19 epoch | 79 cột đã chuẩn hóa |

Chú thích dưới bảng: "Cấu hình ban đầu: notebook 03, 04, 06 (các ô định nghĩa RF_PARAMS, GB_PARAMS, mlp_params). Cấu hình tinh chỉnh: tệp models/*_tuned_metadata.json và final_model_configuration.csv. Số tổ hợp thử và không gian tìm kiếm nằm ở đoạn "Tinh chỉnh siêu tham số" của Mục thiết lập thực nghiệm (hoặc chuyển thành Phụ lục A2)."

Mô tả ngắn của Bảng 7: cần nêu rõ (1) "Gradient Boosting" trong báo cáo là HistGradientBoostingRegressor; (2) Persistence và Linear Regression không có bước tinh chỉnh; (3) số liệu validation ở Mục 6.1 và test ở Mục 6.4 ứng với cột nào.

**Hình mô hình (cần thêm):**

> **Hình 8 (mới). Kiến trúc MLP sau tinh chỉnh.** Đầu vào 27 cột thô, qua tiền xử lý thành 79 cột, qua lớp ẩn 79 → 32 (ReLU), lớp ẩn 32 → 16 (ReLU), lớp ra 16 → 1, rồi đổi ngược chuẩn hóa nhãn về µg/m³. Tổng 3.105 tham số huấn luyện (79×32+32, 32×16+16, 16×1+1). Mạng dùng Adam, loss squared_error cộng phạt L2 (alpha = 0,0001).

Nguồn: outputs/notebooks/tables/final_model_configuration.csv (cột layer_shapes: [[79, 32], [32, 16], [16, 1]]; alpha 0,0001; loss squared_error); nạp models/mlp_tuned.joblib: coefs_ có hình dạng (79,32), (32,16), (16,1), n_iter_ = 19, transformer = StandardScaler; số tham số 3.105 là phép tính từ các hình dạng này. Nếu muốn một hình so sánh, vẽ thêm hai ô nhỏ cho RF (50 cây, trung bình dự báo) và HGB (100 cây nối tiếp, tối đa 127 lá). Ghi chú: cấu hình MLP ban đầu có hình dạng (79,64), (64,32), (32,1) và dừng sau 25 epoch ở lần fit cuối.

### 5.3 Hàm mất mát và tiêu chí huấn luyện (tiểu mục mới, đặt ngay sau 5.2; đánh số 3.6 nếu đổi cấu trúc)

> **Hàm mất mát và tiêu chí.** Mục này tách "đại lượng mô hình giảm khi học" (loss, tiêu chí) khỏi "thước đo chất lượng" (metric). Cả bốn mô hình có học đều tối ưu dạng bình phương sai số.
>
> **Bảng 8. Loss hoặc tiêu chí của từng mô hình**
>
> | Mô hình | Đại lượng được tối thiểu hóa khi huấn luyện | Ghi chú theo code |
> |---|---|---|
> | Persistence | Không có (không huấn luyện) | Chỉ lấy PM2.5(t) |
> | Linear Regression | Tổng bình phương sai số (bình phương tối thiểu) | Không có phạt; đầu vào qua StandardScaler |
> | Random Forest | criterion = squared_error: chọn điểm tách giảm phương sai của nhãn trong nút | Mỗi cây trên mẫu bootstrap; dự báo là trung bình các cây |
> | Gradient Boosting (histogram) | loss = squared_error; mỗi cây mới khớp phần sai số còn lại | Có l2_regularization (0 ban đầu, 1,0 sau tinh chỉnh) |
> | MLP | loss = squared_error cộng phạt L2 theo alpha; tối ưu bằng Adam | Nhãn được chuẩn hóa khi huấn luyện, dự báo được đổi ngược về µg/m³ trước khi chấm |
>
> Độ đo MAE, RMSE và R² được tính ở đơn vị µg/m³ trên dự báo cuối cùng, không phải trên loss. Riêng đường loss huấn luyện của MLP (file outputs/experiments/validation_diagnostics/mlp_loss_curves.csv, cột loss_scaled_target; hình mlp_convergence.png) được tính trên nhãn đã chuẩn hóa, nên không phải đường RMSE ở µg/m³ và không so sánh trực tiếp với RMSE trong các bảng. Tiêu chí chọn siêu tham số là RMSE trung bình 5 fold (scoring neg_root_mean_squared_error), nhất quán với việc cả bốn mô hình học theo bình phương sai số. Nhóm chưa thực hiện thí nghiệm so sánh hàm mất mát khác (ví dụ MAE hoặc Huber); nội dung này được đưa vào hướng phát triển.

Nguồn: models/*.joblib (get_params: RandomForestRegressor criterion squared_error; HistGradientBoostingRegressor loss squared_error, l2_regularization 0,0 và 1,0; MLPRegressor loss squared_error, alpha 0,001 và 0,0001; TransformedTargetRegressor với StandardScaler); final_model_configuration.csv (cột loss, criterion, alpha); validation_diagnostics/README.md ("loss trong huấn luyện với target đã chuẩn hóa, không đo trực tiếp bằng µg/m³"); notebooks 05 và 07 (RandomizedSearchCV scoring="neg_root_mean_squared_error", refit=False, n_jobs=1).

### 5.4 Thiết lập thực nghiệm (viết lại Mục 5.3 cũ)

**Giữ nguyên** các số: 360.954 và 51.063 mẫu; 5 fold expanding-window nhóm theo thời điểm nhãn; tập huấn luyện từ 60.258 đến 300.886 mẫu (khoảng 60 nghìn đến 301 nghìn) và mỗi fold validation khoảng 60 nghìn mẫu (59.858 đến 60.595); trung bình PM2.5 nhãn 78,04 (train/validation) và 92,18 µg/m³ (test). Nguồn: random_forest_fold_overview.csv; target_split_summary.csv.

**Sửa các điểm sau:**

1. Bullet "Phân tích theo tháng trên test hiện có cho hai baseline" đã lỗi thời. Notebook 08 và outputs/experiments/final_test/analysis/ hiện có sai số theo tháng, mùa, trạm và mức PM2.5 cho cả năm mô hình. Thay bằng: "Kết quả test của năm mô hình được phân tích theo 12 trạm, 6 tháng, 2 mùa và 6 nhóm mức PM2.5 (final_test_error_by_*.csv)."
2. Làm rõ độ lệch chuẩn là độ lệch chuẩn mẫu (ddof=1) của 5 giá trị theo fold (đã kiểm: LR RMSE 5 fold 23,39; 16,81; 20,06; 18,84; 17,37 có trung bình 19,2950 và độ lệch chuẩn mẫu 2,6205 đúng bằng bảng).
3. Thêm khối Độ đo, Seed, Môi trường, Vai trò dữ liệu và Nguồn số liệu dưới đây.

**Độ đo (đoạn dán được):**

> MAE = trung bình |y − ŷ|; RMSE = căn bậc hai của trung bình (y − ŷ)²; R² = 1 − tổng bình phương sai số / tổng bình phương độ lệch so với trung bình. MAE và RMSE tính bằng µg/m³, càng thấp càng tốt; R² không có đơn vị. Sai số có dấu (residual) = y thực − ŷ dự báo; giá trị dương nghĩa là dự báo thấp hơn số đo. Điểm validation là trung bình số học của metric theo 5 fold (độ lệch chuẩn mẫu), không phải RMSE tính gộp các dự đoán ngoài mẫu. Các nhóm mức PM2.5 đóng bên phải: <=35, (35,75], (75,115], (115,150], (150,250], >250; giá trị đúng bằng biên thuộc nhóm thấp hơn. Với nhóm có khoảng nồng độ hẹp, R² có thể âm hoặc dao động mạnh (ví dụ nhóm <=35 trên test), nên các bảng nhóm dùng MAE, RMSE và residual.

Nguồn: outputs/experiments/final_test/analysis/evaluation_manifest.json (residual_definition "y_true - y_pred"; pm25_intervals "right-closed"); src/analysis_groups.py; final_test_error_by_pm25_level.csv (R² nhóm <=35: Persistence -2,10, RF -1,42).

**Seed và tái lập (đoạn dán được):**

> Mọi mô hình ngẫu nhiên (Random Forest, Gradient Boosting, MLP) và ba lượt RandomizedSearchCV (Random Forest, Gradient Boosting, MLP) dùng random_state = 42; Persistence và Linear Regression là tất định. Chẩn đoán MLP dùng thêm seed 7 và 2026; permutation importance dùng seed 42 (30.000 mẫu validation của fold 5, 5 lần hoán vị); bootstrap ghép cặp dùng seed 42, 2.000 lần lặp, khối 7 ngày lịch, 181 ngày lịch của giai đoạn test. Môi trường: Python 3.13 trên Windows, NumPy 2.3.3, pandas 2.3.3, scikit-learn 1.7.2, SciPy 1.17.1, joblib 1.5.3, matplotlib 3.10.8 (requirements-lock.txt, requirements.txt). Các pipeline đã lưu chỉ nạp được bằng scikit-learn 1.7.2 (bản 1.8.0 báo lỗi khi dự đoán), vì vậy không dùng kernel Python hệ thống.

Nguồn: notebooks 03, 04, 05, 06, 07 (random_state 42); outputs/experiments/final_test/analysis/evaluation_manifest.json (python_version 3.13.12; packages; uncertainty: n_bootstrap 2000, block_days 7, seed 42; n_calendar_days 181 trong paired_model_uncertainty.csv); validation_diagnostics (seed 7/42/2026); rf_group_permutation_importance.csv (n_validation_sample 30000, n_repeats 5, seed 42, fold 5). Lưu ý nhỏ: metadata của RF và GB tinh chỉnh ghi Python 3.13.9 (lưu ngày 11/11/2026), các mô hình còn lại và lần kiểm chứng ngày 20/11/2026 ghi 3.13.12; báo cáo nên viết "Python 3.13" thay vì một bản vá cụ thể, hoặc ghi cả hai.

**Vai trò của các tập dữ liệu và lịch sử dùng test (đoạn dán được, viết để không thể bị phản bác):**

> **Cách dùng validation và test.** Tập train/validation (360.954 mẫu, nhãn trước 01/09/2016) được dùng để huấn luyện, so sánh mô hình trên 5 fold và chọn siêu tham số; tiêu chí chọn là RMSE trung bình 5 fold thấp nhất (RandomizedSearchCV, refit=False, các fold không chứa mẫu test). Sau khi chọn, mỗi mô hình được huấn luyện lại trên toàn bộ 360.954 mẫu và lưu; hồ sơ lưu của Random Forest và Gradient Boosting tinh chỉnh (ngày 11/11/2026) và của MLP tinh chỉnh (ngày 18/11/2026) ghi test_evaluated = false tại thời điểm lưu. Notebook 08 nạp các pipeline đã lưu, không huấn luyện lại, chấm năm mô hình trên 51.063 mẫu test; các phân tích sau đó (sai số theo nhóm, bootstrap, chẩn đoán MLP, permutation importance) chỉ để mô tả và kiểm tra, không dùng để đổi cấu hình hay chọn lại mô hình. Về lịch sử, ít nhất một bản notebook 02 trước đây (commit ngày 07/11/2026) bật sẵn tùy chọn RUN_FINAL_TEST nên hai baseline (không có siêu tham số học từ test) đã có thể được chấm trên test sớm hơn; vì vậy nhóm chỉ khẳng định rằng không siêu tham số hay lựa chọn mô hình nào được quyết định bằng kết quả test, không khẳng định rằng tập test chưa từng được xem trước bước đánh giá cuối. [nhóm xác nhận câu này]

Nguồn: models/random_forest_tuned_metadata.json và gradient_boosting_tuned_metadata.json (created_at 2026-11-11T08:45, test_used_for_tuning false, test_evaluated false); models/mlp_tuned_metadata.json (created_at 2026-11-18T23:28:59, test_evaluated false); experiment_log.csv (ghi chú "Configurations fixed before test evaluation" ở các dòng *_test); lịch sử git của notebooks/02_model_training_baseline.ipynb (tại commit 9047dd8 ngày 07/11/2026, RUN_FINAL_TEST mặc định là True; bản làm việc hiện tại là False; chuỗi RUN_FINAL_TEST xuất hiện từ commit dbaafe4 ngày 01/11/2026); docs/ra-soat-do-an-va-ke-hoach-khac-phuc.md mục R05. Không nên dùng cụm "test chưa từng được xem".

**Tinh chỉnh siêu tham số (thay bullet 5):**

> RandomizedSearchCV với scoring neg_root_mean_squared_error trên đúng 5 fold của pipeline chung, refit=False, random_state=42: Random Forest 8 tổ hợp trong lưới 192 tổ hợp (n_estimators 50/100/200; max_depth 12/16/24/None; min_samples_leaf 2/5/10/20; max_features 0,3/0,5/0,7/1,0); Gradient Boosting 20 tổ hợp (learning_rate loguniform 0,02 đến 0,3; max_iter 100/200/300/500; max_leaf_nodes 15/31/63/127; min_samples_leaf 20/50/100/200; l2_regularization 0/0,1/1/10); MLP 8 tổ hợp trong lưới 243 tổ hợp (hidden_layer_sizes (32,16)/(64,32)/(128,64); learning_rate_init 0,0003/0,001/0,003; alpha 0,0001/0,001/0,01; batch_size 256/512/1024; max_iter 40/60/100). Ngân sách tìm kiếm nhỏ và nhiều tham số được chọn nằm ở biên lưới (ví dụ min_samples_leaf=20 của Random Forest; max_leaf_nodes=127 và min_samples_leaf=200 của Gradient Boosting; learning_rate_init=0,003 và các giá trị nhỏ nhất của hidden_layer_sizes, alpha, batch_size, max_iter của MLP), nên cấu hình chọn được là tốt nhất trong các tổ hợp đã thử, chưa chắc là tối ưu.

Nguồn: models/random_forest_tuned_metadata.json, gradient_boosting_tuned_metadata.json, mlp_tuned_metadata.json (trường tuning.search_space, n_iter, best_params); outputs/notebooks/tables/tuning_{random_forest,gradient_boosting,mlp}_search_results.csv (số hàng 8, 20, 8). Thời gian tìm kiếm: RF 1.532,5 giây, GB 691,4 giây, MLP 931,0 giây (cấu hình máy không có trong repo [nhóm bổ sung nếu cần]).

**Nguồn gốc số liệu (đoạn dán được, thay cho câu "Nhật ký experiment_log.csv ..."):**

> Số liệu trong báo cáo lấy từ các CSV trong outputs/ và được liên kết với notebook, mã ô, thời điểm ghi và hash trong outputs/notebooks/tables/report_sources.csv. Notebook 01 đến 04, 06 và 08 được thực thi lại và ghi nguồn vào ngày 20/11/2026 (UTC 16:09 đến 16:20). Với notebook 05 và 07, bảng nguồn ở chế độ verified_saved_search: notebook chỉ đối chiếu kết quả tìm kiếm đã lưu, không chạy lại RandomizedSearchCV; kết quả tìm kiếm gốc được lưu cùng mô hình ngày 11/11/2026 (RF, GB) và 18/11/2026 (MLP). Người thực hiện từng lần chạy: [nhóm xác nhận]; báo cáo không suy ra từ tác giả commit.

Nguồn: report_sources.csv (cột mode, recorded_at_utc: nb 01 16:09:52, 02 16:11:04, 03 16:13:04, 04 16:14:01, 05 16:15:34, 06 16:16:07, 07 16:15:37, 08 16:20:04, ngày 2026-11-20). Không chạy scripts/verify_result_sources.py trong rà soát này vì script ghi chỉ mục vào repo; cần chạy lại trước khi nộp.

### 5.5 Danh sách thí nghiệm (mục mới, đặt trước Mục 6.1)

Câu mở đầu dán được: "Nhóm có bảy nhóm thí nghiệm. Mỗi nhóm trả lời một câu hỏi và được trình bày theo thứ tự mục tiêu, kết quả, bình luận ở Mục 6."

**Bảng. Danh sách thí nghiệm** (đã kiểm tra: mọi notebook và artifact trong cột dưới đây đều tồn tại trong repo)

| Mã | Thí nghiệm | Câu hỏi (chứng minh điều gì) | Notebook | Artifact chính |
|---|---|---|---|---|
| TN1 | Hai baseline trên validation | Persistence mạnh đến đâu? Linear Regression cải thiện metric nào, và có giảm đồng thời MAE không? | 02 | baseline_cv_summary.csv, baseline_cv_metrics.csv; outputs/experiments/experiments01 (ket_qua_tong_hop.csv) |
| TN2 | Ba mô hình ở cấu hình ban đầu | Random Forest, Gradient Boosting, MLP có vượt hai baseline trên validation không, và dao động theo fold ra sao? | 03, 04, 06 | random_forest_cv_summary.csv, gradient_boosting_cv_summary.csv, mlp_cv_summary.csv; experiments02 |
| TN3 | Tinh chỉnh siêu tham số | Cấu hình được chọn cải thiện RMSE validation bao nhiêu, đặc biệt ở fold nào? | 05, 07 (chế độ verified_saved_search) | tuning_random_forest_search_results.csv, tuning_gradient_boosting_search_results.csv, tuning_mlp_search_results.csv, *_tuned_cv_summary.csv; experiments03 |
| TN4 | Đánh giá cuối trên test | Cấu hình đã khóa của năm mô hình đạt kết quả thế nào trên cùng 51.063 mẫu test? | 08 | final_test_metrics.csv, final_test_relative_improvements.csv, final_model_configuration.csv |
| TN5 | Phân tích sai số | Mô hình hay sai ở trạm, tháng, mùa hoặc mức PM2.5 nào? Có thua baseline ở đâu không? | 02, 04, 06 (validation); 08 (test) | baseline_error_analysis.csv, gradient_boosting_error_by_level.csv, mlp_error_by_group.csv; final_test_error_by_{station,month,season,pm25_level}.csv, final_test_worst_cases.csv |
| TN6 | Đóng góp đặc trưng | Linear Regression và Random Forest phụ thuộc vào nhóm đặc trưng nào? | 02 (LR); 08 (RF, qua src.validation_diagnostics) | baseline_lr_group_permutation_importance.csv; rf_group_permutation_importance.csv |
| TN7 | Độ ổn định và mức chắc chắn | Seed, số epoch và bootstrap cho phép kết luận thứ hạng tới mức nào? | 08 | paired_model_uncertainty.csv; mlp_seed_summary.csv; mlp_validation_diagnostics.csv; mlp_loss_curves.csv |

Câu kết nên có: "Nhóm không thực hiện thí nghiệm bóc tách bằng cách huấn luyện lại với từng bộ đặc trưng, không so sánh các hàm mất mát và không thử đặc trưng ngoài bộ 27; permutation importance (TN6) đo mức phụ thuộc của mô hình đã fit, không thay thế thí nghiệm bóc tách." (Cơ sở: README R04 nói chưa chạy ablation đầy đủ.)

### 5.6 Các hình cần thêm hoặc sửa (tóm tắt)

| Hình | Việc cần làm |
|---|---|
| Hình 7 pipeline | Vẽ lại 7 khối (mục 5.1 trên), dùng chung với slide 14 |
| Hình mới: MLP | Kiến trúc [79,32], [32,16], [16,1] (mục 5.2 trên) |
| Hình mới (tùy chọn) | outputs/experiments/validation_diagnostics/mlp_convergence.png kèm chú thích "loss trên nhãn đã chuẩn hóa, không phải RMSE µg/m³" |
| Hình 1, 3, 5 | Chuyển phụ lục hoặc bỏ nếu đã có bảng số |
| Hình 8 chia fold | Giữ (đúng với random_forest_fold_overview.csv); thêm nhãn số mẫu mỗi fold nếu còn chỗ |
