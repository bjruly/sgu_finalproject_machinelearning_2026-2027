# Chẩn đoán validation của cấu hình đã chốt

Tái lập bằng .venv/Scripts/python.exe -m src.validation_diagnostics. Không thay các joblib cuối.

## Random Forest

rf_group_permutation_importance.csv/png dùng cấu hình RF tuned, fit lại chỉ trên train fold 5. Lấy 30.000 mẫu validation fold 5, seed 42, lặp hoán vị 5 lần. Mỗi nhóm dùng cùng một hoán vị cho các cột trong nhóm.

RMSE gốc trên mẫu là 17,5518 µg/m³. Mức tăng RMSE: PM2.5 hiện tại 51,8617; chất ô nhiễm khác 5,9398; lag/rolling 2,0905; khí tượng 1,4415; thời gian 0,0800; trạm 0,0030. Đây là mức phụ thuộc của mô hình trong phép thử, không phải tác động nhân quả. Các feature tương quan có thể chia sẻ thông tin.

## MLP

- mlp_validation_diagnostics.csv: điểm từng fold và trạng thái hội tụ.
- mlp_seed_summary.csv: trung bình số học metric của 5 folds theo seed; không phải pooled OOF.
- mlp_loss_curves.csv và mlp_convergence.png: loss trong huấn luyện với target đã chuẩn hóa, không đo trực tiếp bằng µg/m³.
- diagnostics_manifest.json: phạm vi, seed và mốc train/validation.

RMSE CV trung bình theo seed: 7 = 19,5268; 42 = 19,6317; 2026 = 19,2951 µg/m³. Các lần này chỉ là kiểm tra độ biến động; không chọn lại seed từ test.

Khi tăng giới hạn từ 40 lên 100 epoch ở seed 42, fold 1 dừng ở 75 epoch, RMSE 26,9824; fold 2 dừng ở 47 epoch, RMSE 16,2132. Hai điểm này đều cao hơn cấu hình 40 epoch tương ứng (26,1727 và 15,9833). Hết cảnh báo hội tụ không tự động làm validation tốt hơn. Bộ mô hình cuối vẫn giữ cấu hình gốc.
