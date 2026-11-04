"""Vòng rút gọn thứ hai, đưa báo cáo về khoảng 50-55 trang.

Vòng này nén các đoạn mô tả cài đặt kỹ thuật và diễn giải lý thuyết còn dài,
giữ nguyên toàn bộ số liệu thực nghiệm, bảng biểu và hình.
"""

from __future__ import annotations

from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

CHAPTER_ONE_BLOCKS: list[tuple[str, str]] = [
    (
        """Công nghệ tri thức phân biệt ba khái niệm theo mức độ trừu tượng tăng dần. **Dữ liệu** là các ký hiệu, con số thô chưa diễn giải, ví dụ "Toyota Vios, 2019, 95.000 km, 365 triệu đồng". **Thông tin** là dữ liệu đã được tổ chức và đặt trong ngữ cảnh: "giá rao phổ biến của Vios 1.5G đời 2019 tại Hà Nội nằm trong khoảng 340–390 triệu đồng". **Tri thức** là hiểu biết rút ra từ thông tin và kinh nghiệm, cho phép giải thích, dự đoán và ra quyết định: "xe Toyota thường giữ giá tốt hơn mặt bằng chung", "xe từng ngập nước mất giá rất mạnh và tiềm ẩn rủi ro hệ thống điện".

Quan hệ giữa ba khái niệm được mô tả bằng tháp DIKW: càng lên cao khối lượng càng giảm nhưng giá trị cho việc ra quyết định càng tăng. Các hệ thống thông minh dựa trên tri thức hướng tới nắm bắt tầng tri thức và vận dụng nó một cách tự động, nhất quán.""",
        """Công nghệ tri thức phân biệt ba khái niệm theo mức độ trừu tượng tăng dần. **Dữ liệu** là ký hiệu, con số thô chưa diễn giải, ví dụ "Toyota Vios, 2019, 95.000 km, 365 triệu đồng". **Thông tin** là dữ liệu đã được tổ chức và đặt trong ngữ cảnh: "giá rao phổ biến của Vios 1.5G đời 2019 tại Hà Nội là 340–390 triệu đồng". **Tri thức** là hiểu biết rút ra từ thông tin và kinh nghiệm, cho phép giải thích, dự đoán và ra quyết định: "xe Toyota thường giữ giá tốt hơn mặt bằng chung".

Quan hệ giữa ba khái niệm được mô tả bằng tháp DIKW: càng lên cao khối lượng càng giảm nhưng giá trị cho việc ra quyết định càng tăng. Các hệ thống thông minh dựa trên tri thức hướng tới nắm bắt tầng tri thức và vận dụng nó tự động, nhất quán.""",
    ),
    (
        """Một hệ chuyên gia hoàn chỉnh gồm bảy thành phần tương tác với nhau như Hình 1.1. **Cơ sở tri thức** chứa tri thức lâu dài của lĩnh vực. **Bộ nhớ làm việc** lưu các sự kiện của phiên làm việc hiện tại, ví dụ thông tin chiếc xe đang định giá và các kết luận trung gian. **Máy suy diễn** so khớp luật với sự kiện rồi chọn và thực thi luật. **Lịch công tác** là danh sách các luật đã thỏa điều kiện đang chờ thực thi, sắp theo độ ưu tiên. **Bộ phận giải thích** trả lời câu hỏi "Tại sao?" và "Như thế nào?" dựa trên vết suy diễn. **Bộ phận thu nhận tri thức** giúp kỹ sư tri thức bổ sung và kiểm tra tri thức. **Giao diện người dùng** tiếp nhận yêu cầu và hiển thị kết quả.""",
        """Một hệ chuyên gia hoàn chỉnh gồm bảy thành phần tương tác với nhau như Hình 1.1: **cơ sở tri thức** chứa tri thức lâu dài của lĩnh vực; **bộ nhớ làm việc** lưu sự kiện của phiên hiện tại; **máy suy diễn** so khớp luật với sự kiện rồi chọn và thực thi luật; **lịch công tác** là danh sách luật đã thỏa điều kiện đang chờ thực thi, sắp theo độ ưu tiên; **bộ phận giải thích** trả lời câu hỏi "Tại sao?" dựa trên vết suy diễn; **bộ phận thu nhận tri thức** giúp kỹ sư tri thức bổ sung và kiểm tra tri thức; và **giao diện người dùng**.""",
    ),
    (
        """Ưu điểm của luật sản xuất là tính mô-đun, dễ hiểu, dễ bổ sung và hỗ trợ tự nhiên cho việc giải thích. Hạn chế là khi số luật tăng dễ phát sinh mâu thuẫn và trùng lặp, đòi hỏi cơ chế kiểm tra tính nhất quán cùng chiến lược giải quyết xung đột phù hợp.""",
        """Ưu điểm của luật sản xuất là tính mô-đun, dễ hiểu, dễ bổ sung và hỗ trợ tự nhiên cho việc giải thích; hạn chế là khi số luật tăng dễ phát sinh mâu thuẫn, đòi hỏi cơ chế kiểm tra tính nhất quán.""",
    ),
    (
        """Hệ chuyên gia có bốn đặc trưng cơ bản: chứa tri thức chuyên sâu của một lĩnh vực hẹp; có khả năng suy luận trên tri thức; giải thích được quá trình dẫn tới kết luận; và tách biệt tri thức khỏi cơ chế điều khiển, nhờ đó cập nhật tri thức mà không phải sửa chương trình.

Ưu điểm chính là đưa ra quyết định nhanh và nhất quán, bảo tồn tri thức chuyên gia giảm phụ thuộc vào cá nhân, và minh bạch nên người dùng kiểm chứng được kết quả.

Hạn chế của hệ chuyên gia thuần luật gồm ba điểm: **nút thắt thu nhận tri thức** vì khai thác tri thức từ chuyên gia tốn thời gian và nhiều tri thức ẩn khó diễn đạt thành luật; **tính giòn** khi gặp tình huống ngoài phạm vi các luật đã có; và **khó bảo trì khi số luật lớn**, các hệ số nhanh lỗi thời khi thị trường thay đổi. Chính những hạn chế này là lý do đề tài kết hợp hệ chuyên gia với lập luận dựa trên tình huống và khai phá dữ liệu.""",
        """Hệ chuyên gia có bốn đặc trưng cơ bản: chứa tri thức chuyên sâu của một lĩnh vực hẹp; suy luận được trên tri thức; giải thích được quá trình dẫn tới kết luận; và tách biệt tri thức khỏi cơ chế điều khiển nên cập nhật tri thức mà không phải sửa chương trình. Ưu điểm chính là quyết định nhanh và nhất quán, bảo tồn tri thức chuyên gia, và minh bạch nên người dùng kiểm chứng được kết quả.

Hạn chế của hệ chuyên gia thuần luật gồm ba điểm: **nút thắt thu nhận tri thức** vì nhiều tri thức ẩn khó diễn đạt thành luật; **tính giòn** khi gặp tình huống ngoài phạm vi luật đã có; và **khó bảo trì khi số luật lớn**, các hệ số nhanh lỗi thời khi thị trường thay đổi. Đây chính là lý do đề tài kết hợp hệ chuyên gia với lập luận dựa trên tình huống và khai phá dữ liệu.""",
    ),
    (
        """DSS được ứng dụng rộng rãi trong định giá tài sản: định giá nhà đất dựa trên vị trí và các giao dịch tương tự; định giá tài sản bảo đảm khi ngân hàng cho vay mua xe hoặc khi công ty bảo hiểm bồi thường; giúp salon định giá thu mua nhanh và nhất quán giữa các nhân viên; và cung cấp cơ sở tham khảo cho người mua bán cá nhân khi đàm phán.

Với riêng bài toán định giá xe, KB-DSS mang lại bốn lợi ích: **nhanh và nhất quán** vì cùng đầu vào luôn cho cùng kết quả; **minh bạch** vì mỗi kết quả kèm vết suy diễn và danh sách xe tương tự; **quản trị rủi ro** nhờ tự động cảnh báo dấu hiệu bất thường; và **tích lũy tri thức tổ chức** khi tri thức của người định giá được lưu lại và chia sẻ.""",
        """DSS được ứng dụng rộng rãi trong định giá tài sản: định giá nhà đất theo vị trí và các giao dịch tương tự; định giá tài sản bảo đảm khi ngân hàng cho vay mua xe hoặc công ty bảo hiểm bồi thường; giúp salon định giá thu mua nhất quán giữa các nhân viên; và cung cấp cơ sở tham khảo cho người mua bán cá nhân.

Với bài toán định giá xe, KB-DSS mang lại bốn lợi ích: **nhanh và nhất quán** vì cùng đầu vào luôn cho cùng kết quả; **minh bạch** vì mỗi kết quả kèm vết suy diễn và danh sách xe tương tự; **quản trị rủi ro** nhờ tự động cảnh báo dấu hiệu bất thường; và **tích lũy tri thức tổ chức**.""",
    ),
]

CHAPTER_THREE_BLOCKS: list[tuple[str, str]] = [
    (
        """**Truy hồi (Retrieve).** Độ tương tự toàn cục giữa xe cần định giá và một tình huống là trung bình có trọng số của tám độ tương tự cục bộ, với tổng trọng số bằng 1,0. Bảng 3.7 liệt kê các trọng số.""",
        """**Truy hồi (Retrieve).** Độ tương tự toàn cục là trung bình có trọng số của tám độ tương tự cục bộ, tổng trọng số bằng 1,0 (Bảng 3.7).""",
    ),
    (
        """Dòng xe được gán trọng số cao nhất vì đây là yếu tố quyết định phân khúc giá. Năm sản xuất và số km xếp tiếp theo vì chúng quyết định mức khấu hao. Các thuộc tính còn lại chỉ điều chỉnh biên.

Hai hàm tương tự cục bộ cho thuộc tính số được tính theo công thức `max(0, 1 − |giá trị truy vấn − giá trị tình huống| / ngưỡng)`. Nghĩa là hai xe chênh nhau 3 năm có độ tương tự cục bộ về năm sản xuất là 0,5; chênh từ 6 năm trở lên thì độ tương tự về thuộc tính này bằng 0.

Ngoài ra, hệ thống áp một ràng buộc cứng: **chỉ các tình huống cùng hãng mới được xét**, các tình huống khác hãng bị gán độ tương tự bằng 0. Ràng buộc này tránh việc so sánh một chiếc Toyota với một chiếc BMW cùng phân khúc nhưng khác hẳn về mặt bằng giá.

Hệ thống truy hồi k = 5 tình huống tương tự nhất vượt ngưỡng tương tự tối thiểu 0,55.

**Hiệu chỉnh (Revise).** Mỗi tình huống truy hồi được hiệu chỉnh giá về điều kiện của xe cần định giá theo hai bước: chênh lệch tuổi xe được hiệu chỉnh với hệ số 7% mỗi năm, chênh lệch số km được hiệu chỉnh với hệ số 1,2% cho mỗi 10.000 km và giới hạn biên độ trong khoảng ±15%. Việc giới hạn biên độ tránh hiệu chỉnh quá đà khi hai xe chênh nhau quá nhiều về số km.

**Tái sử dụng (Reuse).** Giá từ CBR là trung bình của các giá đã hiệu chỉnh, có trọng số theo độ tương tự. Tình huống càng giống xe cần định giá thì càng ảnh hưởng mạnh tới kết quả.

Mô-đun cũng tính hệ số biến thiên của các giá đã hiệu chỉnh – tỷ số giữa độ lệch chuẩn và trung bình. Hệ số này đo mức độ phân tán giá của các xe tương tự, được dùng làm đầu vào cho luật R24 và cho công thức tính khoảng giá.""",
        """Dòng xe có trọng số cao nhất vì quyết định phân khúc giá; năm sản xuất và số km xếp tiếp theo vì quyết định mức khấu hao. Hai thuộc tính số này dùng công thức `max(0, 1 − |chênh lệch| / ngưỡng)`, nghĩa là hai xe chênh 3 năm có độ tương tự về năm sản xuất là 0,5, chênh từ 6 năm trở lên thì bằng 0.

Hệ thống còn áp một ràng buộc cứng: **chỉ các tình huống cùng hãng mới được xét**, tránh so sánh một chiếc Toyota với một chiếc BMW cùng phân khúc nhưng khác hẳn mặt bằng giá. Hệ thống truy hồi k = 5 tình huống vượt ngưỡng tương tự tối thiểu 0,55.

**Hiệu chỉnh (Revise).** Mỗi tình huống được hiệu chỉnh giá về điều kiện của xe cần định giá: chênh lệch tuổi xe hiệu chỉnh với hệ số 7% mỗi năm, chênh lệch số km với hệ số 1,2% cho mỗi 10.000 km và giới hạn biên độ ±15% để tránh hiệu chỉnh quá đà.

**Tái sử dụng (Reuse).** Giá từ CBR là trung bình có trọng số theo độ tương tự của các giá đã hiệu chỉnh. Mô-đun cũng tính hệ số biến thiên – tỷ số giữa độ lệch chuẩn và trung bình – để đo mức phân tán giá của các xe tương tự, dùng làm đầu vào cho luật R24 và công thức khoảng giá.""",
    ),
    (
        """Lớp `ValuationService` tại `src/valuation_service.py` điều phối toàn bộ quy trình định giá theo sáu bước:

1. Tra khung tri thức để lấy thông tin phiên bản xe.
2. Chạy mô-đun CBR để truy hồi các tình huống tương tự.
3. Dựng bộ nhớ làm việc gồm 18 sự kiện, trong đó có kết quả của bước 2 (số tình huống truy hồi được, hệ số biến thiên) để các luật R23 và R24 có thể dùng.
4. Chạy máy suy diễn tiến.
5. Chạy máy suy diễn lần thứ hai sau khi đã tính được độ lệch giữa giá từ luật và giá từ CBR, để luật R25 có đủ thông tin kích hoạt.
6. Tổng hợp kết quả, tính khoảng giá và độ tin cậy, sinh lời giải thích.

Việc chạy máy suy diễn hai lần ở bước 4 và 5 là cần thiết vì luật R25 so sánh kết quả của hai nguồn tri thức, mà kết quả từ luật chỉ có sau khi suy diễn xong lần đầu.""",
        """Lớp `ValuationService` điều phối quy trình định giá theo sáu bước: tra khung tri thức lấy thông tin phiên bản xe; chạy mô-đun CBR truy hồi các tình huống tương tự; dựng bộ nhớ làm việc gồm 18 sự kiện, trong đó có số tình huống truy hồi được và hệ số biến thiên để các luật R23, R24 dùng; chạy máy suy diễn tiến; chạy suy diễn lần hai sau khi đã tính được độ lệch giữa hai nguồn để luật R25 đủ thông tin kích hoạt; cuối cùng tổng hợp kết quả, tính khoảng giá, độ tin cậy và sinh lời giải thích.""",
    ),
    (
        """Mô hình Random Forest được cài đặt trong `scripts/run_evaluation.py` làm kênh đối chứng, sử dụng lớp `RandomForestRegressor` của scikit-learn với các siêu tham số: 300 cây quyết định, độ sâu tối đa 18, số mẫu tối thiểu ở nút lá là 2.

Mô hình sử dụng 17 đặc trưng gồm 8 thuộc tính định danh đã mã hóa, 5 thuộc tính số và 4 thuộc tính luận lý. Đáng chú ý, `gia_xe_moi` được đưa vào làm đặc trưng, nghĩa là mô hình Random Forest cũng được cung cấp cùng một mẩu tri thức nền tảng mà hệ thống dựa trên luật sử dụng. Điều này bảo đảm so sánh công bằng giữa hai hướng tiếp cận.""",
        """Mô hình Random Forest đóng vai trò kênh đối chứng, dùng `RandomForestRegressor` của scikit-learn với 300 cây quyết định, độ sâu tối đa 18 và số mẫu tối thiểu ở nút lá là 2. Mô hình sử dụng 17 đặc trưng gồm 8 thuộc tính định danh đã mã hóa, 5 thuộc tính số và 4 thuộc tính luận lý. Đáng chú ý, `gia_xe_moi` được đưa vào làm đặc trưng, nghĩa là Random Forest cũng nhận cùng mẩu tri thức nền tảng mà hệ thống dựa trên luật sử dụng, bảo đảm so sánh công bằng giữa hai hướng tiếp cận.""",
    ),
    (
        """**Mức dòng xe và phiên bản** định nghĩa 28 dòng xe với tổng cộng 55 phiên bản. Mỗi phiên bản là một khe cụ thể với bốn thuộc tính: giá xe mới niêm yết, loại hộp số, loại nhiên liệu và phân khúc kế thừa từ dòng xe.

Cấu trúc phân cấp này cho phép kế thừa thuộc tính theo đúng cơ chế của biểu diễn tri thức bằng khung: khi suy diễn cho một chiếc Toyota Fortuner 2.4G AT, hệ thống lấy giá xe mới và hộp số từ mức phiên bản, lấy hệ số khấu hao và thanh khoản từ phân khúc SUV hạng D, lấy hệ số thương hiệu từ mức hãng Toyota.""",
        """**Mức dòng xe và phiên bản** định nghĩa 28 dòng xe với 55 phiên bản, mỗi phiên bản có bốn thuộc tính: giá xe mới niêm yết, loại hộp số, loại nhiên liệu và phân khúc kế thừa từ dòng xe.

Cấu trúc phân cấp này cho phép kế thừa thuộc tính đúng theo cơ chế biểu diễn tri thức bằng khung: khi suy diễn cho một chiếc Toyota Fortuner 2.4G AT, hệ thống lấy giá xe mới và hộp số từ mức phiên bản, hệ số khấu hao và thanh khoản từ phân khúc SUV hạng D, hệ số thương hiệu từ mức hãng Toyota.""",
    ),
    (
        """Phần điều kiện là danh sách các mệnh đề, mỗi mệnh đề so sánh một sự kiện trong bộ nhớ làm việc với một giá trị theo một toán tử. Hệ thống hỗ trợ chín toán tử: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not_in` và `exists`. Luật chỉ kích hoạt khi mọi mệnh đề đều thỏa mãn.

Phần hành động hỗ trợ bốn loại:

- `multiply` nhân một hệ số vào giá. Hệ số có thể là hằng số (`factor`) hoặc một biểu thức tính từ các sự kiện trong bộ nhớ làm việc (`expr`).
- `flag` thêm một cảnh báo rủi ro vào kết quả.
- `confidence` điều chỉnh độ tin cậy lên hoặc xuống.
- `set` gán giá trị cho một sự kiện mới.

Về việc hiệu chỉnh hệ số, các hệ số khởi tạo được đặt theo kinh nghiệm thị trường, sau đó đối chiếu với tỷ lệ giữ giá thực tế tính từ dữ liệu. Bảng 3.6 so sánh tỷ lệ giữ giá trung bình theo tuổi xe mà tập luật dự đoán với tỷ lệ quan sát được trên dữ liệu.""",
        """Phần điều kiện là danh sách các mệnh đề, mỗi mệnh đề so sánh một sự kiện trong bộ nhớ làm việc với một giá trị theo một trong chín toán tử (`==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not_in`, `exists`); luật chỉ kích hoạt khi mọi mệnh đề đều thỏa mãn. Phần hành động hỗ trợ bốn loại: `multiply` nhân hệ số vào giá (hằng số hoặc biểu thức tính từ bộ nhớ làm việc), `flag` thêm cảnh báo rủi ro, `confidence` điều chỉnh độ tin cậy, và `set` gán giá trị cho sự kiện mới.

Các hệ số khởi tạo được đặt theo kinh nghiệm thị trường rồi đối chiếu với tỷ lệ giữ giá thực tế tính từ dữ liệu. Bảng 3.6 so sánh hai nguồn này.""",
    ),
    (
        """Về độ phủ, cơ sở tình huống bao phủ cả 28 dòng xe và 55 phiên bản, với số lượng tình huống mỗi dòng xe tỷ lệ với mức độ phổ biến của dòng đó trên thị trường. Dòng xe có nhiều tình huống nhất đạt trên 200 tình huống; hai dòng xe sang có ít tình huống nhất, mỗi dòng khoảng 20–30 tình huống.

Độ phủ theo năm sản xuất trải từ 2012 đến 2026, tập trung nhiều nhất ở các năm 2021–2024 (mỗi năm trên 300 tin), thưa dần ở các năm cũ hơn. Đây là phân bố hợp lý vì xe càng cũ càng ít được rao bán trên các sàn trực tuyến.""",
        """Cơ sở tình huống bao phủ cả 28 dòng xe và 55 phiên bản, số lượng tình huống mỗi dòng tỷ lệ với mức độ phổ biến của dòng đó: dòng nhiều nhất trên 200 tình huống, hai dòng xe sang ít nhất khoảng 20–30 tình huống mỗi dòng. Độ phủ theo năm sản xuất trải từ 2012 đến 2026, tập trung ở các năm 2021–2024 và thưa dần ở năm cũ hơn – phân bố hợp lý vì xe càng cũ càng ít được rao trên sàn trực tuyến.""",
    ),
]

CONCLUSION_BLOCKS: list[tuple[str, str]] = [
    (
        """**Về cơ sở tri thức,** đề tài đã xây dựng được một cơ sở tri thức có cấu trúc rõ ràng cho miền định giá xe cũ, gồm ba thành phần:

- Khung tri thức ba mức phân cấp phân khúc – hãng – dòng xe/phiên bản, bao phủ 10 phân khúc, 12 hãng, 28 dòng xe và 55 phiên bản, cho phép kế thừa thuộc tính theo đúng cơ chế biểu diễn bằng khung.
- Tập 25 luật sản xuất chia thành sáu nhóm: khấu hao theo tuổi xe, điều chỉnh theo số km, điều chỉnh theo tình trạng và lịch sử, điều chỉnh theo cấu hình kỹ thuật, điều chỉnh theo thị trường và khu vực, cảnh báo rủi ro và độ tin cậy.
- Cơ sở tình huống gồm 2.344 tin rao, bao phủ toàn bộ 28 dòng xe và dải năm sản xuất từ 2012 đến 2026.

**Về hệ thống,** đề tài đã cài đặt đầy đủ và chạy được một sản phẩm hoàn chỉnh gồm máy suy diễn tiến với cơ chế giải quyết xung đột theo độ ưu tiên và lưu vết suy diễn, mô-đun lập luận dựa trên tình huống với độ đo tương tự có trọng số trên tám thuộc tính, mô-đun tổng hợp hai nguồn tri thức theo hệ số α thích nghi, cơ chế tính khoảng giá và độ tin cậy, cơ chế giải thích bằng ngôn ngữ tự nhiên, và giao diện web bốn trang chức năng.""",
        """**Về cơ sở tri thức,** đề tài đã xây dựng cơ sở tri thức có cấu trúc rõ ràng cho miền định giá xe cũ gồm ba thành phần: khung tri thức ba mức phân cấp phân khúc – hãng – dòng xe/phiên bản bao phủ 10 phân khúc, 12 hãng, 28 dòng xe và 55 phiên bản; tập 25 luật sản xuất chia thành sáu nhóm từ khấu hao, số km, tình trạng và lịch sử, cấu hình kỹ thuật, thị trường đến cảnh báo rủi ro; và cơ sở tình huống gồm 2.344 tin rao bao phủ toàn bộ 28 dòng xe, dải năm sản xuất 2012–2026.

**Về hệ thống,** đề tài đã cài đặt và chạy được sản phẩm hoàn chỉnh gồm máy suy diễn tiến với cơ chế giải quyết xung đột theo độ ưu tiên và lưu vết suy diễn, mô-đun CBR với độ đo tương tự có trọng số trên tám thuộc tính, mô-đun tổng hợp hai nguồn tri thức theo hệ số α thích nghi, cơ chế tính khoảng giá và độ tin cậy, cơ chế giải thích bằng ngôn ngữ tự nhiên, và giao diện web bốn trang chức năng.""",
    ),
    (
        """**Ưu tiên trước hết là kiểm chứng trên dữ liệu thật.** Việc cần làm ngay nếu đề tài được phát triển tiếp là thu thập hợp pháp dữ liệu tin rao từ các sàn giao dịch, thông qua thỏa thuận chia sẻ dữ liệu hoặc API chính thức, rồi chạy lại toàn bộ quy trình thực nghiệm ở Chương 3. Chỉ sau bước này mới có thể kết luận về độ chính xác thực tế của hệ thống và quyết định những cải tiến tiếp theo.

**Tối ưu hóa hệ số bằng giải thuật di truyền.** Các hệ số trong luật và trọng số trong độ đo tương tự hoàn toàn có thể được tối ưu tự động. Hàm mục tiêu có thể là tổ hợp của MAPE và tỷ lệ giá thực nằm trong khoảng đề xuất, với ràng buộc giữ các hệ số trong khoảng hợp lý về mặt nghiệp vụ để tránh mất ý nghĩa giải thích.

**Xây dựng tác tử thu thập và cập nhật tri thức tự động.** Cơ sở tình huống cần được cập nhật liên tục để phản ánh mặt bằng giá hiện tại. Một tác tử chạy định kỳ có thể bổ sung tin rao mới vào cơ sở tình huống, phát hiện khi tỷ lệ giữ giá thực tế lệch khỏi dự đoán của luật, và đề xuất hiệu chỉnh hệ số cho người quản trị duyệt.

**Mở rộng độ phủ và loại hình xe.** Bổ sung các dòng xe còn thiếu, mở rộng sang xe điện – phân khúc đang tăng nhanh tại Việt Nam và có quy luật khấu hao khác hẳn xe động cơ đốt trong do phụ thuộc vào tình trạng pin.

**Bổ sung mô hình hóa biến động thị trường.** Thêm một chiều thời gian vào cơ sở tình huống, cho phép hiệu chỉnh giá các tình huống cũ về mặt bằng hiện tại theo một chỉ số giá thị trường.

**Thử nghiệm mạng nơ-ron làm kênh tri thức thứ ba.** Có thể bổ sung một mô hình học sâu vào cơ chế tổng hợp, với hệ số trọng số được chọn thích nghi tương tự như hệ số α hiện tại. Điều kiện là phải giữ được khả năng giải thích tổng thể của hệ thống.

**Đánh giá khả năng giải thích với người dùng thật.** Tổ chức khảo sát với người mua, người bán và nhân viên salon để đánh giá xem lời giải thích hệ thống đưa ra có dễ hiểu, có đáng tin và có giúp họ ra quyết định tốt hơn hay không.

**Triển khai thực tế.** Đóng gói hệ thống thành dịch vụ web có thể tích hợp vào các sàn rao vặt hoặc phần mềm quản lý salon, bổ sung cơ chế ghi nhận phản hồi để hệ thống học dần từ các giao dịch thành công.""",
        """**Ưu tiên trước hết là kiểm chứng trên dữ liệu thật.** Việc cần làm ngay là thu thập hợp pháp dữ liệu tin rao từ các sàn giao dịch, qua thỏa thuận chia sẻ dữ liệu hoặc API chính thức, rồi chạy lại toàn bộ quy trình thực nghiệm ở Chương 3. Chỉ sau bước này mới kết luận được về độ chính xác thực tế và quyết định các cải tiến tiếp theo.

**Tối ưu hóa hệ số bằng giải thuật di truyền.** Các hệ số trong luật và trọng số trong độ đo tương tự có thể được tối ưu tự động, với hàm mục tiêu là tổ hợp của MAPE và tỷ lệ giá thực nằm trong khoảng đề xuất, kèm ràng buộc giữ hệ số trong khoảng hợp lý về nghiệp vụ để không mất ý nghĩa giải thích.

**Xây dựng tác tử cập nhật tri thức tự động.** Một tác tử chạy định kỳ có thể bổ sung tin rao mới vào cơ sở tình huống, phát hiện khi tỷ lệ giữ giá thực tế lệch khỏi dự đoán của luật, và đề xuất hiệu chỉnh hệ số cho người quản trị duyệt.

**Mở rộng độ phủ và mô hình hóa thời gian.** Bổ sung các dòng xe còn thiếu và mở rộng sang xe điện – phân khúc có quy luật khấu hao khác hẳn do phụ thuộc tình trạng pin. Đồng thời thêm chiều thời gian vào cơ sở tình huống để hiệu chỉnh giá các tình huống cũ về mặt bằng hiện tại.

**Thử nghiệm mạng nơ-ron và đánh giá với người dùng thật.** Có thể bổ sung một mô hình học sâu làm kênh tri thức thứ ba với trọng số chọn thích nghi như hệ số α, miễn là giữ được khả năng giải thích tổng thể. Song song đó, cần khảo sát với người mua, người bán và nhân viên salon để đánh giá lời giải thích có thực sự dễ hiểu và hữu ích hay không.

**Triển khai thực tế.** Đóng gói hệ thống thành dịch vụ web tích hợp vào các sàn rao vặt hoặc phần mềm quản lý salon, kèm cơ chế ghi nhận phản hồi để hệ thống học dần từ giao dịch thành công.""",
    ),
]


def _apply(file_name: str, blocks: list[tuple[str, str]]) -> None:
    path = SCRATCHPAD / file_name
    text = path.read_text(encoding="utf-8")
    original_word_count = len(text.split())

    applied = 0
    for original, condensed in blocks:
        if original not in text:
            print(f"  CANH BAO [{file_name}]: khong tim thay '{original[:50]}...'")
            continue
        text = text.replace(original, condensed)
        applied += 1

    path.write_text(text, encoding="utf-8")
    final_word_count = len(text.split())
    print(f"{file_name:26} {original_word_count:>6,} -> {final_word_count:>6,} tu "
          f"({applied}/{len(blocks)} doan)")


def main() -> None:
    _apply("chuong1_rut_gon.md", CHAPTER_ONE_BLOCKS)
    _apply("chuong3_rut_gon.md", CHAPTER_THREE_BLOCKS)
    _apply("ketluan.md", CONCLUSION_BLOCKS)


if __name__ == "__main__":
    main()
