"""Generate the requested DOCX/slide edit list from verified notebook tables."""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.notebook_evidence import verify_evidence


def markdown_table(frame, digits=4):
    def cell(value):
        if pd.isna(value):
            return "—"
        if isinstance(value, float):
            return f"{value:.{digits}f}".replace(".", ",")
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(str, frame.columns)) + " |",
             "| " + " | ".join("---" for _ in frame.columns) + " |"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |"
              for row in frame.itertuples(index=False, name=None)]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-date", default=datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d/%m/%Y"))
    args = parser.parse_args()
    sources = verify_evidence(ROOT, write_index=True)
    if sources.notebook.nunique() != 8:
        raise ValueError("Finish the notebook executions/checks before generating requirements.")
    tables = ROOT / "outputs/notebooks/tables"
    analysis = ROOT / "outputs/experiments/final_test/analysis"
    diagnostics = ROOT / "outputs/experiments/validation_diagnostics"
    final = pd.read_csv(tables / "final_test_metrics.csv")
    high = pd.read_csv(analysis / "final_test_error_by_pm25_level.csv")
    high = high.loc[high.pm25_level.eq(">250"), ["model", "n", "mae", "rmse", "mean_residual"]]
    importance = pd.read_csv(diagnostics / "rf_group_permutation_importance.csv")
    intervals = pd.read_csv(analysis / "paired_model_uncertainty.csv")
    seeds = pd.read_csv(diagnostics / "mlp_seed_summary.csv")
    convergence = pd.read_csv(diagnostics / "mlp_validation_diagnostics.csv")
    original = convergence.loc[convergence.diagnostic.eq("seed_stability") & convergence.seed.eq(42),
                               ["fold", "max_iter", "rmse"]]
    epoch = convergence.loc[convergence.diagnostic.eq("epoch_limit_check"),
                             ["fold", "max_iter", "epochs", "rmse", "convergence_warning"]]
    epoch = original.merge(epoch, on="fold", suffixes=("_original", "_diagnostic"))
    configs = pd.read_csv(tables / "final_model_configuration.csv")
    counts = pd.read_csv(ROOT / "outputs/eda/tables/dataset_counts.csv")
    improvements = pd.read_csv(tables / "final_test_relative_improvements.csv")
    improvements = improvements.loc[improvements.model.eq("Random Forest - tuned")]
    baseline_groups = pd.read_csv(tables / "baseline_error_analysis.csv")
    baseline_levels = baseline_groups.loc[baseline_groups.group_type.eq("pm25_level"),
                                          ["group", "model", "n", "mae", "rmse", "mean_residual"]]
    index = sources[["notebook", "cell_id", "mode", "csv_path"]]
    main_index = index.loc[~index.csv_path.str.contains("oof_predictions|loss_curves|worst_cases|acf_by_station|predictions.csv")]
    text = f"""# Yêu cầu chỉnh sửa báo cáo DOCX và slide — đồ án Beijing PM2.5

**Ngày cập nhật:** {args.review_date}.  
**Đối tượng cần sửa:** Nhom10_BeijingAirQuality_BaoCaoCuoiKy.docx và Nhom10__Slide.pptx.  
**Mục đích:** hướng dẫn sửa nội dung tài liệu sau khi code/CSV đã được rà soát và chạy kiểm chứng.

## 1. Phạm vi đã thống nhất với người dùng

- Tạm chưa thực hiện và không đặt W&B/MLflow thành điều kiện phải hoàn thành trong đợt này.
- Không tự thêm thư viện, framework, dịch vụ, mô hình hoặc công nghệ mới. Mọi mở rộng công nghệ cần hỏi ý kiến trước.
- Chỉ áp dụng góp ý phù hợp với hồi quy chuỗi thời gian PM2.5 đa trạm.
- Không áp dụng yêu cầu riêng của đề tài đầu gối/MRI: DICOM, CNN/BiLSTM, phân loại đa nhãn, Macro F1/AUC, bác sĩ hoặc dữ liệu bệnh viện.
- Không ép đồ án ứng dụng này đề xuất thuật toán mới hoặc chứng minh thắng SOTA. Có thể đối chiếu nghiên cứu liên quan một cách trung thực.
- File này là yêu cầu sửa DOCX/PPTX, không phải tuyên bố hai tệp đã được chỉnh sửa.
- Các bảng số dưới đây lấy bằng chương trình từ CSV được đối chiếu với output notebook. Không nhập số theo suy đoán.

Các ghi chú của thầy còn phù hợp: nêu bài toán rõ; có pipeline; nói danh sách thực nghiệm trước kết quả; trình bày mục tiêu → kết quả → bình luận; có metric/setup; nguồn số liệu rõ; bài nói gọn và tránh lặp. Các phần nghe không rõ trong ghi chú không trở thành quy định bắt buộc.

## 2. Nguồn bằng chứng và cách sử dụng số liệu

Tra [report_sources.csv](../outputs/notebooks/tables/report_sources.csv) để tìm notebook, mã ô, lượt thực thi và hash của từng CSV.

- computed: bảng được tính/xuất trong lần thực thi notebook.
- verified_saved_search: notebook chỉ đối chiếu artifact tuning đã lưu. Không được viết rằng vừa chạy lại toàn bộ RandomizedSearchCV.
- File trong notebooks_unexecuted chỉ là bản xóa output; dẫn nguồn kết quả bằng notebook đã có output trong notebooks.
- Bảng tổng hợp experiments01–03 được sinh từ CSV nguồn notebook; hồ sơ lịch sử trong Experimental Log không được sửa thành lần chạy mới.
- Không suy tên người chạy từ tác giả commit; chỉ ghi tên/ngày chạy có bằng chứng hoặc được nhóm xác nhận.
- Khi code/CSV thay đổi, chạy scripts/verify_result_sources.py. Nếu báo sai hash hoặc sai giá trị, kiểm chứng lại trước khi đưa số vào tài liệu.

### Bản đồ nguồn đang dùng

{markdown_table(main_index)}

Các bảng số có dấu phẩy thập phân để đọc; CSV gốc dùng định dạng số của pandas. Đổi cách trình bày không được làm đổi giá trị hoặc đơn vị.

## 3. Yêu cầu sửa báo cáo DOCX theo vị trí hiện tại

| Vị trí | Yêu cầu sửa | Dẫn chứng/nguồn |
|---|---|---|
| Mục 1: thông tin và tiến độ | Rút gọn phần quản lý; chuyển bảng phân công/tiến độ dài sang phụ lục nếu không phải yêu cầu mẫu nộp | Đây là báo cáo dự báo PM2.5; tránh để tiến độ lấn át phương pháp và thực nghiệm |
| Mục 2: giới thiệu | Viết rõ vấn đề, thách thức, mục tiêu và đóng góp trong phạm vi môn học | Notebook 01 mô tả dữ liệu; notebook 02–08 có kết quả so sánh |
| Mục tiêu/CH2 | Mở rộng từ chỉ Linear Regression sang cả phân tích RF đã có | Notebook 02: LR importance; notebook 08: RF importance |
| Mục tiêu/CH3 | Phân biệt phân tích validation với phân tích test của năm mô hình cuối | Notebook 02/04/06 và notebook 08 |
| Phần công trình liên quan | Thêm phần tổng quan ngắn, chỉ nêu nghiên cứu/phương pháp liên quan, khó khăn và nhận xét | Đồng bộ với các nguồn thực sự được dùng ở slide 9; kiểm tra bài gốc trước khi trích |
| Mục 3–4: dữ liệu, EDA, tiền xử lý | Giữ số mẫu và thống kê lấy từ notebook 01; ghi target t+1, không impute target và fit tiền xử lý trên train | Notebook 01; src/data_loader.py; src/features.py |
| Mục 4.3: feature | Giữ đúng bộ đầu vào hiện có, phân biệt trước/sau preprocessing; ghi rõ feature trong proposal chưa dùng | Notebook 01/02/08; final_model_configuration.csv |
| Mục 5.1: pipeline | Một hình tổng quan trước khi mô tả từng khối | Hình pipeline hiện có; mô tả đúng thứ tự target, feature, split và fit preprocessing |
| Mục 5.2: mô hình | Ghi đúng cấu hình ban đầu/tuned; GB thực tế là HistGradientBoostingRegressor | Notebook 03–08 và CSV cấu hình từ notebook 08 |
| Sau mục mô hình | Thêm mục ngắn giải thích loss/tiêu chí đang dùng và phân biệt với metric | Code estimator trong notebook 02–07; cấu hình notebook 08 |
| Mục 5.3: thiết lập | Mốc nhãn, cùng folds/feature, seed, môi trường đã dùng; cách chọn theo validation | Notebook 02–08, lockfile, output thật |
| Trước mục 6.1 | Thêm danh sách thí nghiệm với câu hỏi cần kiểm chứng | Dùng danh sách gợi ý tại mục 4 của file này |
| Mục 6.1–6.3: validation và tuning | Giữ đủ folds; ghi trung bình metric giữa folds; số tổ hợp lấy từ CSV search được notebook kiểm tra | Notebook 02–07; không gọi trung bình fold 2–5 là kết quả chính |
| Mục 6.4: test | Bảng năm mô hình trên cùng mẫu, xếp theo RMSE; mức giảm lấy từ bảng do notebook 08 tính | final_test_metrics.csv; final_test_relative_improvements.csv |
| Mục 6.5: sai số nhóm | Thay bảng/nhận xét cũ nếu khác quy tắc biên; bổ sung lỗi của mô hình tuned trên test | baseline_error_analysis.csv và final_test_error_by_*.csv |
| Mục 6.6: importance | Giữ LR đúng phạm vi, bổ sung RF và bình luận khác biệt | CSV importance của notebook 02 và 08 |
| Sau phần kết quả chính | Bổ sung mức chắc chắn, seed/hội tụ khi dùng để kết luận | Notebook 08: các bảng bootstrap, seed và epoch |
| Mục 6.7/kết luận | Trả lời câu hỏi bằng kết quả; nêu giới hạn test theo thời gian/trạm và trường hợp sai | Không gọi R² là Accuracy, không tự nhận triển khai thực tế |
| Mục 7: hạn chế/việc còn lại | Xóa nhận xét đã lỗi thời về thiếu code/thiếu bảng; chỉ giữ phần thực sự chưa làm | So với output notebook hiện tại và danh sách file CSV mới |
| Tài liệu tham khảo | Đồng bộ các nguồn giữa DOCX/PPTX; không chèn kết quả định lượng ngoài notebook vào bảng thực nghiệm của nhóm | Tên tác giả, năm, bài và DOI phải kiểm tra từ nguồn gốc |
| Phụ lục chạy lại | Bổ sung lệnh chạy notebook/kiểm tra nguồn CSV, lockfile và fallback baseline | README và scripts hiện tại |

### Nội dung cần viết rõ, không cần bổ sung công nghệ

**Đóng góp của đề tài khác với đóng góp từng thành viên.** Có thể trình bày pipeline đa trạm tránh rò rỉ, so sánh các mô hình đang có và phân tích sai số/độ ổn định. Chỉ nhận những đóng góp đã có code và kết quả.

**Loss:** Persistence không fit; LR dùng bình phương sai số; RF dùng tiêu chí squared_error; Histogram Gradient Boosting dùng squared_error; MLP dùng squared_error với regularization và target scaling theo code. RMSE/MAE báo cáo được tính ở đơn vị µg/m³. Đường training loss của MLP không phải đường RMSE ở đơn vị gốc.

**Công trình liên quan:** có thể giữ các bài đang trích để giải thích bối cảnh/lựa chọn phương pháp. Không buộc phải cài thuật toán của bài đó; không lấy RMSE trên dataset/split khác để tuyên bố nhóm thắng bài báo.

**Giới hạn:** kết quả trên các trạm đã quan sát trong giai đoạn test không chứng minh độ chính xác tại trạm mới, mọi mùa hay khả năng đưa ra quyết định sức khỏe. Các điểm dữ liệu còn nghi ngờ phải mô tả đúng trạng thái, không tự xác nhận là lỗi đo.

## 4. Danh sách thực nghiệm nên giới thiệu trước phần kết quả

Đây là cách tổ chức các việc đã có; không phải yêu cầu chạy thêm mô hình.

| Nhóm | Câu hỏi | Notebook |
|---|---|---|
| Baseline | Persistence đã mạnh đến đâu; LR cải thiện metric nào? | 02 |
| Mô hình ban đầu | RF/GB/MLP có vượt baseline trong validation không? | 03, 04, 06 |
| Tuning | Cấu hình được chọn cải thiện ở đâu, đặc biệt theo fold? | 05, 07; trạng thái artifact được ghi rõ |
| Test cuối | Cấu hình đã khóa đạt kết quả thế nào trên cùng tập test? | 08 |
| Phân tích sai số | Mô hình hay sai ở trạm, tháng, mức PM2.5 hoặc đợt nào? | 02, 04, 06, 08 |
| Đóng góp feature | LR và RF phụ thuộc vào nhóm feature nào? | 02, 08 |
| Độ ổn định | Seed/epoch và bootstrap cho phép kết luận tới mức nào? | 08 |

Với từng nhóm: ghi mục tiêu, điều kiện, bảng/hình, bình luận và đường dẫn notebook/CSV. Không chỉ đọc lại các số.

## 5. Bảng số có nguồn notebook để cập nhật tài liệu

### 5.1. Quy mô dữ liệu

Nguồn: notebook 01, ô evidence-nb-01; [dataset_counts.csv](../outputs/eda/tables/dataset_counts.csv).

{markdown_table(counts)}

Diễn giải đúng: dòng dữ liệu gốc khác mẫu đã có nhãn t+1; có số đo thiếu không đồng nghĩa thiếu timestamp. Mốc chia dựa trên target_datetime.

### 5.2. Test của các mô hình đã khóa

Nguồn: notebook 08, ô evidence-nb-08; [final_test_metrics.csv](../outputs/notebooks/tables/final_test_metrics.csv).

{markdown_table(final)}

Nguồn tỷ lệ cải thiện: [final_test_relative_improvements.csv](../outputs/notebooks/tables/final_test_relative_improvements.csv), cũng được tính và hiển thị trong notebook 08.

{markdown_table(improvements)}

Không gọi phần trăm giảm RMSE là Accuracy. Không sửa cấu hình dựa trên bảng test này.

### 5.3. Bảng baseline theo mức PM2.5 phải cập nhật đồng bộ

Nguồn: notebook 02, ô evidence-nb-02; [baseline_error_analysis.csv](../outputs/notebooks/tables/baseline_error_analysis.csv).

{markdown_table(baseline_levels)}

Baseline cũ dùng cách đóng biên khác với MLP/test. Bản hiện tại thống nhất: <=35, (35,75], (75,115], (115,150], (150,250], >250. Khi thay bảng, phải thay cả nhãn khoảng, số mẫu và metric; không chỉ thay tiêu đề.

Không trộn bảng baseline validation với bảng tuned test dưới đây như thể chúng dùng cùng tập mẫu.

### 5.4. Test ở mức PM2.5 cao

Nguồn: notebook 08; [final_test_error_by_pm25_level.csv](../outputs/experiments/final_test/analysis/final_test_error_by_pm25_level.csv).

{markdown_table(high)}

Viết theo số thực tế: RF đứng đầu tổng thể không đồng nghĩa mọi mô hình đều thắng baseline ở PM2.5 cao. Dùng thêm CSV theo trạm/tháng/mùa và hình worst-event để bình luận, không suy đoán nguyên nhân chưa được kiểm tra.

### 5.5. Importance của RF

Nguồn: notebook 08 chạy run_diagnostics rồi hiển thị kết quả; [rf_group_permutation_importance.csv](../outputs/experiments/validation_diagnostics/rf_group_permutation_importance.csv).

{markdown_table(importance[["feature_group","baseline_sample_rmse","rmse_increase_mean","rmse_increase_std","n_repeats","n_validation_sample","fold","seed"]])}

Ghi rõ RF fit trên train fold được chỉ định, chấm validation và hoán vị theo nhóm. Phép đo là mức phụ thuộc của model, không phải nhân quả hoặc thí nghiệm loại feature rồi huấn luyện lại.

Giữ kết quả LR ở phần riêng với nguồn [baseline_lr_group_permutation_importance.csv](../outputs/notebooks/tables/baseline_lr_group_permutation_importance.csv) của notebook 02. Không dùng bảng LR để giải thích RF.

### 5.6. Mức chắc chắn của chênh lệch

Nguồn: notebook 08; [paired_model_uncertainty.csv](../outputs/experiments/final_test/analysis/paired_model_uncertainty.csv).

{markdown_table(intervals[["model_a","model_b","rmse_difference_a_minus_b","ci_95_low","ci_95_high","n_bootstrap","block_days","seed"]])}

Số âm là model_a có RMSE thấp hơn. Nếu khoảng chứa 0, không khẳng định thắng chắc trong phép đánh giá này. Đây là bootstrap có điều kiện trên dự đoán cố định, cách lấy khối và giai đoạn đã quan sát; không khái quát hóa tùy ý.

### 5.7. Seed và epoch của MLP

Nguồn: notebook 08; [mlp_seed_summary.csv](../outputs/experiments/validation_diagnostics/mlp_seed_summary.csv).

{markdown_table(seeds)}

Nguồn kiểm tra epoch: [mlp_validation_diagnostics.csv](../outputs/experiments/validation_diagnostics/mlp_validation_diagnostics.csv).

{markdown_table(epoch)}

Đối chiếu giá trị thật trước khi nhận xét. Hết cảnh báo hội tụ không tự động cải thiện validation. Không dùng thí nghiệm chẩn đoán để âm thầm thay model cuối đã được chọn.

### 5.8. Kích thước model lấy từ pipeline thực tế

Nguồn: notebook 08; [final_model_configuration.csv](../outputs/notebooks/tables/final_model_configuration.csv).

{markdown_table(configs)}

Khi vẽ MLP, phân biệt cột input gốc và số cột sau imputation/missing-indicator/One-Hot/scaling. Kích thước sau biến đổi là thuộc pipeline đã fit, không phải hằng số cho mọi dữ liệu.

## 6. Yêu cầu sửa slide hiện tại

Số dưới đây theo thứ tự trình chiếu của PowerPoint hiện tại, không theo tên slide XML.

| Slide | Sửa như thế nào |
|---|---|
| 1–2 | Giữ tiêu đề và bố cục, thống nhất tên mô hình/bài toán với DOCX |
| 3–8 | Gộp input/output/ví dụ bị lặp; làm rõ thách thức, mục tiêu và đóng góp đã có bằng chứng |
| 9 | Có nhận xét về nghiên cứu liên quan, dẫn nguồn; không biến thành yêu cầu cài công nghệ mới |
| 10–13 | Ghi số từ notebook 01, giữ EDA/tiền xử lý liên quan trực tiếp đến quyết định mô hình |
| 14 | Pipeline tổng quan trước phần chi tiết; giữ quy tắc chỉ dùng dữ liệu đã có tại t |
| 15 | Thêm hình model nếu cần; ghi HistGradientBoostingRegressor; tách loss đang dùng khỏi metric đánh giá |
| 16 | Bổ sung cách chọn bằng validation, nguồn notebook/CSV; tránh tuyên bố test chưa từng được xem nếu không có bằng chứng lịch sử |
| 17 | Nêu danh sách nhóm thực nghiệm và câu hỏi của từng nhóm trước kết quả |
| 18–22 | Kiểm tra CV/test, trước/tuned và đủ folds; tỷ lệ giảm phải lấy từ bảng notebook tính |
| 23 | Cập nhật biên nhóm và lỗi test của mô hình cuối; ghi rõ baseline validation khác tuned test |
| 24 | Ghi rõ LR/RF, split, điều kiện lấy mẫu, số lần lặp; dùng bảng importance có nguồn tương ứng |
| 25–26 | Cập nhật độ chắc chắn, trường hợp thất bại và kết luận trong phạm vi dữ liệu |
| 27–28 | Giữ cảm ơn/phụ lục phù hợp; có thể chuyển chi tiết CV, ví dụ dài và loss curves sang dự phòng |

Gợi ý trình bày gọn: bố cục → bài toán → dữ liệu → pipeline/model/loss → thiết lập và danh sách TN → kết quả chính → phân tích lỗi/độ chắc chắn → kết luận. Số slide và thời lượng phải theo yêu cầu thực tế của môn; không coi ví dụ phân bổ cho bài đầu gối là quy định cứng cho đồ án này.

Chân bảng/hình nên ghi notebook, mã ô và artifact, ví dụ: “Notebook 08, evidence-nb-08; final_test_metrics.csv”. File report_sources.csv cung cấp số ô hiện tại để tra.

## 7. Các phát biểu cần sửa hoặc tránh

- “R² cao nghĩa là Accuracy cao”: sai cách diễn giải hồi quy.
- “RF tốt nhất nên luôn tốt ở mọi trạm/mùa/mức bụi”: kết luận vượt bằng chứng.
- “Importance chứng minh yếu tố gây ô nhiễm”: vượt ý nghĩa phép hoán vị.
- “Bảng baseline theo mức cũ vẫn dùng được mà không đổi biên”: cần cập nhật cả nhóm mẫu.
- “Đã chạy lại toàn bộ tuning”: chỉ viết nếu thực sự chạy; verified_saved_search là đối chiếu artifact cũ.
- “Tất cả số đều do một thành viên chạy”: chỉ ghi khi nhóm xác nhận được.
- “Đồ án còn bắt buộc W&B/MLflow/công nghệ mới theo bài MRI”: không thuộc phạm vi đang được người dùng cho phép.
- “Đã sửa báo cáo/slide”: file này chỉ đưa yêu cầu; sửa hai tệp sau theo các nguồn trên.

## 8. Checklist chốt DOCX và slide

- [ ] Mục tiêu/đóng góp nói đúng các việc đã thực hiện.
- [ ] Giữ phạm vi hồi quy PM2.5; bỏ yêu cầu đặc thù đầu gối/MRI.
- [ ] Mỗi số thực nghiệm có notebook, mã ô và CSV nguồn kiểm chứng được.
- [ ] Không đưa số thử nghiệm mới hoặc kết quả bên ngoài vào bài nếu không có nguồn được chấp nhận.
- [ ] Thống nhất biên nhóm PM2.5, model gốc/tuned, validation/test và đơn vị.
- [ ] Các bảng dữ liệu, CV, test, importance, seed/epoch và bootstrap khớp output notebook.
- [ ] Có setup/metric, pipeline và giải thích loss thực tế, không yêu cầu đổi loss hay thêm model.
- [ ] Có danh sách thực nghiệm trước kết quả và bình luận sau mỗi kết quả.
- [ ] Chú thích hình và trích dẫn giữa DOCX/PPTX nhất quán.
- [ ] Các hạn chế phản ánh phần thực sự chưa làm; không nhận đã triển khai/xác nhận chuyên gia.
- [ ] Tuyến trình bày gọn, ít lặp, mỗi thành viên giải thích được phần mình trình bày.
- [ ] Mọi ý định bổ sung công nghệ được hỏi ý kiến người dùng trước.

**Ưu tiên:** thay số/bảng bằng nguồn notebook hiện tại → sửa nhận xét và phạm vi kết luận → đồng bộ DOCX/PPTX → gộp nội dung lặp và tập trình bày. Chưa đặt việc triển khai W&B/MLflow hoặc công nghệ mới vào checklist phải làm.
"""
    destination = ROOT / "docs/nhung-phan-con-thieu-theo-yeu-cau-giang-vien.md"
    destination.write_text(text, encoding="utf-8")
    print(f"Updated {destination.relative_to(ROOT)} from verified notebook evidence.")


if __name__ == "__main__":
    main()
