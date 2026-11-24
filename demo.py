from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st

from src.artifacts import resolve_model_paths
from src.data_loader import load_data, time_split
from src.evaluation import predict_test, summarize_predictions
from src.features import add_features

st.set_page_config(page_title="Dự báo PM2.5", layout="wide")
st.title("Dự báo PM2.5 trước một giờ tại Bắc Kinh")
st.caption("Nhóm 10 · So sánh 5 mô hình trên cùng tập kiểm tra")

# Đầu vào: nhận CSV chuẩn hóa do người dùng chọn.
uploaded_file = st.file_uploader("Chọn tệp dữ liệu quan trắc đã chuẩn hóa", type=["csv"])

if st.button("Chạy dự báo", disabled=uploaded_file is None):
    try:
        with st.spinner("Đang đọc dữ liệu và chạy 5 mô hình..."):
            with TemporaryDirectory() as temp_dir:
                csv_path = Path(temp_dir) / "input.csv"
                csv_path.write_bytes(uploaded_file.getbuffer())
                data = load_data(csv_path)

            featured = add_features(data)
            labeled = featured.dropna(subset=["target"])
            train_validation, test = time_split(labeled)

            if test.empty:
                raise ValueError("CSV cần có dữ liệu test từ ngày 01/09/2016.")

            model_paths = resolve_model_paths()
            predictions = predict_test(test, train_validation, model_paths)
            scores = summarize_predictions(predictions)
    except (OSError, ValueError, RuntimeError) as error:
        st.error(str(error))
        st.stop()

    # Đầu ra: hiện bảng điểm và biểu đồ trên trang web.
    st.success(f"Đã đánh giá {len(predictions):,} mẫu test.")
    st.subheader("Kết quả trên tập kiểm tra")
    st.dataframe(
        scores[["rank", "model", "mae", "rmse", "r2"]].round(4),
        hide_index=True,
    )

    station = predictions["station"].iloc[0]
    example = (
        predictions.loc[predictions["station"].eq(station)]
        .sort_values("target_datetime")
        .head(72)
        .set_index("target_datetime")[["y_true", "pred_random_forest_tuned"]]
        .rename(columns={
            "y_true": "PM2.5 thực tế",
            "pred_random_forest_tuned": "Random Forest tinh chỉnh",
        })
    )
    st.subheader(f"Thực tế và dự báo tại trạm {station}")
    st.caption("72 mẫu test đầu tiên của trạm · PM2.5 tính bằng µg/m³")
    st.line_chart(example)