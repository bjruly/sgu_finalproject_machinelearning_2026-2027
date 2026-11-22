# Đề xuất chỉnh sửa DOCX phần 2: Mục 6 đến Mục 9 và Phụ lục A, B, C

Phạm vi rà soát: dòng 213 đến 406 của bản trích văn bản DOCX (Kết quả thực nghiệm 6.1 đến 6.7, Đánh giá tiến độ 7, Phân công 8, Tài liệu tham khảo 9, Phụ lục A, B, C).

Quy ước dùng trong tệp này:

- Mọi con số đều lấy từ CSV/JSON trong kho mã nguồn (ghi nguồn ngay dưới từng bảng) hoặc được tính lại bằng chương trình từ chính các CSV đó. Dấu phẩy là dấu thập phân; dấu chấm là dấu phân cách hàng nghìn.
- Khối có tiêu đề "DÁN VÀO DOCX" là nội dung sẵn sàng dán. Khối "Ghi chú kiểm chứng" chỉ dành cho nhóm, không dán.
- Bảng mới đánh số tạm bằng hậu tố chữ (ví dụ Bảng 7A). Khi dán vào DOCX, đánh số lại toàn bộ Bảng và Hình theo thứ tự xuất hiện, rồi cập nhật Mục lục và các tham chiếu chéo (ví dụ Mục 1.2 đang nói "Bảng 1", Mục 8 đang nói "Bảng 1").
- Người chạy notebook không được suy ra từ tác giả commit. diagnostics_manifest.json ghi operator = null và ghi chú "Not inferred from account, Git author or machine name". Những chỗ cần nhóm xác nhận được đánh dấu [CẦN NHÓM XÁC NHẬN].
- Phạm vi: chỉ hồi quy PM2.5 chuỗi thời gian. Không đề xuất thay đổi cấu hình mô hình đã khóa, không chọn lại mô hình theo kết quả test, không thêm thư viện hay công nghệ mới.

---

## 0. Bảng tổng hợp các điểm cần sửa (chi tiết ở các mục sau)

| Vị trí | Mức | Vấn đề ngắn gọn |
|---|---|---|
| Bảng 14 (Mục 6.5) | Cao | Còn dùng biên nhóm cũ (số mẫu 112.846; 72.798; ...). Biên hiện hành là ≤35, (35;75], (75;115], (115;150], (150;250], >250 với số mẫu 115.085; 72.055; 45.799; 24.358; 30.226; 13.173. Mọi cột metric đều đổi. Residual LR ở nhóm >250 là 19,06 chứ không phải 18,98. |
| Mục 6.5 | Cao | Thiếu sai số theo nhóm của mô hình tinh chỉnh trên test (đã có 4 CSV final_test_error_by_*). |
| Mục 6.4, Bảng 12 | Cao | Bảng theo tháng chỉ có 2 baseline và dẫn nguồn notebook 02; đã có đủ 5 mô hình từ notebook 08. Thiếu bảng mùa, trạm. |
| Mục 6.6, Bảng 15 | Trung bình | Thiếu importance của Random Forest. Mục LR: nhóm khí tượng ghi 1,38 nhưng CSV là 1,3749 (làm tròn 1,37). RMSE gốc 17,76 chỉ có trong output notebook 02, không có trong CSV. |
| Mục 6.7 | Cao | CH2 chỉ nói LR; CH3 chỉ nói validation baseline; thiếu độ chắc chắn, thiếu giới hạn. Cần viết lại. |
| Thiếu mục mới | Cao | Chưa có mục về độ chắc chắn (bootstrap), ổn định seed MLP, hội tụ MLP; chưa có "Đánh giá tổng thể" (so sánh công trình liên quan và ý nghĩa thực tế). |
| Mục 6 mở đầu | Cao | Thiếu danh sách thí nghiệm kèm câu hỏi cần kiểm chứng trước khi trình bày kết quả. |
| Mục 6.1 | Trung bình | Câu "chấm trên 300.696 dự đoán OOF cộng lại" dễ gây hiểu nhầm: Bảng 8 là trung bình số học của 5 chỉ số theo fold (LR 19,2950), không phải RMSE gộp OOF (LR 19,44; Persistence 20,12 theo baseline_error_analysis.csv). |
| Bảng 10 (Mục 6.3) | Trung bình | Cột "RMSE giảm" không nói giảm so với gì (so với cấu hình ban đầu, trung bình 5 fold). Thiếu nhận xét: phần lớn mức giảm đến từ fold 1. |
| Mục 7.2, 7.3, Bảng 16 | Cao | Còn câu lỗi thời "Notebook 08 xuất điểm test tổng thể. Bảng sai số theo tháng trên test hiện có cho hai baseline" và dòng "Phân tích bổ sung ... nếu mở rộng báo cáo" (đã làm). |
| Mục 8, Bảng 17 | Cao | Phân công suy từ lịch sử commit. Mâu thuẫn: tests/ gán cho Tài nhưng phan-cong-cong-viec.docx gán kiểm thử cho Trần Lê Gia Bảo. Phần mới (phân tích sai số, importance RF, bootstrap, seed/epoch, kiểm tra nguồn) chưa có người nhận. |
| Mục 9 | Trung bình | Slide 9 trích Seng 2021, Bekkar 2021, Wei 2025 và slide 10 trích WHO 2021 nhưng DOCX chưa có. |
| Phụ lục A | Thấp | A1 khớp experiment_log.csv (13 dòng). Nên thêm cột nguồn notebook/ô. |
| Phụ lục B | Thấp | B1 khớp baseline_error_analysis.csv. Nên thêm B2 (test, 5 mô hình, theo trạm). |
| Phụ lục C | Trung bình | Thiếu lệnh verify_result_sources.py, run_notebooks.py, src.evaluation, src.validation_diagnostics, requirements-lock.txt, fallback baseline. |

---

## Mục 6. Kết quả thực nghiệm (đoạn mở đầu thay thế)

### DÁN VÀO DOCX

Mục này trình bày kết quả theo bảy nhóm thực nghiệm ở Bảng 7A. Mỗi nhóm nêu câu hỏi cần kiểm chứng, điều kiện chạy, kết quả và nhận xét. Kết quả validation (Mục 6.1 đến 6.3) dùng 5 fold expanding-window trên các mẫu có nhãn trước 01/09/2016. Kết quả test (Mục 6.4 trở đi) dùng 51.063 mẫu có nhãn từ 01/09/2016 đến 28/02/2017 và chỉ dùng để đánh giá các cấu hình đã khóa; nhóm không chọn lại mô hình hay siêu tham số theo kết quả test. Các cấu hình được chọn bằng 5 fold validation; điểm test của năm mô hình được chấm ở notebook 08, và điểm test của hai baseline cũng từng xuất hiện trong lịch sử notebook 02, nên báo cáo không khẳng định tập test chưa từng được nhìn tới trước bước cuối.

Mọi số liệu lấy từ các bảng CSV do notebook 01 đến 08 xuất. Bảng ánh xạ giữa từng CSV, notebook, mã ô, lượt thực thi và thời điểm ghi nhận nằm ở outputs/notebooks/tables/report_sources.csv và được kiểm tra bằng scripts/verify_result_sources.py (Bảng 7B). Notebook 05 và 07 chạy ở chế độ verified_saved_search: chỉ đối chiếu kết quả tìm kiếm tham số đã lưu từ lần tìm kiếm trước, không chạy lại RandomizedSearchCV.

Bảng 7A. Danh sách thực nghiệm và câu hỏi cần kiểm chứng

| Mã | Nhóm thực nghiệm | Câu hỏi cần kiểm chứng | Điều kiện | Mục | Notebook và nguồn |
|---|---|---|---|---|---|
| E1 | Baseline | Persistence mạnh đến đâu? Linear Regression cải thiện ở độ đo nào? | 5 fold validation, 300.696 dự đoán ngoài mẫu | 6.1, 6.2 | 02; baseline_cv_metrics.csv, baseline_cv_summary.csv |
| E2 | Mô hình ban đầu | Random Forest, Gradient Boosting, MLP có vượt hai baseline trên validation không? | Cùng 5 fold, cùng 27 đặc trưng | 6.1, 6.2 | 03, 04, 06; *_cv_metrics.csv |
| E3 | Tinh chỉnh | Cấu hình được chọn cải thiện ở đâu, đặc biệt theo fold? | RandomizedSearchCV: 8, 20, 8 tổ hợp; chọn theo RMSE trung bình 5 fold | 6.3 | 05, 07 (verified_saved_search); tuning_*_search_results.csv |
| E4 | Test cuối | Cấu hình đã khóa đạt kết quả thế nào trên cùng tập test? | 51.063 mẫu, 09/2016 đến 02/2017 | 6.4 | 08; final_test_metrics.csv, final_test_relative_improvements.csv |
| E5 | Phân tích sai số | Mô hình sai nhiều ở trạm, tháng, mùa, mức PM2.5 hay sự kiện nào? | Baseline trên validation; năm mô hình trên test | 6.4, 6.5 | 02, 04, 06, 08; baseline_error_analysis.csv, final_test_error_by_*.csv, final_test_worst_cases.csv |
| E6 | Đóng góp đặc trưng | Linear Regression và Random Forest phụ thuộc vào nhóm đặc trưng nào? | Fold 5, mẫu 30.000 dòng validation, 5 lần hoán vị | 6.6 | 02, 08; baseline_lr_group_permutation_importance.csv, rf_group_permutation_importance.csv |
| E7 | Độ chắc chắn và ổn định | Chênh lệch giữa các mô hình có phân biệt được không? MLP ổn định theo seed và giới hạn epoch đến đâu? | Bootstrap khối 7 ngày, 2.000 lần; MLP 3 seed; kiểm tra epoch ở fold 1 và 2 | 6.7 | 08; paired_model_uncertainty.csv, mlp_seed_summary.csv, mlp_validation_diagnostics.csv |

Nguồn Bảng 7A: docs/nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md mục 4; số tổ hợp từ tuning_*_search_results.csv (8, 20, 8 dòng).

Bảng 7B. Truy vết nguồn số liệu (trích từ report_sources.csv)

| Notebook | Mã ô nguồn | Chế độ | Lượt thực thi | Số CSV | Thời điểm ghi nhận (UTC) |
|---|---|---|---|---|---|
| 01 | evidence-nb-01 | tính trong lần chạy | 9 | 7 | 2026-11-20 16:09:52 |
| 02 | evidence-nb-02 | tính trong lần chạy | 28 | 6 | 2026-11-20 16:11:04 |
| 03 | evidence-nb-03 | tính trong lần chạy | 13 | 4 | 2026-11-20 16:13:04 |
| 04 | evidence-nb-04 | tính trong lần chạy | 15 | 5 | 2026-11-20 16:14:01 |
| 05 | verify-saved-search-05 | đối chiếu bản lưu | 1 | 6 | 2026-11-20 16:15:34 |
| 06 | evidence-nb-06 | tính trong lần chạy | 11 | 4 | 2026-11-20 16:16:07 |
| 07 | verify-saved-search-07 | đối chiếu bản lưu | 1 | 3 | 2026-11-20 16:15:37 |
| 08 | evidence-nb-08 | tính trong lần chạy | 9 | 15 | 2026-11-20 16:20:04 |

Giờ ghi nhận là UTC; giờ Việt Nam sớm hơn 7 giờ (ví dụ 16:09 UTC là 23:09 ngày 20/11/2026). Lần tính phân tích bổ sung trên test (evaluation_manifest.json) tạo lúc 2026-11-20 16:16:23 UTC, lần chẩn đoán validation (diagnostics_manifest.json) lúc 2026-11-20 16:20:03 UTC, cùng Python 3.13.12 và scikit-learn 1.7.2. Tệp manifest ghi commit nền ceacd7b và working_tree_dirty = true, nghĩa là kho mã có thay đổi chưa commit tại thời điểm chạy. Người thực hiện lần chạy này chưa được ghi trong artifact [CẦN NHÓM XÁC NHẬN].

### Ghi chú kiểm chứng (không dán)

- Nguồn: outputs/notebooks/tables/report_sources.csv (cột recorded_at_utc, execution_count, mode); outputs/experiments/final_test/analysis/evaluation_manifest.json (created_at_utc, git_commit, working_tree_dirty); outputs/experiments/validation_diagnostics/diagnostics_manifest.json (operator null).
- Mô hình tinh chỉnh được lưu trước khi chấm test: models/*_tuned_metadata.json ghi created_at 2026-11-11 (RF, GB) và 2026-11-18 (MLP) với test_evaluated = False. Có thể dùng làm bằng chứng "cấu hình được khóa trước khi chấm test" nhưng không đủ để khẳng định chưa ai từng nhìn test.
- Thư mục Experimental Log có README nói một số thư mục ngày là bản dựng lại (RECONSTRUCTION_NOTE.md). Không dùng tên thư mục ngày để khẳng định ai chạy ngày nào.

---

## Mục 6.1. So sánh trên tập validation

Bảng 8 (và các giá trị trong đó) khớp baseline_cv_summary.csv và các *_cv_summary.csv. Không cần đổi số. Cần sửa cách diễn đạt và thêm nhận xét.

### DÁN VÀO DOCX (thay đoạn bắt đầu "Mỗi cấu hình được chấm trên 300.696 dự đoán...")

Mỗi giá trị trong Bảng 8 là trung bình số học của chỉ số tính riêng trên từng fold trong 5 fold, kèm độ lệch chuẩn giữa các fold. Đây không phải RMSE gộp trên toàn bộ 300.696 dự đoán ngoài mẫu (OOF); hai cách tính cho kết quả hơi khác nhau (ví dụ Linear Regression: 19,2950 theo trung bình fold và 19,44 theo RMSE gộp OOF; Persistence: 19,9665 và 20,12). Các Bảng 13, 14 và B1 dùng cách gộp OOF theo nhóm nên không so trực tiếp được với Bảng 8. Nguồn: baseline_cv_summary.csv, baseline_metrics.csv và baseline_error_analysis.csv (notebook 02, ô evidence-nb-02), random_forest_*_cv_summary.csv, gradient_boosting_*_cv_summary.csv, mlp_*_cv_summary.csv.

Random Forest tinh chỉnh có RMSE validation trung bình thấp nhất (19,18 µg/m³), tiếp theo là Linear Regression (19,29) và MLP tinh chỉnh (19,63). Khoảng cách giữa Random Forest tinh chỉnh và Linear Regression chỉ là 0,12 µg/m³, nhỏ hơn nhiều so với độ lệch chuẩn giữa các fold (2,62 đến 3,44 µg/m³), nên nhóm không xem đây là khác biệt chắc chắn trên validation. Theo từng fold (Bảng 9), Random Forest tinh chỉnh thấp hơn Linear Regression ở 4 trong 5 fold (fold 2 đến 5) và cao hơn ở fold 1 (24,92 so với 23,39). Gradient Boosting tinh chỉnh (20,04) vẫn cao hơn Persistence (19,97) và Linear Regression. Linear Regression giảm RMSE 3,36% so với Persistence nhưng làm MAE tăng 3,01%.

### Ghi chú kiểm chứng (không dán)

- 19,2950 - 19,1779 = 0,1171 (baseline_cv_summary.csv, random_forest_tuned_cv_summary.csv). Độ lệch chuẩn RMSE: LR 2,6205; RF tinh chỉnh 3,4416.
- RMSE gộp OOF tính lại từ baseline_error_analysis.csv (nhóm theo mùa, gộp theo số mẫu): LR 19,4446; Persistence 20,1232. Hai số này làm tròn thành 19,44 và 20,12. Đây là phép tính lại từ bảng nhóm, không phải cột có sẵn trong CSV; nếu muốn dẫn nguồn chính thức, đối chiếu với output notebook 02 hoặc bỏ phần ví dụ trong ngoặc.
- Theo fold: RF tinh chỉnh so với LR = 24,92/23,39; 16,09/16,81; 19,05/20,06; 18,82/18,84; 17,00/17,37 (random_forest_tuned_cv_metrics.csv, baseline_cv_metrics.csv). Fold 4 chênh 0,02, thực chất ngang nhau.

---

## Mục 6.2. Kết quả theo từng fold

Bảng 9 khớp các *_cv_metrics.csv (đã kiểm tra cả 8 dòng, cả cột TB 2 đến 5). Đoạn dưới bổ sung nhận xét còn thiếu về fold 1.

### DÁN VÀO DOCX (thêm sau đoạn "Fold 1 huấn luyện trên 60.258 mẫu...")

Ở fold 1, tập huấn luyện chỉ gồm các nhãn từ 01/03/2013 đến 30/09/2013, tức không có tháng mùa đông, trong khi tập validation chạy đến 01/05/2014. Chỉ Linear Regression (23,39 µg/m³) thấp hơn Persistence (24,15) ở fold này; cả sáu cấu hình Random Forest, Gradient Boosting và MLP (ban đầu và tinh chỉnh) đều cao hơn Persistence, từ 24,92 đến 37,11 µg/m³. Từ fold 2 đến fold 5, khoảng cách giữa các mô hình thu hẹp (trung bình 17,74 đến 18,92 µg/m³ ở cột TB 2 đến 5). Nhóm chỉ ghi nhận các mô hình cây và MLP kém hơn trong điều kiện tập huấn luyện chưa có dữ liệu mùa đông; nguyên nhân chưa được kiểm chứng bằng thí nghiệm riêng.

### Ghi chú kiểm chứng (không dán)

- Nguồn: random_forest_fold_overview.csv (fold 1: train 2013-03-01 đến 2013-09-30, validation 2013-09-30 01:00 đến 2014-05-01 17:00), *_cv_metrics.csv.
- Fold 1 RMSE: Persistence 24,1516; LR 23,3928; RF ban đầu 29,8863; RF tinh chỉnh 24,9225; GB ban đầu 37,1143; GB tinh chỉnh 27,1892; MLP ban đầu 28,0582; MLP tinh chỉnh 26,1727. Chỉ LR (23,3928) thấp hơn Persistence (24,1516); sáu cấu hình RF, GB, MLP đều cao hơn (24,9225 đến 37,1143).

---

## Mục 6.3. Tinh chỉnh siêu tham số

Số tổ hợp (8, 20, 8) và bộ tham số trong Bảng 10 khớp tuning_*_search_results.csv. Phần trăm giảm RMSE khớp: RF 4,92%, GB 8,80%, MLP 2,25% (so với RMSE trung bình 5 fold của cấu hình ban đầu). Cần thay Bảng 10 để nêu rõ mốc so sánh và thêm nhận xét.

### DÁN VÀO DOCX (thay Bảng 10 và đoạn nhận xét sau bảng)

Bảng 10. Cấu hình được chọn và mức giảm RMSE validation (trung bình 5 fold, so với cấu hình ban đầu)

| Mô hình | Số tổ hợp đã thử | Cấu hình được chọn | Cấu hình ban đầu | RMSE validation (µg/m³) | RMSE giảm |
|---|---|---|---|---|---|
| Random Forest | 8 (trong không gian 192 tổ hợp) | n_estimators=50, max_depth=None, min_samples_leaf=20, max_features=0,7 | 20 cây, max_depth=16, min_samples_leaf=5, max_features=0,7 | 20,1707 → 19,1779 | 4,92% |
| Gradient Boosting | 20 (learning_rate lấy mẫu liên tục) | learning_rate≈0,06937, max_iter=100, max_leaf_nodes=127, min_samples_leaf=200, l2_regularization=1 | learning_rate=0,1, max_iter=200, max_leaf_nodes=31, min_samples_leaf=20, l2_regularization=0 | 21,9726 → 20,0384 | 8,80% |
| MLP | 8 (trong không gian 243 tổ hợp) | hidden_layer_sizes=(32, 16), learning_rate_init=0,003, alpha=0,0001, batch_size=256, max_iter=40 | (64, 32), learning_rate_init=0,001, alpha=0,001, batch_size=512, max_iter=60 | 20,0840 → 19,6317 | 2,25% |

Nguồn Bảng 10: tuning_random_forest_search_results.csv, tuning_gradient_boosting_search_results.csv, tuning_mlp_search_results.csv, random_forest_tuned_metadata.json, gradient_boosting_tuned_metadata.json, mlp_tuned_metadata.json (notebook 05 ô verify-saved-search-05; notebook 07 ô verify-saved-search-07). Hai notebook này chỉ đối chiếu kết quả tìm kiếm đã lưu (verified_saved_search), không chạy lại RandomizedSearchCV; metadata ghi thời điểm lưu mô hình là 11/11/2026 (RF, GB) và 18/11/2026 (MLP).

Mức giảm RMSE trung bình có được chủ yếu nhờ fold 1. Với Random Forest, RMSE fold 1 giảm từ 29,89 xuống 24,92 µg/m³ và đóng góp khoảng 100% mức giảm trung bình; với Gradient Boosting, fold 1 giảm từ 37,11 xuống 27,19 và mức giảm ở bốn fold còn lại bằng không hoặc âm (trung bình fold 2 đến 5 đổi từ 18,19 thành 18,25); với MLP, fold 1 giảm từ 28,06 xuống 26,17 và đóng góp khoảng 83% mức giảm. Nói cách khác, tinh chỉnh chủ yếu cải thiện giai đoạn đầu khi tập huấn luyện chưa có mùa đông và gần như không đổi trung bình fold 2 đến 5 (Random Forest 17,74 trước và sau; MLP 18,09 xuống 18,00). Cấu hình được chọn có xu hướng chính quy hóa mạnh hơn hoặc mô hình nhỏ hơn ở một số tham số (lá tối thiểu 20 thay vì 5 ở Random Forest; min_samples_leaf=200 và l2=1 ở Gradient Boosting, dù max_leaf_nodes tăng từ 31 lên 127 và Random Forest dùng 50 thay vì 20 cây; mạng (32, 16) thay cho (64, 32) ở MLP). Nhóm chưa kiểm tra riêng tham số nào tạo ra mức giảm.

Số tổ hợp thử nhỏ so với không gian tìm kiếm (8 trên 192 ở Random Forest, 8 trên 243 ở MLP), nên các cấu hình tinh chỉnh là kết quả tìm kiếm có giới hạn, không phải tối ưu toàn cục. Điểm validation sau tinh chỉnh dùng đúng các fold đã tham gia chọn cấu hình, nên có thể lạc quan; Bảng 11 đánh giá các cấu hình đó trên dữ liệu giữ riêng.

### Ghi chú kiểm chứng (không dán)

- Không gian tìm kiếm: RF 3x4x4x4 = 192; MLP 3x3x3x3x3 = 243 (mlp_tuned_metadata.json, random_forest_tuned_metadata.json trong evaluation_manifest.json); GB: learning_rate loguniform(0,02; 0,3), max_iter 4 giá trị, max_leaf_nodes 4, min_samples_leaf 4, l2 4 giá trị.
- Phần đóng góp của fold 1 tính lại: RF tổng giảm 0,9929, từ fold 1 0,9928 (100,0%); GB tổng 1,9341, từ fold 1 1,9850 (102,6%); MLP tổng 0,4523, từ fold 1 0,3771 (83,4%). GB vượt 100% vì bốn fold còn lại hơi tệ đi.
- Cấu hình ban đầu lấy từ trường untuned_params / baseline_params trong evaluation_manifest.json (models.*.metadata.tuning). Bảng 7 của DOCX đã ghi đúng cấu hình ban đầu của RF (20 cây, max_depth=16, min_samples_leaf=5, max_features=0,7) và GB (max_iter=200, learning_rate=0,1); max_leaf_nodes=31, min_samples_leaf=20, l2=0 của GB và batch_size=512, learning_rate_init=0,001, alpha=0,001, max_iter=60 của MLP lấy từ metadata.

---

## Mục 6.4. Đánh giá cuối trên tập test

Bảng 11 khớp final_test_metrics.csv (đã kiểm tra 5 dòng). Đề xuất thêm cột mức giảm từ final_test_relative_improvements.csv và thay đoạn nhận xét.

### DÁN VÀO DOCX (thay Bảng 11 và hai đoạn sau Bảng 11)

Bảng 11. Kết quả đánh giá cuối trên tập test (51.063 mẫu), xếp theo RMSE

| Hạng | Mô hình | MAE (µg/m³) | RMSE (µg/m³) | R² | RMSE giảm so với Persistence | RMSE giảm so với Linear Reg. |
|---|---|---|---|---|---|---|
| 1 | Random Forest tinh chỉnh | 10,5906 | 20,9613 | 0,9550 | 9,31% | 3,86% |
| 2 | Gradient Boosting tinh chỉnh | 10,8195 | 21,2957 | 0,9536 | 7,86% | 2,33% |
| 3 | MLP tinh chỉnh | 11,1583 | 21,4967 | 0,9527 | 6,99% | 1,40% |
| 4 | Linear Regression | 11,3510 | 21,8027 | 0,9513 | 5,67% | — |
| 5 | Persistence | 11,5864 | 23,1133 | 0,9453 | — | −6,01% |

Nguồn: final_test_metrics.csv, final_test_relative_improvements.csv (notebook 08, ô evidence-nb-08). Số âm ở dòng Persistence nghĩa là Persistence cao hơn Linear Regression.

Random Forest tinh chỉnh đạt MAE thấp nhất (10,5906 µg/m³), RMSE thấp nhất (20,9613) và R² cao nhất (0,9550). RMSE của mô hình thấp hơn Persistence 9,31% (2,15 µg/m³) và thấp hơn Linear Regression 3,86% (0,84 µg/m³); với MAE, mức giảm lần lượt là 8,60% (1,00 µg/m³) và 6,70% (0,76 µg/m³). Gradient Boosting và MLP tinh chỉnh xếp thứ 2 và 3 theo RMSE, cùng thấp hơn Linear Regression ở giá trị ước lượng (2,33% và 1,40%). Mục 6.7 cho thấy khoảng bootstrap của Random Forest so với Gradient Boosting và MLP đều chứa 0 nên thứ hạng 1 đến 3 chưa được phân biệt chắc chắn; chỉ chênh lệch giữa Random Forest và hai baseline là tách khỏi 0.

Thứ hạng trên test khác thứ hạng trên validation (Bảng 8): trên validation Linear Regression (19,29) đứng trước MLP tinh chỉnh (19,63) và Gradient Boosting tinh chỉnh (20,04), còn trên test cả hai mô hình này đứng trước Linear Regression (21,80). Các chênh lệch đều nhỏ so với độ lệch chuẩn giữa các fold (2,6 đến 4,4 µg/m³), nên nhóm không rút ra kết luận chắc chắn về thứ tự của Linear Regression, Gradient Boosting và MLP. RMSE test của mọi mô hình cao hơn RMSE validation trung bình nhưng R² test cao hơn; R² phụ thuộc phương sai của số đo thực (PM2.5 trung bình test 92,18 so với 78,04 ở train/validation), nên R² giữa hai tập không dùng để so sánh độ khó, và với hồi quy nhóm không dùng từ "độ chính xác (accuracy)" cho R² hay phần trăm giảm RMSE.

### Ghi chú kiểm chứng (không dán)

- MAE giảm: RF so với Persistence 11,5864 - 10,5906 = 0,9958; so với LR 11,3510 - 10,5906 = 0,7604. RMSE: 23,1133 - 20,9613 = 2,1520 (khớp paired_model_uncertainty.csv: -2,1520); 21,8027 - 20,9613 = 0,8414 (khớp -0,8414).
- Phần trăm: final_test_relative_improvements.csv (RF/Persistence 9,3107 và 8,5951; RF/LR 3,8593 và 6,6990; GB/Persistence 7,8638; MLP/Persistence 6,9943; LR/Persistence 5,6702; GB/LR 2,3255; MLP/LR 1,4036; Persistence/LR -6,0111).
- PM2.5 trung bình: target_split_summary.csv (78,0440 và 92,1773).


### DÁN VÀO DOCX (thay Bảng 12 và câu dẫn trước nó: "Bảng dưới đây bổ sung phân tích theo tháng của hai baseline từ notebook 02...")

Phân tích sai số theo tháng, mùa và trạm của cả năm mô hình lấy từ notebook 08 (final_test_error_by_month.csv, final_test_error_by_season.csv, final_test_error_by_station.csv); số mẫu của mỗi cách nhóm cộng lại đúng 51.063 cho từng mô hình. Chữ đậm là giá trị thấp nhất trong hàng. Các nhóm này nhỏ hơn tập đầy đủ, nên chênh lệch giữa các mô hình trong từng nhóm chưa có khoảng tin cậy.

Bảng 12. RMSE (µg/m³) theo tháng trên test của năm mô hình

| Tháng | Số mẫu | PM2.5 TB thực | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|---|---|
| 09/2016 | 8.209 | 54,1 | 12,46 | 12,58 | 11,36 | 11,19 | **11,10** |
| 10/2016 | 8.665 | 84,2 | 15,98 | 15,37 | 14,31 | **14,09** | 14,22 |
| 11/2016 | 8.609 | 97,5 | 20,83 | 19,29 | 19,13 | **18,86** | 19,86 |
| 12/2016 | 8.852 | 129,2 | 29,20 | 27,16 | 26,39 | 26,64 | **25,94** |
| 01/2017 | 8.886 | 113,3 | 32,16 | 30,53 | **29,57** | 31,07 | 31,83 |
| 02/2017 | 7.842 | 69,3 | 20,57 | 19,27 | 17,91 | 17,80 | **17,78** |

Bảng 12b. MAE (µg/m³) theo tháng trên test của năm mô hình

| Tháng | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|
| 09/2016 | 7,35 | 7,79 | **6,93** | 6,95 | 7,07 |
| 10/2016 | 8,92 | 9,15 | 8,10 | **8,04** | 8,38 |
| 11/2016 | 11,95 | 11,22 | 10,82 | **10,74** | 11,37 |
| 12/2016 | 15,75 | 14,92 | **14,28** | 14,88 | 14,86 |
| 01/2017 | 15,27 | 14,76 | **14,09** | 14,91 | 15,49 |
| 02/2017 | 9,70 | 9,76 | **8,79** | 8,80 | 9,19 |

Bảng 12c. RMSE (µg/m³) và MAE (µg/m³) theo mùa trên test của năm mô hình

| Mùa | Số mẫu | Độ đo | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|---|---|
| Thu (9–11) | 25.483 | RMSE | 16,83 | 16,03 | 15,32 | **15,10** | 15,54 |
|  |  | MAE | 9,43 | 9,41 | 8,64 | **8,60** | 8,97 |
| Đông (12–2) | 25.580 | RMSE | 28,00 | 26,32 | **25,36** | 26,04 | 26,11 |
|  |  | MAE | 13,73 | 13,28 | **12,53** | 13,03 | 13,34 |

Nhận xét. Sai số tăng mạnh theo mức ô nhiễm: RMSE của Random Forest tinh chỉnh là 11,36 µg/m³ vào 09/2016 (PM2.5 trung bình 54,1) và 29,57 µg/m³ vào 01/2017 (PM2.5 trung bình 113,3), tức gấp khoảng 2,6 lần trong khi mức PM2.5 trung bình gấp khoảng 2,1 lần. Tháng 01/2017 có RMSE cao nhất ở cả năm mô hình. Mùa đông khó hơn mùa thu ở mọi mô hình (RMSE Random Forest: 25,36 so với 15,32 µg/m³).

Random Forest không phải mô hình tốt nhất ở mọi nhóm. Theo RMSE, Random Forest đứng đầu ở 1 trong 6 tháng (01/2017); MLP đứng đầu ở 09/2016, 12/2016 và 02/2017; Gradient Boosting đứng đầu ở 10/2016 và 11/2016. Chênh lệch giữa Random Forest và mô hình tốt nhất trong tháng chỉ từ 0,13 đến 0,45 µg/m³. Theo MAE, Random Forest thấp nhất ở 4 trong 6 tháng (09/2016, 12/2016, 01/2017, 02/2017). Ở mùa thu, Gradient Boosting có RMSE thấp nhất (15,10 so với 15,32 của Random Forest); ở mùa đông, Random Forest thấp nhất (25,36). Linear Regression thấp hơn Gradient Boosting và MLP về RMSE trong 01/2017 (30,53 so với 31,07 và 31,83) và thấp hơn MLP trong 11/2016 (19,29 so với 19,86), nên thứ hạng giữa Linear Regression, Gradient Boosting và MLP đổi theo tháng. Random Forest có RMSE thấp hơn Persistence và Linear Regression ở cả 6 tháng.

### Ghi chú kiểm chứng (không dán)

- Nguồn: final_test_error_by_month.csv (cột month, rmse, mae, mean_pm25). Kiểm tra cụ thể: RF 09/2016 RMSE 11,3593; RF 01/2017 RMSE 29,5740, khớp phát biểu "11,36 so với 29,57". PM2.5 trung bình 54,1247 (09/2016) và 113,3009 (01/2017). 29,5740/11,3593 = 2,60; 113,3009/54,1247 = 2,09.
- RMSE tốt nhất theo tháng: 09/2016 MLP 11,0999; 10/2016 GB 14,0905; 11/2016 GB 18,8631; 12/2016 MLP 25,9436; 01/2017 RF 29,5740; 02/2017 MLP 17,7776. Hiệu RF so với tốt nhất: 0,26; 0,22; 0,26; 0,45; 0; 0,13.
- Bảng 12 cũ (hai baseline) khớp final_test_error_by_month.csv ở cả 6 tháng (kiểm tra từng ô), chỉ thiếu 3 mô hình còn lại.
- Mùa: final_test_error_by_season.csv (Autumn n=25.483; Winter n=25.580). Mô hình theo mùa thu RMSE: Persistence 16,83; LR 16,03; RF 15,32; GB 15,10; MLP 15,54. Mùa đông: 28,00; 26,32; 25,36; 26,04; 26,11.


### DÁN VÀO DOCX (đoạn mới về trạm, đặt sau nhận xét theo tháng và mùa)

Theo trạm (Phụ lục B2), Random Forest có RMSE thấp nhất ở 7 trong 12 trạm, Gradient Boosting ở 3 trạm (Changping, Dingling, Guanyuan) và MLP ở 2 trạm (Huairou, Shunyi); theo MAE, Random Forest thấp nhất ở 11 trong 12 trạm (Gradient Boosting ở Changping). Khoảng cách giữa Random Forest và mô hình tốt nhất tại mỗi trạm không vượt 0,83 µg/m³. Không mô hình nào có RMSE cao hơn Persistence ở bất kỳ trạm nào; Random Forest thấp hơn Linear Regression ở cả 12 trạm, trong khi Gradient Boosting cao hơn Linear Regression ở 3 trạm (Dongsi, Gucheng, Tiantan) và MLP cao hơn ở 2 trạm (Dongsi, Wanliu). RMSE của Random Forest dao động từ 18,42 µg/m³ (Dingling) đến 24,64 µg/m³ (Wanshouxigong).

### Ghi chú kiểm chứng (không dán)

- Nguồn: final_test_error_by_station.csv. Tính lại: số trạm có RMSE thấp nhất theo mô hình RF = 7, GB = 3, MLP = 2, LR = 0, Persistence = 0; theo MAE RF = 11, GB = 1. Chênh lớn nhất giữa RF và mô hình tốt nhất theo trạm là 0,83 (Changping: GB 19,50 so với RF 20,32).
- "Không mô hình nào cao hơn Persistence ở trạm nào" kiểm tra bằng so sánh RMSE từng trạm: số trạm có RMSE > Persistence bằng 0 cho cả 4 mô hình còn lại.

---

## Mục 6.5. Sai số theo mùa, mức PM2.5 và trạm

Bảng 13 (theo mùa) khớp baseline_error_analysis.csv ở mọi ô, không cần đổi. Bảng 14 phải thay hoàn toàn: biên nhóm cũ (số mẫu 112.846; 72.798; 46.434; 24.698; 30.572; 13.348) đã được thay bằng quy tắc biên phải hiện hành. Tổng vẫn là 300.696 mẫu.

### DÁN VÀO DOCX (thay Bảng 14 và đoạn nhận xét sau Bảng 13)

Các nhóm theo mức PM2.5 dùng chung quy tắc đóng biên phải: ≤35, (35; 75], (75; 115], (115; 150], (150; 250] và >250 µg/m³; giá trị đúng bằng biên thuộc nhóm thấp hơn (src/analysis_groups.py). Quy tắc này được dùng thống nhất cho baseline, Gradient Boosting, MLP và test.

Bảng 14. Sai số validation của hai baseline theo mức PM2.5 thực tế (300.696 dự đoán OOF)

| Mức PM2.5 | Số mẫu | MAE Persistence | MAE Linear Reg. | RMSE Persistence | RMSE Linear Reg. | Residual TB Persistence | Residual TB Linear Reg. |
|---|---|---|---|---|---|---|---|
| ≤ 35 | 115.085 | 5,59 | 6,89 | 12,45 | 12,55 | −1,78 | −1,37 |
| (35; 75] | 72.055 | 9,87 | 9,72 | 16,97 | 16,19 | −0,88 | −2,88 |
| (75; 115] | 45.799 | 12,27 | 11,46 | 19,46 | 18,00 | 0,69 | −0,37 |
| (115; 150] | 24.358 | 14,35 | 13,42 | 22,71 | 20,90 | 1,98 | 2,21 |
| (150; 250] | 30.226 | 17,53 | 17,00 | 27,79 | 26,02 | 3,13 | 6,47 |
| > 250 | 13.173 | 25,84 | 28,18 | 47,67 | 48,30 | 7,90 | 19,06 |

Nguồn: baseline_error_analysis.csv (notebook 02, ô evidence-nb-02). Residual bằng số đo thực trừ dự báo; giá trị dương là dự báo thấp hơn số đo. Các bảng nhóm dùng MAE, RMSE và residual; R² trong nhóm có khoảng nồng độ hẹp nên không dùng.

Nhận xét. Ở mức trên 250 µg/m³, Linear Regression dự báo thấp hơn số đo trung bình 19,06 µg/m³ (Persistence: 7,90), còn ở mức không quá 35 µg/m³ cả hai dự báo cao hơn số đo (residual −1,78 với Persistence và −1,37 với Linear Regression). Mùa đông vẫn là mùa có RMSE cao nhất ở hai baseline (26,61 với Persistence và 25,48 với Linear Regression). Cùng quy tắc nhóm cho MLP ban đầu cho RMSE 54,92 µg/m³ ở nhóm >250 (so với 47,67 của Persistence và 48,30 của Linear Regression) và 27,83 µg/m³ vào mùa đông (mlp_error_by_group.csv, notebook 06); Gradient Boosting ban đầu có RMSE 80,9 ở nhóm >250 và 37,1 vào mùa đông (gradient_boosting_error_by_level.csv và gradient_boosting_error_by_season.csv, notebook 04, chỉ làm tròn 1 chữ số). Theo trạm, RMSE của Linear Regression dao động từ 17,55 (Huairou) đến 20,62 µg/m³ (Changping) (Phụ lục B1).

### Ghi chú kiểm chứng (không dán)

- Bảng 14 mới tạo từ baseline_error_analysis.csv (group_type = pm25_level). Tổng n mỗi mô hình = 115.085 + 72.055 + 45.799 + 24.358 + 30.226 + 13.173 = 300.696.
- Khác biệt so với bảng cũ: ví dụ nhóm ≤35 trước 112.846 mẫu, MAE Persistence 5,53, MAE LR 6,86, RMSE 12,41 và 12,53, residual −1,34; nay 115.085 mẫu, MAE 5,59 và 6,89, RMSE 12,45 và 12,55, residual −1,37. Nhóm >250 trước 13.348 mẫu, residual LR 18,98; nay 13.173 mẫu, 19,06.
- Chuỗi số liệu của GB ban đầu: gradient_boosting_error_by_level.csv cột "RMSE" và "Sai lệch TB (dương = đoán thấp)" (chỉ 1 chữ số thập phân, không có MAE).


### DÁN VÀO DOCX (đoạn và bảng mới: sai số của mô hình tinh chỉnh trên test theo mức PM2.5)

Các bảng sau dùng 51.063 mẫu test và cùng quy tắc biên; không so trực tiếp với Bảng 14 vì khác tập mẫu (validation OOF và test) và khác giai đoạn.

Bảng 14b. RMSE (µg/m³) theo mức PM2.5 thực tế trên test của năm mô hình

| Mức PM2.5 | Số mẫu | PM2.5 TB thực | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|---|---|
| ≤ 35 | 20.149 | 15,1 | 15,29 | 14,92 | 13,50 | 13,09 | **12,95** |
| (35; 75] | 8.881 | 54,5 | 20,82 | 19,60 | 17,77 | 17,20 | **16,29** |
| (75; 115] | 6.623 | 94,5 | 20,73 | 18,85 | 17,91 | **17,50** | 17,79 |
| (115; 150] | 4.332 | 132,1 | 23,35 | 21,27 | 21,25 | **20,85** | 21,14 |
| (150; 250] | 7.393 | 194,0 | 27,59 | 25,09 | 24,81 | **24,58** | 26,12 |
| > 250 | 3.685 | 349,0 | 46,25 | 44,84 | **44,59** | 48,59 | 48,83 |

Bảng 14c. MAE (µg/m³) theo mức PM2.5 thực tế trên test của năm mô hình

| Mức PM2.5 | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|
| ≤ 35 | 5,69 | 6,52 | 5,19 | **5,10** | 5,12 |
| (35; 75] | 10,67 | 10,26 | 9,51 | **9,39** | 9,58 |
| (75; 115] | 12,65 | 11,34 | 11,15 | **11,02** | 11,68 |
| (115; 150] | 14,77 | **13,33** | 13,50 | 13,47 | 14,05 |
| (150; 250] | 17,38 | 16,22 | **16,04** | 16,23 | 17,53 |
| > 250 | 28,75 | 28,32 | **27,39** | 31,20 | 30,85 |

Bảng 14d. Residual trung bình (số đo thực trừ dự báo, µg/m³) theo mức PM2.5 trên test

| Mức PM2.5 | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|
| ≤ 35 | −1,92 | −2,55 | −2,62 | −2,35 | −2,08 |
| (35; 75] | −1,38 | −4,34 | −2,24 | −2,34 | −1,44 |
| (75; 115] | 0,66 | −0,96 | −0,06 | −0,11 | 1,09 |
| (115; 150] | 1,02 | 0,87 | 0,98 | 0,63 | 2,29 |
| (150; 250] | 2,52 | 4,76 | 3,31 | 2,91 | 5,14 |
| > 250 | 6,64 | 15,82 | 13,07 | 13,24 | 17,99 |

Nguồn: final_test_error_by_pm25_level.csv (notebook 08, ô evidence-nb-08).

Nhận xét. (1) Random Forest tinh chỉnh chỉ có RMSE thấp nhất ở nhóm >250 µg/m³ (44,59); ở các nhóm còn lại, MLP thấp nhất ở hai nhóm đầu (≤35: 12,95; (35; 75]: 16,29) và Gradient Boosting thấp nhất ở ba nhóm giữa. Nhóm >250 chỉ chiếm 7,2% số mẫu test (3.685 trên 51.063) nhưng đóng góp 32,7% tổng bình phương sai số của Random Forest (28,9% với Persistence, 30,5% với Linear Regression, 37,6% với Gradient Boosting, 37,2% với MLP); vì RMSE nhạy với sai số lớn, vị trí đầu bảng tổng thể của Random Forest chịu ảnh hưởng đáng kể từ nhóm này.

(2) Ở nhóm >250 µg/m³, Gradient Boosting (RMSE 48,59; MAE 31,20) và MLP (48,83; 30,85) đều kém hơn Persistence (46,25; 28,75) cả về RMSE lẫn MAE, trong khi Linear Regression (44,84) và Random Forest (44,59) thấp hơn Persistence. Như vậy kết luận Gradient Boosting và MLP thắng Persistence ở mức tổng thể không áp dụng cho các đợt ô nhiễm nặng. Độ chệch trung bình của Gradient Boosting (13,24) không lớn hơn của Linear Regression (15,82), nên phần chênh này chưa thể quy cho độ chệch; nguyên nhân chưa được kiểm chứng. Khoảng chênh ở từng mức chưa có khoảng tin cậy.

(3) Mọi mô hình đều dự báo cao hơn số đo ở nhóm ≤35 (residual từ −1,92 đến −2,62) và thấp hơn số đo ở nhóm >250 (từ 6,64 của Persistence đến 17,99 của MLP): giá trị dự báo bị kéo về phía mức trung bình. Đây là mô tả quan sát được, không phải kết luận về nguyên nhân.

### Ghi chú kiểm chứng (không dán)

- Phát biểu "GB và MLP kém Persistence ở >250" đã kiểm: RMSE 48,5900 và 48,8324 so với 46,2470; MAE 31,2044 và 30,8459 so với 28,7476 (final_test_error_by_pm25_level.csv). Đúng cả hai độ đo. Khớp README của final_test/analysis.
- Nhóm thấp nhất RMSE: ≤35 MLP 12,9475; (35;75] MLP 16,2874; (75;115] GB 17,4956; (115;150] GB 20,8456; (150;250] GB 24,5788; >250 RF 44,5925. Theo MAE: LR thấp nhất ở (115;150] (13,3346), RF ở (150;250] và >250, GB ở ba nhóm đầu.
- Tỷ trọng bình phương sai số = n x RMSE^2 chia tổng n x RMSE^2 của mô hình đó (tính lại, không có sẵn trong CSV). Tổng khôi phục đúng RMSE tổng thể (ví dụ RF 20,9613).


### DÁN VÀO DOCX (đoạn mới về trường hợp sai số lớn)

Bảng 14e. Bốn mẫu test có sai số tuyệt đối lớn nhất của Random Forest tinh chỉnh (µg/m³; thời điểm là giờ của nhãn t+1)

| Trạm | Thời điểm nhãn | Số đo thực | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|---|---|
| Wanshouxigong | 04/01/2017 13:00 | 3 | 621 | 609 | 602 | 482 | 617 |
| Wanshouxigong | 20/12/2016 15:00 | 3 | 461 | 452 | 450 | 490 | 457 |
| Huairou | 28/01/2017 01:00 | 556 | 161 | 138 | 117 | 115 | 83 |
| Nongzhanguan | 11/02/2017 22:00 | 529 | 141 | 150 | 140 | 168 | 153 |

Nguồn: final_test_worst_cases.csv và final_test_predictions.csv (notebook 08); hình final_test_worst_event.png.

Bốn mẫu sai lớn nhất của Random Forest cũng nằm trong nhóm sai lớn nhất của cả bốn mô hình còn lại, với sai số tuyệt đối từ khoảng 360 đến 620 µg/m³: số đo thực là 3 µg/m³ ở hai mẫu Wanshouxigong trong khi dự báo từ khoảng 450 đến 620, và là 556 và 529 µg/m³ ở hai mẫu Huairou và Nongzhanguan trong khi dự báo chỉ từ 83 đến 168. Đối chiếu với dữ liệu chuẩn hóa, số đo giờ liền trước ở bốn mẫu này lần lượt là 621, 461, 161 và 141 µg/m³, tức giá trị đổi rất mạnh trong một giờ. Ngày 28/01/2017 xuất hiện trong 14 đến 24 mẫu trong số 100 mẫu sai lớn nhất của từng mô hình. Mô hình một bước dự báo giờ kế tiếp không dự đoán được các thay đổi đột ngột này. Nhóm chưa kiểm chứng nguyên nhân (diễn biến thời tiết, sự kiện nguồn thải hay số đo cần xác minh), và không kết luận đó là lỗi cảm biến.

### Ghi chú kiểm chứng (không dán)

- Số lần xuất hiện ngày 28/01/2017 trong 100 mẫu sai lớn nhất: Persistence 18, LR 14, RF 20, GB 24, MLP 24 (tính từ final_test_worst_cases.csv). Câu "từ 14 đến 24" đúng.
- Phạm vi sai số tuyệt đối của 4 mẫu ở bảng: Persistence 618, 458, 395, 388; RF 599, 447, 439, 389; GB 487, 479, 441, 361; MLP 614, 454, 473, 376; LR 606, 449, 418, 379. Khoảng "360 đến 620" đúng cho phần lớn; GB mẫu thứ 4 là 361.
- Dự báo Persistence bằng giá trị PM2.5 tại giờ t (đã forward-fill tối đa 6 giờ). Đã đối chiếu data/processed/beijing_air_quality_standardized.csv: PM2.5 giờ t của bốn mẫu là 621 (Wanshouxigong 04/01/2017 12:00), 461 (20/12/2016 14:00), 161 (Huairou 28/01/2017 00:00), 141 (Nongzhanguan 11/02/2017 21:00), đều là số đo thật, không phải giá trị điền; vì vậy câu "số đo giờ liền trước" là đúng. Giá trị 999 nằm ở train/validation (Wanshouxigong 08/02/2016), 844 ở Nongzhanguan 05/05/2013, không phải ở test.

---

## Mục 6.6. Đóng góp đặc trưng của Linear Regression và Random Forest (đổi tên mục)

Kiểm tra Bảng 15 với baseline_lr_group_permutation_importance.csv: PM2.5 hiện tại 74,7763 (docx 74,78 đúng); lag và rolling 5,0472 (5,05 đúng); khí tượng 1,3749 (docx ghi 1,38, nên là 1,37 vì CSV 4 chữ số là 1,3749; chữ số 1,38 là do làm tròn lại từ 1,375 hiển thị ở output notebook); chất ô nhiễm khác 0,9051 (0,91 đúng); thời gian 0,6230 (0,62 đúng); trạm 0,0118 (0,01 đúng). Độ lệch chuẩn đều khớp. RMSE gốc 17,76 trên mẫu 30.000 dòng đúng theo output notebook 02 (ô cell-038: "RMSE gốc trên mẫu validation (fold 5): 17.76") nhưng không nằm trong CSV; cần ghi nguồn là output notebook. Cần bổ sung bảng Random Forest và so sánh.

### DÁN VÀO DOCX (thay toàn bộ Mục 6.6)

Nhóm dùng permutation importance theo nhóm đặc trưng. Mỗi nhóm cột được xáo trộn cùng một hoán vị trên mẫu ngẫu nhiên 30.000 dòng của tập validation fold 5 (seed 42), lặp 5 lần; đại lượng báo cáo là mức tăng RMSE so với RMSE trên mẫu chưa xáo trộn. Với Linear Regression, mô hình là pipeline của fold 5 (fit chỉ trên train của fold này) và RMSE gốc trên mẫu là 17,76 µg/m³ (notebook 02). Với Random Forest, nhóm fit lại cấu hình tinh chỉnh chỉ trên train của fold 5 (không dùng pipeline cuối vốn được fit trên toàn bộ 360.954 mẫu) và RMSE gốc trên mẫu là 17,55 µg/m³ (notebook 08). Phép đo cho biết mức phụ thuộc của từng mô hình vào mỗi nhóm; đây không phải quan hệ nhân quả và không phải thí nghiệm bỏ đặc trưng rồi huấn luyện lại.

Bảng 15. Mức tăng RMSE (µg/m³) khi xáo trộn từng nhóm đặc trưng, Linear Regression (RMSE gốc 17,76)

| Nhóm đặc trưng | RMSE tăng (µg/m³) | Độ lệch chuẩn (5 lần) |
|---|---|---|
| PM2.5 hiện tại (t) | 74,78 | 0,115 |
| PM2.5 lag và rolling | 5,05 | 0,036 |
| Khí tượng (gồm hướng gió) | 1,37 | 0,015 |
| Chất ô nhiễm khác | 0,91 | 0,017 |
| Thời gian (sin/cos) | 0,62 | 0,027 |
| Trạm | 0,01 | 0,004 |

Nguồn: baseline_lr_group_permutation_importance.csv (notebook 02, ô evidence-nb-02).

Bảng 15b. Mức tăng RMSE (µg/m³) khi xáo trộn từng nhóm đặc trưng, Random Forest tinh chỉnh fit trên train fold 5 (RMSE gốc 17,55)

| Nhóm đặc trưng | RMSE tăng (µg/m³) | Độ lệch chuẩn (5 lần) |
|---|---|---|
| PM2.5 hiện tại (t) | 51,86 | 0,096 |
| Chất ô nhiễm khác | 5,94 | 0,050 |
| PM2.5 lag và rolling | 2,09 | 0,066 |
| Khí tượng (gồm hướng gió) | 1,44 | 0,033 |
| Thời gian (sin/cos) | 0,080 | 0,011 |
| Trạm | 0,003 | 0,001 |

Nguồn: rf_group_permutation_importance.csv (notebook 08, ô evidence-nb-08; fold 5, 30.000 dòng, 5 lần, seed 42).

Bảng 15c. So sánh thứ hạng nhóm đặc trưng giữa hai mô hình

| Nhóm đặc trưng | LR: RMSE tăng | LR: hạng | RF: RMSE tăng | RF: hạng |
|---|---|---|---|---|
| PM2.5 hiện tại (t) | 74,78 | 1 | 51,86 | 1 |
| PM2.5 lag và rolling | 5,05 | 2 | 2,09 | 3 |
| Khí tượng (gồm hướng gió) | 1,37 | 3 | 1,44 | 4 |
| Chất ô nhiễm khác | 0,91 | 4 | 5,94 | 2 |
| Thời gian (sin/cos) | 0,62 | 5 | 0,08 | 5 |
| Trạm | 0,01 | 6 | 0,00 | 6 |

Nhận xét. Cả hai mô hình phụ thuộc chủ yếu vào PM2.5 ở giờ hiện tại: xáo trộn nhóm này làm RMSE tăng 74,78 µg/m³ với Linear Regression (khoảng 4,2 lần RMSE gốc) và 51,86 µg/m³ với Random Forest (khoảng 3,0 lần). Sự khác nhau nằm ở các nhóm sau: Random Forest phụ thuộc vào chất ô nhiễm khác (PM10, SO2, NO2, CO, O3) hơn Linear Regression (5,94 so với 0,91 µg/m³, gấp khoảng 6,6 lần) và ít phụ thuộc hơn vào nhóm lag và rolling (2,09 so với 5,05). Nhóm khí tượng có mức đóng góp tương đương (1,44 và 1,37), còn nhóm thời gian và trạm gần như bằng không ở Random Forest (0,08 và 0,003) và nhỏ ở Linear Regression (0,62 và 0,01). Thông tin về PM2.5 gần đây (giờ hiện tại, lag, rolling) vì vậy chiếm phần lớn khả năng dự báo ở cả hai mô hình, khí tượng đóng góp nhỏ ở bước dự báo một giờ.

Cần đọc kết quả thận trọng. Các nhóm đặc trưng có tương quan (PM10 với PM2.5, các lag của PM2.5 với PM2.5 hiện tại), nên khi xáo trộn một nhóm, nhóm khác có thể bù một phần và mức đóng góp của nhóm phụ có thể bị đánh giá thấp; việc Random Forest dùng nhiều hơn nhóm chất ô nhiễm khác có thể phản ánh thông tin chung với PM2.5 hơn là một cơ chế riêng. Độ lệch chuẩn trong Bảng 15 và 15b chỉ phản ánh biến thiên giữa 5 lần hoán vị trên cùng một mẫu, không phản ánh biến thiên giữa các fold hay các mẫu khác. Hai mô hình dùng chung fold 5, cùng cách lấy mẫu (seed 42) nhưng RMSE gốc khác nhau (17,76 và 17,55), nên so sánh định lượng giữa hai bảng chỉ mang tính định tính.

### Ghi chú kiểm chứng (không dán)

- RF: rf_group_permutation_importance.csv, baseline_sample_rmse = 17,5518 ở mọi hàng; n_validation_sample 30.000; n_repeats 5; seed 42; fold 5. Khớp README của validation_diagnostics (51,8617; 5,9398; 2,0905; 1,4415; 0,0800; 0,0030).
- Cách lấy mẫu: nb02 (cell-038) dùng np.random.default_rng(RANDOM_STATE).choice(last_va, 30000, replace=False) với RANDOM_STATE = 42; src/validation_diagnostics.py dùng np.random.default_rng(42).choice(val_idx, 30000, replace=False). Theo mã nguồn, đây là cùng cách chọn; chưa đối chiếu trực tiếp chỉ số dòng. Hai RMSE gốc khác nhau vì mô hình khác nhau.
- LR: baseline_lr_group_permutation_importance.csv (74,7763; 5,0472; 1,3749; 0,9051; 0,6230; 0,0118; std 0,1147; 0,0356; 0,0146; 0,0168; 0,0274; 0,0041). Chỉ một ô cần sửa: khí tượng 1,38 thành 1,37 (độ lệch 0,005, mức thấp).
- Tỷ lệ so với RMSE gốc: 74,7763/17,76 = 4,2; 51,8617/17,5518 = 3,0; 5,9398/0,9051 = 6,6; 5,0472/2,0905 = 2,4.
- Nhận định "khí tượng đóng góp nhỏ" bám theo ghi chú trong notebook 02 (mục Nhận xét về hệ số và permutation importance) và phải đi kèm cảnh báo tương quan.

---

## Mục 6.7 mới. Mức chắc chắn, độ ổn định theo seed và hội tụ của MLP

Đây là mục mới (nguồn: notebook 08, ô evidence-nb-08). Nếu dán vào DOCX, mục "Kết luận theo câu hỏi nghiên cứu" cũ trở thành Mục 6.8 và mục "Đánh giá tổng thể" là Mục 6.9; cập nhật Mục lục.

### DÁN VÀO DOCX

**Khoảng bootstrap ghép cặp.** Để biết chênh lệch RMSE giữa các mô hình có tách khỏi 0 hay không, nhóm dùng bootstrap ghép cặp theo khối ngày trượt: mỗi lần lấy lại mẫu chọn ngẫu nhiên vị trí bắt đầu của các khối 7 ngày liên tiếp (các khối có thể chồng lấn nhau) và ghép đủ 181 ngày test, lặp 2.000 lần (seed 42), giữ nguyên tất cả các trạm cùng ngày trong cùng khối và lấy khoảng phân vị 2,5% đến 97,5% của hiệu RMSE (khoảng 95%). Bootstrap dựa trên dự đoán đã cố định, nên chỉ phản ánh dao động do chọn khối ngày trong giai đoạn test đã quan sát; không phản ánh dao động do huấn luyện lại, do trạm mới hay do mùa khác.

Bảng U1. Hiệu RMSE (µg/m³) giữa Random Forest tinh chỉnh và các mô hình khác trên test

| Mô hình A | Mô hình B | RMSE(A) − RMSE(B) | Khoảng 95% | Chứa 0? | Kết luận trong phép đo này |
|---|---|---|---|---|---|
| Random Forest tinh chỉnh | Persistence | −2,15 | [−2,56; −1,77] | Không | RF thấp hơn |
| Random Forest tinh chỉnh | Linear Regression | −0,84 | [−1,13; −0,59] | Không | RF thấp hơn |
| Random Forest tinh chỉnh | Gradient Boosting tinh chỉnh | −0,33 | [−0,78; 0,13] | Có | Chưa phân biệt được |
| Random Forest tinh chỉnh | MLP tinh chỉnh | −0,54 | [−1,34; 0,26] | Có | Chưa phân biệt được |

Nguồn: paired_model_uncertainty.csv (n_bootstrap 2.000, block_days 7, seed 42, n_calendar_days 181, phương pháp "paired moving calendar-day blocks; all stations together").

Random Forest tách khỏi hai baseline: hiệu RMSE so với Persistence là −2,15 µg/m³ (khoảng từ −2,56 đến −1,77) và so với Linear Regression là −0,84 µg/m³ (từ −1,13 đến −0,59), không chứa 0. Với Gradient Boosting (−0,33; từ −0,78 đến 0,13) và MLP (−0,54; từ −1,34 đến 0,26), khoảng chứa 0, nên nhóm không khẳng định Random Forest tốt hơn hai mô hình này. Nhóm chỉ tính bốn cặp có Random Forest; các cặp còn lại (Gradient Boosting hay MLP so với Linear Regression hoặc Persistence, Gradient Boosting so với MLP) chưa có khoảng tin cậy, nên các thứ hạng 2 đến 5 ở Bảng 11 là thứ hạng điểm ước lượng, chưa phải kết luận thống kê.

**Độ ổn định theo seed (MLP).** Nhóm chạy lại cấu hình MLP tinh chỉnh với ba seed 7, 42 và 2026 trên cùng 5 fold validation (không chấm test, không thay mô hình cuối).

Bảng U2. Điểm validation trung bình 5 fold của MLP tinh chỉnh theo seed

| Seed | MAE (µg/m³) | RMSE (µg/m³) | R² |
|---|---|---|---|
| 7 | 11,1151 | 19,5268 | 0,9345 |
| 42 | 11,0718 | 19,6317 | 0,9339 |
| 2026 | 11,0171 | 19,2951 | 0,9361 |

Nguồn: mlp_seed_summary.csv (trung bình số học của 5 fold theo seed; không phải RMSE gộp OOF). Seed 42 cho 19,6317, đúng bằng điểm validation đã dùng ở Bảng 8 (tái lập được).

RMSE validation dao động từ 19,30 đến 19,63 µg/m³ giữa ba seed (hiệu 0,34; trung bình 19,48), lớn hơn khoảng cách 0,12 µg/m³ giữa Random Forest tinh chỉnh và Linear Regression ở Bảng 8. Với seed 2026, RMSE MLP (19,2951) gần như trùng Linear Regression (19,2950), trong khi seed 7 và 42 cao hơn; cả ba seed vẫn cao hơn Random Forest tinh chỉnh (19,1779). Vì vậy thứ tự giữa MLP và Linear Regression trên validation phụ thuộc vào seed. Nhóm chưa kiểm tra seed cho Random Forest và Gradient Boosting.

**Hội tụ và giới hạn epoch (MLP).** Cấu hình tinh chỉnh dùng max_iter = 40. Ở seed 42, fold 1 và fold 2 dừng đúng ở giới hạn 40 epoch và có cảnh báo hội tụ; fold 3, 4, 5 dừng sớm ở 20, 21 và 22 epoch. Trên cả ba seed, số fold chạm giới hạn là 1 (seed 7), 2 (seed 42) và 2 (seed 2026), luôn bao gồm fold 1. Nhóm chạy lại hai fold này với giới hạn 100 epoch (seed 42).

Bảng U3. Kiểm tra giới hạn epoch của MLP tinh chỉnh (seed 42)

| Fold | Giới hạn gốc | Epoch dùng | Cảnh báo | RMSE gốc | Giới hạn chẩn đoán | Epoch dùng | Cảnh báo | RMSE chẩn đoán |
|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 40 | Có | 26,1727 | 100 | 75 | Không | 26,9824 |
| 2 | 40 | 40 | Có | 15,9833 | 100 | 47 | Không | 16,2132 |

Nguồn: mlp_validation_diagnostics.csv (diagnostic = epoch_limit_check và seed_stability), mlp_loss_curves.csv, mlp_convergence.png.

Khi nâng giới hạn lên 100 epoch, cả hai fold đều dừng trước giới hạn (75 và 47 epoch) và hết cảnh báo hội tụ, nhưng RMSE validation không tốt hơn: fold 1 tăng từ 26,1727 lên 26,9824 và fold 2 tăng từ 15,9833 lên 16,2132 µg/m³. Hàm loss huấn luyện trên thang đã chuẩn hóa của biến mục tiêu (không phải µg/m³) giảm nhẹ (fold 1: từ 0,0302 ở epoch 40 xuống 0,0282 ở epoch 75; fold 2: từ 0,0256 xuống 0,0252 ở epoch 47). Do đó giới hạn 40 epoch không phải nguyên nhân gây sai số cao ở fold 1 và nhóm giữ cấu hình đã chọn; kiểm tra này chỉ chạy cho fold 1 và 2 và không dùng để thay mô hình cuối. Mô hình MLP cuối cùng (fit trên toàn bộ 360.954 mẫu) dừng sau 19 epoch, nên không bị giới hạn này cắt (trường final_fit_epochs trong mlp_tuned_metadata.json).

### Ghi chú kiểm chứng (không dán)

- paired_model_uncertainty.csv: RF - Persistence -2,1520 [-2,5553; -1,7699]; RF - LR -0,8414 [-1,1251; -0,5930]; RF - GB -0,3344 [-0,7799; 0,1339]; RF - MLP -0,5354 [-1,3431; 0,2557]. Khớp README final_test/analysis.
- Chỉ có bốn cặp; hàm paired_model_uncertainty trong src/evaluation.py mặc định chỉ khai báo bốn cặp này. Không nên viết "MLP tốt hơn Linear Regression có ý nghĩa thống kê".
- mlp_seed_summary.csv: seed 7 RMSE 19,5268; seed 42 19,6317; seed 2026 19,2951; trung bình ba seed 19,4845; độ lệch chuẩn mẫu 0,1723. Số fold có convergence_warning theo seed: 7 là 1 (fold 1), 42 là 2 (fold 1, 2), 2026 là 2 (fold 1, 2).
- final_fit_epochs = 19 lấy từ evaluation_manifest.json (models.mlp_tuned.metadata.final_fit_epochs); max_iter cấu hình 40.
- Chỉ số loss trong mlp_loss_curves.csv là loss của hàm mục tiêu trên biến mục tiêu đã chuẩn hóa theo train (README validation_diagnostics và diagnostics_manifest.json: "not µg/m³ RMSE").

---

## Mục 6.8 (Mục 6.7 cũ). Kết luận theo câu hỏi nghiên cứu

Đề xuất cũng chỉnh Mục 2.2 cho khớp: CH2 mở rộng sang Random Forest; CH3 nêu cả validation của baseline và test của năm mô hình.

### DÁN VÀO DOCX (thay toàn bộ phần CH1 đến CH3)

**CH1. Mô hình sau tinh chỉnh so với hai baseline trên test theo thời gian.** Random Forest tinh chỉnh đạt MAE 10,5906 µg/m³, RMSE 20,9613 µg/m³ và R² 0,9550 trên 51.063 mẫu test, thấp nhất trong năm mô hình ở cả ba độ đo. RMSE thấp hơn Persistence 9,31% (2,15 µg/m³, khoảng bootstrap 95% từ −2,56 đến −1,77) và thấp hơn Linear Regression 3,86% (0,84 µg/m³, từ −1,13 đến −0,59). Gradient Boosting (RMSE 21,2957) và MLP tinh chỉnh (21,4967) có điểm ước lượng thấp hơn Linear Regression (21,8027) nhưng khoảng bootstrap của Random Forest so với hai mô hình này chứa 0 và chưa có khoảng cho các cặp còn lại, nên chỉ có thể kết luận chắc chắn rằng Random Forest tốt hơn hai baseline trong giai đoạn test này. Mức cải thiện thực tế khiêm tốn: Persistence đã đạt R² 0,9453, vì PM2.5 liên tiếp tự tương quan mạnh. R² không phải độ chính xác; nhóm dùng MAE và RMSE (µg/m³) để so sánh.

**CH2. Nhóm đặc trưng nào mô hình dựa vào nhiều nhất.** Trên fold 5 (mẫu 30.000 dòng, 5 lần hoán vị), xáo trộn PM2.5 ở giờ hiện tại làm RMSE tăng 74,78 µg/m³ với Linear Regression và 51,86 µg/m³ với Random Forest; đây là nhóm chi phối ở cả hai mô hình. Nhóm tiếp theo khác nhau: lag và rolling của PM2.5 với Linear Regression (5,05) và chất ô nhiễm khác với Random Forest (5,94). Khí tượng đóng góp nhỏ ở cả hai (1,37 và 1,44); thời gian và trạm gần như không đóng góp. Kết quả mô tả mức phụ thuộc của mô hình, có điều kiện trên một fold, một mẫu và các đặc trưng tương quan với nhau; không phải bằng chứng nhân quả hay thí nghiệm bỏ đặc trưng.

**CH3. Sai số thay đổi thế nào theo trạm, mùa và mức PM2.5.** Trên validation, sai số của hai baseline cao hơn vào mùa đông (RMSE 26,61 và 25,48 µg/m³) và tăng theo mức PM2.5; ở nhóm trên 250 µg/m³, Linear Regression dự báo thấp hơn số đo trung bình 19,06 µg/m³. Trên test, các mô hình tinh chỉnh cho kết quả cùng chiều: RMSE của Random Forest tăng từ 11,36 µg/m³ (09/2016) lên 29,57 µg/m³ (01/2017), và mùa đông cao hơn mùa thu ở mọi mô hình. Theo trạm, RMSE của Random Forest nằm trong khoảng 18,42 đến 24,64 µg/m³ và không mô hình nào kém Persistence ở trạm nào. Theo mức PM2.5, Random Forest chỉ đứng đầu ở nhóm trên 250 µg/m³ (RMSE 44,59), nơi Gradient Boosting (48,59) và MLP (48,83) kém Persistence (46,25); ở các nhóm thấp và trung bình, MLP hoặc Gradient Boosting có RMSE thấp hơn. Bốn mẫu sai lớn nhất của Random Forest (sai số tuyệt đối khoảng 360 đến 620 µg/m³ ở cả năm mô hình) đều ứng với số đo đổi rất mạnh trong một giờ (Bảng 14e).

**Giới hạn của các kết luận trên.** Test chỉ gồm 6 tháng thu và đông (09/2016 đến 02/2017) tại 12 trạm đã có trong dữ liệu huấn luyện, nên kết quả không chứng minh độ chính xác tại trạm mới, vào mùa xuân và hè, ở tầm dự báo dài hơn một giờ, hay cho quyết định liên quan đến sức khỏe. Khoảng bootstrap có điều kiện trên dự đoán cố định và thời kỳ đã quan sát.

### Ghi chú kiểm chứng (không dán)

- CH1: final_test_metrics.csv, final_test_relative_improvements.csv, paired_model_uncertainty.csv. "thấp nhất ở cả ba độ đo": MAE 10,5906, RMSE 20,9613, R² 0,9550 đều tốt nhất (final_test_metrics.csv).
- CH2: baseline_lr_group_permutation_importance.csv; rf_group_permutation_importance.csv.
- CH3: baseline_error_analysis.csv; final_test_error_by_*.csv. "không mô hình nào kém Persistence ở trạm nào" xem Ghi chú ở Mục 6.4.
- Thiếu so với bản cũ: CH2 cũ chỉ đúng với Linear Regression (74,78; 5,05); CH3 cũ chỉ về validation của baseline và dẫn Phụ lục B; CH1 cũ nói "Cả GB và MLP đều có RMSE test thấp hơn LR" nhưng không có khoảng tin cậy và không nói rằng khoảng của RF so với GB/MLP chứa 0.

---

## Mục 6.9 mới. Đánh giá tổng thể

### DÁN VÀO DOCX

**(a) So sánh với công trình liên quan.** Nhóm không so sánh số RMSE hay MAE của mình với các bài báo ở Bảng R1, vì các công trình khác nhau về bộ dữ liệu, giai đoạn, số trạm, tầm dự báo, cách chia tập và độ đo; không có điều kiện đánh giá chung nên không đủ cơ sở để nói mô hình của nhóm tốt hơn hay kém hơn. Bảng R1 chỉ đối chiếu hướng tiếp cận.

Bảng R1. Đối chiếu hướng tiếp cận với các công trình liên quan (theo nội dung Slide 9; các thông tin về bài gốc như số trạm và giai đoạn là số của bài gốc theo slide, chưa kiểm tra bản gốc, không so sánh trực tiếp với số của nhóm; [CẦN KIỂM TRA bài gốc trước khi nộp])

| Công trình | Hướng và dữ liệu (theo slide) | Điểm có thể đối chiếu với đề tài | Điều kiện không cho phép so số trực tiếp |
|---|---|---|---|
| Seng và cộng sự (2021) | LSTM không gian–thời gian; PM2.5, khí tượng và dữ liệu trạm lân cận; 35 trạm Bắc Kinh, 2016–2017 | Cùng bài toán dự báo PM2.5 đa trạm tại Bắc Kinh. Đề tài chỉ dùng đặc trưng của chính trạm, chưa dùng thông tin trạm lân cận. | Khác số trạm (35 và 12), giai đoạn, cách chia và độ đo; đề tài không dùng mô hình học sâu chuỗi thời gian. |
| Bekkar và cộng sự (2021) | CNN–LSTM; PM2.5 theo giờ tại Bắc Kinh; so sánh LSTM, GRU, CNN và mô hình lai | Cùng bước thời gian theo giờ. Đề tài chỉ so sánh mô hình hồi quy cổ điển và MLP. | Khác bộ dữ liệu, tập kiểm thử và độ đo; đề tài không cài đặt kiến trúc học sâu chuỗi. |
| Wei và cộng sự (2025) | RF, XGBoost, FCNN; PM2.5 và O3 vùng Bắc Kinh–Thiên Tân–Hà Bắc, 2019–2023 | Dùng Random Forest và mạng nơ-ron truyền thẳng, gần với RF và MLP của đề tài. | Khác khu vực, giai đoạn (2019–2023 so với 2013–2017), chất ô nhiễm khảo sát và quy trình đánh giá; đề tài không dùng XGBoost. |

Điều có thể nói một cách trung thực: kết quả của đề tài (Random Forest tinh chỉnh tốt nhất trong năm mô hình, hơn Persistence 9,31% RMSE và hơn Linear Regression 3,86%) cùng chiều với nhận định mà Slide 9 nêu cho Wei và cộng sự (2025) rằng mô hình cây và mạng nơ-ron có thể khai thác tương tác phi tuyến [cần xác nhận: chưa kiểm tra bài gốc]. Tuy nhiên chênh lệch giữa Random Forest, Gradient Boosting và MLP chưa phân biệt được (Mục 6.7) và Linear Regression chỉ kém Random Forest 3,86%, nên bằng chứng của đề tài chưa đủ để kết luận mô hình phi tuyến vượt trội rõ rệt. Đề tài cũng không thử LSTM, CNN–LSTM, XGBoost hay dữ liệu trạm lân cận nên không đánh giá được các hướng đó.

**(b) Ý nghĩa thực tế và giới hạn.**

- Ý nghĩa. Persistence đã là mốc rất mạnh cho dự báo một giờ (R² 0,9453 trên test). Random Forest giảm MAE khoảng 1,00 µg/m³ (8,60%) và RMSE khoảng 2,15 µg/m³ (9,31%) so với Persistence; mức cải thiện khiêm tốn nhưng nhất quán ở cả 12 trạm (RMSE của Random Forest thấp hơn Persistence từ 1,07 đến 2,96 µg/m³ tùy trạm) và ở cả 6 tháng test. Về chi phí, lần fit cuối cùng của Random Forest, Gradient Boosting và MLP tinh chỉnh mất lần lượt khoảng 33,8; 8,2 và 11,4 giây (metadata mô hình, máy chạy không được ghi nhận nên chỉ để tham khảo). Vì vậy kết quả hỗ trợ việc dùng mô hình học máy như một bổ sung cho Persistence trong dự báo ngắn hạn tại các trạm đã quan sát, không thay thế quan trắc.
- Giới hạn về dữ liệu và phạm vi. Test chỉ gồm thu–đông 09/2016 đến 02/2017 (PM2.5 trung bình 92,18 µg/m³ so với 78,04 ở train/validation); tất cả 12 trạm đều có trong huấn luyện; chỉ dự báo một giờ tới; chưa có kiểm tra trạm giữ ngoài, mùa xuân và hè, hay nhiều tầm dự báo.
- Giới hạn về sai số. Ở nhóm trên 250 µg/m³ mọi mô hình dự báo thấp hơn số đo (residual trung bình từ 6,64 đến 17,99 µg/m³), Gradient Boosting và MLP kém Persistence, và bốn mẫu sai lớn nhất của Random Forest (số đo đổi rất mạnh trong một giờ, Bảng 14e) gây sai số khoảng 360 đến 620 µg/m³ ở cả năm mô hình. Mô hình vì vậy chưa phù hợp để dùng một mình cho cảnh báo ô nhiễm nặng hay quyết định sức khỏe.
- Giới hạn về phương pháp. Tìm siêu tham số chỉ thử 8 đến 20 tổ hợp; seed chỉ được kiểm tra cho MLP; khoảng bootstrap chỉ có bốn cặp và có điều kiện trên dự đoán cố định; phần lớn mức cải thiện trên validation đến từ fold 1 (Mục 6.3); hai quan trắc 999 và 844 µg/m³ chưa được xác minh và được giữ nguyên; bộ 27 đặc trưng chưa gồm độ lệch so với trung bình trượt, lag khí tượng và cờ cuối tuần.

### Ghi chú kiểm chứng (không dán)

- Nội dung cột "Hướng và dữ liệu" chép từ Slide 9 (pptx.txt dòng 143 đến 153). Bảng của DOCX phải được đối chiếu với bài gốc bởi người kiểm tra tài liệu tham khảo trước khi nộp; nếu bài gốc khác slide, sửa cả slide.
- Số liệu của đề tài trong 6.9: final_test_metrics.csv; final_test_relative_improvements.csv; final_test_error_by_station.csv (RF thấp hơn Persistence từ 1,07 ở Dingling đến 2,96 ở Shunyi); final_test_error_by_month.csv (RF thấp hơn Persistence cả 6 tháng).
- final_fit_seconds: evaluation_manifest.json, models.random_forest_tuned.metadata.final_fit_seconds = 33,8352; gradient_boosting_tuned = 8,2074; mlp_tuned = 11,3529. Đây là thời gian khi tạo metadata, không đo lại.
- Không đưa số RMSE/MAE của bài báo vào bảng thực nghiệm của nhóm, đúng yêu cầu mục 3 của nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md.

---

## Hình đề xuất bổ sung cho Mục 6 (đã có sẵn trong kho, không cần vẽ lại)

| Hình đề xuất | Tệp | Đặt ở | Ghi chú nguồn |
|---|---|---|---|
| RMSE theo tháng, năm mô hình (test) | outputs/experiments/final_test/analysis/figures/final_test_rmse_by_month.png | Mục 6.4, cạnh Bảng 12 | Notebook 08 |
| RMSE theo mùa (test) | .../figures/final_test_rmse_by_season.png | Mục 6.4, cạnh Bảng 12c | Notebook 08 |
| RMSE theo trạm (test) | .../figures/final_test_rmse_by_station.png | Phụ lục B, cạnh Bảng B2 | Notebook 08 |
| RMSE theo mức PM2.5 (test) | .../figures/final_test_rmse_by_pm25_level.png | Mục 6.5, cạnh Bảng 14b | Notebook 08 |
| Chuỗi thời gian quanh mẫu RF sai lớn nhất | .../figures/final_test_worst_event.png | Mục 6.5, cạnh Bảng 14e | Notebook 08 |
| Importance theo nhóm của Random Forest | outputs/experiments/validation_diagnostics/rf_group_permutation_importance.png | Mục 6.6, cạnh Bảng 15b | Notebook 08 |
| Hội tụ MLP theo epoch | outputs/experiments/validation_diagnostics/mlp_convergence.png | Mục 6.7, cạnh Bảng U3 | Notebook 08; loss trên thang chuẩn hóa, ghi rõ không phải µg/m³ |

Hình 10 hiện có (RMSE test của năm mô hình) tương ứng final_test_rmse.png. Nếu giữ Hình 11 và 12 (validation của baseline), ghi rõ trong chú thích rằng đây là validation, không phải test.

---

## Mục 7. Đánh giá tiến độ

### 7.1 Công việc đã hoàn thành (đề xuất thay)

- Tổ chức bảng, biểu đồ và báo cáo cho ba thực nghiệm validation trong experiments01 đến 03; kết quả đánh giá cuối nằm trong final_test.
- EDA đầy đủ trên 12 trạm (notebook 01), nhật ký EDA, bảng kết luận và tệp dữ liệu chuẩn hóa.
- Pipeline dữ liệu chống rò rỉ (nạp dữ liệu, target t+1, đặc trưng lag/rolling/thời gian, forward-fill có giới hạn, chia thời gian, CV theo timestamp) cùng bộ kiểm thử pytest (51 hàm kiểm thử trong 7 tệp theo cách đếm "def test_"; kết quả chạy pytest [cần xác nhận: chưa được chạy lại trong lần rà soát này]).
- Đánh giá Persistence và Linear Regression; phân tích sai số theo trạm, mùa và mức PM2.5; permutation importance theo nhóm cho Linear Regression.
- Huấn luyện Random Forest, Gradient Boosting dạng histogram và MLP; tinh chỉnh cả ba trên 5 fold; chấm năm mô hình trên cùng tập test.
- Phân tích bổ sung trên cấu hình đã khóa: sai số của năm mô hình theo trạm, tháng, mùa và mức PM2.5; các trường hợp sai lớn nhất; bootstrap ghép cặp theo khối 7 ngày; permutation importance của Random Forest; kiểm tra seed và giới hạn epoch của MLP (outputs/experiments/final_test/analysis và validation_diagnostics).
- Kiểm tra nguồn số liệu: report_sources.csv liên kết từng CSV với notebook, ô, lượt thực thi và hash; scripts/verify_result_sources.py đối chiếu CSV với output notebook và experiment_log.csv.

### Ghi chú kiểm chứng (không dán)

- Số hàm test (đếm "def test_" tại thời điểm kiểm tra này): tests/test_data_pipeline.py 6, test_diagnostics_and_validation.py 15, test_feature_engineering.py 8, test_integration.py 1, test_metrics_and_bootstrap.py 8, test_model_evaluation.py 9, test_notebook_evidence.py 4 = 51 hàm trong 7 tệp (bản nháp trước ghi 28 hàm trong 5 tệp, chưa tính hai tệp test_diagnostics_and_validation.py và test_metrics_and_bootstrap.py mới xuất hiện; có test được tham số hóa nên số ca chạy có thể lớn hơn 51). Việc pytest chạy qua hay không chưa được xác nhận trong lần rà soát này (quy tắc không ghi vào kho). Nên chạy python -m pytest -q và ghi kết quả thật trước khi viết "đạt".
- Câu cũ "Chạy Random Forest, ... sau đó chấm 5 mô hình trên tập test" vẫn đúng; câu cũ "Đánh giá Persistence và Linear Regression ... xuất bảng so sánh Excel và CSV" vẫn đúng.

### 7.2 Khó khăn và hạn chế hiện tại (đề xuất thay toàn bộ)

Xóa câu "Notebook 08 xuất điểm test tổng thể. Bảng sai số theo tháng trên test hiện có cho hai baseline." vì đã lỗi thời: notebook 08 hiện xuất sai số theo tháng, mùa, trạm và mức PM2.5 cho cả năm mô hình, cộng với các trường hợp sai lớn và khoảng bootstrap. Chỉ giữ những phần thực sự chưa làm:

- Tập test chỉ gồm sáu tháng thu và đông (09/2016 đến 02/2017) tại 12 trạm đã có trong huấn luyện. Khả năng dự báo vào mùa xuân và hè, tại trạm chưa thấy trong huấn luyện (hold-out theo trạm), và ở tầm dự báo dài hơn một giờ chưa được đánh giá.
- Bộ 27 đặc trưng còn thiếu một số biến dự kiến trong đề cương: độ lệch so với trung bình trượt, lag khí tượng và cờ cuối tuần. Nhóm chưa huấn luyện lại để so sánh bộ đặc trưng (ablation); phần importance chỉ cho biết mức phụ thuộc của mô hình đã huấn luyện.
- Hai quan trắc 999 và 844 µg/m³ (và hai mẫu có số đo 3 µg/m³ trong khi dự báo từ khoảng 450 trở lên ở Bảng 14e) cần nguồn đo bổ sung để xác minh khả năng bão hòa hay sai số cảm biến; hiện được giữ nguyên.
- Ở nhóm PM2.5 trên 250 µg/m³ mọi mô hình dự báo thấp hơn số đo, và Gradient Boosting cùng MLP kém Persistence; nguyên nhân chưa được kiểm chứng.
- Khoảng bootstrap chỉ tính cho bốn cặp có Random Forest; độ ổn định theo seed chỉ kiểm tra cho MLP; tìm siêu tham số chỉ thử một phần nhỏ không gian (8 trên 192 ở Random Forest, 8 trên 243 ở MLP).
- Người thực hiện từng lần chạy notebook chưa được ghi lại trong artifact; cần nhóm xác nhận để hoàn thiện truy vết (Mục 8).

### Ghi chú kiểm chứng (không dán)

- "Hold-out theo trạm", "mùa khác", "nhiều tầm dự báo", "bộ đặc trưng": không có thí nghiệm hay bảng nào trong outputs/ cho các nội dung này (đã tìm trong outputs/experiments và outputs/notebooks/tables).
- Các giá trị 3 µg/m³: final_test_worst_cases.csv (Wanshouxigong 04/01/2017 13:00 và 20/12/2016 15:00).

### 7.3 Công việc còn lại và kế hoạch hoàn thành (đề xuất thay)

Bảng 16. Việc còn lại, không bao gồm các phân tích đã hoàn thành

| Hạng mục | Nội dung | Đầu ra cần đối chiếu | Trạng thái |
|---|---|---|---|
| Báo cáo và slide | Dán các bảng mới (6.4 đến 6.9), đồng bộ cách chia dữ liệu, biên nhóm PM2.5, siêu tham số, kết quả validation và test giữa DOCX và slide. | Bảng và hình ở Mục 6; report_sources.csv | Chưa làm |
| Truy vết | Nhóm xác nhận người chạy và ngày chạy từng notebook (diagnostics_manifest.json ghi operator = null). | Mục 8 và Phụ lục A | Chưa làm |
| Tái lập | Chạy lại pytest, scripts/verify_result_sources.py trên môi trường .venv đã khóa và ghi kết quả thật. | Phụ lục C; kết quả lệnh | Chưa ghi nhận trong báo cáo |
| Xác minh dữ liệu | Đối chiếu nguồn cho 999 và 844 µg/m³ và các mẫu sai lớn nhất (Bảng 14e). | Ghi chú dữ liệu trong EDA | Chưa làm |
| Mở rộng đánh giá (chỉ là hướng mở rộng, cần nhóm đồng ý; ngoài phạm vi báo cáo hiện tại; không đổi mô hình đã khóa) | Đánh giá theo trạm giữ ngoài, các giai đoạn khác và nhiều tầm dự báo; huấn luyện lại để so sánh bộ đặc trưng; bổ sung các đặc trưng còn thiếu. | Bảng sai số ghi rõ tập dữ liệu và quy tắc nhóm | Chưa làm |
| Độ chắc chắn (tùy chọn) | Mở rộng bootstrap sang các cặp chưa tính và kiểm tra seed cho Random Forest, Gradient Boosting. | paired_model_uncertainty.csv mở rộng | Chưa làm |

Bỏ dòng "Phân tích bổ sung: Nếu mở rộng báo cáo, kiểm tra sai số của ba mô hình tinh chỉnh theo trạm, mùa và mức PM2.5" khỏi Bảng 16 vì đã làm xong (final_test_error_by_station.csv, final_test_error_by_season.csv, final_test_error_by_pm25_level.csv).

---

## Mục 8. Phân công và đóng góp

### Phát hiện

- Bảng 17 hiện ghi "những phần việc có sản phẩm hoặc lịch sử cập nhật trong kho mã nguồn", tức suy từ lịch sử commit. Phần lớn tác giả commit là tên tài khoản (git log hiện có các tên tác giả "bjruly", "daohuutai", "Quang", "ITSGU20", "BinBin826", "Nhan To Thanh", "Tô Nhân" và "Trần Lê Gia Bảo"; chỉ vài tên giống tên thành viên, và việc giống tên cũng không phải bằng chứng người chạy từng notebook), không đủ để xác định người thực hiện từng notebook. Quy tắc của kho mã (nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md mục 2 và mục 7): chỉ ghi tên người chạy khi có bằng chứng hoặc nhóm xác nhận.
- Chỉ có một tài liệu nội bộ về phân công: docs/phan-cong-cong-viec.docx (nhóm trưởng Trần Lê Gia Bảo). Tài liệu này nêu phạm vi của Bảo gồm tổ chức dự án và tài liệu, khảo sát và chuẩn hóa dữ liệu (EDA, CSV chuẩn hóa), pipeline dữ liệu và viết kiểm thử cho nạp dữ liệu, tạo đặc trưng, chia tập và pipeline; và nêu rõ không bao gồm xây dựng, huấn luyện, tinh chỉnh hay đánh giá mô hình.
- Mâu thuẫn cần giải quyết: Bảng 17 gán thư mục tests/ và bộ kiểm thử cho Đào Hữu Tài, trong khi phan-cong-cong-viec.docx gán việc viết kiểm thử cho Trần Lê Gia Bảo.
- Bảng 1 (đề cương) và Bảng 17 khác nhau nhiều: đề cương gán Gradient Boosting và chia dữ liệu theo thời gian cho Bảo, EDA cho Nhân, tiền xử lý và baseline cho Tài, Random Forest và tinh chỉnh cho Quang, đánh giá cuối, phân tích sai số theo trạm/mùa và permutation importance cho Tuấn. Cần một câu giải thích vì sao phân công thực tế thay đổi (nếu nhóm xác nhận có thay đổi).
- Phần mới (phân tích sai số trên test, importance của Random Forest, bootstrap, seed và epoch của MLP, kiểm tra nguồn số liệu, scripts) chưa gắn với người nào.

### DÁN VÀO DOCX (thay đoạn mở đầu và Bảng 17)

Phân công trong Bảng 1 là dự kiến theo đề cương. Bảng 17 ghi các hạng mục đã có sản phẩm trong kho mã nguồn và cột cuối nêu trạng thái xác nhận. Nhóm không suy người thực hiện từ tác giả commit: tên tài khoản Git không nhất thiết trùng tên thành viên. Phần việc nào chưa được cả nhóm xác nhận được đánh dấu [CẦN NHÓM XÁC NHẬN] và sẽ được điền khi có xác nhận.

Đóng góp của đề tài (khác với đóng góp từng thành viên): pipeline đa trạm chống rò rỉ cho dự báo PM2.5 giờ kế tiếp; so sánh năm mô hình trên cùng 5 fold và cùng tập test; phân tích sai số theo trạm, tháng, mùa, mức PM2.5 và sự kiện; phân tích mức phụ thuộc đặc trưng và độ chắc chắn của chênh lệch; truy vết nguồn số liệu từ CSV về notebook.

Bảng 17. Hạng mục thực hiện, sản phẩm liên quan và trạng thái xác nhận

| Thành viên | Công việc ghi nhận (sản phẩm có trong kho mã nguồn) | Sản phẩm liên quan | Trạng thái xác nhận |
|---|---|---|---|
| Trần Lê Gia Bảo (nhóm trưởng) | Tổ chức kho mã nguồn và tài liệu; khảo sát và chuẩn hóa dữ liệu 12 trạm; pipeline dữ liệu (target t+1, đặc trưng, chia tập theo thời gian, xử lý thiếu, chống rò rỉ); kiểm thử cho nạp dữ liệu, tạo đặc trưng, chia tập và pipeline. | Notebook 01, src/, tests/, outputs/eda/ | Có tài liệu docs/phan-cong-cong-viec.docx. [CẦN NHÓM XÁC NHẬN] mục tests/ do hai bản ghi khác nhau. |
| Tô Thành Nhân | [CẦN NHÓM XÁC NHẬN] Bản nháp cũ ghi: tích hợp nhánh và cập nhật notebook tinh chỉnh MLP theo lịch sử commit. | Notebook 07 (nếu được xác nhận) | Chưa có xác nhận ngoài lịch sử commit. |
| Đào Hữu Tài | [CẦN NHÓM XÁC NHẬN] Bản nháp cũ ghi: triển khai và đánh giá hai baseline, xuất bảng đối chiếu, cập nhật nhật ký và bộ kiểm thử dữ liệu (phần bộ kiểm thử mâu thuẫn với tài liệu phân công). | Notebook 02, experiment_log.csv, bảng baseline | Chưa có xác nhận ngoài lịch sử commit; phần tests/ mâu thuẫn với tài liệu phân công. |
| Huỳnh Nhật Quang | [CẦN NHÓM XÁC NHẬN] Bản nháp cũ ghi: Gradient Boosting, tinh chỉnh RF và GB, MLP và tinh chỉnh MLP, đánh giá cuối và tổng hợp kết quả thực nghiệm. | Notebook 04 đến 08 | Chưa có xác nhận; commit của các notebook này có nhiều tài khoản khác nhau. |
| Nguyễn Thanh Tuấn | [CẦN NHÓM XÁC NHẬN] Bản nháp cũ ghi: Random Forest ban đầu, chạy 5 fold, lưu mô hình và kết quả, cập nhật tài liệu notebook. | Notebook 03 | Chưa có xác nhận ngoài lịch sử commit. |
| [CẦN NHÓM ĐIỀN TÊN] | Phân tích sai số test theo trạm/tháng/mùa/mức PM2.5, trường hợp sai lớn, bootstrap, permutation importance của RF, seed và epoch của MLP. | src/evaluation.py, src/validation_diagnostics.py, notebook 08, outputs/experiments/final_test/analysis, outputs/experiments/validation_diagnostics | Chưa gắn với người nào; manifest ghi operator = null. |
| [CẦN NHÓM ĐIỀN TÊN] | Kiểm tra nguồn số liệu và tái lập: report_sources.csv, scripts/run_notebooks.py, scripts/verify_result_sources.py, requirements-lock.txt. | scripts/, outputs/notebooks/tables/report_sources.csv | Chưa gắn với người nào. |

### Ghi chú kiểm chứng (không dán)

- Nguồn: docs/phan-cong-cong-viec.docx (đã trích ra phancong.txt), git log (tác giả commit: daohuutai, Quang, Tô Nhân, Nhan To Thanh, ITSGU20, BinBin826, bjruly, Trần Lê Gia Bảo), docx Bảng 1 và Bảng 17, diagnostics_manifest.json.
- Không dùng git log để quyết định ai làm gì. Hai tài khoản ITSGU20 và BinBin826 xuất hiện ở các commit notebook 03, 04, 05 và MLP nhưng chưa có bằng chứng nào nối chúng với tên thành viên cụ thể.
- Phần "Bản nháp cũ ghi" chép lại Bảng 17 hiện tại để nhóm xác nhận hoặc sửa; không phải khẳng định mới.

---

## Mục 9. Tài liệu tham khảo

### Phát hiện

- Slide 9 trích: Seng và cộng sự (2021) DOI 10.1016/j.aej.2020.12.009; Bekkar và cộng sự (2021) DOI 10.1186/s40537-021-00548-1; Wei và cộng sự (2025) DOI 10.3390/su17209211. Slide 10 trích WHO Global Air Quality Guidelines (2021). Cả bốn nguồn chưa có trong DOCX (hiện có 5 nguồn: Chen 2017, Zhang và cộng sự 2017, Breiman 2001, Friedman 2001, Pedregosa và cộng sự 2011).
- Đề xuất Mục 6.9 (Bảng R1) dẫn ba bài báo này nên phải có mục tương ứng. Phần chi tiết thư mục (tác giả, tập, trang) chưa được kiểm chứng trong lần rà soát này; một agent khác kiểm tra DOI và thông tin từ nguồn gốc.

### DÁN VÀO DOCX (thêm sau 5 mục hiện có; thay các dấu [ ] sau khi kiểm tra)

- Seng, [danh sách tác giả cần kiểm tra]. (2021). [Tên bài: cần kiểm tra]. [Tên tạp chí, tập và trang cần kiểm tra]. https://doi.org/10.1016/j.aej.2020.12.009 [cần kiểm tra DOI]
- Bekkar, [danh sách tác giả cần kiểm tra]. (2021). [Tên bài: cần kiểm tra]. [Tên tạp chí, tập và trang cần kiểm tra]. https://doi.org/10.1186/s40537-021-00548-1 [cần kiểm tra DOI]
- Wei, [danh sách tác giả cần kiểm tra]. (2025). [Tên bài: cần kiểm tra]. [Tên tạp chí, tập và trang cần kiểm tra]. https://doi.org/10.3390/su17209211 [cần kiểm tra DOI]
- World Health Organization. (2021). [Tên ấn phẩm WHO global air quality guidelines và địa chỉ truy cập: cần kiểm tra]. [cần kiểm tra DOI hoặc URL]

Ghi chú: DOI của ba bài lấy nguyên văn từ Slide 9; mọi thông tin thư mục khác phải kiểm tra từ nguồn gốc.

Không thêm số liệu định lượng của các bài này vào bảng thực nghiệm của nhóm. Nếu muốn dẫn phương pháp permutation importance, bootstrap theo khối hoặc Adam trong phần phương pháp, nhóm tự tra bài gốc rồi ghi; lần rà soát này không đề xuất nguồn cụ thể.

---

## Phụ lục A. Nhật ký thực nghiệm

Bảng A1 hiện có 13 dòng, khớp từng giá trị với experiment_log.csv (13 dòng; đã so MAE, RMSE, R² đến 4 chữ số). Đề xuất thêm cột nguồn và thêm đoạn giải thích.

### DÁN VÀO DOCX (thay đoạn dẫn và Bảng A1)

Nguồn là experiment_log.csv ở gốc kho mã nguồn; mỗi mã thực nghiệm có một dòng và được cập nhật theo mã khi chạy lại. Mã có đuôi _cv5 là trung bình số học của chỉ số tính trên từng fold trong 5 fold validation; mã có đuôi _test là độ đo trên 51.063 mẫu test. MAE và RMSE có đơn vị µg/m³. Cột nguồn ghi notebook và mã ô sinh bảng CSV tương ứng (report_sources.csv); các dòng của notebook 05 và 07 là kết quả đối chiếu với tìm kiếm đã lưu.

Bảng A1. Các thí nghiệm đã ghi nhận

| Mã thực nghiệm | MAE | RMSE | R² | Nguồn (notebook / ô) |
|---|---|---|---|---|
| baseline_persistence_cv5 | 10,4240 | 19,9665 | 0,9318 | 02 / evidence-nb-02 |
| baseline_linreg_cv5 | 10,7380 | 19,2950 | 0,9363 | 02 / evidence-nb-02 |
| random_forest_cv5 | 10,5256 | 20,1707 | 0,9309 | 03 / evidence-nb-03 |
| random_forest_tuned_cv5 | 10,1254 | 19,1779 | 0,9377 | 05 / verify-saved-search-05 |
| gradient_boosting_cv5 | 11,0743 | 21,9726 | 0,9173 | 04 / evidence-nb-04 |
| gradient_boosting_tuned_cv5 | 10,5222 | 20,0384 | 0,9328 | 05 / verify-saved-search-05 |
| mlp_cv5 | 11,7282 | 20,0840 | 0,9314 | 06 / evidence-nb-06 |
| mlp_tuned_cv5 | 11,0718 | 19,6317 | 0,9339 | 07 / verify-saved-search-07 |
| random_forest_tuned_test | 10,5906 | 20,9613 | 0,9550 | 08 / evidence-nb-08 |
| gradient_boosting_tuned_test | 10,8195 | 21,2957 | 0,9536 | 08 / evidence-nb-08 |
| mlp_tuned_test | 11,1583 | 21,4967 | 0,9527 | 08 / evidence-nb-08 |
| baseline_linreg_test | 11,3510 | 21,8027 | 0,9513 | 08 / evidence-nb-08 |
| baseline_persistence_test | 11,5864 | 23,1133 | 0,9453 | 08 / evidence-nb-08 |

Bảng A2 (mới). Tệp phân tích bổ sung đã tạo cho cấu hình đã khóa

| Thư mục hoặc tệp | Nội dung | Nguồn tạo |
|---|---|---|
| outputs/experiments/final_test/analysis/final_test_error_by_station.csv, _by_month.csv, _by_season.csv, _by_pm25_level.csv | MAE, RMSE, R², residual trung bình của năm mô hình theo nhóm; số mẫu mỗi nhóm cộng lại 51.063 | Notebook 08, evidence-nb-08; python -m src.evaluation |
| outputs/experiments/final_test/analysis/final_test_worst_cases.csv | 100 mẫu sai số tuyệt đối lớn nhất của mỗi mô hình | Như trên |
| outputs/experiments/final_test/analysis/paired_model_uncertainty.csv | Hiệu RMSE và khoảng 95% bootstrap theo khối 7 ngày, 2.000 lần, seed 42 | Như trên |
| outputs/experiments/validation_diagnostics/rf_group_permutation_importance.csv | Importance theo nhóm của Random Forest fit trên train fold 5 | Notebook 08; python -m src.validation_diagnostics |
| outputs/experiments/validation_diagnostics/mlp_seed_summary.csv, mlp_validation_diagnostics.csv, mlp_loss_curves.csv | Seed 7, 42, 2026 trên 5 fold; kiểm tra epoch ở fold 1 và 2; đường loss trên thang đã chuẩn hóa | Như trên |
| evaluation_manifest.json, diagnostics_manifest.json | Môi trường, commit nền, hash dữ liệu và mô hình; operator = null (chưa ghi người chạy) | Do lệnh tương ứng ghi |

---

## Phụ lục B. Sai số theo trạm

Bảng B1 (validation, hai baseline) khớp baseline_error_analysis.csv ở mọi ô (24 hàng x 4 cột số; số mẫu từng trạm đúng). Chỉ lưu ý nhỏ về làm tròn (mức thấp): MAE Persistence của Gucheng trong CSV là 10,795 (4 chữ số) còn DOCX ghi 10,79, trong khi MAE Persistence của Dongsi là 10,985 và DOCX ghi 10,99; hai ô làm tròn không cùng quy tắc, chênh 0,01. Đề xuất thêm B2 và B3 từ kết quả test của năm mô hình.

### DÁN VÀO DOCX (thêm sau Bảng B1)

Bảng B2. RMSE (µg/m³) theo trạm trên test của năm mô hình (chữ đậm là thấp nhất trong hàng)

| Trạm | Số mẫu | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|---|
| Aotizhongxin | 4.292 | 22,27 | 20,74 | **19,79** | 20,02 | 19,97 |
| Changping | 4.297 | 21,64 | 20,74 | 20,32 | **19,50** | 20,26 |
| Dingling | 4.143 | 19,49 | 19,06 | 18,42 | **18,39** | 18,47 |
| Dongsi | 4.234 | 25,56 | 24,01 | **22,93** | 24,13 | 24,68 |
| Guanyuan | 4.248 | 23,92 | 22,61 | 21,66 | **21,64** | 22,42 |
| Gucheng | 4.251 | 24,51 | 22,96 | **22,24** | 23,39 | 22,94 |
| Huairou | 4.280 | 21,01 | 20,30 | 19,79 | 19,61 | **19,59** |
| Nongzhanguan | 4.260 | 23,34 | 21,90 | **20,86** | 21,66 | 21,87 |
| Shunyi | 4.210 | 23,66 | 21,81 | 20,70 | 20,75 | **20,59** |
| Tiantan | 4.284 | 22,02 | 20,36 | **19,65** | 20,50 | 20,17 |
| Wanliu | 4.288 | 21,73 | 20,39 | **19,75** | 19,91 | 20,49 |
| Wanshouxigong | 4.276 | 27,12 | 25,83 | **24,64** | 24,97 | 25,36 |

Bảng B3. MAE (µg/m³) theo trạm trên test của năm mô hình (chữ đậm là thấp nhất trong hàng)

| Trạm | Persistence | Linear Reg. | RF tinh chỉnh | GB tinh chỉnh | MLP tinh chỉnh |
|---|---|---|---|---|---|
| Aotizhongxin | 11,69 | 11,38 | **10,54** | 10,60 | 11,03 |
| Changping | 11,50 | 11,45 | 10,89 | **10,73** | 11,10 |
| Dingling | 9,61 | 9,94 | **9,25** | 9,30 | 9,40 |
| Dongsi | 12,77 | 12,51 | **11,59** | 12,20 | 12,47 |
| Guanyuan | 12,48 | 12,17 | **11,36** | 11,41 | 11,90 |
| Gucheng | 11,89 | 11,75 | **10,86** | 11,47 | 12,03 |
| Huairou | 9,46 | 9,55 | **8,84** | 8,93 | 9,15 |
| Nongzhanguan | 12,04 | 11,60 | **10,88** | 11,17 | 11,55 |
| Shunyi | 12,20 | 11,43 | **10,58** | 10,73 | 11,02 |
| Tiantan | 11,79 | 11,37 | **10,79** | 11,13 | 11,24 |
| Wanliu | 10,89 | 10,66 | **9,95** | 10,17 | 10,71 |
| Wanshouxigong | 12,69 | 12,37 | **11,54** | 11,95 | 12,29 |

Nguồn B2 và B3: final_test_error_by_station.csv (notebook 08, ô evidence-nb-08). Số mẫu của 12 trạm cộng lại 51.063 cho từng mô hình. Chênh lệch giữa các mô hình trong từng trạm chưa có khoảng tin cậy.

---

## Phụ lục C. Cấu trúc sản phẩm và cách chạy lại

Các đoạn Phụ lục C hiện có đúng về cấu trúc, nhưng thiếu: (1) lệnh kiểm tra nguồn số liệu; (2) lệnh chạy notebook trong kernel sạch; (3) hai lệnh phân tích bổ sung; (4) requirements-lock.txt; (5) mô tả đầy đủ fallback baseline. Câu "cài thư viện bằng python -m pip install -r requirements.txt" cần nói rõ khác biệt giữa hai tệp.

### DÁN VÀO DOCX (thêm sau đoạn "Tạo môi trường ảo, cài thư viện ...", hoặc thay đoạn đó)

**Môi trường.** Dùng Python 3.13 trong môi trường ảo riêng. Các mô hình đã lưu yêu cầu scikit-learn 1.7.2 (không dùng kernel hệ thống nếu có scikit-learn 1.8.0). requirements-lock.txt ghi toàn bộ phiên bản của môi trường Windows đã kiểm chứng; requirements.txt ghi phiên bản các thư viện chính. Các lệnh sau chạy trong PowerShell, từ thư mục gốc của kho mã nguồn:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
python -m pip install ipykernel
```

Nếu PowerShell không cho kích hoạt môi trường ảo, gọi trực tiếp: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt ipykernel`.

**Kiểm thử pipeline dữ liệu.**

```powershell
python -m pytest -q
```

**Chạy lại notebook trong kernel sạch và kiểm tra nguồn số liệu.** scripts/run_notebooks.py xóa output rồi thực thi lại notebook trong thư mục notebooks/; nếu một lần chạy lỗi giữa chừng, bản chạy dở được lưu thành tệp .failed.ipynb trong thư mục .notebook_runtime và notebook đã chạy trong notebooks/ được giữ nguyên; sau khi chạy xong, script gọi scripts/sync_notebooks.py để cập nhật notebooks_unexecuted/. Notebook 05 và 07 với cờ --verify-searches chỉ đối chiếu kết quả tìm kiếm đã lưu, không chạy lại RandomizedSearchCV và không được ghi là lần tìm kiếm mới; muốn tìm kiếm lại thật phải chạy 05 và 07 đầy đủ (theo search_seconds trong metadata, lần tìm kiếm trước mất RF 1.532 giây, GB 691 giây, MLP 931 giây; thời gian phụ thuộc máy).

```powershell
.\.venv\Scripts\python.exe -B scripts/run_notebooks.py 01 02 03 04 06 08
.\.venv\Scripts\python.exe -B scripts/run_notebooks.py 05 07 --verify-searches
.\.venv\Scripts\python.exe -B scripts/verify_result_sources.py
.\.venv\Scripts\python.exe -B scripts/refresh_experiment_tables.py
.\.venv\Scripts\python.exe -B scripts/build_report_requirements.py
```

verify_result_sources.py kiểm tra rằng cả 8 notebook có ô bằng chứng đã thực thi, giá trị trong CSV khớp output notebook, hash CSV và mã nguồn không đổi, điểm CV và test khớp experiment_log.csv, và số mẫu theo nhóm của test cộng lại bằng 51.063; lệnh in "PASS" cùng danh sách CSV được liên kết (outputs/notebooks/tables/report_sources.csv). Không chỉnh tay CSV để khớp một kết luận.

**Phân tích bổ sung trên cấu hình đã khóa.**

```powershell
.\.venv\Scripts\python.exe -m src.eda
.\.venv\Scripts\python.exe -m src.evaluation
.\.venv\Scripts\python.exe -m src.validation_diagnostics
```

src.eda tạo lại bảng và hình EDA (ACF, phân bố tuyến tính và log, quan hệ gió) tại outputs/eda. src.evaluation nạp các mô hình đã lưu, kiểm tra điểm test khớp bảng gốc rồi xuất sai số theo nhóm, mẫu sai lớn, khoảng bootstrap và manifest vào outputs/experiments/final_test/analysis. src.validation_diagnostics tính importance của Random Forest và kiểm tra seed, epoch của MLP, xuất vào outputs/experiments/validation_diagnostics; các lệnh này không thay thế tệp joblib của mô hình cuối.

**Mô hình đã lưu và phương án dự phòng cho baseline.** Notebook 08 và src.evaluation tìm mô hình trong models/ trước. Nếu thiếu models/baseline_linear_regression.joblib, chương trình dùng bản lưu trong outputs/experiments/experiments01/models/; nếu thiếu ba mô hình tinh chỉnh thì dùng bản trong outputs/experiments/experiments03/models/. Có thể đặt biến LINEAR_MODEL_PATH ở notebook 08 để chỉ định đường dẫn khác cho Linear Regression. Nếu không có bản lưu nào, chạy notebook 02 với SAVE_ARTIFACTS=True để tạo lại. Persistence không cần tệp mô hình; dự báo lấy PM2.5 giờ t (forward-fill tối đa 6 giờ), nếu vẫn thiếu thì dùng trung vị nhãn train + validation. Chương trình kiểm tra phiên bản scikit-learn khớp metadata (hiện là 1.7.2) trước khi nạp.

**Lưu ý trước khi chạy.** Các notebook bật SAVE_ARTIFACTS=True sẽ ghi lại bảng, hình và mô hình; sao lưu thư mục models/ và outputs/ nếu muốn giữ bản hiện tại. Notebook 02 mặc định RUN_FINAL_TEST=False; phần chấm test tập trung ở notebook 08. notebooks_unexecuted/ là bản xóa output của notebooks/; đồng bộ bằng python scripts/sync_notebooks.py sau khi sửa notebooks/.

### Ghi chú kiểm chứng (không dán)

- Lệnh lấy từ README.md (mục Thiết lập môi trường, Chạy kiểm thử, Nguồn số liệu báo cáo từ notebook, Tái lập và phân tích bổ sung), scripts/run_notebooks.py (tham số names, --verify-searches), scripts/verify_result_sources.py (các kiểm tra), src/artifacts.py (resolve_model_paths: thứ tự models/ rồi outputs/experiments/experiments01 hoặc 03; MODEL_FILES), src/evaluation.py và src/validation_diagnostics.py (docstring "Run: python -m ...").
- Lệnh trong README dùng cả requirements-lock.txt (mục môi trường) và requirements.txt (đường dẫn dự phòng và mục tái lập); giữ cả hai và giải thích.
- README.md nói notebook 05 và 07 chỉ chạy --verify-searches; việc "chạy đầy đủ 05 và 07" lấy từ câu "Muốn chạy lại search thật, chạy 05/07 đầy đủ theo hướng dẫn notebook". Thời gian tìm kiếm lấy từ search_seconds trong metadata (RF 1532,5; GB 691,4; MLP 931,0 giây), là số đo lúc tạo mô hình, tùy máy.
- Không chạy pytest, run_notebooks hay verify_result_sources trong lần rà soát này (không được ghi vào kho; verify_result_sources ghi report_sources.csv). Nhóm nên chạy và dán dòng PASS thật vào báo cáo hoặc biên bản.
- Bảng C1 hiện có đúng 8 notebook và khớp danh sách tệp trong notebooks/.

