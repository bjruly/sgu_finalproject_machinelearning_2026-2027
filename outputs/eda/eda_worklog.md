# Nhật ký EDA và chuẩn hóa dữ liệu

## Mục đích của nhật ký

Tài liệu này ghi lại bằng ngôn ngữ thông thường nhóm đang làm gì, vì sao làm, đã quan sát được điều gì và quyết định nào còn để mở. Có thể đọc nhật ký mà không cần lần theo code trong notebook.

EDA là khám phá dữ liệu, không đồng nghĩa với việc mọi giá trị đã được làm sạch. Bản CSV được tạo trong bước này chỉ chuẩn hóa cấu trúc để nhóm dùng lại; missing và các giá trị đáng ngờ vẫn được giữ nguyên cho tới khi có quy tắc xử lý được thống nhất.

## Phạm vi dữ liệu

Phân tích dùng 12 tệp CSV trong `data/raw/PRSA_Data_20130301-20170228/`, mỗi tệp tương ứng một trạm. Các tệp `data.csv`, `test.csv` có cấu trúc OHLCV và ảnh JPG nằm ở cấp `data/raw/` không được đưa vào phân tích PM2.5 vì chúng không thuộc schema PRSA của 12 trạm.

Mỗi CSV PRSA có 35.064 dòng giờ, từ 01/03/2013 00:00 đến 28/02/2017 23:00. Sau khi gộp, dữ liệu có 420.768 dòng, 12 trạm và 18 cột gốc. Cột thời gian ghép `year`, `month`, `day`, `hour` thành `datetime`.

## Việc đã thực hiện

1. Đọc 12 CSV PRSA, chuyển marker `NA` thành giá trị missing trong bộ nhớ và gộp các trạm.
2. Tạo `datetime`, sắp xếp bản ghi theo trạm và thời gian.
3. Kiểm tra schema, kiểu dữ liệu, số dòng, khoảng thời gian, timestamp trùng và giờ bị thiếu.
4. Thống kê missing tổng thể và theo trạm; không điền giá trị nào.
5. Khảo sát phân bố PM2.5, xu hướng theo tháng/giờ/mùa, và tương quan giữa các biến số.
6. Kiểm tra ngữ cảnh thời gian và các trạm lân cận cho một số giá trị PM2.5 rất cao.
7. Ghi một bản CSV chuẩn hóa vào `data/processed/`; không sửa các tệp gốc.

Notebook thực hiện các bước EDA là [`../../notebooks/01_eda_and_preprocessing.ipynb`](../../notebooks/01_eda_and_preprocessing.ipynb). Bảng tóm tắt có cấu trúc ở [`eda_conclusions.csv`](eda_conclusions.csv).

## Kết quả kiểm tra cấu trúc và thời gian

- Đã đọc đủ 12/12 tệp và tìm thấy 12 trạm.
- Mỗi trạm có đúng 35.064 dòng và 35.064 timestamp duy nhất.
- Mỗi trạm bao phủ đầy đủ khoảng 01/03/2013 00:00 đến 28/02/2017 23:00; kiểm tra không phát hiện giờ bị thiếu trong lịch kỳ vọng.
- Không có bản ghi trùng khóa `(station, datetime)`.
- Không có timestamp nào bị lỗi khi chuyển thành datetime.

Điều này cho thấy chuỗi thời gian có cấu trúc giờ đầy đủ ở cấp timestamp. Nó **không** có nghĩa là các phép đo PM2.5 hay biến đầu vào đều đầy đủ; missing của phép đo được kiểm tra riêng bên dưới.

## Missing: lượng thiếu và ý nghĩa

Tổng cộng có 74.027 ô missing trên các giá trị đo. Các cột thiếu nhiều nhất:

| Cột | Số ô thiếu | Tỷ lệ xấp xỉ |
|---|---:|---:|
| CO | 20.701 | 4,920% |
| O3 | 13.277 | 3,155% |
| NO2 | 12.116 | 2,879% |
| SO2 | 9.021 | 2,144% |
| PM2.5 | 8.739 | 2,077% |
| PM10 | 6.449 | 1,533% |
| wd (hướng gió) | 1.822 | 0,433% |
| DEWP | 403 | 0,096% |
| TEMP | 398 | 0,095% |
| PRES | 393 | 0,093% |
| RAIN | 390 | 0,093% |
| WSPM | 318 | 0,076% |

Tỷ lệ PM2.5 missing không giống nhau giữa các trạm: thấp nhất khoảng 1,089% ở Wanliu và cao nhất khoảng 2,718% ở Huairou. Vì target bị thiếu thì không biết giá trị thật để chấm điểm, proposal yêu cầu không tự điền target; các dòng mà target dự đoán bị thiếu sẽ không được dùng làm nhãn huấn luyện/đánh giá.

Missing không phải lúc nào cũng là vài ô rải rác. Một số khoảng thiếu liên tục đáng chú ý:

- PM2.5 tại Aotizhongxin: 343 bản ghi giờ liên tiếp, từ 17/12/2014 10:00 đến 31/12/2014 16:00.
- PM2.5 tại Huairou: 208 giờ liên tiếp, từ 06/05/2013 20:00 đến 15/05/2013 11:00.
- PM2.5 tại Shunyi: 197 giờ liên tiếp, từ 09/07/2013 15:00 đến 17/07/2013 19:00.
- CO tại Dongsi: 1.517 giờ liên tiếp, từ 11/06/2013 12:00 đến 13/08/2013 16:00.
- NO2 tại Dongsi: 900 giờ liên tiếp, từ 19/01/2014 09:00 đến 25/02/2014 20:00.
- O3 tại Shunyi: 497 giờ liên tiếp, từ 05/09/2016 17:00 đến 26/09/2016 09:00.

Các khoảng kéo dài nhiều ngày có thể không phù hợp để forward-fill toàn bộ một cách mù quáng. Bước modeling cần áp dụng giới hạn forward-fill theo trạm như proposal, sau đó xử lý phần còn thiếu bằng thống kê chỉ fit từ train và có cờ báo missing. Cần đo lại mức missing sau giới hạn fill để biết feature nào vẫn thiếu nhiều. Imputer không được fit trên validation/test.

## Giá trị PM2.5 cao: điều đã kiểm tra và điều chưa kết luận

Trong dữ liệu có 953 quan sát PM2.5 từ 500 µg/m³ trở lên. Giá trị lớn nhất là 999 tại Wanshouxigong lúc 08/02/2016 02:00.

### Đợt 08/02/2016

Giá trị 999 không đứng một mình trong cùng thời điểm: 10/12 trạm ghi PM2.5 từ 500 trở lên lúc 02:00. Wanliu ghi 957; Shunyi 941; Aotizhongxin 898; Changping 882; các trạm còn lại phân bố thấp hơn. Ở Wanshouxigong, PM2.5 là 826 lúc 01:00, 999 lúc 02:00, 857 lúc 03:00 và 748 lúc 04:00.

Sự đồng thời giữa nhiều trạm và các số đo lân cận đều cao là bằng chứng ủng hộ khả năng đây là một đợt ô nhiễm rộng, chứ không chỉ một lỗi đơn lẻ. Tuy vậy, dữ liệu này chưa đủ để chứng minh 999 chắc chắn hợp lệ hoặc chắc chắn không phải giới hạn/mã bão hòa của thiết bị.

**Quyết định hiện tại:** giữ giá trị 999 và các điểm cao khác trong CSV chuẩn hóa; không cắt ngưỡng, winsorize hay đổi thành missing. Đánh dấu 999 để nhóm xác minh với tài liệu UCI/nguồn thiết bị trước khi quyết định cho bước modeling.

### Điểm cần xem lại: Nongzhanguan ngày 05/05/2013

Nongzhanguan có PM2.5 bằng 844 lúc 12:00. Cùng trạm ghi 194 lúc 11:00 và 216 lúc 13:00; cùng thời điểm 12:00, giá trị cao nhất trong 11 trạm còn lại là 258. Đây là một đỉnh đơn lẻ khác biệt rõ hơn so với đợt tháng 02/2016.

**Quyết định hiện tại:** giữ nguyên 844 nhưng xem đây là điểm cần xác minh, không tự kết luận là lỗi. Trước khi loại hoặc sửa, nên xem thêm các biến PM10, CO, SO2, NO2, O3 cùng giờ, các dòng gốc và nguồn dữ liệu. Có thể so sánh kết quả mô hình có/không có điểm này như một phân tích độ nhạy nếu nhóm xác nhận cần thiết.

Không có PM2.5 âm trong tập dữ liệu. PM2.5 trung bình là 79,79; trung vị 55; phân vị 95% là 242 và phân vị 99% là 370 µg/m³. Phân bố có đuôi giá trị cao, nên MAE/RMSE và sai số ở nhóm nồng độ cao cần được báo cáo riêng theo proposal.

## Xu hướng mùa và tương quan

Theo cách chia mùa bằng tháng (xuân 3–5, hè 6–8, thu 9–11, đông 12–2), PM2.5 trung bình toàn bộ các trạm là:

| Mùa | PM2.5 trung bình |
|---|---:|
| Đông | 95,48 µg/m³ |
| Thu | 82,33 µg/m³ |
| Xuân | 76,97 µg/m³ |
| Hè | 64,67 µg/m³ |

Tương quan Pearson với PM2.5 cao nhất trong các cột số đã khảo sát là PM10 (0,884), CO (0,790) và NO2 (0,667). Đây là tương quan trên các cặp số đo sẵn có, không chứng minh quan hệ nhân quả; missing có thể làm số lượng quan sát dùng cho từng cặp khác nhau.

## Tệp CSV đã tạo là gì?

Tệp [`beijing_air_quality_standardized.csv`](../../data/processed/beijing_air_quality_standardized.csv) là **bản gộp và chuẩn hóa cấu trúc**, không phải bản đã làm sạch hoàn toàn để đưa thẳng vào model:

- Gộp 12 tệp và giữ đủ 420.768 dòng.
- Giữ nguyên 18 cột dữ liệu nguồn; thêm cột `datetime` đã parse, tổng cộng 19 cột.
- Sắp xếp theo `station`, sau đó `datetime`; khóa `(station, datetime)` vẫn duy nhất.
- Giữ nguyên tất cả 74.027 giá trị missing (được ghi dưới dạng ô trống trong CSV và đọc lại thành missing).
- Giữ nguyên 953 giá trị PM2.5 từ 500 trở lên và giá trị 999.
- Giữ cột `No` để truy vết thứ tự dòng nguồn; proposal cho biết không dùng `No` làm feature modeling.
- Không thêm cột EDA như `season`, không thêm cột nguồn phụ thuộc đường dẫn máy.

Tệp này có thể được mở bằng Excel, pandas hoặc công cụ bảng dữ liệu để đọc và kiểm tra. Không chỉnh sửa thủ công các giá trị trong đó; nếu phát hiện quy tắc làm sạch mới, hãy cập nhật notebook và tái tạo CSV từ dữ liệu gốc.

## Việc chưa làm và bước tiếp theo

1. Xác minh điểm 999 với tài liệu nguồn và điểm Nongzhanguan 844 với các biến đo lân cận. Tạm thời cả hai vẫn được giữ.
2. Quyết định chính thức cách xử lý các khoảng missing dài; không forward-fill xuyên qua mọi khoảng dài.
3. Tạo pipeline chia dữ liệu theo thời gian trước khi fit imputer, encoder hoặc scaler. Theo proposal, train/validation dự kiến đến 08/2016, test từ 09/2016 đến 02/2017; validation expanding-window 5 fold. Khi chia dữ liệu nhiều trạm, cùng một timestamp phải nằm trong cùng fold.
4. Tạo target PM2.5 ở giờ t+1 trong từng trạm; mọi lag/rolling chỉ dùng dữ liệu quá khứ và tính riêng theo trạm.
5. Sau các quyết định trên, mới tạo bản model-ready trong pipeline và chạy baseline persistence/Linear Regression. CSV chuẩn hóa hiện tại không thay thế bước đó.

## Nguyên tắc giữ an toàn cho dữ liệu

- Không sửa `data/raw/`.
- Không bỏ missing hoặc điểm cao khi chưa có quy tắc được ghi nhận.
- Không tính median, scaler hoặc encoder trên toàn bộ dữ liệu trước khi chia thời gian.
- Ghi lại lý do và ảnh hưởng nếu nhóm sau này quyết định loại hoặc chuyển đổi bất kỳ quan sát nào.
