# Phân tích bổ sung của mô hình cuối

Tái lập bằng .venv/Scripts/python.exe -m src.evaluation hoặc notebook 08. Các mô hình đã được chọn bằng CV; phân tích này không chọn lại cấu hình theo test.

- final_test_predictions.csv: 51.063 khóa trạm–thời điểm nhãn, giá trị thật và dự đoán năm mô hình.
- final_test_metrics_reproduced.csv: điểm được đối chiếu với bảng test gốc.
- final_test_error_by_*.csv: lỗi theo trạm, tháng, mùa và mức PM2.5. Số mẫu cộng lại bằng 51.063 cho mỗi mô hình ở từng cách nhóm.
- final_test_worst_cases.csv: 100 mẫu sai số tuyệt đối lớn nhất của từng mô hình.
- paired_model_uncertainty.csv: chênh lệch RMSE model_a - model_b và khoảng percentile 95%, bootstrap ghép cặp 2.000 lần với khối 7 ngày, giữ tất cả trạm cùng thời điểm trong cùng khối.
- figures/: biểu đồ tổng thể, nhóm lỗi, residual và chuỗi thời gian quanh mẫu RF sai số lớn nhất.
- evaluation_manifest.json: môi trường, dữ liệu/mã nguồn/model và hash artifact tại thời điểm chạy.

Residual = y_true - y_pred. Nhóm PM2.5 đóng bên phải: <=35, (35,75], (75,115], (115,150], (150,250], >250. Không trộn trực tiếp với bảng dùng quy tắc biên khác.

RF có RMSE tổng thể thấp nhất. Trong nhóm PM2.5 >250, GB và MLP có RMSE cao hơn Persistence; cần phản ánh hạn chế này trong báo cáo.

Khoảng chênh lệch RMSE của RF so với LR là [-1,1251; -0,5930] µg/m³. Khoảng so với GB là [-0,7799; 0,1339], so với MLP là [-1,3431; 0,2557], đều còn chứa 0 ở hai cặp sau. Đây là kết quả có điều kiện trên dự đoán cố định, block length đã chọn, test thu–đông và các trạm đã quan sát; không chứng minh hiệu năng cho mọi mùa hoặc trạm mới.
