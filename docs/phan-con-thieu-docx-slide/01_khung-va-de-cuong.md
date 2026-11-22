# Rà soát cấu trúc DOCX + PPTX theo khung của giảng viên (Nhóm 10, PM2.5 t+1)

Phạm vi: chỉ hồi quy PM2.5 chuỗi thời gian. Không đề xuất W&B/MLflow, thư viện/mô hình mới, nội dung MRI. Không đề xuất đổi cấu hình mô hình đã khóa.
Nguồn đọc: `docx_clean.txt` (DOCX), `pptx.txt` (PPTX, thứ tự trình chiếu 1-28), `phancong.txt`, `docs/nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md` (gọi tắt YC), `docs/ra-soat-do-an-va-ke-hoach-khac-phuc.md`, `docs/bo-nho-quy-trinh-de-tai-ML-theo-giang-vien.md`, `README.md`, `outputs/README.md`, `outputs/notebooks/tables/report_sources.csv`, proposal PDF, các CSV ở `outputs/experiments/final_test/analysis/` và `outputs/experiments/validation_diagnostics/`, `experiment_log.csv`, ruột file .pptx/.docx (đã giải nén vào scratchpad, chỉ đọc).
Mọi số trong "văn bản đề xuất" lấy từ CSV đã đọc hoặc từ chính DOCX/PPTX (đã ghi nguồn); các số DOCX/PPTX không tự tính lại ở đây vì có agent khác kiểm số.

---------------------------------------------------------------------

## (A) Ma trận phủ khung giảng viên

Ký hiệu: Đ = đủ; T = thiếu hẳn; L = có nhưng lỗi thời; S = có nhưng sai/chưa đạt chuẩn; Ng = có nhưng thiếu ý.

| # | Hạng mục khung | DOCX (ở đâu) | PPTX (slide) | DOCX | PPTX |
|---|---|---|---|---|---|
| 1a | Bối cảnh / vấn đề | 2.1, 2.3 | 3, 4, 6 | Đ | Đ (lặp, xem B) |
| 1b | Thách thức | chỉ 1 câu cuối 2.1 ("chuỗi thời gian, nhiều trạm, giá trị thiếu, phi tuyến") | không có | T | T |
| 1c | Mục tiêu nghiên cứu + CH | 2.2 (CH1-CH3) | 8 | L (CH2 chỉ LR; CH3 chỉ validation baseline) | L (như DOCX) |
| 1d | Đóng góp của đề tài | không có (mục 8 chỉ là đóng góp từng người) | không có | T | T |
| 2a | Related works chia theo hướng (ai làm, bài nào, khó khăn, cách làm, nhận xét của nhóm) | không có mục; mục 9 chỉ có 5 tài liệu, không trích dẫn trong thân bài | 9 (3 hướng: Seng 2021, Bekkar 2021, Wei 2025) | T | Ng (thiếu "khó khăn", thiếu "nhận xét của nhóm" riêng từng hướng, không có bảng) |
| 2b | Cơ sở lý thuyết (ngắn) | không có | 15 (nguyên lý từng mô hình), 28 (thuật ngữ, ở cuối) | T | Ng |
| 2c | Đánh giá loss hoặc đưa vào future work | không có | 15 cột "Loss / tiêu chí" mơ hồ ("Tiêu chí chia nhánh", "Loss hồi quy") | T | S |
| 3a | Datasets (dữ liệu nói trước) | 3.1-3.3 (+ đoạn thừa về 2 CSV OHLCV) | 10, 11 | Đ | Đ |
| 3b | Pipeline tổng quan trước khi vào chi tiết | 5.1 + Hình 7 (nằm SAU tiền xử lý, EDA) | 14 (nằm SAU 10-13) | S (sai thứ tự; Hình 7 không có khối mô hình/tuning) | S (sai thứ tự; khác Hình 7 của DOCX) |
| 3c | Xử lý dữ liệu + kỹ thuật đặc thù (lag/rolling, chống rò rỉ) | 4.2, 4.3, 4.4 | 5, 7, 13 | Đ | Đ nhưng lặp (5, 7, 13) |
| 3d | Models (1 hình + vài chi tiết) | 5.2 Bảng 7 (cấu hình ban đầu); cấu hình tuned nằm ở 6.3 Bảng 10; không có hình mô hình | 15 (bảng chữ), 20 (tham số tuned) | Ng (không hình; tuned tách khỏi mục mô hình) | Ng (không hình; không ghi HistGradientBoostingRegressor) |
| 3e | Loss (mục riêng) | không có | 15 (một cột) | T | S |
| 4a | Thiết lập thực nghiệm | 5.3 | 16 | Ng (thiếu seed ngoài tuning, môi trường, n_iter, nguồn/ngày chạy) | Ng |
| 4b | Độ đo | 2.3 (1 dòng) + 5.3 (1 gạch) | rải ở 14, 15, 16 | Ng (không công thức, không nêu vì sao RMSE) | T (không slide độ đo) |
| 4c | DANH SÁCH thí nghiệm TRƯỚC kết quả (mỗi cái chứng minh gì) | không có (đầu mục 6 chỉ nói "Thực nghiệm 01/02/03/final_test" theo tên thư mục) | 17 (danh sách 7 phương pháp) | T | Ng (có "mục đích" nhưng không phải câu hỏi cần kiểm chứng, thiếu nguồn, thiếu độ chắc chắn/seed) |
| 4d | Từng TN: mục tiêu → kết quả → bình luận | 6.1-6.6 | 18-24 | Ng (có kết quả, ít "vì sao") | Ng |
| 4e | Sai số theo nhóm của MÔ HÌNH CUỐI (test, 5 mô hình) | chỉ baseline: Bảng 12 (tháng test), 13-14 (validation), B1 | 23 (baseline validation, biên cũ) | L/S (biên nhóm cũ; thiếu 5 mô hình, thiếu worst case) | L/S |
| 4f | Importance của RF | không có | không có | T | T |
| 4g | Độ chắc chắn (bootstrap) + ổn định (seed, epoch) | không có | không có | T | T |
| 4h | Đánh giá tổng: so với công trình liên quan (trung thực, không tuyên bố thắng) | không có | chỉ câu cuối slide 9 | T | Ng |
| 4i | Đánh giá tổng: ý nghĩa thực tế + hạn chế | 7.2 (hạn chế, một phần lỗi thời) | 25, ghi chú 16, 21 | L | Ng (thiếu ý nghĩa thực tế/chi phí) |
| 5 | Kết luận (1 slide) + hướng phát triển | 6.7 (trả lời CH) nhưng không có chương Kết luận, không có Future work | 26 (đủ 1 slide, không có hướng phát triển) | Ng/T | Ng |
| + | Truy vết số: ở đâu ra, ngày nào, ai chạy, cách chạy | chỉ nhắc `experiment_log.csv`, "notebook 08"; không có mã ô, hash, ngày | chỉ ghi "Nguồn dữ liệu: UCI" | T | T |
| + | Phân công/đóng góp thật | 1.2, 8 (Bảng 1, 17) | không có (slide 1 chỉ có tên) | S (xem C) | T |
| + | Tái lập/phụ lục | Phụ lục C | slide 28 chỉ là thuật ngữ | Ng (thiếu verify_result_sources.py, requirements-lock.txt, python/sklearn version) | T |

Kết quả tóm tắt: DOCX thiếu hẳn 10 hạng mục (1b, 1d, 2a, 2b, 2c, 3e, 4c, 4f, 4g, 4h) và thiếu chương Kết luận riêng; PPTX thiếu hẳn 1b, 1d, 4b, 4f, 4g và chỉ có nửa vời ở 2a, 2c, 3e, 4c, 4h.

---------------------------------------------------------------------

## (B) Mục/slide nguyên khối còn thiếu

### B1. DOCX (chưa có mục nào tương ứng)
1. Tóm tắt (abstract) ~150-200 từ.
2. Thách thức (trong phần Giới thiệu).
3. Đóng góp của đề tài (khác với đóng góp từng thành viên).
4. Bố cục báo cáo / câu mở "báo cáo gồm N phần" (nguyên tắc bài luận).
5. Công trình liên quan: cơ sở lý thuyết ngắn, các hướng nghiên cứu (bảng: hướng - công trình - dữ liệu/cách làm - khó khăn - nhận xét), đánh giá loss hoặc đưa vào hướng phát triển.
6. Mục Hàm mất mát (loss) và phân biệt loss với metric.
7. Hình mô hình (một hình tổng hợp 5 mô hình hoặc MLP 79-32-16-1) + bảng cấu hình ban đầu và tuned đặt cạnh nhau.
8. Mục Độ đo có công thức MAE, RMSE, R², residual = thực tế − dự đoán và lý do chọn RMSE để chọn mô hình.
9. Danh sách thí nghiệm (E1-E7) trước 6.1.
10. Sai số theo trạm/tháng/mùa/mức PM2.5 cho 5 mô hình trên test (CSV `final_test_error_by_*.csv`) + worst cases (`final_test_worst_cases.csv`, hình `final_test_worst_event.png`).
11. Importance của RF (`rf_group_permutation_importance.csv`) và so sánh với LR.
12. Độ chắc chắn (bootstrap ghép cặp `paired_model_uncertainty.csv`), ổn định seed MLP (`mlp_seed_summary.csv`), kiểm tra epoch (`mlp_validation_diagnostics.csv`).
13. Bình luận chuyển tiếp validation → test (thứ hạng GB/LR đảo, R² test cao hơn dù RMSE cao hơn).
14. Đánh giá tổng thể: đối chiếu công trình liên quan (không tuyên bố thắng), ý nghĩa thực tế, hạn chế.
15. Chương Kết luận (trả lời CH1-CH3) + Hướng phát triển (t+24, mô hình từng trạm, trạm mới, feature chưa dùng, so sánh loss...).
16. Đối chiếu train vs validation/test để nhận diện over/underfitting (proposal mục 7 đã hứa: "đối chiếu sai số train và validation/test"). Hiện DOCX không có chữ overfit/underfit nào. Có sẵn `train_rmse` trong `mlp_validation_diagnostics.csv`; với RF/GB cần kiểm tra nguồn trước khi viết (nếu không có thì ghi vào hạn chế, không tự tính lại).
17. Ưu/nhược điểm từng mô hình dựa trên số liệu (proposal mục 7 đã hứa).
18. Bảng nguồn số liệu (bảng/hình → notebook → mã ô → CSV → thời điểm ghi → chế độ computed/verified_saved_search).
19. Trích dẫn trong thân bài [n] cho các tài liệu ở mục 9.

### B2. PPTX
1. Thách thức (có thể ghép với mục tiêu).
2. Đóng góp (ghép với mục tiêu: 1 slide "Thách thức - Mục tiêu - Đóng góp").
3. Slide Thiết lập thực nghiệm và Độ đo (hiện chỉ có bullet ở slide 16 và dòng chữ nhỏ ở 14/15).
4. Hình mô hình (1 hình) trong slide 15; ghi HistGradientBoostingRegressor; tách loss khỏi metric đúng theo code.
5. Danh sách thí nghiệm có "câu hỏi cần kiểm chứng" cho từng TN (slide 17 hiện là danh sách phương pháp).
6. Slide kết quả test theo nhóm của MÔ HÌNH CUỐI (thay slide 23).
7. Slide importance RF + so sánh LR (slide 24 hiện chỉ LR và không nói là LR).
8. Slide độ chắc chắn và ổn định (bootstrap CI, seed MLP, epoch).
9. Slide Đánh giá tổng (so công trình liên quan, ý nghĩa thực tế, hạn chế) - hiện chỉ có slide 25 "lưu ý diễn giải" chung.
10. Hướng phát triển (thêm vào slide Kết luận, vẫn 1 slide).
11. Slide dự phòng: cấu hình mô hình (`final_model_configuration.csv`), kết quả theo tháng/trạm test, worst case, loss curve MLP, lệnh tái lập, tài liệu tham khảo.
12. Ghi chú người thuyết trình (speaker notes): 22/22 notesSlide hiện RỖNG (đã kiểm tra trong `ppt/notesSlides/*.xml`). Chưa có chỗ ghi nguồn số, ai nói slide nào.
13. Phân công trình bày (ai nói phần nào) - YC mục 8: "mỗi thành viên giải thích được phần mình trình bày".

---------------------------------------------------------------------

## (C) Mâu thuẫn giữa các tài liệu

| # | Nội dung | DOCX | PPTX | Nguồn/ghi chú | Mức |
|---|---|---|---|---|---|
| C1 | Tên mô hình "Gradient Boosting" | Chỉ Bảng 7 và Phụ lục C ghi HistGradientBoostingRegressor; thân bài viết "Gradient Boosting" | Không slide nào ghi HistGradientBoostingRegressor | YC mục 3 (5.2) và slide 15; `final_model_configuration.csv` ghi estimator HistGradientBoostingRegressor | Cao |
| C2 | Biên nhóm PM2.5 | Bảng 14: "0-35 ... 112.846", "35-75 72.798"... (biên cũ); đoạn MLP "54,92 nhóm >250 theo cách chia notebook 06" | Slide 23 y hệt Bảng 14 | `baseline_error_analysis.csv` hiện: `<=35` n=115085, `(35,75]` 72055, `(75,115]` 45799, `(115,150]` 24358, `(150,250]` 30226, `>250` 13173; test dùng cùng biên (`final_test_error_by_pm25_level.csv`) | Cao |
| C3 | Danh sách tài liệu tham khảo | 5 tài liệu (Chen, Zhang, Breiman, Friedman, Pedregosa) = y nguyên proposal; không có chỗ nào trích dẫn trong thân | Slide 9 trích Seng 2021, Bekkar 2021, Wei 2025; slide 3 trích WHO 2021; không trích Zhang, Breiman, Friedman, Pedregosa | DOCX không có 4 nguồn của slide; PPTX không có 4 nguồn của DOCX. Phải kiểm tra bài gốc trước khi ghi (YC mục 3) | Cao |
| C4 | Hình pipeline | Hình 7: 6 khối (Dữ liệu gốc - Chuẩn hóa - Nhãn và đặc trưng - Chia theo thời gian - Đánh giá validation - Đánh giá cuối), không có khối mô hình/tuning | Slide 14: 6 bước khác (Dữ liệu - Xác định mục tiêu - Chia - Tiền xử lý - Dự báo (5 mô hình) - Đánh giá), không có tuning, không có test khóa | Hai bản đều "6 bước" nhưng khối khác nhau, giảng viên cần "tôi có N phần" nhất quán | Trung bình |
| C5 | Ảnh pipeline cũ nằm trong file PPTX | - | `ppt/slides/_rels/slide12.xml.rels` (slide 14) vẫn gắn `media/image5.png`: pipeline cũ ghi "GB: sắp làm" và "Scaler chỉ dùng cho Linear Regression"; ảnh không hiển thị trên slide nhưng còn trong tệp | Xóa quan hệ ảnh mồ côi để file nộp không chứa nội dung lỗi thời | Thấp |
| C6 | Đánh số hình | Hình 1-13 liên tục | Slide 12 ghi "Hình 4", "Hình 6"; slide 16 "Hình 8"; slide 24 hình không có chú thích | Slide không có Hình 1-3, 5, 7: số nhảy. Dùng số riêng cho slide hoặc ghi "(Hình 4, báo cáo)" | Thấp |
| C7 | Phạm vi CH2 và CH3 | CH2 "Linear Regression"; CH3 "Sai số validation" | slide 8 y hệt | YC mục 3 dòng "Mục tiêu/CH2, CH3": mở rộng sang RF và test của 5 mô hình cuối | Cao |
| C8 | Khẳng định về test | 5.3: "Tập test được giữ riêng cho bước đánh giá sau khi chốt cấu hình"; Bảng 12 là phân tích test theo tháng của 2 baseline từ notebook 02 | Slide 16: "Chỉ dùng test sau khi chốt cấu hình, không dùng test để tuning"; slide 18 đã đưa test của baseline trước slide 21 | Proposal ghi "chỉ dùng một lần"; ra-soat R05: ở bản được rà soát notebook 02 mặc định `RUN_FINAL_TEST=True` (hiện cả `notebooks/` và `notebooks_unexecuted/` đã đặt `False`); lịch sử đã xem test baseline vẫn phải nêu trung thực. YC mục 6 (slide 16): "tránh tuyên bố test chưa từng được xem nếu không có bằng chứng lịch sử". `experiment_log.csv` ghi "Configurations fixed before test evaluation"; `evaluation_manifest.json` ghi "no tuning on test" | Trung bình |
| C9 | Vai trò thành viên | Bảng 1 (proposal): Bảo có mô hình GB, Tuấn làm đánh giá cuối + importance + README; Bảng 17 (thực tế): Tuấn làm RF ban đầu (notebook 03), Quang làm đánh giá cuối | `README.md` mục Phân công: Nhân, Tài, Tuấn đều ghi "Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật"; `phancong.txt`: phạm vi Bảo kết thúc ở pipeline dữ liệu | Bảng 17 gán phần việc cho từng người; riêng dòng Nhân ghi nguyên văn "theo lịch sử commit", và mở đầu mục 8 nói bảng ghi "phần việc có sản phẩm hoặc lịch sử cập nhật trong kho mã nguồn" (git log có các tên tài khoản BinBin826, ITSGU20, daohuutai, Tô Nhân, bjruly...; không có bằng chứng ánh xạ tên người). YC mục 2: "Không suy tên người chạy từ tác giả commit". `diagnostics_manifest.json`: `"operator": null` kèm ghi chú "Not inferred from account, Git author or machine name." | Cao |
| C10 | Loại tài liệu và thời điểm | Bìa: "BÁO CÁO CẬP NHẬT TIẾN ĐỘ ĐỒ ÁN"; tên file "GiuaKy"; mục 1.3, 7 (đánh giá tiến độ), Bảng 2, 16 viết như báo cáo tiến độ, trong khi đã có kết quả cuối | Slide không có ngày, không nêu là giữa kỳ hay cuối kỳ | `docs/README.md` gọi là "Báo cáo cập nhật tiến độ"; ra-soat R15 yêu cầu "tài liệu cuối phản ánh bộ kết quả đã chốt, không còn mô tả ... là chưa làm" | Trung bình |
| C11 | Mô tả validation: "pooled" hay "trung bình fold" | 6.1: "Mỗi cấu hình được chấm trên 300.696 dự đoán ngoài mẫu (OOF) cộng lại từ 5 fold" ngay trên Bảng 8 là trung bình ± SD qua 5 fold | Slide 19: "Trung bình ± độ lệch chuẩn trên 5 fold" | ra-soat R12: trung bình RMSE 5 fold khác RMSE gộp OOF (RF ban đầu 20,1707 so với 20,7948). Câu của DOCX dễ khiến người đọc nghĩ là RMSE gộp | Trung bình |
| C12 | Slide 24 so với DOCX 6.6 | 6.6: LR, fold 5, mẫu 30.000, lặp 5, RMSE gốc 17,76 | Slide 24: không nói LR, không nói fold 5/30.000/5 lần; chữ "phép đánh giá minh họa" (số là kết quả thật) | YC mục 6 (slide 24) | Cao |
| C13 | Đóng góp trong bảng tiến độ "Tuần 1..5" | Bảng 2 vẫn nói "Nhóm tiếp tục rà soát slide và khả năng tái lập" | - | Lỗi thời so với trạng thái repo (bộ pytest hiện lớn hơn 27 test, xem P2 mục 1; `scripts/verify_result_sources.py`) | Trung bình |
| C14 | Số liệu giữa hai tài liệu | Đã đối chiếu máy mọi số có dấu phẩy và số có dấu chấm nghìn ở slide với DOCX: chỉ lệch là các mảnh DOI ở slide 9 (không phải số liệu) | - | Không phát hiện mâu thuẫn số giữa Bảng 3, 8, 9, 10, 11, 14, 15 và slide tương ứng; cả hai cùng lỗi thời ở Bảng 14 (C2) | Thông tin |
| C15 | Tên gọi nhóm thí nghiệm | 6 (đầu mục): "Thực nghiệm 01, 02, 03, final_test" (tên thư mục) | Slide 17: "Bước 1-7" | Hai cách đặt tên khác nhau. Dùng E1-E7 ở cả hai (đề xuất ở E) | Thấp |
| C16 | Số trang/slide so với khung 15 phút | DOCX ~23 trang | 26 slide nội dung + cảm ơn + phụ lục = 28 | 15 phút cho 26 slide ≈ 35 giây/slide; khung giảng viên: phần phụ chuyển dự phòng | Trung bình |

Điểm đã nhất quán (để khỏi sửa nhầm): tên 5 mô hình và đơn vị µg/m³; 27 đặc trưng và 11+6+2+6+2; 12 trạm, 420.768, 412.017, 360.954, 51.063; 5 fold expanding-window; "ban đầu/tinh chỉnh"; xếp hạng test; bảng validation 8 cấu hình; bảng per-fold; bảng tuning 8/20/8 và 4,92%/8,80%/2,25%.

---------------------------------------------------------------------

## (D) Giọng văn và phát biểu cần sửa hoặc tránh (YC mục 7)

| Mẫu phát biểu | Tìm thấy ở đâu | Đánh giá | Cách sửa |
|---|---|---|---|
| "R² cao = Accuracy cao" | Không có nguyên văn. DOCX 2.3 ghi đúng "không dùng Accuracy". Slide 6 tiêu đề "dự đoán chính xác điều gì?", slide 16 "không kết luận độ chính xác cho cả bốn mùa", slide 25 "Độ chính xác có thể thay đổi" dùng "chính xác/độ chính xác" kiểu thường. DOCX 6.4 nêu "R² cao nhất 0,9550" nhưng không giải thích vì sao R² test cao hơn validation dù RMSE test (20,96) cao hơn RMSE validation (19,18) | Rủi ro thấp - trung bình | Đổi sang "sai số", "dự đoán đại lượng nào". Thêm 1 câu: R² phụ thuộc phương sai nhãn của giai đoạn (PM2.5 trung bình 78,04 ở train/validation so với 92,18 ở test, DOCX 5.3), không so R² giữa hai tập như thể "chính xác hơn". |
| "RF tốt nhất nên luôn tốt ở mọi nơi" | DOCX 1.3, 6.4, 6.7(CH1); slide 21, 26: xếp hạng RF đứng đầu, có câu giới hạn mùa/trạm chưa đánh giá | Thiếu hai lớp bằng chứng: (i) khoảng bootstrap RF-GB [-0,7799; 0,1339] và RF-MLP [-1,3431; 0,2557] chứa 0 (`paired_model_uncertainty.csv`), (ii) `final_test_error_by_*.csv` cho thấy RF có RMSE thấp nhất ở 7/12 trạm, 1/6 tháng (chỉ 01/2017), 1/6 nhóm mức PM2.5 (chỉ >250), 1/2 mùa (mùa đông; mùa thu GB 15,101 < RF 15,323) | Sửa như văn bản đề xuất mục P8, P9 |
| "Importance chứng minh nguyên nhân" | Không có. DOCX 6.6 và slide 7, 24, 25 đã rào đúng. Hai điểm yếu: slide 24 không ghi LR; DOCX 6.6 viết hệ số PM2.5(t) dương, lag 1 âm mà không có bảng/hình hệ số trong DOCX (hình `baseline_lr_coefficients.png` có trong repo nhưng chưa chèn) | Thấp | Thêm hình hệ số hoặc bỏ câu về dấu hệ số; ghi "LR" vào tiêu đề slide 24 |
| Bảng baseline theo mức dùng biên cũ | DOCX Bảng 14 + đoạn MLP 54,92; slide 23 | Sai (C2) | Thay cả nhãn, n, số; ghi quy tắc biên |
| "Đã chạy lại toàn bộ tuning" | Không có nguyên văn. DOCX 5.3, 6.3 mô tả RandomizedSearchCV ở thì hiện tại, không nói notebook 05/07 hiện chỉ đối chiếu artifact đã lưu (`mode = verified_saved_search`, cell `verify-saved-search-05/07`) | Thiếu minh bạch nguồn | Thêm câu provenance (P11) |
| "Tất cả số do một thành viên chạy" / ai chạy | Không có nguyên văn nhưng Bảng 17 gán người theo commit (C9); không có bảng/số nào ghi ngày chạy/người chạy | Cao | Bỏ "theo lịch sử commit"; chỉ ghi người/ngày khi nhóm xác nhận; ngày máy ghi có sẵn trong `report_sources.csv` (`recorded_at_utc` 2026-11-20) |
| Test "chưa từng xem / chỉ dùng một lần" | DOCX 5.3; slide 16; proposal | Xem C8 | Văn bản đề xuất P5 |
| Công dụng thực tế vượt bằng chứng | DOCX 2.1: "hỗ trợ cảnh báo sớm, khuyến cáo sức khỏe cộng đồng và bổ sung giá trị cho các trạm bị thiếu dữ liệu" | Dùng điều kiện nhưng chưa được kiểm chứng (không thử trạm mới, không thử nhập liệu thiếu, không có chuyên gia) | Chuyển thành "động lực", đưa phần giới hạn ở P10 |
| "W&B/MLflow/công nghệ mới" | Không thấy | Đạt | - |
| "Đã sửa báo cáo/slide" | Không thấy | Đạt | - |
| Từ ngữ nội bộ "Thực nghiệm 01/02/03", "notebook 08" mà không giải thích | DOCX đầu mục 6, 6.4, 6.3 | Khó theo dõi với người đọc ngoài nhóm | Dùng E1-E7 và chú thích nguồn cuối bảng |
| Câu "Nhóm đã kiểm tra trực tiếp ... và xác nhận" | DOCX 3.2 | Chấp nhận, nhưng thêm nguồn: `outputs/eda/tables/dataset_counts.csv` (notebook 01, evidence-nb-01) | Thêm chú thích nguồn |

---------------------------------------------------------------------

## (E) Đề cương cuối đề xuất

### E1. DOCX (đánh số sau khi chèn). Ngân sách: thân bài ≤ 22 trang + phụ lục ≤ 5 trang (hiện ~23 trang gồm bìa + mục lục)

| Mục | Nội dung | Nguồn cũ → mới | Trang |
|---|---|---|---|
| Bìa + Mục lục | Đổi tiêu đề "BÁO CÁO CẬP NHẬT TIẾN ĐỘ" nếu nhóm quyết định nộp như báo cáo kết quả; ghi ngày | cũ bìa | 2 |
| Tóm tắt | 150-200 từ: bài toán, dữ liệu, 5 mô hình, kết quả chính (RF tuned RMSE 20,9613), giới hạn | MỚI | 0,5 |
| 1. Giới thiệu | 1.1 Bối cảnh và vấn đề; 1.2 Bài toán: input-output; 1.3 Thách thức; 1.4 Mục tiêu và câu hỏi nghiên cứu (CH2, CH3 mở rộng); 1.5 Đóng góp; 1.6 Bố cục | cũ 2.1-2.3 + MỚI 1.3, 1.5, 1.6 | 2 |
| 2. Công trình liên quan | 2.1 Cơ sở lý thuyết ngắn; 2.2 Hướng A: học sâu chuỗi thời gian PM2.5; 2.3 Hướng B: mô hình cây và MLP trên đặc trưng bảng; 2.4 Hướng C: cách đánh giá/chia dữ liệu theo thời gian (nếu có nguồn đã kiểm tra bài gốc); 2.5 Loss (nhận xét + đưa vào hướng phát triển); bảng tổng hợp | MỚI (đồng bộ slide 9) | 2 |
| 3. Dữ liệu và phương pháp | 3.1 Dữ liệu (nguồn, quy mô, thuộc tính, target) | cũ 3.1-3.3 (bỏ đoạn OHLCV) | 1,5 |
| | 3.2 Tổng quan giải pháp (pipeline, "N phần") | cũ 5.1, chuyển lên, vẽ lại Hình 7 có khối mô hình/tuning/test | 0,7 |
| | 3.3 Khám phá dữ liệu (EDA) | cũ 4.1 (giữ Hình 2, 4, 6; chuyển Hình 1, 3, 5 sang phụ lục nếu cần cắt trang) | 3 |
| | 3.4 Tiền xử lý, đặc trưng, chống rò rỉ | cũ 4.2, 4.3, 4.4 | 1,5 |
| | 3.5 Mô hình (hình + bảng ban đầu/tuned cạnh nhau, kích thước 27→79 cột, lớp MLP [79,32],[32,16],[16,1]) | cũ 5.2 + 6.3 Bảng 10 + MỚI hình | 1 |
| | 3.6 Hàm mất mát và phân biệt với metric | MỚI | 0,5 |
| 4. Thực nghiệm và bình luận | 4.1 Thiết lập và độ đo (công thức, môi trường, seed, n_iter, quy tắc chọn, lịch sử dùng test) | cũ 5.3 + MỚI | 1 |
| | 4.2 Danh sách thí nghiệm E1-E7 | MỚI | 0,5 |
| | 4.3 E1-E2 Baseline và mô hình ban đầu (validation, đủ fold) | cũ 6.1, 6.2 | 1,5 |
| | 4.4 E3 Tinh chỉnh | cũ 6.3 | 0,7 |
| | 4.5 E4 Test cuối + bình luận validation → test | cũ 6.4 + MỚI | 1 |
| | 4.6 E5 Sai số theo nhóm: baseline validation (biên mới) và 5 mô hình trên test; worst cases | cũ 6.5 thay bảng + MỚI | 2 |
| | 4.7 E6 Đóng góp feature: LR và RF | cũ 6.6 + MỚI | 1 |
| | 4.8 E7 Độ chắc chắn và ổn định | MỚI | 1 |
| | 4.9 Đánh giá tổng: đối chiếu công trình liên quan, ý nghĩa thực tế, hạn chế | MỚI (thay 7.2) | 1 |
| 5. Kết luận và hướng phát triển | Trả lời CH1-CH3; hạn chế; hướng phát triển | cũ 6.7 + MỚI | 1 |
| Tài liệu tham khảo | Hợp nhất DOCX + slide, kiểm DOI từ nguồn gốc, trích dẫn [n] trong thân | cũ 9 | 1 |
| Phụ lục A | Nhật ký thí nghiệm (Bảng A1) + bảng nguồn số liệu | cũ A + MỚI | 1 |
| Phụ lục B | Sai số theo trạm (validation baseline + test 5 mô hình) | cũ B | 1 |
| Phụ lục C | Tái lập: pytest, verify_result_sources.py, requirements-lock.txt, Python 3.13.12/scikit-learn 1.7.2, fallback baseline | cũ C | 1 |
| Phụ lục D | Thông tin nhóm, phân công/đóng góp (chỉ phần nhóm xác nhận), tiến độ | cũ 1.1-1.3, 7, 8 rút gọn | 1 |

Cắt gọn bắt buộc: cũ 1 (thông tin/tiến độ) → Phụ lục D; cũ 7 (đánh giá tiến độ) bỏ 7.1, 7.3 vì lỗi thời, 7.2 gộp vào 4.9; Bảng 12 (baseline tháng test) thay bằng bảng 5 mô hình; Bảng 14 thay biên.

### E2. Slide chính ≈ 15 phút (19 slide + cảm ơn) + dự phòng

| # | Slide | Lấy từ slide cũ | Giây |
|---|---|---|---|
| 1 | Tiêu đề (thêm ngày) | 1 | 10 |
| 2 | Bố cục (5 phần) | 2 | 10 |
| 3 | ① Bài toán: bối cảnh + input → output (gộp) | 3, 4, 6 (rút) | 50 |
| 4 | ① Thách thức - Mục tiêu - CH - Đóng góp | 8 + MỚI | 60 |
| 5 | ② Công trình liên quan: bảng 3 hướng, khó khăn, nhận xét | 9 (sửa) | 60 |
| 6 | ③ Dữ liệu (nguồn, quy mô, chia) | 10 | 45 |
| 7 | ③ EDA: điều rút ra cho quyết định mô hình | 12 | 45 |
| 8 | ③ Pipeline tổng quan "N phần" (đặt TRƯỚC tiền xử lý) | 14 (chuyển lên) | 40 |
| 9 | ③ Tiền xử lý, 27 đặc trưng, chống rò rỉ | 13 + 5 (rút) | 50 |
| 10 | ③ Mô hình (1 hình) + loss | 15 | 60 |
| 11 | ④ Thiết lập và độ đo | 16 + MỚI | 45 |
| 12 | ④ Danh sách thí nghiệm E1-E7 | 17 (sửa) | 35 |
| 13 | ④ E1-E3 Validation: baseline, ban đầu, tuned, theo fold | 18, 19, 20, 22 (gộp) | 80 |
| 14 | ④ E4 Test cuối (thêm cột/ghi khoảng tin cậy RF-LR) | 21 | 55 |
| 15 | ④ E5 Sai số theo nhóm trên test (5 mô hình) | 23 (thay) | 55 |
| 16 | ④ E6 Importance: LR và RF | 24 (sửa) | 45 |
| 17 | ④ E7 Độ chắc chắn và ổn định | MỚI | 45 |
| 18 | ④ Đánh giá tổng: công trình liên quan, ý nghĩa thực tế, hạn chế | 25 (thay) | 50 |
| 19 | ⑤ Kết luận + hướng phát triển (1 slide) | 26 | 55 |
| 20 | Cảm ơn / Hỏi đáp | 27 | 5 |
| | **Tổng** | | **900 s = 15:00** |

Dự phòng (B1-B14): B1 thuộc tính dữ liệu (cũ 11); B2 chi tiết 27 đặc trưng (cũ 5); B3 ví dụ I/O giả định + lý do nhóm đặc trưng (cũ 6, 7); B4 bảng validation 8 cấu hình (cũ 19); B5 bảng per-fold (cũ 22); B6 tuning: tổ hợp thử + tham số (cũ 20); B7 baseline validation theo mức (biên mới); B8 test theo tháng/mùa/trạm (5 mô hình); B9 worst case (`final_test_worst_event.png`); B10 hội tụ MLP (`validation_diagnostics/mlp_convergence.png`); B11 cấu hình mô hình cuối (`final_model_configuration.csv`); B12 lệnh tái lập + môi trường; B13 thuật ngữ (cũ 28); B14 tài liệu tham khảo. Tổng 34 slide (20 chính + 14 dự phòng).

Hình/bảng sẵn có trong repo để dựng slide mới (không cần chạy lại): `outputs/experiments/final_test/analysis/figures/final_test_rmse_by_month.png`, `..._by_station.png`, `..._by_pm25_level.png`, `..._by_season.png`, `final_test_worst_event.png`; `outputs/experiments/validation_diagnostics/rf_group_permutation_importance.png`, `mlp_convergence.png`; `outputs/eda/figures/pm25_autocorrelation.png`, `pm25_distribution_linear_log.png`, `pm25_wind_relationships.png`.

---------------------------------------------------------------------

## Văn bản tiếng Việt sẵn dán, theo vị trí

### P1. DOCX mục 1.3 Thách thức
Bài toán có bốn thách thức, mỗi thách thức đều có bằng chứng trong dữ liệu. Thứ nhất, PM2.5 lệch phải rõ rệt (trung bình 79,79 µg/m³ cao hơn trung vị 55 µg/m³; có 953 quan sát từ 500 µg/m³ trở lên), nên sai số ở nhóm nồng độ cao có thể chi phối RMSE. Thứ hai, giá trị thiếu không chỉ rải rác mà có khoảng liên tục dài (ví dụ CO tại Dongsi thiếu 1.517 giờ liên tiếp), nên không thể điền tùy ý. Thứ ba, tự tương quan của PM2.5 rất cao (0,969 ở lag 1 giờ) làm mốc Persistence trở nên mạnh, nên mô hình khó vượt xa mốc này. Thứ tư, dữ liệu là chuỗi thời gian nhiều trạm, đòi hỏi cách chia và tiền xử lý không để thông tin tương lai lọt vào huấn luyện; đồng thời tập test (09/2016-02/2017) có PM2.5 trung bình 92,18 µg/m³ so với 78,04 µg/m³ ở train/validation. (Số lấy từ DOCX 3.3, 4.1.1, 4.1.4, 5.3; đã đối chiếu: trung bình 79,79 và trung vị 55 ở `outputs/eda/tables/raw_pm25_summary.csv`; 953 quan sát ≥ 500 và CO Dongsi thiếu liên tục 1.517 giờ tính lại từ `data/processed/beijing_air_quality_standardized.csv`; 0,969 là tương quan lag 1 trung bình 12 trạm ở `outputs/eda/tables/pm25_acf.csv` (0,9686); 92,18 và 78,04 ở `outputs/eda/tables/target_split_summary.csv`.)

### P2. DOCX mục 1.5 và slide 4: Đóng góp (trong phạm vi môn học, chỉ nhận cái đã có code và kết quả)
1. Một pipeline đa trạm tránh rò rỉ cho dự báo PM2.5 một giờ tới: nhãn t+1 tạo theo từng trạm trước khi forward-fill, chia theo thời điểm của nhãn, imputer/encoder/scaler fit trên train của từng fold, có bộ kiểm thử tự động (pytest: [cần xác nhận: số test chốt trước khi dán; `docs/ra-soat-do-an-va-ke-hoach-khac-phuc.md` ghi 27/27 ở lần chạy trước, phiên làm việc trước ghi 31/31, lần chạy lại lúc kiểm này (.venv, `python -X utf8 -B -m pytest -q -p no:cacheprovider`) đạt 54/54 sau khi `tests/` có thêm `test_metrics_and_bootstrap.py` và `test_diagnostics_and_validation.py`]).
2. So sánh năm mô hình (Persistence, Linear Regression, Random Forest, HistGradientBoosting, MLP) trên cùng 5 fold validation và cùng tập test, trong đó Random Forest, Gradient Boosting và MLP được so trước và sau tinh chỉnh; cùng 5 fold expanding-window và cùng 51.063 mẫu test.
3. Phân tích sai số theo trạm, tháng, mùa, mức PM2.5 và các trường hợp sai lớn của chính các mô hình cuối.
4. Đánh giá mức chắc chắn (bootstrap ghép cặp theo khối 7 ngày, ba seed MLP, kiểm tra giới hạn epoch) và importance theo nhóm cho LR và RF.
5. Hồ sơ truy vết số liệu (`report_sources.csv`, manifest, `requirements-lock.txt`).
Đề tài không đề xuất thuật toán mới và không tuyên bố vượt kết quả của công trình khác.

### P3. DOCX mục 1.4 (viết lại CH2, CH3) và slide 4
- CH1 (giữ): Random Forest, Gradient Boosting và MLP sau tinh chỉnh đạt MAE, RMSE, R² thế nào so với Persistence và Linear Regression trên tập test theo thời gian?
- CH2: Linear Regression và Random Forest phụ thuộc mạnh nhất vào nhóm đặc trưng nào trong phép đo permutation importance theo nhóm, và hai mô hình khác nhau ra sao?
- CH3: Sai số thay đổi thế nào theo trạm, tháng/mùa và mức PM2.5, ở validation (baseline) và ở test (năm mô hình cuối)?
- (Thêm) CH4: Chênh lệch giữa các mô hình có chắc chắn không (bootstrap, seed, hội tụ)?

### P4. DOCX mục 2 Công trình liên quan: bảng khung (điền "khó khăn" sau khi đọc bài gốc, KHÔNG suy đoán)
Câu mở: "Phần này gồm ba hướng nghiên cứu liên quan và một nhận xét về hàm mất mát."

| Hướng | Công trình (DOI) | Dữ liệu và cách làm (theo slide 9) | Khó khăn (CẦN ĐIỀN TỪ BÀI GỐC) | Nhận xét của nhóm |
|---|---|---|---|---|
| A. Học sâu không gian-thời gian cho PM2.5 | Seng và cs. (2021), 10.1016/j.aej.2020.12.009 | PM2.5, khí tượng và dữ liệu trạm lân cận; 35 trạm Bắc Kinh (2016-2017); LSTM | [điền] | Đề tài chỉ dự báo từng trạm bằng đặc trưng của chính trạm đó, chưa dùng thông tin trạm lân cận (hướng phát triển). Không so RMSE vì khác dữ liệu và giai đoạn. |
| A. Học sâu chuỗi thời gian | Bekkar và cs. (2021), 10.1186/s40537-021-00548-1 | Dự báo PM2.5 theo giờ tại Bắc Kinh; so LSTM, GRU, CNN và mô hình lai CNN-LSTM | [điền] | Đề tài dùng MLP trên lag/rolling thay vì mạng chuỗi; không khẳng định ngang hay hơn mô hình lai. |
| B. Mô hình cây và mạng nơ-ron trên dữ liệu bảng | Wei và cs. (2025), 10.3390/su17209211 | PM2.5 và O3 vùng Bắc Kinh-Thiên Tân-Hà Bắc, 2019-2023; RF, XGBoost, FCNN | [điền] | Gần nhất với đề tài (RF, boosting, MLP); khác vùng, giai đoạn, độ đo. |
| C. Mô hình nền | Breiman (2001); Friedman (2001) | Nền tảng của RF và gradient boosting | không áp dụng | Cơ sở lý thuyết cho hai mô hình cây. |
| D. Loss | chưa có công trình đã đọc | - | - | Đề tài dùng loss bình phương sai số cho cả bốn mô hình học; chưa đánh giá loss khác (MAE, Huber, trọng số cho PM2.5 cao): để ở hướng phát triển. |

Ghi chú nhãn nguồn (bắt buộc khi dán): các chi tiết trong cột "Dữ liệu và cách làm" (35 trạm, 2016-2017; 2019-2023; danh sách kiến trúc LSTM/GRU/CNN/CNN-LSTM; RF/XGBoost/FCNN) là số và mô tả của bài gốc theo slide 9 hiện tại, [cần xác nhận: chưa kiểm tra bản gốc], không so sánh trực tiếp với kết quả của đề tài. DOI chưa được đối chiếu với trang nhà xuất bản.

Ghi chú bắt buộc dưới bảng: "Cần xét thời kỳ dữ liệu, tập kiểm thử, tầm dự báo và độ đo trước khi kết luận mô hình nào tốt hơn; do đó nhóm không so trực tiếp RMSE với các công trình trên." Cột "Khó khăn" phải điền sau khi nhóm đọc bài gốc (YC mục 3: "kiểm tra bài gốc trước khi trích"); tên tác giả, năm, DOI phải đối chiếu từ nguồn gốc. Zhang và cs. (2017) hiện chỉ có trong danh sách tham khảo của DOCX: nếu không dùng trong Related works hoặc Dữ liệu thì thêm câu trích dẫn đúng chỗ dùng hoặc bỏ khỏi danh sách.

### P5. DOCX 4.1 / slide 11: Thiết lập thực nghiệm và độ đo (thay đoạn "test được giữ riêng")
- Chia dữ liệu: train/validation gồm các mẫu có nhãn trước 01/09/2016 (360.954 mẫu); test gồm 51.063 mẫu có nhãn từ 01/09/2016 đến 28/02/2017; validation là TimeSeriesSplit expanding-window 5 fold nhóm theo thời điểm nhãn.
- Cấu hình RF, GB, MLP chọn bằng RandomizedSearchCV (n_iter RF=8, GB=20, MLP=8; scoring neg_root_mean_squared_error; seed=42; `experiment_log.csv`) trên đúng 5 fold, rồi khóa trước khi chấm test ở notebook 08. Các điểm test của hai baseline đã được in ở notebook 02 trong quá trình phát triển (ra-soat R05); test không được dùng để chọn lại cấu hình hay mô hình sau khi chốt. Notebook 05 và 07 hiện đối chiếu artifact tuning đã lưu (`verified_saved_search`), không chạy lại toàn bộ RandomizedSearchCV.
- Môi trường: Python 3.13.12, scikit-learn 1.7.2, numpy 2.3.3, pandas 2.3.3 (`final_test/analysis/evaluation_manifest.json`); khóa ở `requirements-lock.txt`.
- Độ đo (đơn vị µg/m³ với MAE, RMSE): MAE = trung bình |y − ŷ|; RMSE = căn của trung bình (y − ŷ)², phạt nặng sai số lớn nên phù hợp khi quan tâm đợt ô nhiễm cao; R² = 1 − tổng bình phương sai số / tổng bình phương độ lệch so với trung bình, không đơn vị và phụ thuộc phương sai nhãn của giai đoạn; residual = thực tế − dự đoán (dương = dự báo thấp hơn thực tế). RMSE trung bình qua 5 fold là tiêu chí chọn; MAE và R² dùng để đối chiếu. Không dùng Accuracy.
- Trong bảng nhóm (theo mức PM2.5) dùng MAE, RMSE, residual vì R² dao động khi khoảng nồng độ hẹp (đã có ở DOCX 6.5; trong `final_test_error_by_pm25_level.csv` R² ở các nhóm ≤150 là số âm).

### P6. DOCX 4.2 và slide 12: Danh sách thí nghiệm (đặt trước kết quả)
Câu mở: "Nhóm thực hiện bảy thí nghiệm. E1 và E2 cho biết mốc dễ đến đâu và mô hình phi tuyến có vượt mốc không; E3 cho biết tinh chỉnh cải thiện ở đâu; E4 chấm cấu hình đã khóa trên test; E5 tìm nơi mô hình sai; E6 tìm nhóm đặc trưng mô hình dựa vào; E7 cho biết kết luận chắc đến mức nào."

| Mã | Thí nghiệm | Câu hỏi chứng minh | Điều kiện | Nguồn |
|---|---|---|---|---|
| E1 | Baseline (Persistence, LR) | Persistence đã mạnh đến đâu; LR cải thiện metric nào? | 5 fold validation | notebook 02 (evidence-nb-02), `baseline_cv_summary.csv` |
| E2 | Mô hình ban đầu (RF, GB, MLP) | Có vượt baseline trên validation không? | cùng 5 fold, cùng 27 đặc trưng | notebook 03, 04, 06 |
| E3 | Tinh chỉnh | Cấu hình được chọn cải thiện ở đâu, đặc biệt theo fold? | RandomizedSearchCV, 5 fold | notebook 05, 07 (verified_saved_search), `tuning_*_search_results.csv` |
| E4 | Test cuối | Cấu hình đã khóa đạt gì trên cùng 51.063 mẫu test? | chỉ chấm, không chọn lại | notebook 08, `final_test_metrics.csv` |
| E5 | Phân tích sai số | Sai ở trạm, tháng, mức PM2.5, đợt nào? | validation (baseline) và test (5 mô hình) | notebook 02, 04, 06, 08; `final_test_error_by_*.csv`, `final_test_worst_cases.csv` |
| E6 | Đóng góp feature | LR và RF phụ thuộc nhóm feature nào? | permutation theo nhóm, fold 5, mẫu 30.000, lặp 5 | notebook 02 (LR), 08 (RF) |
| E7 | Độ chắc chắn và ổn định | Chênh lệch mô hình và kết quả MLP chắc đến mức nào? | bootstrap theo khối 7 ngày (2000 lần); 3 seed; kiểm tra epoch | notebook 08; `paired_model_uncertainty.csv`, `mlp_seed_summary.csv`, `mlp_validation_diagnostics.csv` |

Mỗi thí nghiệm sau đó viết theo thứ tự: Mục tiêu → Kết quả (bảng/hình + nguồn) → Bình luận (vì sao).

### P7. DOCX 3.6 và slide 10: Hàm mất mát và tiêu chí huấn luyện
Câu mở: "Loss là đại lượng mô hình giảm khi học; metric là thước đo đánh giá trên dữ liệu chưa thấy. Hai thứ này khác nhau."

| Mô hình | Loss / tiêu chí huấn luyện thực dùng | Ghi chú |
|---|---|---|
| Persistence | Không huấn luyện | dự đoán PM2.5(t+1) = PM2.5(t) |
| Linear Regression | Bình phương sai số (bình phương tối thiểu) | đầu vào số được chuẩn hóa |
| Random Forest | criterion = squared_error | tiêu chí chia nhánh của cây hồi quy |
| Gradient Boosting (HistGradientBoostingRegressor) | loss = squared_error | cây xây tuần tự |
| MLP (MLPRegressor) | squared_error cộng chuẩn hóa L2 (alpha = 0,0001), tối ưu Adam; nhãn được chuẩn hóa khi học | đường loss huấn luyện trên thang đã chuẩn hóa, không phải RMSE theo µg/m³ |

(Nguồn: YC mục 3, "Loss"; `final_model_configuration.csv` ở YC 5.8.) Câu giới hạn: "Nhóm không so sánh các loss khác (ví dụ MAE, Huber, trọng số cho PM2.5 cao); đây là hướng phát triển." RMSE/MAE báo cáo luôn tính ở µg/m³.

### P8. DOCX 4.5 / slide 14: Bình luận chuyển từ validation sang test
- RF tuned có RMSE test thấp nhất (20,9613 µg/m³; MAE 10,5906; R² 0,9550), thấp hơn Persistence 9,31% và Linear Regression 3,86% (`final_test_relative_improvements.csv`).
- Khoảng bootstrap 95% (khối 7 ngày, 2000 lần, seed 42) của hiệu RMSE: RF - Persistence [-2,5553; -1,7699]; RF - LR [-1,1251; -0,5930] (không chứa 0); RF - GB [-0,7799; 0,1339] và RF - MLP [-1,3431; 0,2557] (chứa 0). Vì vậy chỉ khẳng định RF tốt hơn Persistence và LR trong phép đo này; chưa khẳng định RF thắng chắc GB hoặc MLP. (`paired_model_uncertainty.csv`; phép bootstrap có điều kiện trên dự đoán cố định và giai đoạn đã quan sát.)
- Thứ hạng đổi giữa validation và test: ở validation, GB tuned (20,04) cao hơn cả Persistence (19,97) và LR (19,29); ở test, GB tuned (21,2957) thấp hơn LR (21,8027). Khác biệt có thể đến từ việc test là giai đoạn thu-đông có PM2.5 trung bình cao hơn (92,18 so với 78,04 µg/m³) và từ cấu hình được chọn trên 5 fold; nhóm chưa kiểm tra nguyên nhân cụ thể.
- R² test của RF tuned (0,9550) cao hơn R² validation trung bình 5 fold của chính RF tuned (0,9377) trong khi RMSE test (20,9613) cao hơn RMSE validation (19,1779): R² phụ thuộc phương sai nhãn của giai đoạn, không nên đọc như "chính xác hơn".

### P9. DOCX 4.6 / slide 15: Sai số theo nhóm trên test, 5 mô hình (`final_test_error_by_*.csv`)
- Mức PM2.5 > 250 µg/m³ (3.685 mẫu): RMSE RF 44,593; LR 44,837; Persistence 46,247; GB 48,590; MLP 48,832. GB và MLP kém cả Persistence ở nhóm này dù xếp 2-3 tổng thể. Residual trung bình đều dương (RF 13,07; GB 13,24; LR 15,82; MLP 17,99): dự báo thấp hơn thực tế ở nồng độ rất cao.
- Mô hình có RMSE thấp nhất thay đổi theo nhóm: trạm (RF 7/12, GB 3, MLP 2), tháng (MLP 3, GB 2, RF 1: chỉ 01/2017), mùa (thu: GB 15,101; đông: RF 25,361), mức PM2.5 (GB 3 nhóm, MLP 2 nhóm: MLP thấp nhất ở ≤35 với 12,948 và (35,75]; RF chỉ thấp nhất ở >250).
- Theo tháng RF tuned có RMSE 11,359 (09/2016) đến 29,574 (01/2017); theo trạm RMSE RF từ 18,418 (Dingling) đến 24,639 (Wanshouxigong); cả năm mô hình đều thấp nhất ở Dingling và cao nhất ở Wanshouxigong.
- Giới hạn: nhóm chưa kiểm tra nguyên nhân (không suy đoán); chỉ mô tả.

### P10. DOCX 4.7 / slide 16: Importance theo nhóm
Bảng đặt cạnh nhau (RMSE tăng, µg/m³): PM2.5 hiện tại: LR 74,78, RF 51,86; PM2.5 lag và rolling: LR 5,05, RF 2,09; Chất ô nhiễm khác: LR 0,91 (xếp 4), RF 5,94 (xếp 2); Khí tượng: LR 1,37 (1,3749), RF 1,44; Thời gian: LR 0,62, RF 0,08; Trạm: LR 0,01, RF 0,003. Nguồn: `baseline_lr_group_permutation_importance.csv` (notebook 02), `rf_group_permutation_importance.csv` (notebook 08). Bình luận: cả hai mô hình dựa chủ yếu vào PM2.5 hiện tại; thứ hạng phía sau khác nhau (LR: lag/rolling thứ 2; RF: chất ô nhiễm khác thứ 2), nên không áp dụng thứ hạng LR cho RF. Điều kiện: RF fit trên train fold 5, chấm validation, mẫu 30.000, lặp 5, seed 42; RMSE gốc trên mẫu 17,5518 (LR: 17,76, chỉ in ở stdout notebook 02 ô cell-038 với 2 chữ số thập phân, không có CSV; cùng mẫu 30.000 dòng nhưng khác mô hình nên không so mức tăng tuyệt đối). Đây là mức phụ thuộc của mô hình, không phải nhân quả và không phải thí nghiệm bỏ feature rồi huấn luyện lại.

### P11. DOCX 4.8 / slide 17: Ổn định và hội tụ
- MLP tuned theo seed (RMSE trung bình 5 fold validation): 19,5268 (seed 7), 19,6317 (42), 19,2951 (2026); phạm vi 0,3366 µg/m³, cùng bậc với khoảng cách giữa MLP seed 42 và LR (19,6317 − 19,2950 = 0,3367) trên validation, nên thứ hạng LR và MLP tuned ở validation không đủ để kết luận. (`mlp_seed_summary.csv`; LR 19,2950 từ Bảng 8.)
- Kiểm tra giới hạn epoch (seed 42, fold 1-2; max_iter 40 → 100): fold 1 RMSE 26,1727 → 26,9824 (75 epoch, hết cảnh báo hội tụ); fold 2 15,9833 → 16,2132 (47 epoch, hết cảnh báo). Hết cảnh báo không làm validation tốt hơn; không dùng chẩn đoán này để đổi mô hình cuối. (`mlp_validation_diagnostics.csv`.)
- Provenance (đưa vào Phụ lục A và chú thích bảng): notebook 05 và 07 ghi `verify-saved-search-05/07`, chế độ `verified_saved_search`: đối chiếu artifact tuning đã lưu, không chạy lại RandomizedSearchCV; các notebook còn lại `computed`, thời điểm máy ghi 2026-11-20 (UTC) trong `report_sources.csv`. `diagnostics_manifest.json` ghi "operator: null" (không suy người chạy từ tài khoản/commit): tên người chạy chỉ điền khi nhóm xác nhận.

### P12. DOCX 4.9 / slide 18: Đánh giá tổng thể
1. So với công trình liên quan: nhóm không so trực tiếp RMSE với Seng và cs. (2021), Bekkar và cs. (2021), Wei và cs. (2025) vì khác dữ liệu, giai đoạn, tầm dự báo và độ đo; vì vậy không có tuyên bố vượt kết quả công bố. Đối chiếu chỉ ở mức phương pháp (theo mô tả trên slide 9, chưa kiểm tra bản gốc): Seng và cs. và Bekkar và cs. dùng mạng chuỗi hoặc mô hình lai; Wei và cs. dùng RF, XGBoost và FCNN; đề tài dùng mô hình cây và MLP trên đặc trưng lag/rolling và đạt cải thiện 9,31% RMSE so với Persistence, 3,86% so với LR trên test của chính đề tài.
2. Ý nghĩa thực tế (mức tối đa chứng minh được): với dự báo một giờ, Persistence đã đạt R² 0,9453 trên test; RF tuned chỉ giảm RMSE thêm 2,15 µg/m³ (23,1133 → 20,9613) và 0,84 µg/m³ so với LR (21,8027 → 20,9613). Chi phí tìm tham số trong `experiment_log.csv`: RF 1532,5 s, MLP 931,0 s, GB 691,4 s. Nhóm chưa có đánh giá của chuyên gia môi trường hay y tế, chưa triển khai và chưa kiểm tra trên trạm mới.
3. Hạn chế: test chỉ gồm thu-đông và các trạm đã quan sát; mô hình sai nhiều ở PM2.5 > 250 µg/m³ (dự báo thấp hơn thực tế); chưa dùng lag khí tượng, độ lệch so với rolling, cờ cuối tuần (Bảng 6); hai quan trắc 999 và 844 µg/m³ chưa xác minh được; hội tụ MLP và khoảng bootstrap phụ thuộc cách lấy khối.

### P13. DOCX mục 5 / slide 19: Kết luận và hướng phát triển
Kết luận (1 slide): (1) PM2.5(t+1) là bài toán hồi quy; Persistence mạnh (RMSE test 23,1133). (2) RF tuned có RMSE test thấp nhất (20,9613), tốt hơn Persistence và LR theo khoảng bootstrap; chưa đủ chắc so với GB và MLP. (3) Sai số tăng ở mùa đông và ở PM2.5 cao; không mô hình nào thắng ở mọi nhóm. (4) Importance LR và RF đều dựa chủ yếu vào PM2.5 hiện tại; không suy nhân quả. Phạm vi: 01/09/2016-28/02/2017 tại 12 trạm đã quan sát.
Hướng phát triển (chưa làm): dự báo t+24; mô hình riêng từng trạm / đánh giá trạm mới; thêm lag khí tượng, độ lệch so với rolling, cờ cuối tuần; phân tích độ nhạy hai điểm 999 và 844; so sánh loss khác. (Không đưa W&B/MLflow hay mô hình mới vào danh sách.)

### P14. DOCX mục 3.2 Pipeline và slide 8: câu "N phần" + khối
"Giải pháp gồm 7 phần: (1) dữ liệu 12 trạm; (2) nhãn t+1 và 27 đặc trưng; (3) chia theo thời gian (train/validation đến 31/08/2016; test từ 01/09/2016); (4) tiền xử lý fit trên train của fold; (5) 5 mô hình + tuning bằng RandomizedSearchCV trên 5 fold; (6) khóa cấu hình theo RMSE validation; (7) chấm test và phân tích sai số/độ chắc chắn." Dùng cùng một bản hình cho DOCX (Hình 7) và slide 8; thêm chú thích: tiền xử lý chỉ fit trên train của từng fold.

### P15. DOCX Phụ lục D (Bảng 17 viết lại, không dùng "theo lịch sử commit")
Cột: Thành viên | Phần việc có sản phẩm trong repo (notebook/thư mục) | Nhóm xác nhận (Đã/Chưa). Chỉ giữ dòng có bằng chứng sản phẩm và để cột xác nhận; không ghi tên người chạy hoặc ngày chạy cho tới khi nhóm xác nhận. Thống nhất với `README.md` (hiện ba thành viên Nhân, Tài, Tuấn còn ghi "Phần việc cụ thể sẽ được nhóm thống nhất và cập nhật") và `phan-cong-cong-viec.docx` (phạm vi Bảo kết thúc ở pipeline dữ liệu).

### P16. DOCX bảng nguồn số liệu (Phụ lục A, trích `report_sources.csv`)
| Bảng/Hình trong báo cáo | Notebook, mã ô | CSV nguồn | Chế độ | Ghi lúc (UTC) | Người chạy |
|---|---|---|---|---|---|
| Bảng 3, EDA (3.1-4.1) | 01, evidence-nb-01 | `outputs/eda/tables/dataset_counts.csv`, `raw_pm25_summary.csv`, `pm25_acf.csv`, `pm25_by_wind_*.csv` | computed | 2026-11-20 16:09 | [nhóm xác nhận] |
| Bảng 8, 9 (baseline) | 02, evidence-nb-02 | `baseline_cv_metrics.csv`, `baseline_cv_summary.csv` | computed | 2026-11-20 16:11 | [nhóm xác nhận] |
| Bảng 8, 9 (RF, GB, MLP ban đầu) | 03, 04, 06 | `random_forest_cv_*.csv`, `gradient_boosting_cv_*.csv`, `mlp_cv_*.csv` | computed | 2026-11-20 16:13 / 16:14 / 16:16 | [nhóm xác nhận] |
| Bảng 8, 9, 10 (tuned) | 05, 07, verify-saved-search-05/07 | `tuning_*_search_results.csv`, `*_tuned_cv_*.csv` | verified_saved_search | 2026-11-20 16:15 | [nhóm xác nhận] |
| Bảng 11 và bảng test mới | 08, evidence-nb-08 | `final_test_metrics.csv`, `final_test_relative_improvements.csv`, `final_test_error_by_*.csv`, `paired_model_uncertainty.csv` | computed | 2026-11-20 16:20 | [nhóm xác nhận] |
| Bảng importance RF, seed, epoch | 08, evidence-nb-08 | `rf_group_permutation_importance.csv`, `mlp_seed_summary.csv`, `mlp_validation_diagnostics.csv` | computed | 2026-11-20 16:20 | [nhóm xác nhận] |
| Bảng 15 (LR importance) | 02 | `baseline_lr_group_permutation_importance.csv` | computed | 2026-11-20 16:11 | [nhóm xác nhận] |

Chân bảng/hình mẫu: "Nguồn: notebook 08, evidence-nb-08; `outputs/notebooks/tables/final_test_metrics.csv`."

### P17. Slide: chỉnh theo yêu cầu cấu trúc
- Slide 10 (Mô hình + loss, thay slide 15): tiêu đề "Năm mô hình, bốn loss bình phương sai số"; 1 hình (khối Input 27 cột → tiền xử lý 79 cột → mô hình → ŷ µg/m³; MLP [79,32],[32,16],[16,1]); bảng loss như P7; ghi "Gradient Boosting = HistGradientBoostingRegressor". Cột 79 và layer shapes theo `final_model_configuration.csv` (YC 5.8); cần xác nhận khi dựng hình.
- Slide 12 (Danh sách TN): dùng bảng P6 rút gọn hai cột (Mã, câu hỏi).
- Slide 13: một bảng Validation 8 cấu hình rút gọn (RMSE) + 1 hình fold; ghi "đủ 5 fold".
- Slide 16: tiêu đề "Importance theo nhóm: LR và RF" (không phải "chỉ LR").
- Slide 18: ba cột "So với công trình liên quan / Ý nghĩa thực tế / Hạn chế" theo P12.
- Slide 19: Kết luận + hướng phát triển theo P13, 1 slide.
- Ghi chú người thuyết trình: mỗi slide thêm 1 dòng nguồn (notebook, mã ô, CSV) và người trình bày.
- Xóa ảnh pipeline cũ mồ côi (`ppt/media/image5.png`) khỏi slide 14.
