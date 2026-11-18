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
$d = "Experimental Log\baseline\v1"
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
