# Hướng dẫn lưu nhật ký thí nghiệm (Experimental Log)

Thư mục `Experimental Log/` lưu lại **ảnh chụp (snapshot)** của từng notebook sau mỗi lần chạy: bản notebook, các file output và các dòng tương ứng trong `experiment_log.csv`. Mục đích là để xem lại và so sánh kết quả giữa các lần chạy mà không bị ghi đè.

Mỗi model/notebook có một thư mục riêng; bên trong là các bản lưu theo ngày chạy.

Quy ước đặt tên: `<tên_model>/<tên_model>_dd_MM_yy/`.

## 2. Quy trình

1. Chạy notebook (`Restart & Run All`) cho đến khi xong.
2. Mở terminal **tại thư mục gốc của repo** (PowerShell).
3. Chạy khối lệnh tương ứng ở mục 3.
4. Kiểm tra bằng `tree "Experimental Log" /F`.

## 3. Lệnh theo từng notebook

Mỗi khối gồm 5 bước: tạo thư mục, chép notebook, chép output, chép hình, trích dòng log.

### 02: Baseline

```powershell
$d = "Experimental Log\1. Baseline\v1"
mkdir "$d\outputs\figures"
copy notebooks\02_model_training_baseline.ipynb $d
copy outputs\baseline_* "$d\outputs"
copy outputs\figures\baseline_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -like "baseline_*" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 03: Random Forest

```powershell
$d = "Experimental Log\2. Random_forest\v1"
mkdir "$d\outputs\figures"
copy notebooks\03_random_forest.ipynb $d
copy outputs\random_forest_cv_*, outputs\random_forest_fold_overview.csv, outputs\random_forest_validation_oof_predictions.csv "$d\outputs"
copy outputs\figures\random_forest_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "random_forest_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 04: Gradient Boosting

```powershell
$d = "Experimental Log\3. Gradient_boosting\v1"
mkdir "$d\outputs\figures"
copy notebooks\04_gradient_boosting.ipynb $d
copy outputs\gradient_boosting_cv_*, outputs\gradient_boosting_validation_oof_predictions.csv "$d\outputs"
copy outputs\figures\gradient_boosting_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "gradient_boosting_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 05: Tuning (Random Forest + Gradient Boosting)

Notebook 05 tune cả hai mô hình trong cùng một lần chạy nên snapshot chứa output của cả hai.

```powershell
$d = "Experimental Log\4. Turning\v1"
mkdir "$d\outputs\figures"
copy notebooks\05_tuning.ipynb $d
copy outputs\random_forest_tuned_*, outputs\gradient_boosting_tuned_*, outputs\tuning_random_forest_search_results.csv, outputs\tuning_gradient_boosting_search_results.csv "$d\outputs"
copy outputs\figures\tuning_rmse_by_fold.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? { $_.experiment_id -in "random_forest_tuned_cv5", "gradient_boosting_tuned_cv5" } | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 06: MLP Regression

```powershell
$d = "Experimental Log\5. mlp_regression\v1"
mkdir "$d\outputs\figures"
copy notebooks\06_mlp_regression.ipynb $d
copy outputs\mlp_cv_*, outputs\mlp_error_by_group.csv, outputs\mlp_validation_oof_predictions.csv "$d\outputs"
copy outputs\figures\mlp_cv_rmse_by_fold.png, outputs\figures\mlp_pred_vs_actual.png, outputs\figures\mlp_residuals.png, outputs\figures\mlp_rmse_by_pm25_level.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "mlp_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

### 07: MLP Tuning

```powershell
$d = "Experimental Log\6. mlp_turning\v1"
mkdir "$d\outputs\figures"
copy notebooks\07_mlp_tuning.ipynb $d
copy outputs\mlp_tuned_*, outputs\tuning_mlp_search_results.csv "$d\outputs"
copy outputs\figures\mlp_tuning_rmse_by_fold.png "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -eq "mlp_tuned_cv5" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

## 4. Lưu ý

- **Chạy lại trong cùng một ngày** sẽ ghi đè thư mục cùng tên. Muốn giữ cả hai bản, thêm hậu tố giờ vào tên thư mục, ví dụ đổi `dd_MM_yy` thành `dd_MM_yy_HHmm`.
- **Notebook 03, 04 và 06** dùng tên file cụ thể (`random_forest_cv_*`, `gradient_boosting_cv_*`, `mlp_cv_*`) để không chép nhầm file `_tuned`. Không dùng mẫu rộng `random_forest_*`, `gradient_boosting_*` hay `mlp_*` cho `outputs\`.
- **Hình của notebook 06** được liệt kê từng file thay vì dùng `mlp_*`, vì `mlp_*` sẽ chép luôn `mlp_tuning_rmse_by_fold.png` của notebook 07. Còn ở `outputs\figures\`, `random_forest_*` và `gradient_boosting_*` thì an toàn vì hình tuning được đặt tên `tuning_rmse_by_fold.png`.
- **Notebook 05** ghi cả `random_forest_tuned_*` và `gradient_boosting_tuned_*` trong một lần chạy. Nếu chỉ tune lại một mô hình, vẫn nên chép snapshot như trên và dùng cùng tên thư mục để dễ so sánh.
- **File OOF** (`*_validation_oof_predictions.csv`, và `*_tuned_validation_oof_predictions.csv` ở 05 và 07; ở 03, 04, 06 là các file có tên cụ thể trong lệnh `copy`) nặng khoảng 28 MB mỗi file. Nếu không cần lưu lại, bỏ khỏi lệnh `copy` ở bước output.
- **File `.joblib`** không được lưu trong snapshot (nặng, nhất là `random_forest_tuned.joblib` khoảng 20 MB). Tham số và cấu hình đã có trong `models/*_metadata.json` và cột `notes` của `experiment_log.csv`.
- **Dòng log** được lọc theo `experiment_id`: `baseline_*` (notebook 02), `random_forest_cv5` (03), `gradient_boosting_cv5` (04), `random_forest_tuned_cv5` + `gradient_boosting_tuned_cv5` (05), `mlp_cv5` (06), `mlp_tuned_cv5` (07). Không dùng mẫu `*tuned*` hay `*_tuned_cv5` cho notebook 05 vì sẽ lẫn cả dòng `mlp_tuned_cv5` của notebook 07. Nếu thêm thí nghiệm mới, đặt `experiment_id` theo quy ước `<tên_thí_nghiệm>_cv5` / `_test` như trong README gốc để lọc được.
- **Đã lỡ tạo thư mục sai chỗ** (ví dụ `Experimental Log\baseline_18_11_26`), di chuyển bằng:

  ```powershell
  mkdir "Experimental Log\baseline"
  move "Experimental Log\baseline_18_11_26" "Experimental Log\baseline"
  ```
- **Dùng macOS/Linux**: thay `mkdir` bằng `mkdir -p`, `copy` bằng `cp`, và dùng `/` thay cho `\`. Phần lọc dòng log có thể dùng `grep "^experiment_id\|^baseline_" experiment_log.csv`.
- **Thêm vào `.gitignore`** nếu không muốn đưa snapshot nặng lên Git: `Experimental Log/**/*oof_predictions.csv`

# Hướng dẫn lưu nhật ký thí nghiệm (Experimental Log)

Thư mục `Experimental Log/` lưu lại **ảnh chụp (snapshot)** của từng notebook sau mỗi lần chạy: bản notebook, các file output và các dòng tương ứng trong `experiment_log.csv`. Mục đích là để xem lại và so sánh kết quả giữa các lần chạy mà không bị ghi đè.

Mỗi model/notebook có một thư mục riêng; bên trong là các bản lưu theo ngày chạy.

Quy ước đặt tên: `<tên_model>/<tên_model>_dd_MM_yy/`.

## 2. Quy trình

1. Chạy notebook (`Restart & Run All`) cho đến khi xong.
2. Mở terminal **tại thư mục gốc của repo** (PowerShell).
3. Chạy khối lệnh tương ứng ở mục 3.
4. Kiểm tra bằng `tree "Experimental Log" /F`.

## 3. Lệnh theo từng notebook

Mỗi khối gồm 5 bước: tạo thư mục, chép notebook, chép output, chép hình, trích dòng log.

### 02: Baseline

```powershell
$d = "Experimental Log\1. aseline\v1"
mkdir "$d\outputs\figures"
copy notebooks\02_model_training_baseline.ipynb $d
copy outputs\baseline_* "$d\outputs"
copy outputs\figures\baseline_* "$d\outputs\figures"
Import-Csv experiment_log.csv | ? experiment_id -like "baseline_*" | Export-Csv "$d\experiment_log_rows.csv" -NoTypeInformation -Encoding UTF8
```

## 4. Lưu ý

- **Chạy lại trong cùng một ngày** sẽ ghi đè thư mục cùng tên. Muốn giữ cả hai bản, thêm hậu tố giờ vào tên thư mục, ví dụ đổi `dd_MM_yy` thành `dd_MM_yy_HHmm`.
- **Notebook 03 và 04** dùng tên file cụ thể (`random_forest_cv_*`, `gradient_boosting_cv_*`) để không chép nhầm file `_tuned`. Không dùng mẫu rộng `random_forest_*` cho `outputs\`.
- **File OOF** (`*_validation_oof_predictions.csv`) nặng khoảng 28 MB mỗi file. Nếu không cần lưu lại, bỏ khỏi lệnh `copy` ở bước output.
- **File `.joblib`** không được lưu trong snapshot (nặng, nhất là `random_forest_tuned.joblib` khoảng 20 MB). Tham số và cấu hình đã có trong `models/*_metadata.json` và cột `notes` của `experiment_log.csv`.
- **Dòng log** được lọc theo `experiment_id`: `baseline_*`, `random_forest_cv5`, `gradient_boosting_cv5`, `*tuned*`. Nếu thêm thí nghiệm mới, đặt `experiment_id` theo quy ước `<tên_thí_nghiệm>_cv5` / `_test` như trong README gốc để lọc được.
- **Đã lỡ tạo thư mục sai chỗ** (ví dụ `Experimental Log\baseline_18_11_26`), di chuyển bằng:

  ```powershell
  mkdir "Experimental Log\baseline"
  move "Experimental Log\baseline_18_11_26" "Experimental Log\baseline"
  ```
- **Dùng macOS/Linux**: thay `mkdir` bằng `mkdir -p`, `copy` bằng `cp`, và dùng `/` thay cho `\`. Phần lọc dòng log có thể dùng `grep "^experiment_id\|^baseline_" experiment_log.csv`.
- **Thêm vào `.gitignore`** nếu không muốn đưa snapshot nặng lên Git: `Experimental Log/**/*oof_predictions.csv`.
