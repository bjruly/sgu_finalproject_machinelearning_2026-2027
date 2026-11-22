# Phần còn thiếu trong DOCX và slide — tổng hợp (22/11/2026)

Kết quả rà soát toàn bộ đồ án (code, kiểm thử, notebook 01–08, CSV, DOCX, PPTX). Mọi số trong các file 02–06 đã được tính lại từ CSV; chỗ chưa kiểm chứng được ghi `[cần xác nhận]` / `[CẦN NHÓM XÁC NHẬN]`. Chưa có file DOCX/PPTX nào bị sửa.

## 1. Sai/lỗi thời cần sửa trước (cao nhất)
| Vị trí | Vấn đề | Giá trị đúng (nguồn) |
|---|---|---|
| DOCX Bảng 14, 6.5; slide 23 | Bảng sai số theo mức PM2.5 dùng biên cũ [a,b) | n = 115.085 / 72.055 / 45.799 / 24.358 / 30.226 / 13.173; LR >250: RMSE 48,30, residual 19,06 (`baseline_error_analysis.csv`) |
| DOCX Bảng 15; slide 24 | Nhóm "Khí tượng" làm tròn kép | 1,37 (giá trị 1,3749) |
| DOCX 6.1; slide 18–19 | "chấm trên 300.696 dự đoán OOF" dễ hiểu nhầm | Bảng là trung bình số học 5 fold (không phải RMSE gộp OOF; RF ban đầu gộp 20,79 vs 20,17) |
| DOCX Bảng 17 (mục 8) | Gán đóng góp theo tác giả commit | Chỉ ghi khi nhóm xác nhận |
| DOCX mục 9 vs slide 3, 9 | Hai danh sách tài liệu tham khảo không giao nhau | Xem 06_cong-trinh-lien-quan.md |
| DOCX 5.3/7.2/7.3, slide 16 | Câu về việc dùng test và "còn thiếu phân tích test" đã lỗi thời | `outputs/experiments/final_test/analysis/` đã có đủ cho 5 mô hình |

## 2. Còn thiếu — DOCX
Công trình liên quan; Thách thức; Đóng góp; Loss/tiêu chí (HistGradientBoostingRegressor, squared_error); Danh sách thí nghiệm trước mục 6; Độ đo & thiết lập (môi trường, seed); sai số test của 5 mô hình theo trạm/tháng/mùa/mức PM2.5 + trường hợp sai lớn; importance của RF (so với LR); độ chắc chắn (bootstrap ghép cặp), seed MLP, kiểm tra epoch MLP; Đánh giá tổng thể (so công trình liên quan không so số trực tiếp, ý nghĩa thực tế, hạn chế); Kết luận/Hướng phát triển; phụ lục lệnh chạy lại.

## 3. Còn thiếu — Slide
Thách thức & Đóng góp; Thiết lập/Độ đo; danh sách thí nghiệm trước kết quả (kèm câu hỏi + nguồn); hình mô hình/loss; RF importance; slide độ chắc chắn (RF vs GB, RF vs MLP có khoảng chứa 0); đánh giá tổng thể; hướng phát triển; ghi chú trình bày (22/22 notes đang trống); gộp slide 3–7 lặp ý; chuyển CV chi tiết/loss curve sang dự phòng. Đề cương đề xuất: ~19 slide chính (15 phút) + slide dự phòng — xem 01 và 04/05.

## 4. Phát hiện thực nghiệm nên đưa vào bình luận
- RF tuned thấp nhất tổng thể (RMSE test 20,9613) nhưng chỉ thấp nhất ở 7/12 trạm; RF–GB và RF–MLP có CI 95% chứa 0.
- Nhóm PM2.5 >250 (n = 3.685): RF 44,59; LR 44,84; Persistence 46,25; GB 48,59; MLP 48,83 → GB/MLP kém baseline ở nhóm cao.
- MLP: tăng giới hạn epoch không cải thiện (fold 1: 26,98 vs 26,17); seed 7/42/2026 cho RMSE CV 19,53/19,63/19,30.

## 5. Code — đã làm
- Kết quả rà soát: không có lỗi tính toán/rò rỉ; điểm test, bảng nhóm, bootstrap tái lập đúng.
- Đã thêm 23 test (tests/test_metrics_and_bootstrap.py, tests/test_diagnostics_and_validation.py): độ đo, quy ước residual, bootstrap ghép cặp theo khối, importance theo nhóm, nhánh báo lỗi, fit chỉ trên train theo fold, hằng số báo cáo trích, hash CSV nguồn (chỉ đọc), đường dẫn manifest. **pytest: 54 passed** (từ 31).
- `scripts/run_notebooks.py` và đường dẫn tương đối trong manifest (`src/evaluation.py`) đã được sửa sẵn từ trước; chỉ bổ sung test. Các `evaluation_manifest.json` cũ trên đĩa có thể vẫn chứa đường dẫn tuyệt đối đến khi xuất lại.
- Không đổi: `time_split/cv_folds` vẫn fallback sang `datetime` nếu thiếu `target_datetime` (test hiện có dựa vào đó).

## 6. Việc còn lại (cần bạn/nhóm quyết định)
1. Commit: nhiều file `src/`, `tests/`, `scripts/`, `outputs/` còn untracked; `models/baseline_linear_regression.joblib` bị `.gitignore`.
2. Xác nhận phân công thực tế từng thành viên (không suy từ commit).
3. Kiểm tra bản gốc Seng 2021, Bekkar 2021, Wei 2025 (số liệu/kết luận của bài gốc chưa kiểm được).
4. Chạy lại pytest ngay trước khi nộp (số test có thể đổi).
5. Chưa làm (ghi vào hạn chế/hướng phát triển): ablation huấn luyện lại theo nhóm feature, seed cho RF/GB, OOF validation cho mô hình tuned, xác minh điểm 999/844, đánh giá trạm mới/mùa khác.

## File chi tiết (nội dung tiếng Việt dán được vào DOCX/slide)
01 khung & đề cương · 02 DOCX mục 1–5 · 03 DOCX mục 6–9 + phụ lục · 04 slide 1–15 · 05 slide 16–28 · 06 công trình liên quan & tài liệu tham khảo.
