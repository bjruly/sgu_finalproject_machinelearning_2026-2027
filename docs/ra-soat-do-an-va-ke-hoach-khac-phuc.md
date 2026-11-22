# Rà soát toàn bộ đồ án và kế hoạch khắc phục

## Phạm vi mới theo yêu cầu người dùng — 20/11/2026

Danh sách cũ bên dưới là lịch sử rà soát. Phạm vi đang áp dụng: chưa cần W&B/MLflow và không tự thêm công nghệ mới; các yêu cầu riêng của bài MRI không áp dụng cho đồ án PM2.5.

Code/CSV đã được bổ sung nguồn notebook, thống nhất biên nhóm PM2.5 và quy trình kiểm chứng. Danh sách hiện hành để sửa riêng DOCX/PPTX là [nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md](nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md). Tra report_sources.csv thay vì sao chép số từ nhận xét cũ có thể khác quy tắc nhóm.


- **Ngày rà soát:** 20/11/2026.
- **Phạm vi:** mã nguồn, dữ liệu, kiểm thử tự động, notebook 01–08, mô hình đã lưu, kết quả CSV/Excel, nhật ký thực nghiệm và tài liệu trong repository.
- **Trọng tâm:** tính đúng đắn, đầy đủ và khả năng tái lập của kiểm thử thực nghiệm.
- **Trạng thái của tài liệu:** danh sách phát hiện và công việc cần thực hiện; các checkbox chưa đánh dấu không có nghĩa là đã sửa.
- **Giới hạn kiểm chứng:** đã chạy pytest, đối chiếu dữ liệu và tính lại kết quả từ dự đoán/mô hình lưu sẵn; chưa huấn luyện lại toàn bộ mô hình và chưa chạy lại toàn bộ tìm kiếm siêu tham số từ đầu.
- **Nguồn bằng chứng:** các tệp nội bộ của repository và các lệnh kiểm chứng trong lần rà soát này. Các bảng tính thêm theo nhóm ở tài liệu này chưa được xuất thành artifact của pipeline.

## Cập nhật sau sửa code và chạy kiểm chứng — 20/11/2026

Đây là trạng thái mới nhất sau danh sách rà soát ban đầu. Các mục bên dưới tài liệu giữ nguyên làm bằng chứng và kế hoạch; không coi tất cả checkbox cũ là đã được hoàn tất.

**Kiểm chứng đã chạy:** 27/27 pytest đạt; pip check không có xung đột; notebook 08 chạy thành công từ kernel sạch. Điểm test của năm mô hình tái lập đúng bảng gốc. Dữ liệu nguồn, joblib cuối và cấu hình mô hình không bị thay đổi.

| Mục | Trạng thái sau cập nhật |
|---|---|
| R01 | Đã tạo .venv, ghim dependencies và ghi requirements-lock.txt cho Python 3.13/Windows; scikit-learn 1.7.2. |
| R02 | Đã thêm fallback tự tìm baseline trong hồ sơ experiments01 và kiểm tra phiên bản trước khi nạp. |
| R03 | Đã xuất predictions, lỗi theo trạm/tháng/mùa/mức PM2.5, worst cases và hình cho cả năm mô hình cuối. |
| R04 | Đã chạy permutation importance theo nhóm cho RF fit riêng trên train fold 5; chưa chạy lại một chương trình ablation đầy đủ với mọi bộ feature. |
| R05 | Notebook 02 mặc định tắt test; lịch sử các lần đã xem test vẫn cần được nhóm trình bày trung thực. |
| R06 | Đã có bootstrap ghép cặp theo khối 7 ngày và kiểm tra MLP với ba seed trên cả năm folds. Khoảng phụ thuộc thời kỳ và cách lấy khối. |
| R07 | Đã lưu loss curve, số epoch, cảnh báo và kiểm tra giới hạn 100 epoch ở hai fold đầu. Không đổi mô hình cuối theo chẩn đoán. |
| R08 | Đã có kiểm thử fit–lưu–nạp–predict cho bốn họ mô hình và kiểm tra model lưu sẵn. |
| R09 | Hai bộ notebook có cùng source/cấu hình; có script đồng bộ. Đã chạy lại riêng notebook 08; chưa chạy lại toàn bộ tuning 05/07. |
| R10 | Đã xuất manifest đánh giá cuối với hash dữ liệu, source, model, metadata và các artifact; nhật ký lịch sử cũ vẫn giữ cơ chế cập nhật theo experiment_id. |
| R11 | Giữ nguyên các ghi chú snapshot dựng bổ sung; không biến chúng thành lịch sử gốc. |
| R12 | Hướng dẫn đã phân biệt trung bình metric qua folds với pooled OOF. |
| R13 | Giữ bộ 27 đầu vào để so sánh công bằng; báo cáo mới đã nêu các feature chưa triển khai. |
| R14 | Đã thêm code, CSV và hình tái tạo ACF/log-scale/gió. Các điểm 999/844 vẫn cần xác minh ngoài dữ liệu quan sát hiện có. |
| R15 | Nhóm đã cung cấp DOCX/PPTX cập nhật. Các bảng/hình mới của đợt sửa code này cần được đưa vào báo cáo/slide khi chốt nội dung. |
| R16 | Đã sửa README, liên kết slide mới, đường dẫn model và chú thích nguồn workbook test. |
| R17 | Không di chuyển dữ liệu gốc ngoài phạm vi; pipeline vẫn chỉ đọc đúng 12 CSV PRSA. Việc dọn gói bàn giao còn để nhóm quyết định. |

### Kết quả mới cần dùng khi viết báo cáo

1. Test theo nhóm PM2.5 >250: RF RMSE 44,593; LR 44,837; Persistence 46,247; GB 48,590; MLP 48,832 µg/m³. Không suy từ thứ hạng tổng thể rằng mô hình luôn thắng ở mọi nhóm.
2. Khoảng chênh lệch RMSE RF - LR: [-1,1251; -0,5930]; RF - GB: [-0,7799; 0,1339]; RF - MLP: [-1,3431; 0,2557]. Hai cặp sau chứa 0 trong phép bootstrap đã chọn.
3. Importance RF có thứ tự PM2.5 hiện tại → chất ô nhiễm khác → lag/rolling → khí tượng → thời gian → trạm. Không sao chép thứ hạng importance của LR sang RF.
4. MLP tăng giới hạn epoch không cải thiện hai fold được kiểm tra. MLP theo seed có RMSE CV trung bình 19,5268 (7), 19,6317 (42), 19,2951 (2026); không dùng test để chọn lại seed.

**Đầu ra:** outputs/experiments/final_test/analysis/, outputs/experiments/validation_diagnostics/, outputs/eda/tables/ và outputs/eda/figures/. README gốc có lệnh tái lập; mỗi thư mục phân tích có ghi chú cách diễn giải.

## 1. Kết luận hiện trạng

Phần huấn luyện và so sánh mô hình đã có cấu trúc tương đối đầy đủ: baseline, mô hình ban đầu, tinh chỉnh và đánh giá cuối trên cùng tập test. Những việc còn thiếu tập trung vào:

1. Sửa khả năng chạy lại mô hình và notebook đánh giá cuối.
2. Hoàn thiện phân tích sai số của chính các mô hình đã tinh chỉnh.
3. Bổ sung bằng chứng giải thích đóng góp của nhóm đặc trưng.
4. Đánh giá độ ổn định và mức chắc chắn của chênh lệch mô hình.
5. Làm rõ quy trình sử dụng test và lịch sử các thí nghiệm.
6. Hoàn thiện báo cáo, slide và gói bàn giao cuối kỳ.

Không phát hiện rò rỉ dữ liệu trực tiếp trong phần tạo target, lag/rolling và chia thời gian đã kiểm tra. Tuy nhiên, điều này không chứng minh rằng mọi quyết định phát triển mô hình trong lịch sử đều độc lập với kết quả test; phần lịch sử sử dụng test cần được nhóm xác nhận và trình bày đúng.

Không cần ưu tiên thêm mô hình mới, demo hoặc dự báo t+24 trước khi hoàn tất các việc trên.

## 2. Những phần đã kiểm chứng đạt

| Hạng mục | Kết quả kiểm chứng | Ý nghĩa và giới hạn |
|---|---|---|
| Kiểm thử tự động | 15/15 test đạt; lệnh: `python -X utf8 -B -m pytest -q -p no:cacheprovider` | Kiểm tra pipeline dữ liệu; chưa thay thế đánh giá thực nghiệm mô hình. |
| Dữ liệu processed | Đủ 420.768 dòng; giá trị các cột khớp dữ liệu gộp từ 12 CSV PRSA gốc | Không thấy sai lệch do bước chuẩn hóa dữ liệu. |
| Số mẫu sau tạo nhãn | 412.017 mẫu có target; 8.751 dòng không có target | Train + validation: 360.954; test: 51.063. |
| Tạo target | PM2.5 giờ kế tiếp của cùng trạm, tạo từ dữ liệu gốc trước forward-fill | Không điền target bằng giá trị giả. |
| Đặc trưng thời gian | Lag/rolling tính riêng theo trạm, chỉ dùng quá khứ | Dùng quan sát có sẵn tại từng giờ để dự báo trước một giờ. |
| Chia dữ liệu | Chia theo thời điểm nhãn; các trạm cùng timestamp ở cùng phía của fold | Tránh tách các trạm cùng giờ sang train và validation. |
| Tiền xử lý | Imputer/scaler/encoder nằm trong pipeline, fit trên train của từng fold | Không thấy việc học thống kê tiền xử lý từ test trong các notebook mô hình. |
| Dự đoán validation | RF, GB, MLP đều có 300.696 mẫu OOF; khóa mẫu và target khớp dữ liệu/fold | Tính lại RMSE từng fold khớp CSV, sai khác chỉ ở mức làm tròn số thực. |
| Mô hình lưu sẵn | Với scikit-learn 1.7.2, bốn mô hình tái lập đúng MAE/RMSE/R² test | Với môi trường hiện tại dùng 1.8.0, cả bốn pipeline lỗi khi dự đoán. |
| Bảng tổng hợp | Điểm chính trong CSV, workbook thực nghiệm và experiment log nhất quán | Một số đường dẫn nguồn và trạng thái mô tả trong tài liệu vẫn cần cập nhật. |
| Bản mô hình theo đợt | Các joblib đối chiếu giữa thư mục models và hồ sơ thực nghiệm tương ứng khớp | Metadata có khác biệt ở đường dẫn artifact; không coi đây là sai lệch điểm mô hình. |

**Không nên sửa các điểm đã đúng chỉ để làm lại toàn bộ quy trình.** Ví dụ: không chuyển sang chia ngẫu nhiên, không điền target thiếu, không xóa đợt PM2.5 cao chỉ vì làm tăng RMSE.

## 3. Quy ước ưu tiên

| Mức | Cách hiểu |
|---|---|
| **P1 — cần hoàn tất trước bàn giao** | Có thể làm người nhận không chạy được dự án, hoặc khiến kết luận thực nghiệm thiếu bằng chứng trọng yếu. |
| **P2 — cần hoàn thiện để kết luận chắc chắn hơn** | Bổ sung độ tin cậy, khả năng truy vết, kiểm thử và tính nhất quán của hồ sơ. |
| **P3 — mở rộng tùy thời gian** | Hữu ích nhưng không phải điều kiện cốt lõi để hoàn thành phạm vi hiện tại. |

Mức ưu tiên là đề xuất từ lần rà soát, không thay thế tiêu chí chấm hoặc yêu cầu riêng của giảng viên.

## 4. Danh sách cần sửa chi tiết

### R01 — Khóa môi trường tái lập và sửa lỗi nạp mô hình [P1]

**Bằng chứng**

- [requirements.txt](../requirements.txt) chưa cố định phiên bản thư viện.
- Metadata của mô hình chính ghi scikit-learn 1.7.2.
- Môi trường dùng để rà soát ban đầu có Python 3.13.12, pandas 3.0.1, NumPy 2.4.0 và scikit-learn 1.8.0.
- Bốn mô hình lưu sẵn đều lỗi khi dự đoán với 1.8.0:

```text
AttributeError: 'SimpleImputer' object has no attribute '_fill_dtype'
```

- Khi kiểm chứng bằng scikit-learn 1.7.2 trong thư mục tạm, điểm test tái lập khớp hoàn toàn.

**Cần làm**

- [ ] Chọn và ghi rõ phiên bản Python được hỗ trợ.
- [ ] Tạo bộ dependencies cố định cho môi trường đã kiểm chứng; tối thiểu phải xử lý sự tương thích scikit-learn 1.7.2 của các joblib hiện có.
- [ ] Ghi đầy đủ phiên bản các thư viện trực tiếp dùng trong pipeline và notebook.
- [ ] Thử cài từ môi trường sạch theo đúng README.
- [ ] Kiểm tra nạp và dự đoán bằng cả bốn mô hình cuối.
- [ ] Ghi rõ môi trường cho các thí nghiệm bổ sung dùng phiên bản khác.

**Tiêu chí hoàn thành:** người nhận tạo môi trường theo hướng dẫn, nạp mô hình và tính lại được điểm cuối mà không cần tự đoán phiên bản hoặc sửa thuộc tính nội bộ của thư viện.

### R02 — Sửa đường dẫn Linear Regression trong notebook 08 [P1]

**Bằng chứng**

- [Notebook 08](../notebooks/08_final_evaluation.ipynb) mặc định đọc `models/baseline_linear_regression.joblib`.
- File ở đường dẫn mặc định hiện không tồn tại.
- Bản lưu vẫn có tại [hồ sơ thực nghiệm 01](../outputs/experiments/experiments01/models/baseline_linear_regression.joblib).
- [.gitignore](../.gitignore) bỏ qua bản baseline tại thư mục models.

**Cần làm**

- [ ] Chọn một cơ chế thống nhất: tạo model qua notebook 02, dùng trực tiếp bản lưu theo đợt, hoặc có fallback đường dẫn rõ ràng.
- [ ] Đảm bảo notebook 08 tìm được đủ bốn pipeline khi làm theo quy trình bàn giao.
- [ ] Cập nhật README và thông báo lỗi để người nhận biết bước nào cần chạy.
- [ ] Không tạo nhiều bản mô hình không rõ bản nào là nguồn chính.

**Tiêu chí hoàn thành:** chạy notebook 08 theo hướng dẫn từ một bản checkout sạch không bị dừng vì thiếu baseline ở đường dẫn mặc định.

### R03 — Hoàn thiện phân tích sai số test cho mô hình cuối [P1]

**Bằng chứng**

Notebook 08 hiện chủ yếu có bảng điểm tổng thể và biểu đồ RMSE. Các phân tích ở notebook trước thuộc baseline hoặc mô hình ban đầu, chưa thay thế phân tích cho các pipeline đã tuning.

Tính thêm trên cùng test cho thấy:

| Mô hình | RMSE toàn test, 51.063 mẫu | RMSE nhóm PM2.5 > 250, 3.685 mẫu |
|---|---:|---:|
| Persistence | 23,1133 | 46,247 |
| Linear Regression | 21,8027 | 44,837 |
| Random Forest tuned | **20,9613** | **44,593** |
| Gradient Boosting tuned | 21,2957 | 48,590 |
| MLP tuned | 21,4967 | 48,832 |

Đơn vị: µg/m³. Các ngưỡng là nhóm phân tích của đồ án, không tự diễn giải thành kết luận y tế.

**Nhận xét cần phản ánh trong báo cáo**

- GB và MLP tốt hơn Persistence về RMSE tổng thể nhưng kém hơn ở nhóm PM2.5 > 250.
- RF chỉ cải thiện rất ít so với Linear Regression trong nhóm PM2.5 cao.
- RF có RMSE khoảng 11,36 vào 09/2016 nhưng khoảng 29,57 vào 01/2017.
- RF có RMSE tổng thể thấp nhất, nhưng không thấp nhất ở mọi tháng và mọi trạm.
- Không thể suy từ thứ hạng tổng thể rằng một mô hình luôn tốt hơn trong mọi điều kiện.

**Cần làm**

- [ ] Xuất dự đoán từng mẫu của cả năm mô hình cuối, kèm trạm, thời điểm quan sát, thời điểm nhãn và y_true.
- [ ] Tính MAE, RMSE, số mẫu và residual trung bình theo 12 trạm.
- [ ] Tính các chỉ số theo từng tháng và mùa có trong test.
- [ ] Tính các chỉ số theo mức PM2.5, thống nhất quy tắc biên của các khoảng.
- [ ] Giữ quy ước residual = y_true - y_pred nhất quán.
- [ ] Vẽ thực tế–dự đoán và residual theo thời gian quanh các đợt sai số lớn.
- [ ] Lập bảng các mẫu hoặc đợt sai số lớn nhất, đối chiếu dữ liệu nguồn.
- [ ] Đối chiếu với Persistence và Linear Regression ở từng nhóm.
- [ ] Giải thích test chỉ gồm thu–đông, không đại diện đầy đủ bốn mùa.

**Tiêu chí hoàn thành:** câu hỏi sai số thay đổi theo trạm/mùa/mức ô nhiễm được trả lời bằng artifact của chính các mô hình cuối, có số mẫu và nhận xét cụ thể.

### R04 — Bổ sung giải thích đóng góp nhóm đặc trưng [P1]

**Bằng chứng**

- [Notebook 02](../notebooks/02_model_training_baseline.ipynb) có permutation importance theo nhóm cho Linear Regression.
- [Notebook 03](../notebooks/03_random_forest.ipynb) có feature importance từ cây, nhưng đây là phương pháp khác với permutation importance.
- Chưa có phân tích tương đương cho RF tuned, mô hình có RMSE CV thấp nhất trong các cấu hình chính.
- Các snapshot v1/v2/v3 trong Experimental Log đã có thử nghiệm bộ đặc trưng, nhưng một số dùng môi trường khác hoặc ngân sách tuning khác.

**Cần làm**

- [ ] Bổ sung permutation importance theo nhóm cho RF tuned trên validation mà mô hình dùng để giải thích chưa được fit vào.
- [ ] Có nhóm PM2.5 hiện tại, lag/rolling, chất ô nhiễm khác, khí tượng, thời gian và trạm.
- [ ] Báo cáo RMSE gốc, mức tăng RMSE, số lần lặp, seed và quy tắc lấy mẫu.
- [ ] Nếu tổng hợp thử nghiệm thêm/bớt feature, giữ cấu hình mô hình, folds, dữ liệu và môi trường cố định.
- [ ] Với thử nghiệm có tuning riêng cho từng bộ feature, ghi rõ đây là so sánh các pipeline được tối ưu riêng; không quy toàn bộ chênh lệch cho feature.
- [ ] Không dùng mô hình fit toàn bộ train + validation để đánh giá importance trên chính phần validation đó như thể dữ liệu chưa thấy.
- [ ] Diễn giải importance là mức phụ thuộc của mô hình trong phép thử, không phải quan hệ nhân quả.

**Tiêu chí hoàn thành:** câu hỏi nghiên cứu về đóng góp feature được trả lời cho mô hình chính; bằng chứng và giới hạn phương pháp được ghi rõ.

### R05 — Làm rõ việc sử dụng test và khóa cấu hình [P1]

**Bằng chứng**

- Notebook 02 mặc định `RUN_FINAL_TEST = True`.
- Hồ sơ giữa kỳ đã có kết quả và phân tích test cho baseline trước khi hoàn tất các mô hình còn lại.
- Nhật ký cập nhật theo experiment_id và có thể ghi đè dòng cũ; riêng việc đọc nhật ký cuối không đủ xác nhận toàn bộ thứ tự quyết định trong lịch sử.

Những điểm này chưa chứng minh nhóm đã chọn cấu hình theo test. Tuy nhiên, không nên khẳng định tuyệt đối rằng test chưa từng được xem trước giai đoạn cuối nếu không có bằng chứng.

**Cần làm**

- [ ] Đặt mặc định tắt test trong notebook phát triển/baseline.
- [ ] Chọn cấu hình và mô hình chính bằng validation/CV; ghi rõ quy tắc lựa chọn.
- [ ] Ghi lại cấu hình, phiên bản dữ liệu/mã nguồn và thời điểm khóa trước bước đánh giá cuối.
- [ ] Trình bày trung thực các lần đã xem test và mục đích sử dụng.
- [ ] Phân biệt kiểm chứng lại kết quả với thay đổi mô hình do kết quả test.
- [ ] Mọi thí nghiệm mới về feature/hyperparameter nên dùng validation, không chọn theo test đã xem.
- [ ] Nếu quyết định thay đổi dựa trên test, ghi rõ giới hạn độc lập của đánh giá; không gọi cùng test đó là một holdout mới chưa từng sử dụng.
- [ ] Mô tả đây là đánh giá dự báo một giờ kế tiếp với quan sát cập nhật tại mỗi giờ.

**Tiêu chí hoàn thành:** người đọc phân biệt được dữ liệu dùng để fit, chọn cấu hình, diễn giải validation và đánh giá cuối.

### R06 — Bổ sung độ ổn định và độ chắc chắn của chênh lệch [P2]

**Bằng chứng**

- Thực nghiệm chính chủ yếu dùng seed 42.
- RF tuned giảm RMSE test 3,86% so với Linear Regression và 1,57% so với GB tuned.
- Chưa thấy khoảng tin cậy cho chênh lệch của các mô hình cuối.
- Độ lệch chuẩn giữa folds đã có trong một số bảng, nhưng không thay thế khoảng tin cậy của chênh lệch ghép cặp trên test.

**Cần làm**

- [ ] Chạy thêm một số seed trên validation cho mô hình ngẫu nhiên, ưu tiên MLP.
- [ ] Tính độ biến động của MAE/RMSE và thứ hạng, giữ cùng folds.
- [ ] Khi ước lượng khoảng tin cậy trên test, dùng so sánh ghép cặp trên cùng mẫu.
- [ ] Cân nhắc bootstrap theo khối ngày/tuần; giữ các trạm cùng thời điểm trong cùng khối.
- [ ] Ghi số lần lặp, seed, độ dài khối và giới hạn của phép ước lượng.
- [ ] Không xem từng dòng giờ của 12 trạm là các quan sát hoàn toàn độc lập.
- [ ] Dùng cách kết luận phù hợp với bằng chứng; không tuyên bố vượt trội ổn định chỉ từ một thứ hạng điểm.

**Tiêu chí hoàn thành:** có bằng chứng về mức biến động hoặc ghi rõ giới hạn nếu chưa thực hiện, cùng kết luận không vượt quá số liệu.

### R07 — Kiểm tra và thảo luận hội tụ của MLP [P2]

**Bằng chứng**

[mlp_tuned_cv_metrics.csv](../outputs/notebooks/tables/mlp_tuned_cv_metrics.csv) ghi fold 1 và 2 đều chạy 40 epoch và có `hit_iteration_limit = True`. MLP gốc cũng chạm giới hạn ở fold 1. Notebook có cơ chế thu thập cảnh báo; không nên bỏ qua ý nghĩa của chúng khi viết kết luận.

**Cần làm**

- [ ] Xuất hoặc lưu loss curve cho các lần fit cần phân tích.
- [ ] Kiểm tra tăng giới hạn epoch trên validation với cấu hình được kiểm soát.
- [ ] So sánh chất lượng và chi phí tính toán, thay vì chỉ tăng epoch cho đến khi hết cảnh báo.
- [ ] Ghi rõ max_iter là giới hạn, không phải đảm bảo hội tụ.
- [ ] Giữ lại số epoch thực chạy và trạng thái cảnh báo.
- [ ] Không thay đổi cấu hình theo kết quả test đã xem.

**Tiêu chí hoàn thành:** báo cáo giải thích được giới hạn huấn luyện MLP và ảnh hưởng có thể có đến kết quả. Chạm giới hạn epoch không tự động đồng nghĩa mô hình không hợp lệ.

### R08 — Mở rộng kiểm thử sang vòng đời mô hình [P2]

**Bằng chứng**

Các test hiện tại ở [tests/](../tests/) kiểm tra dữ liệu, target, feature, preprocessing và tích hợp pipeline dữ liệu; test tích hợp chưa thực hiện đủ fit → lưu → nạp → predict cho mô hình.

**Cần làm**

- [ ] Thêm smoke test nhỏ cho Linear Regression, RF, HistGradientBoosting và MLP.
- [ ] Kiểm tra pipeline tạo được dự đoán hữu hạn, đúng số mẫu.
- [ ] Kiểm tra dự đoán trước/sau lưu–nạp tương đương trong môi trường hỗ trợ.
- [ ] Kiểm tra đầu vào/đường dẫn mô hình của bước đánh giá cuối.
- [ ] Bổ sung các kiểm thử có ý nghĩa cho nhánh lỗi: trùng giờ, gián đoạn giờ, thiếu cột và dữ liệu rỗng nếu nhánh đó chưa được bao phủ.
- [ ] Giữ kiểm tra target không được impute và việc fit thống kê chỉ trên train.
- [ ] Không đưa toàn bộ RandomizedSearchCV vào pytest; để riêng kiểm chứng thực nghiệm dài.

**Tiêu chí hoàn thành:** bộ kiểm thử phát hiện được các lỗi tích hợp mô hình quan trọng mà 15 test dữ liệu hiện tại chưa phát hiện.

### R09 — Thống nhất hai bộ notebook và chạy lại từ kernel sạch [P1]

**Bằng chứng**

- `notebooks/` và `notebooks_unexecuted/` không hoàn toàn giống nhau về source.
- Ô lưu baseline_metrics ở bộ chính ghi vào outputs/notebooks/tables, còn bộ chưa chạy ghi vào models.
- Notebook 06 trong bộ chưa chạy mặc định `SAVE_ARTIFACTS = False`.
- Kiểm tra cú pháp code cells không phát hiện lỗi; không thấy error output lưu sẵn trong bộ notebook chính.
- Execution count và output lưu sẵn không chứng minh toàn bộ chuỗi chạy lại được từ kernel sạch.

**Cần làm**

- [ ] Chọn một bộ source làm chuẩn.
- [ ] Nếu giữ bản xóa output, tạo từ cùng source và chỉ khác phần output/execution count hoặc cấu hình có giải thích.
- [ ] Thống nhất nơi lưu baseline_metrics.csv và cập nhật mọi tài liệu liên quan.
- [ ] Đồng bộ cờ lưu model/kết quả để notebook sau có đủ đầu vào.
- [ ] Chạy từng notebook bằng Restart & Run All theo đúng thứ tự.
- [ ] Ghi lại thứ tự, phụ thuộc artifact, thời gian dự kiến và kết quả kiểm chứng.
- [ ] Bảo toàn kết quả chính khi kiểm thử chạy lại, tránh ghi đè không có chủ ý.

**Tiêu chí hoàn thành:** làm theo hướng dẫn từ kernel sạch tạo được đầy đủ artifact cần thiết và chạy được đánh giá cuối.

### R10 — Chuẩn hóa nhật ký, manifest và artifact của lần chạy [P2]

**Bằng chứng**

`dataset_version` chủ yếu là chuỗi mô tả tên CSV và cấu hình feature. Chuỗi này chưa xác định duy nhất nội dung dữ liệu/mã nguồn; log hiện cập nhật đè theo experiment_id.

**Cần làm**

- [ ] Có run_id riêng và thời điểm chạy thực tế.
- [ ] Ghi commit mã nguồn và hash dữ liệu khi có thể.
- [ ] Ghi danh sách feature, seed, folds, tham số và phiên bản thư viện.
- [ ] Ghi đường dẫn hoặc hash của mô hình dùng để đánh giá cuối.
- [ ] Tách log lịch sử chạy khỏi bảng tổng hợp “kết quả mới nhất”.
- [ ] Lưu manifest đánh giá cuối liên kết model, predictions và metrics.
- [ ] Không coi `test_evaluated: false` trong metadata lúc huấn luyện là lỗi nếu nó phản ánh đúng giai đoạn tạo model; dùng manifest đánh giá riêng để ghi việc chấm test sau đó.

**Tiêu chí hoàn thành:** truy ngược được một con số trong báo cáo về dữ liệu, mô hình, cấu hình và lần chạy cụ thể.

### R11 — Trình bày đúng các snapshot dựng bổ sung [P2]

**Bằng chứng**

Nhiều thư mục ngày trong Experimental Log có ghi chú cho biết thực nghiệm được chạy bổ sung ngày 19/11/2026, không phải bản gốc khôi phục. Một số dùng scikit-learn 1.8.0 và chỉ tìm kiếm một cấu hình.

**Cần làm**

- [ ] Giữ các ghi chú hiện có.
- [ ] Trong bảng tổng hợp, phân biệt ngày đặt tên thư mục, ngày chạy thật và loại thực nghiệm.
- [ ] Ghi rõ số cấu hình đã thử, tránh gọi một lượt thử là ngân sách tuning đầy đủ.
- [ ] Không trình bày các bản dựng bổ sung thành lịch sử thực nghiệm gốc.
- [ ] Không coi chúng là các lần lặp độc lập theo seed nếu seed/quy trình không thay đổi.
- [ ] Khi hướng dẫn chạy snapshot cũ, kiểm tra đường dẫn ghi file để không làm đè mô hình chính.
- [ ] Không chạy các notebook thay đổi biến toàn cục của src.features nối tiếp trong cùng kernel mà không khôi phục trạng thái hoặc khởi động lại.

**Tiêu chí hoàn thành:** hồ sơ minh bạch về nguồn gốc, thời điểm và điều kiện thực nghiệm; không làm lẫn với bộ kết quả chính.

### R12 — Làm rõ cách tổng hợp metric giữa folds [P2]

**Bằng chứng**

Điểm CV chính là trung bình cộng metric của năm folds. Đây không phải RMSE tính gộp toàn bộ các dự đoán OOF.

| Mô hình ban đầu | Trung bình RMSE 5 folds | RMSE tính gộp OOF |
|---|---:|---:|
| Random Forest | 20,1707 | 20,7948 |
| Gradient Boosting | 21,9726 | 23,3244 |
| MLP | 20,0840 | 20,5145 |

Hai cách tính trả lời các câu hỏi tổng hợp khác nhau; chênh lệch trên không phải bằng chứng bảng hiện tại bị tính sai.

**Cần làm**

- [ ] Ghi rõ “trung bình RMSE của 5 folds” trong bảng CV chính.
- [ ] Nếu báo cáo pooled OOF, dùng nhãn riêng và cùng tập mẫu cho các mô hình.
- [ ] Không so lẫn hai cách tổng hợp trong cùng bảng xếp hạng.
- [ ] Giữ đầy đủ năm folds làm kết quả chính.
- [ ] Chỉ dùng trung bình fold 2–5 như phân tích bổ sung có giải thích; không bỏ fold 1 vì mô hình có điểm xấu.

**Tiêu chí hoàn thành:** mọi bảng ghi đúng cách tổng hợp và so sánh nhất quán.

### R13 — Đối chiếu feature proposal với feature đã triển khai [P2]

**Bằng chứng**

[src/features.py](../src/features.py) đã có PM2.5 hiện tại, lag 1/2/3/6/12/24, rolling mean 6/24, chất ô nhiễm khác, khí tượng hiện tại, thời gian tuần hoàn, trạm và hướng gió.

Chưa có các phần dự kiến sau:

- Độ lệch so với rolling mean.
- Lag của biến khí tượng.
- Cờ cuối tuần riêng.

**Cần làm**

- [ ] Có bảng “dự kiến → thực hiện → chưa làm/lý do”.
- [ ] Không mô tả feature chưa có như thể đã được dùng huấn luyện.
- [ ] Nếu bổ sung, kiểm tra trên validation và so sánh các mô hình trên cùng bộ feature.
- [ ] Nếu giữ phạm vi hiện tại, giải thích việc hoãn/bỏ; không bắt buộc bổ sung đủ mọi feature đã dự kiến.
- [ ] Nếu thay bộ feature chính, kiểm tra lại model, predictions, metadata và các bảng phụ thuộc.

**Tiêu chí hoàn thành:** báo cáo mô tả đúng feature đã tạo ra kết quả đang công bố.

### R14 — Hoàn thiện bằng chứng EDA và xử lý điểm nghi ngờ [P2]

**Bằng chứng**

Notebook 01 hiện có thống kê missing, kiểm tra thời gian, phân bố, biến động theo tháng/giờ/mùa và tương quan. Chưa có đầy đủ code tái tạo phân tích tự tương quan, phân bố log-scale và quan hệ PM2.5 với gió đã dự kiến.

Nhật ký EDA vẫn để mở việc xác minh PM2.5 = 999 và điểm 844 tại Nongzhanguan.

**Cần làm**

- [ ] Bổ sung ACF hoặc phép đo tự tương quan với quy tắc xử lý missing rõ ràng.
- [ ] Bổ sung hình log-scale nếu sử dụng nhận xét về phân bố đó trong báo cáo.
- [ ] Bổ sung phân tích hướng/tốc độ gió nếu giữ nội dung này trong phạm vi đã thực hiện.
- [ ] Đảm bảo các con số EDA đưa vào báo cáo có code hoặc bảng nguồn tái tạo được.
- [ ] Ghi nhận kết quả xác minh hai điểm nghi ngờ; nếu chưa xác minh được, giữ nguyên và nêu giới hạn.
- [ ] Nếu làm phân tích độ nhạy, xác định quy tắc trước và báo cáo riêng; không tự loại điểm để cải thiện metric.
- [ ] Làm rõ hình trước/sau xử lý là mô tả feature; không phải impute target hoặc preprocessing dùng chung cho mọi fold.

**Tiêu chí hoàn thành:** EDA có bằng chứng tái tạo cho các nhận xét chính và quyết định dữ liệu có giải thích.

### R15 — Bổ sung báo cáo và slide cuối kỳ [P1]

**Bằng chứng**

[docs/](./) hiện có proposal, báo cáo giữa kỳ và slide giữa kỳ. Chưa thấy tài liệu cuối kỳ tổng hợp đầy đủ notebook 04–08.

**Cần làm**

- [ ] Tạo báo cáo cuối kỳ riêng, giữ proposal và báo cáo giữa kỳ như hồ sơ lịch sử.
- [ ] Tạo slide cuối kỳ tương ứng với kết quả mới nhất.
- [ ] Trình bày môi trường, target, feature, split, folds, metric và quy trình chọn cấu hình.
- [ ] Có bảng baseline → mô hình ban đầu → tuning → test.
- [ ] Trả lời từng câu hỏi nghiên cứu bằng số liệu.
- [ ] Phân tích cả kết quả tốt và trường hợp thua baseline.
- [ ] Nêu giới hạn test thu–đông, hội tụ MLP và độ ổn định chưa kiểm chứng đầy đủ.
- [ ] Cập nhật đóng góp thành viên theo công việc thực tế; loại các placeholder của bản giữa kỳ khỏi tài liệu cuối.
- [ ] Đối chiếu nguồn dữ liệu, tài liệu tham khảo và chú thích hình/bảng.
- [ ] Ghi rõ HistGradientBoostingRegressor là biến thể thực tế được dùng.
- [ ] Mọi con số và hình phải truy về artifact tương ứng.

**Tiêu chí hoàn thành:** tài liệu cuối phản ánh đúng bộ kết quả đã chốt, không còn mô tả GB/MLP/tuning là chưa làm nếu chúng đã có kết quả.

### R16 — Đồng bộ README, tài liệu hướng dẫn và đường dẫn nguồn [P2]

**Cần làm**

- [ ] Cập nhật [proposal-review-and-alignment.md](proposal-review-and-alignment.md) về trạng thái mô hình/test hiện tại, hoặc gắn rõ thời điểm áp dụng của các nhận xét cũ.
- [ ] Đồng bộ README gốc với hướng dẫn từng thư mục.
- [ ] Kiểm tra tất cả đường dẫn đến model, metric, hình và notebook.
- [ ] Sửa chú thích nguồn trong workbook final_test: hiện còn ghi outputs/final_test_metrics.csv trong khi bảng chính ở outputs/notebooks/tables/final_test_metrics.csv.
- [ ] Loại mô tả cấu trúc cũ khỏi hướng dẫn hiện hành, ví dụ các file src/models.py hoặc src/evaluate.py nếu không thực sự tồn tại.
- [ ] Nếu giữ bản ZIP và bản Git khác nhau về model, mô tả rõ và bảo đảm cả hai có quy trình chạy hợp lệ.

**Tiêu chí hoàn thành:** hướng dẫn và liên kết khớp cấu trúc đang bàn giao, không yêu cầu người nhận suy đoán.

### R17 — Tách dữ liệu ngoài phạm vi và dọn gói bàn giao [P2]

**Bằng chứng**

`data/raw/data.csv` và `data/raw/test.csv` chứa schema OHLCV của dữ liệu giá, không thuộc PRSA. Pipeline hiện đọc đúng thư mục 12 trạm nên không bị trộn nhầm.

**Cần làm**

- [ ] Chuyển dữ liệu ngoài phạm vi khỏi gói bàn giao hoặc đánh dấu mục đích rõ ràng.
- [ ] Không xóa/sửa 12 CSV nguồn PRSA.
- [ ] Kiểm tra ảnh/tệp phụ không liên quan và artifact trùng lặp không cần thiết.
- [ ] Giữ tài liệu cần thiết để truy vết; không dọn mất nguồn của kết quả đã công bố.

**Tiêu chí hoàn thành:** người nhận phân biệt ngay được dữ liệu của đề tài và dữ liệu ngoài phạm vi.

## 5. Bộ artifact thực nghiệm cần bổ sung

Các tên dưới đây là **đề xuất đầu ra**, không khẳng định các file đã tồn tại. Có thể dùng tên khác nếu được quy định nhất quán trong notebook và README.

| Artifact đề xuất | Nội dung tối thiểu | Công việc liên quan |
|---|---|---|
| final_test_predictions.csv | station, datetime, target_datetime, y_true, dự đoán từng mô hình | R03 |
| final_test_error_by_station.csv | model, station, n, MAE, RMSE, mean_residual | R03 |
| final_test_error_by_month.csv | model, month, n, MAE, RMSE, mean_residual | R03 |
| final_test_error_by_season.csv | model, season, n, MAE, RMSE, mean_residual | R03 |
| final_test_error_by_pm25_level.csv | model, level, n, MAE, RMSE, mean_residual | R03 |
| final_test_worst_cases.csv | các mẫu/đợt sai số lớn, khóa truy vết và dự đoán | R03 |
| feature_group_importance.csv | model/fold, nhóm feature, RMSE gốc, mức tăng, độ biến động | R04 |
| feature_set_comparison.csv | bộ feature, config, folds, seed, môi trường, metric | R04 |
| seed_stability.csv | model, seed, fold, metric | R06 |
| paired_model_uncertainty.csv | cặp mô hình, chênh lệch, khoảng ước lượng, quy tắc bootstrap | R06 |
| evaluation_manifest.json | run_id, model paths/hash, dữ liệu/hash, commit, phiên bản, cấu hình | R05, R10 |
| Hình phân tích cuối | thực tế–dự đoán, residual, nhóm lỗi, chuỗi thời gian, importance | R03, R04 |
| Môi trường cố định | dependencies và hướng dẫn cài/rerun đã kiểm chứng | R01, R09 |
| Báo cáo và slide cuối kỳ | kết quả, giải thích, giới hạn và đóng góp thực tế | R15 |

Nên tích hợp các artifact phân tích cuối vào notebook 08 hoặc một notebook phân tích có nguồn đầu vào rõ ràng. Không chỉ tính thủ công rồi chép số vào báo cáo mà thiếu cách tái tạo.

## 6. Thứ tự triển khai đề nghị

### Đợt A — Làm cho bộ hiện tại chạy lại được

- [ ] R01: khóa và kiểm chứng môi trường.
- [ ] R02: sửa đầu vào model của notebook 08.
- [ ] R09: thống nhất hai bộ notebook, đường dẫn và cờ lưu artifact.
- [ ] R08: thêm smoke test tích hợp mô hình.

**Điểm kiểm tra:** chạy được đánh giá từ mô hình đã lưu và tái lập bảng test hiện tại. Không cần chạy lại toàn bộ tuning chỉ vì đổi tài liệu hoặc sửa đường dẫn.

### Đợt B — Hoàn thiện bằng chứng thực nghiệm

- [ ] R03: lưu predictions, phân tích test theo nhóm và đợt sai số.
- [ ] R04: giải thích nhóm đặc trưng; tổng hợp thử nghiệm feature có kiểm soát.
- [ ] R06: bổ sung độ ổn định và ước lượng chênh lệch.
- [ ] R07: kiểm tra hội tụ MLP trên validation.
- [ ] R12: thống nhất cách tổng hợp metric.

**Điểm kiểm tra:** có thể trả lời vì sao mô hình tốt hơn, tốt ở đâu, kém ở đâu và kết luận chắc chắn đến mức nào.

### Đợt C — Chốt phương pháp, hồ sơ và bàn giao

- [ ] R05: làm rõ lịch sử test và khóa cấu hình.
- [ ] R10–R11: hoàn thiện manifest và nguồn gốc thí nghiệm.
- [ ] R13–R14: đối chiếu proposal, feature và EDA.
- [ ] R15–R16: báo cáo, slide và hướng dẫn nhất quán.
- [ ] R17: gói dữ liệu và artifact đúng phạm vi.

**Điểm kiểm tra:** mọi kết luận truy về được kết quả; người khác làm theo hướng dẫn mà không cần kiến thức ngầm từ nhóm.

## 7. Điều kiện nghiệm thu cuối

- [ ] Môi trường cài mới chạy được và phiên bản được ghi rõ.
- [ ] Pytest đạt và smoke test mô hình đạt.
- [ ] Các notebook chạy theo hướng dẫn từ kernel sạch.
- [ ] Tái lập được bảng test của bộ mô hình đã chốt.
- [ ] Có dự đoán từng mẫu và phân tích nhóm cho các mô hình cuối.
- [ ] Có bằng chứng trả lời đóng góp feature của mô hình chính.
- [ ] Có thảo luận về độ ổn định, hội tụ và giới hạn.
- [ ] Không dùng thứ hạng test để âm thầm chọn lại cấu hình.
- [ ] Báo cáo phân biệt CV, pooled OOF và test.
- [ ] Báo cáo, slide, CSV, Excel, metadata và hình nhất quán.
- [ ] Không trình bày snapshot bổ sung như lịch sử gốc.
- [ ] Phân công và đóng góp thành viên được xác nhận.
- [ ] Đường dẫn model/dữ liệu/hình hoạt động trong gói bàn giao.

## 8. Phần mở rộng không bắt buộc ở thời điểm này [P3]

Các việc sau chỉ nên làm sau khi hoàn thành các điểm cốt lõi:

- Dự báo t+24 hoặc nhiều chân trời.
- Mô hình riêng từng trạm hoặc đánh giá trên trạm chưa thấy.
- Thử thêm họ mô hình mới.
- Demo giao diện dự đoán.
- Nghiên cứu thêm độ nhạy với giới hạn forward-fill và cờ dữ liệu đã được điền.

Nếu triển khai mở rộng, cần quy trình validation và mô tả phạm vi riêng. Không dùng chúng để thay thế các phân tích còn thiếu của bài toán dự báo t+1 hiện tại.
