## 1. Quy trình

1. Chạy notebook (`Restart & Run All`) cho đến khi xong.
2. Mở terminal **tại thư mục gốc của repo** (PowerShell).
3. Chạy khối lệnh tương ứng ở mục 3.
4. Kiểm tra bằng `tree "Experimental Log" /F`.

Notebook ghi kết quả vào hai thư mục chung, và các lệnh bên dưới chép từ đó:

- Bảng CSV/Excel: `outputs\notebooks\tables\`
- Hình PNG: `outputs\notebooks\figures\`

## 2. Lệnh theo từng notebook

Mỗi khối gồm 5 bước: tạo thư mục (đặt theo ngày chạy hôm nay), chép notebook, chép bảng output, chép hình, trích dòng log.

Biến `$d` dùng `Get-Date -Format 'd-M-yyyy'` nên tự ra đúng tên thư mục như `20-11-2026`. Nếu muốn lưu theo ngày khác, thay phần `$(Get-Date -Format 'd-M-yyyy')` bằng ngày cụ thể, ví dụ `20-11-2026`.

### 02: Baseline

```powershell
$d = "Experimental Log\1. Baseline\v1"
mkdir "$d\outputs\figures"
copy notebooks\02_model_training_baseline.ipynb $d
copy outputs\notebooks\tables\baseline_* "$d\outputs"
copy outputs\notebooks\figures\baseline_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -like "baseline_*" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

Mẫu `baseline_*` lấy cả dòng `baseline_*_cv5` và `baseline_*_test` (nếu notebook 02 đã chạy mục chấm test).

### 03: Random Forest

```powershell
$d = "Experimental Log\2. Random_forest\v1"
mkdir "$d\outputs\figures"
copy notebooks\03_random_forest.ipynb $d
copy outputs\notebooks\tables\random_forest_cv_*, outputs\notebooks\tables\random_forest_fold_overview.csv, outputs\notebooks\tables\random_forest_validation_oof_predictions.csv "$d\outputs"
copy outputs\notebooks\figures\random_forest_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "random_forest_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 04: Gradient Boosting

```powershell
$d = "Experimental Log\3. Gradient_boosting\v1"
mkdir "$d\outputs\figures"
copy notebooks\04_gradient_boosting.ipynb $d
copy outputs\notebooks\tables\gradient_boosting_cv_*, outputs\notebooks\tables\gradient_boosting_validation_oof_predictions.csv "$d\outputs"
copy outputs\notebooks\figures\gradient_boosting_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "gradient_boosting_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 05: Tuning (Random Forest + Gradient Boosting)

Notebook 05 tune cả hai mô hình trong cùng một lần chạy nên snapshot chứa output của cả hai.

```powershell
$d = "Experimental Log\4. Turning\v1"
mkdir "$d\outputs\figures"
copy notebooks\05_tuning.ipynb $d
copy outputs\notebooks\tables\random_forest_tuned_*, outputs\notebooks\tables\gradient_boosting_tuned_*, outputs\notebooks\tables\tuning_random_forest_search_results.csv, outputs\notebooks\tables\tuning_gradient_boosting_search_results.csv "$d\outputs"
copy outputs\notebooks\figures\tuning_rmse_by_fold.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? { $_.experiment_id -in "random_forest_tuned_cv5", "gradient_boosting_tuned_cv5" } | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 06: MLP Regression

```powershell
$d = "Experimental Log\5. mlp_regression\v1"
mkdir "$d\outputs\figures"
copy notebooks\06_mlp_regression.ipynb $d
copy outputs\notebooks\tables\mlp_cv_*, outputs\notebooks\tables\mlp_error_by_group.csv, outputs\notebooks\tables\mlp_validation_oof_predictions.csv "$d\outputs"
copy outputs\notebooks\figures\mlp_cv_rmse_by_fold.png, outputs\notebooks\figures\mlp_pred_vs_actual.png, outputs\notebooks\figures\mlp_residuals.png, outputs\notebooks\figures\mlp_rmse_by_pm25_level.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "mlp_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 07: MLP Tuning

```powershell
$d = "Experimental Log\6. mlp_turning\v1"
mkdir "$d\outputs\figures"
copy notebooks\07_mlp_tuning.ipynb $d
copy outputs\notebooks\tables\mlp_tuned_*, outputs\notebooks\tables\tuning_mlp_search_results.csv "$d\outputs"
copy outputs\notebooks\figures\mlp_tuning_rmse_by_fold.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "mlp_tuned_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

## 4. Lưu ý

- **Chạy lại trong cùng một ngày** sẽ ghi đè thư mục cùng tên (`mkdir` báo thư mục đã tồn tại nhưng `copy` vẫn ghi đè file). Muốn giữ cả hai bản, thêm hậu tố giờ vào tên thư mục, ví dụ đổi `'d-M-yyyy'` thành `'d-M-yyyy_HHmm'`.
- **Notebook 03, 04 và 06** dùng tên file cụ thể (`random_forest_cv_*`, `gradient_boosting_cv_*`, `mlp_cv_*`) cho `outputs\notebooks\tables\` để không chép nhầm file `_tuned`. Không dùng mẫu rộng `random_forest_*`, `gradient_boosting_*` hay `mlp_*` cho thư mục `tables\`.
- **Hình của notebook 06** được liệt kê từng file thay vì dùng `mlp_*`, vì `mlp_*` sẽ chép luôn `mlp_tuning_rmse_by_fold.png` của notebook 07. Còn ở `outputs\notebooks\figures\`, `random_forest_*` và `gradient_boosting_*` thì an toàn vì hình tuning được đặt tên `tuning_rmse_by_fold.png`.
- **Notebook 05** ghi cả `random_forest_tuned_*` và `gradient_boosting_tuned_*` trong một lần chạy. Nếu chỉ tune lại một mô hình, vẫn nên chép snapshot như trên và dùng cùng tên thư mục để dễ so sánh.
- **File OOF** (`*_validation_oof_predictions.csv`) nặng khoảng 28 MB mỗi file. Ở 03, 04, 06 chúng là các file có tên cụ thể trong lệnh `copy`; ở 05 và 07 chúng chỉ xuất hiện khi bật `SAVE_OOF = True` trong notebook (mặc định tắt, và được `random_forest_tuned_*`, `gradient_boosting_tuned_*`, `mlp_tuned_*` kéo theo). Nếu không cần lưu lại, bỏ khỏi lệnh `copy`. Trong thư mục hiện tại, chỉ các bản `8-11-2026` (Random Forest), `10-11-2026` (Gradient Boosting) và `13-11-2026` (MLP) còn giữ file OOF.
- **File `.joblib`** không được lưu trong snapshot (nặng, nhất là `random_forest_tuned.joblib` khoảng 20 MB). Tham số và cấu hình đã có trong `models/*_metadata.json` và cột `notes` của `experiment_log.csv`.
- **Bản dựng lại (`RECONSTRUCTION_NOTE.md`)**: một số thư mục ngày (ví dụ `2-11-2026`, `3-11-2026`, `5-11-2026`, `4-11-2026`, `7-11-2026`, `9-11-2026`, `11-11-2026`, `12-11-2026`) là bản bổ sung được chạy lại để có đủ lịch sử, không phải bản gốc phục hồi. Trong đó có file `RECONSTRUCTION_NOTE.md` ghi rõ ngày chạy, bộ đặc trưng và môi trường. Những bản này thường không có file OOF và notebook đã xóa output cell. Các bản chạy thật không có file ghi chú này.
- **Dòng log** được lọc theo `experiment_id`: `baseline_*` (notebook 02), `random_forest_cv5` (03), `gradient_boosting_cv5` (04), `random_forest_tuned_cv5` + `gradient_boosting_tuned_cv5` (05), `mlp_cv5` (06), `mlp_tuned_cv5` (07), `*_test` (08). Không dùng mẫu `*tuned*` hay `*_tuned_cv5` cho notebook 05 vì sẽ lẫn cả dòng `mlp_tuned_cv5` của notebook 07 (và các dòng `*_tuned_test` của notebook 08). Nếu thêm thí nghiệm mới, đặt `experiment_id` theo quy ước `<tên_thí_nghiệm>_cv5` / `_test` để lọc được.
- **Đã lỡ tạo thư mục sai chỗ** (ví dụ `Experimental Log\20-11-2026` nằm ngoài thư mục nhóm), di chuyển vào đúng nhóm bằng:

  ```powershell
  move "Experimental Log\20-11-2026" "Experimental Log\1. Baseline"
  ```
- **Dùng macOS/Linux**: thay `mkdir` bằng `mkdir -p`, `copy` bằng `cp`, và dùng `/` thay cho `\`. Tên thư mục ngày lấy bằng `$(date +%-d-%-m-%Y)`. Phần lọc dòng log (giữ dòng tiêu đề) làm như sau:

  ```bash
  d="Experimental Log/1. Baseline/$(date +%-d-%-m-%Y)"
  mkdir -p "$d/outputs/figures"
  (head -n 1 experiment_log.csv; grep '^baseline_' experiment_log.csv) > "$d/experiment_log_rows.csv"
  ```
- **Thêm vào `.gitignore`** nếu không muốn đưa snapshot nặng lên Git: `Experimental Log/**/*oof_predictions.cs`
