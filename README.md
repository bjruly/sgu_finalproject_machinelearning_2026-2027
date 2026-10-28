# sgu_finalproject_machinelearning_2026-2027
Machine Learning Final Project: Predicting $\text{PM}_{2.5}$ and Air Quality using Beijing Multi-Site Air Quality Dataset (Regression models: Linear Regression, Random Forest, XGBoost, MLP).


# 🌍 Machine Learning Final Project: Beijing Multi-Site Air Quality Prediction

> Đồ án cuối kỳ môn Máy học (Machine Learning) - Xây dựng hệ thống học máy dự đoán nồng độ $\text{PM}_{2.5}$ và đánh giá chất lượng không khí dựa trên tập dữ liệu *Beijing Multi-Site Air Quality* (UCI Machine Learning Repository).

---

## 📌 Giới thiệu đồ án

Chất lượng không khí và nồng độ bụi mịn $\text{PM}_{2.5}$ là một trong những yếu tố ảnh hưởng trực tiếp và nghiêm trọng nhất đến sức khỏe cộng đồng, đặc biệt tại các đô thị lớn. 

Đồ án này tập trung nghiên cứu và xây dựng pipeline học máy (Machine Learning Pipeline) hoàn chỉnh nhằm giải quyết bài toán hồi quy (Regression) dự đoán chỉ số $\text{PM}_{2.5}$ dựa trên dữ liệu chuỗi thời gian khí tượng (nhiệt độ, áp suất, độ ẩm, hướng/tốc độ gió) và các chất ô nhiễm đi kèm.

### 🎯 Mục tiêu chính:
1. **Phân tích & Tiền xử lý dữ liệu (EDA):** Khám phá các mối liên hệ giữa điều kiện thời tiết, chất ô nhiễm và nồng độ $\text{PM}_{2.5}$ xử lý dữ liệu thiếu và trích xuất đặc trưng thời gian.
2. **Xây dựng mô hình dự đoán:** Thử nghiệm mô hình Baseline (Linear/Ridge Regression) cùng các thuật toán học máy phù hợp (Random Forest, XGBoost, MLP).
3. **Đánh giá & Tinh chỉnh:** Đánh giá hiệu năng bằng các độ đo MAE, RMSE, $R^2$; tinh chỉnh siêu tham số để tối ưu hóa khả năng dự đoán và kiểm soát hiện tượng overfitting.

---

## 👥 Danh sách thành viên tham gia
Giảng viên hướng dẫn: TS.Đỗ Như Tài
| STT | Họ và tên | Mã số sinh viên (MSSV) | Vai trò / Phân công nhiệm vụ | Tỷ lệ đóng góp (%) |
| :-: | :--- | :-: | :--- | :-: |
| 1 | Trần Lê Gia Bảo | 3124411038 | Nhóm trưởng| 20% |
| 2 | Tô Thành Nhân  | 3124411198 | Thành viên| 20% |
| 3 | Đào Hữu Tài | 3124411261 | Thành viên | 20% |
| 4 | Huỳnh Nhật Quang | 3124411245 | Thành viên  | 20% |
| 5 | Nguyễn Thanh Tuấn | 3124411337 | Thành viên | 20% |

## 🏗️ Cấu trúc thư mục đồ án (Dự kiến)

```text
air-quality-ml-project/
│
├── 📂 data/                         # [Dự kiến] Dữ liệu thô và dữ liệu sau tiền xử lý
├── 📂 notebooks/                    # [Dự kiến] Jupyter Notebooks phục vụ EDA và thử nghiệm
├── 📂 src/                          # [Dự kiến] Mã nguồn chính (Data Pipeline, Features, Models)
├── 📂 tests/                        # 🎯 [TRỌNG TÂM KIỂM THỬ] Unit tests & Integration tests
│   ├── test_data_pipeline.py        # Test làm sạch dữ liệu và kiểm tra rò rỉ dữ liệu
│   ├── test_feature_engineering.py # Test tính chính xác của các bước biến đổi đặc trưng
│   ├── test_models_performance.py  # Test ngưỡng chất lượng mô hình (MAE/RMSE/R2)
│   └── test_integration.py          # Test tích hợp luồng xử lý end-to-end
├── 📂 models/                       # [Dự kiến] File lưu trữ mô hình (.pkl, .joblib)
├── 📂 outputs/                      # [Dự kiến] Biểu đồ trực quan và báo cáo kết quả kiểm thử
├── 📂 docs/                         # [Dự kiến] Tài liệu proposal, báo cáo và slide trình bày
├── 📄 experiment_log.csv            # Nhật ký thực nghiệm và theo dõi độ đo
├── 📄 pytest.ini                    # File cấu hình kiểm thử (Pytest Framework)
├── 📄 requirements.txt              # Danh sách thư viện cần thiết
└── 📄 README.md                     # Tài liệu hướng dẫn đồ án
## 📁 Tài liệu theo thư mục

README trong từng thư mục mô tả mục đích và các tệp hiện có:

- [data/README.md](data/README.md), [data/raw/README.md](data/raw/README.md), [data/processed/README.md](data/processed/README.md)
- [notebooks/README.md](notebooks/README.md)
- [src/README.md](src/README.md)
- [tests/README.md](tests/README.md)
- [models/README.md](models/README.md)
- [outputs/README.md](outputs/README.md), [outputs/figures/README.md](outputs/figures/README.md), [outputs/test_reports/README.md](outputs/test_reports/README.md)
- [docs/README.md](docs/README.md)
