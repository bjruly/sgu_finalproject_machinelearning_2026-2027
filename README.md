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

#Cấu trúc thư mục dự kiến
air-quality-ml-project/
│
├── 📂 data/                         # [Dự kiến] Dữ liệu đồ án
│   ├── raw/                         # Dữ liệu thô tải từ UCI (Beijing Multi-Site Air Quality)
│   └── processed/                   # Dữ liệu sau khi làm sạch và trích xuất đặc trưng
│
├── 📂 notebooks/                    # [Dự kiến] Jupyter Notebooks cho EDA và thử nghiệm nhanh
│   ├── 01_eda_and_preprocessing.ipynb
│   ├── 02_model_training_baseline.ipynb
│   └── 03_advanced_models_and_tuning.ipynb
│
├── 📂 src/                          # [Dự kiến] Mã nguồn chính (Source code modules)
│   ├── __init__.py
│   ├── data_loader.py               # Module đọc và làm sạch dữ liệu
│   ├── features.py                  # Module trích xuất đặc trưng (Time features, scaling)
│   ├── models.py                    # Định nghĩa và huấn luyện các mô hình (Regression, MLP, XGBoost)
│   └── evaluate.py                  # Hàm tính toán metrics (MAE, RMSE, R2)
│
├── 📂 tests/                        # 
│   ├── __init__.py
│   ├── test_data_pipeline.py        # Kiểm thử dữ liệu: kiểm tra missing value, data types, data leakage
│   ├── test_feature_engineering.py # Kiểm thử biến đổi đặc trưng và scaling
│   ├── test_models_performance.py  # Kiểm thử ngưỡng hiệu năng của mô hình (Regression sanity check)
│   └── test_integration.py          # Kiểm thử tích hợp toàn bộ pipeline từ Data -> Output
│
├── 📂 models/                       # [Dự kiến] Lưu trữ mô hình đã huấn luyện (.pkl, .joblib, .pt)
├── 📂 outputs/                      # [Dự kiến] Biểu đồ EDA, kết quả test và báo cáo so sánh
│   ├── figures/                     # Hình ảnh trực quan hóa, ma trận biểu đồ
│   └── test_reports/                # Báo cáo chi tiết kết quả kiểm thử mô hình
│
├── 📂 docs/                         # [Dự kiến] Tài liệu đồ án (Proposal, Báo cáo tiến độ, Slide)
│
├── 📄 experiment_log.csv            # Nhật ký ghi nhận thực nghiệm (Models, Hyperparameters, Metrics)
├── 📄 requirements.txt              # Danh sách thư viện Python phụ thuộc
├── 📄 pytest.ini                    # File cấu hình framework kiểm thử Pytest
└── 📄 README.md                     # Tài liệu hướng dẫn sử dụng đồ án

## 📁 Tài liệu theo thư mục

README trong từng thư mục mô tả mục đích và các tệp hiện có:

- [data/README.md](data/README.md), [data/raw/README.md](data/raw/README.md), [data/processed/README.md](data/processed/README.md)
- [notebooks/README.md](notebooks/README.md)
- [src/README.md](src/README.md)
- [tests/README.md](tests/README.md)
- [models/README.md](models/README.md)
- [outputs/README.md](outputs/README.md), [outputs/figures/README.md](outputs/figures/README.md), [outputs/test_reports/README.md](outputs/test_reports/README.md)
- [docs/README.md](docs/README.md)
