# Thư mục `data/raw`

Nơi lưu dữ liệu gốc tải về. Giữ nguyên các tệp này để có thể truy vết và chạy lại các bước xử lý; dữ liệu sau xử lý được lưu trong [`../processed/`](../processed/README.md).

## Bộ Beijing Multi-Site Air Quality

Thư mục [`PRSA_Data_20130301-20170228/`](PRSA_Data_20130301-20170228/) chứa 12 tệp CSV, mỗi tệp tương ứng một trạm quan trắc:

- `PRSA_Data_Aotizhongxin_20130301-20170228.csv`
- `PRSA_Data_Changping_20130301-20170228.csv`
- `PRSA_Data_Dingling_20130301-20170228.csv`
- `PRSA_Data_Dongsi_20130301-20170228.csv`
- `PRSA_Data_Guanyuan_20130301-20170228.csv`
- `PRSA_Data_Gucheng_20130301-20170228.csv`
- `PRSA_Data_Huairou_20130301-20170228.csv`
- `PRSA_Data_Nongzhanguan_20130301-20170228.csv`
- `PRSA_Data_Shunyi_20130301-20170228.csv`
- `PRSA_Data_Tiantan_20130301-20170228.csv`
- `PRSA_Data_Wanliu_20130301-20170228.csv`
- `PRSA_Data_Wanshouxigong_20130301-20170228.csv`

Mỗi CSV có 35.064 bản ghi theo giờ từ 01/03/2013 đến 28/02/2017 và 18 cột: số thứ tự, năm/tháng/ngày/giờ, PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, hướng gió (`wd`), tốc độ gió (`WSPM`) và tên trạm. Các giá trị khuyết được biểu diễn bằng `NA`; cần chuyển chúng thành giá trị khuyết phù hợp và xử lý trong pipeline.

## Tệp khác ở cấp thư mục

- `data.csv`: CSV có các cột `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`; vai trò trong đồ án chưa được xác định.
- `test.csv`: CSV có cùng cấu trúc OHLCV như `data.csv`; vai trò trong đồ án chưa được xác định.
- `2A2478DC-8517-4490-9FA7-36F9A7A542BE.JPG`: tệp ảnh; mục đích sử dụng chưa được xác định.
- `.gitkeep`: tệp rỗng để Git lưu thư mục.

Chưa suy diễn các tệp bổ sung này là đầu vào của mô hình PM2.5. Không chỉnh sửa hoặc xóa dữ liệu gốc khi chưa xác nhận mục đích.
