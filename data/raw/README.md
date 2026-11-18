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

Notebook 01 tìm các tệp `PRSA_Data_*_20130301-20170228.csv` trong thư mục 12 trạm. Nếu bản đồ án còn `data.csv` và `test.csv` ở cấp `data/raw/`, hai tệp đó là dữ liệu OHLCV và nằm ngoài quy trình dự báo PM2.5.
