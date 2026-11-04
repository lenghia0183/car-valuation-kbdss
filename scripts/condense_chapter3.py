"""Rút gọn Chương 3 để báo cáo nằm trong giới hạn 40 trang.

Giữ nguyên toàn bộ số liệu, bảng biểu, hình và các kết luận. Chỉ nén phần diễn giải
dài dòng ở các mục cài đặt và phân tích, nơi ý chính có thể trình bày gọn hơn mà
không mất thông tin cần cho người đọc.
"""

from __future__ import annotations

from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

# Mỗi cặp gồm đoạn gốc và đoạn rút gọn thay thế.
CONDENSED_BLOCKS: list[tuple[str, str]] = [
    # --- 3.1.1: gộp phần mô tả cấu trúc thư mục ---
    (
        """Mã nguồn được tổ chức thành bốn nhóm thư mục theo đúng kiến trúc ba tầng đã thiết kế ở Chương 2:

- `kb/` chứa cơ sở tri thức dưới dạng hai tệp JSON: `frames.json` lưu khung tri thức hãng – dòng xe – phiên bản, `rules.json` lưu tập luật sản xuất.
- `src/` chứa tầng xử lý tri thức: `knowledge_base.py` nạp và truy vấn cơ sở tri thức, `inference_engine.py` cài đặt máy suy diễn tiến, `case_based_reasoning.py` cài đặt mô-đun lập luận dựa trên tình huống, `valuation_service.py` điều phối toàn bộ quy trình định giá, `app.py` cài đặt giao diện web.
- `scripts/` chứa các kịch bản chuẩn bị dữ liệu, đánh giá và sinh biểu đồ.
- `data/` và `outputs/` lưu dữ liệu đã xử lý và kết quả thực nghiệm.""",
        """Mã nguồn được tổ chức theo đúng kiến trúc ba tầng đã thiết kế ở Chương 2. Thư mục `kb/` chứa cơ sở tri thức dưới dạng hai tệp JSON là `frames.json` (khung tri thức) và `rules.json` (tập luật). Thư mục `src/` chứa tầng xử lý tri thức gồm `knowledge_base.py`, `inference_engine.py`, `case_based_reasoning.py`, `valuation_service.py` và `app.py`. Thư mục `scripts/` chứa các kịch bản chuẩn bị dữ liệu, đánh giá và sinh biểu đồ; `data/` và `outputs/` lưu dữ liệu đã xử lý và kết quả thực nghiệm.""",
    ),
    # --- 3.1.3: nén phần phân tích thống kê mô tả ---
    (
        """Giá rao bán trải rộng từ 62,7 triệu đồng (xe hạng A đời sâu) đến 1.607,7 triệu đồng (xe sang đời mới), với trung vị 345,15 triệu đồng. Phân bố giá lệch phải rõ rệt: giá trung bình (384,18 triệu) cao hơn trung vị khoảng 11%, do một số ít tin rao xe sang và SUV hạng D kéo đuôi phân bố về phía giá cao. Hình 3.1 thể hiện trực quan phân bố này.

Số km bình quân mỗi năm có trung vị 13.406 km, phù hợp với mức sử dụng thông thường của xe gia đình tại Việt Nam. Tuy nhiên giá trị lớn nhất lên tới 60.944 km mỗi năm, phản ánh nhóm xe từng chạy dịch vụ – nhóm mà hệ thống cần nhận diện và cảnh báo.

Tỷ lệ giữ giá có trung vị 0,50, nghĩa là một chiếc xe điển hình trong tập dữ liệu (5 năm tuổi) được rao bán ở khoảng một nửa giá xe mới. Giá trị lớn nhất 1,22 xuất hiện ở một vài tin rao xe mới đăng ký trong năm, có trang bị thêm và được rao cao hơn giá niêm yết.

Về phân bố theo hãng, Toyota chiếm nhiều tin rao nhất (546 tin), tiếp theo là Hyundai (503), Mazda (367), Kia (331) và Honda (308). Hai hãng xe sang Mercedes-Benz và BMW chỉ có tổng cộng 61 tin, phản ánh đúng thực tế là xe sang có thanh khoản thấp và ít tin rao hơn nhiều so với xe phổ thông. Hình 3.2 thể hiện phân bố này.

Xét theo phân khúc, ba phân khúc có nhiều tin rao nhất là sedan hạng B (508 tin), SUV hạng C (496 tin) và hatchback hạng A (461 tin). Giá trung vị theo phân khúc trải từ 176,8 triệu đồng (hatchback hạng A) đến 686,7 triệu đồng (xe sang), cho thấy sự phân tầng giá rõ rệt giữa các phân khúc.

Về các thuộc tính rủi ro, tập dữ liệu có 69 tin xe từng ngập nước (2,4%), 122 tin xe từng tai nạn nặng (4,2%), 362 tin xe từng đăng ký kinh doanh vận tải (12,4%) và 661 tin xe một chủ bảo dưỡng hãng đầy đủ (22,6%). Tỷ lệ này cho phép đánh giá được các luật xử lý rủi ro nhưng vẫn giữ các trường hợp rủi ro ở mức thiểu số như thực tế.""",
        """Giá rao bán trải từ 62,7 triệu đồng (xe hạng A đời sâu) đến 1.607,7 triệu đồng (xe sang đời mới), trung vị 345,15 triệu. Phân bố lệch phải rõ rệt: giá trung bình cao hơn trung vị khoảng 11% do một số ít tin rao xe sang kéo đuôi phân bố về phía giá cao. Hình 3.1 thể hiện trực quan phân bố này.

Số km bình quân mỗi năm có trung vị 13.406 km, phù hợp với mức sử dụng của xe gia đình tại Việt Nam; giá trị lớn nhất 60.944 km mỗi năm phản ánh nhóm xe từng chạy dịch vụ mà hệ thống cần nhận diện. Tỷ lệ giữ giá có trung vị 0,50, nghĩa là xe điển hình trong tập dữ liệu (5 năm tuổi) được rao ở khoảng một nửa giá xe mới.

Về phân bố theo hãng, Toyota nhiều tin rao nhất (546 tin), tiếp theo là Hyundai (503), Mazda (367), Kia (331) và Honda (308); hai hãng xe sang chỉ có tổng cộng 61 tin, phản ánh đúng thực tế xe sang thanh khoản thấp (Hình 3.2). Xét theo phân khúc, sedan hạng B, SUV hạng C và hatchback hạng A có nhiều tin rao nhất; giá trung vị trải từ 176,8 triệu (hatchback hạng A) đến 686,7 triệu đồng (xe sang).

Về thuộc tính rủi ro, tập dữ liệu có 69 tin xe từng ngập nước (2,4%), 122 tin xe tai nạn nặng (4,2%), 362 tin xe từng kinh doanh vận tải (12,4%) và 661 tin xe một chủ bảo dưỡng hãng đầy đủ (22,6%) – đủ để đánh giá các luật rủi ro mà vẫn giữ chúng ở mức thiểu số như thực tế.""",
    ),
    # --- 3.2.1: nén mô tả ba bước làm sạch ---
    (
        """**Bước một – loại tin trùng lặp.** Hai tin rao được coi là trùng nếu giống nhau đồng thời trên bộ thuộc tính nhận dạng gồm hãng, dòng xe, phiên bản, năm sản xuất, số km, khu vực và giá. Trên bộ dữ liệu này không phát hiện tin trùng lặp nào, do quá trình sinh dữ liệu có tính ngẫu nhiên đủ cao. Bước kiểm tra vẫn được giữ lại vì dữ liệu thu thập thật từ các sàn rao vặt thường chứa nhiều tin đăng lại.

**Bước hai – loại tin thiếu thông tin hoặc có giá trị vô lý.** Tin bị loại nếu thiếu một trong các thuộc tính bắt buộc, hoặc có giá dưới 30 triệu đồng, số km âm, hoặc tuổi xe âm. Không có tin nào bị loại ở bước này.

**Bước ba – loại ngoại lai bằng quy tắc IQR theo nhóm.** Đây là bước có tác động thực sự. Thay vì áp dụng quy tắc IQR trên toàn bộ tập dữ liệu – cách làm sẽ loại nhầm toàn bộ xe sang vì chúng vốn đắt hơn mặt bằng chung – đề tài áp dụng riêng cho từng nhóm (dòng xe, năm sản xuất). Với mỗi nhóm có từ 8 tin trở lên, tính tứ phân vị thứ nhất Q1, tứ phân vị thứ ba Q3 và khoảng tứ phân vị IQR = Q3 − Q1, rồi loại các tin có giá nằm ngoài khoảng [Q1 − 1,5·IQR; Q3 + 1,5·IQR].

Cách làm theo nhóm này quan trọng vì nó so sánh mỗi chiếc xe với những chiếc cùng dòng, cùng đời, thay vì với toàn thị trường. Một chiếc Mercedes C200 giá 700 triệu là bình thường trong nhóm của nó nhưng sẽ bị coi là ngoại lai nếu so với toàn bộ tập dữ liệu.

Kết quả: 72 tin bị loại (2,4%), giữ lại 2.928 tin, tương ứng tỷ lệ giữ lại 97,6%.""",
        """**Bước một – loại tin trùng lặp.** Hai tin rao được coi là trùng nếu giống nhau trên bộ thuộc tính nhận dạng gồm hãng, dòng xe, phiên bản, năm sản xuất, số km, khu vực và giá. Bộ dữ liệu này không có tin trùng lặp; bước kiểm tra vẫn được giữ vì dữ liệu thật từ các sàn rao vặt thường chứa nhiều tin đăng lại.

**Bước hai – loại tin thiếu thông tin hoặc có giá trị vô lý.** Tin bị loại nếu thiếu thuộc tính bắt buộc, hoặc có giá dưới 30 triệu đồng, số km âm hoặc tuổi xe âm. Không có tin nào bị loại ở bước này.

**Bước ba – loại ngoại lai bằng quy tắc IQR theo nhóm.** Đây là bước có tác động thực sự. Thay vì áp dụng IQR trên toàn tập – cách làm sẽ loại nhầm toàn bộ xe sang vì chúng vốn đắt hơn mặt bằng chung – đề tài áp dụng riêng cho từng nhóm dòng xe và năm sản xuất. Với mỗi nhóm từ 8 tin trở lên, loại các tin có giá nằm ngoài khoảng [Q1 − 1,5·IQR; Q3 + 1,5·IQR]. Cách làm này so sánh mỗi chiếc xe với những chiếc cùng dòng, cùng đời: một chiếc Mercedes C200 giá 700 triệu là bình thường trong nhóm của nó nhưng sẽ bị coi là ngoại lai nếu so với toàn thị trường.

Kết quả: 72 tin bị loại (2,4%), giữ lại 2.928 tin, tỷ lệ giữ lại 97,6%.""",
    ),
    # --- 3.4.1: nén mô tả cài đặt máy suy diễn ---
    (
        """**Bước nhận dạng.** Phương thức `_matches` kiểm tra một luật có thỏa mãn bộ nhớ làm việc hay không bằng cách đánh giá toàn bộ các mệnh đề điều kiện. Việc đánh giá từng mệnh đề do lớp `ConditionEvaluator` đảm nhiệm, tách riêng để dễ kiểm thử và dễ bổ sung toán tử mới.

**Bước giải quyết xung đột.** Tập luật được sắp xếp sẵn theo độ ưu tiên giảm dần ngay khi nạp cơ sở tri thức. Phương thức `_select_next_rule` duyệt tập luật đã sắp xếp và trả về luật đầu tiên vừa thỏa mãn điều kiện vừa chưa từng kích hoạt. Việc loại luật đã kích hoạt là cơ chế bảo đảm vòng lặp suy diễn kết thúc, tránh trường hợp một luật tự kích hoạt lại vô hạn.

**Bước thực thi.** Phương thức `_execute_rule` áp dụng lần lượt các hành động của luật. Riêng hành động `multiply` có một điểm cần lưu ý trong cài đặt: các luật thuộc nhóm khấu hao (R01–R05) tính trực tiếp từ giá xe mới chứ không nhân dồn lên giá hiện tại, vì mỗi luật khấu hao đã bao gồm toàn bộ quá trình mất giá từ lúc mới đến tuổi hiện tại. Các nhóm luật còn lại nhân dồn lên giá đang có.

Vòng lặp suy diễn tiếp tục cho tới khi không còn luật mới nào kích hoạt được. Mỗi lần một luật `multiply` được thực thi, hệ thống ghi một bản ghi vào vết suy diễn gồm mã luật, nhãn tác động, hệ số áp dụng, giá trước và giá sau. Vết suy diễn này chính là nguyên liệu cho cơ chế giải thích.

Về biểu thức hệ số, các luật khấu hao dùng biểu thức toán học tham chiếu tới sự kiện trong bộ nhớ làm việc, ví dụ luật R04 có biểu thức `0.90 * pow(1 - base_depreciation, 3) * pow(1 - base_depreciation * 0.85, 4) * pow(1 - base_depreciation * 0.65, tuoi_xe - 7)`. Biểu thức được tính trong một phạm vi hạn chế chỉ chứa các sự kiện số và sáu hàm toán học được phép, không truy cập được các hàm dựng sẵn của Python.""",
        """**Bước nhận dạng** do phương thức `_matches` đảm nhiệm, kiểm tra một luật có thỏa mãn bộ nhớ làm việc hay không bằng cách đánh giá toàn bộ mệnh đề điều kiện; việc đánh giá từng mệnh đề được tách sang lớp `ConditionEvaluator` để dễ kiểm thử và bổ sung toán tử mới.

**Bước giải quyết xung đột** dựa trên tập luật đã sắp xếp theo độ ưu tiên giảm dần ngay khi nạp cơ sở tri thức. Phương thức `_select_next_rule` trả về luật đầu tiên vừa thỏa điều kiện vừa chưa từng kích hoạt. Việc loại luật đã kích hoạt chính là cơ chế bảo đảm vòng lặp suy diễn kết thúc.

**Bước thực thi** áp dụng lần lượt các hành động của luật. Riêng hành động `multiply` có một điểm đáng lưu ý: các luật khấu hao (R01–R05) tính trực tiếp từ giá xe mới chứ không nhân dồn lên giá hiện tại, vì mỗi luật khấu hao đã bao gồm toàn bộ quá trình mất giá từ lúc mới đến tuổi hiện tại; các nhóm còn lại nhân dồn lên giá đang có.

Vòng lặp tiếp tục cho tới khi không còn luật mới nào kích hoạt được. Mỗi lần một luật `multiply` được thực thi, hệ thống ghi vào vết suy diễn một bản ghi gồm mã luật, nhãn tác động, hệ số, giá trước và giá sau – đây chính là nguyên liệu cho cơ chế giải thích. Các luật khấu hao dùng biểu thức toán học tham chiếu sự kiện trong bộ nhớ làm việc; biểu thức được tính trong phạm vi hạn chế chỉ chứa sự kiện số và sáu hàm toán học được phép, không truy cập được hàm dựng sẵn của Python.""",
    ),
    # --- 3.4.3: nén mô tả mô-đun tổng hợp ---
    (
        """**Công thức độ tin cậy.** Độ tin cậy xuất phát từ mức cơ sở 0,80, cộng với tổng các điều chỉnh từ hành động `confidence` của các luật đã kích hoạt, cộng thêm 0,08 nếu truy hồi được từ 5 tình huống trở lên hoặc 0,04 nếu được từ 3 tình huống, cuối cùng giới hạn trong khoảng [0,20; 0,98].

**Công thức khoảng giá.** Bán kính tương đối của khoảng giá được tính là `0,10 + (1 − độ tin cậy) × 0,40`, sau đó lấy cực đại với `hệ số biến thiên × 1,30` và giới hạn trên ở 0,35. Công thức này bảo đảm hai tính chất: độ tin cậy càng thấp thì khoảng giá càng rộng, và khi giá các xe tương tự phân tán mạnh thì khoảng giá cũng phải nới rộng tương ứng.

**Cơ chế giải thích.** Lời giải thích được dựng từ vết suy diễn, gồm bốn phần: mô tả chiếc xe và giá xe mới tham chiếu, thông tin tuổi xe và số km, danh sách từng luật đã kích hoạt kèm hệ số và giá sau khi áp dụng, và phần tổng hợp hai nguồn tri thức kèm khoảng giá cuối cùng.""",
        """**Công thức độ tin cậy.** Độ tin cậy xuất phát từ mức cơ sở 0,80, cộng các điều chỉnh từ hành động `confidence` của những luật đã kích hoạt, cộng thêm 0,08 nếu truy hồi được từ 5 tình huống trở lên hoặc 0,04 nếu từ 3 tình huống, rồi giới hạn trong khoảng [0,20; 0,98].

**Công thức khoảng giá.** Bán kính tương đối được tính là `0,10 + (1 − độ tin cậy) × 0,40`, lấy cực đại với `hệ số biến thiên × 1,30` và giới hạn trên ở 0,35. Công thức bảo đảm hai tính chất: độ tin cậy càng thấp thì khoảng giá càng rộng, và khi giá các xe tương tự phân tán mạnh thì khoảng giá cũng nới rộng theo.

**Cơ chế giải thích** dựng lời giải thích từ vết suy diễn, gồm mô tả chiếc xe và giá xe mới tham chiếu, thông tin tuổi xe và số km, danh sách từng luật đã kích hoạt kèm hệ số và giá sau khi áp dụng, và phần tổng hợp hai nguồn tri thức kèm khoảng giá cuối cùng.""",
    ),
    # --- 3.4.5: nén mô tả giao diện ---
    (
        """**Trang Kết quả và giải thích** (Hình 3.4) hiển thị bốn chỉ số chính ở đầu trang: giá đề xuất, giá từ luật, giá từ tình huống và độ tin cậy kèm nhãn mức độ. Phía dưới là thanh trực quan thể hiện khoảng giá với điểm nhấn ở giá đề xuất. Các cảnh báo rủi ro, nếu có, được hiển thị ngay sau đó. Phần cuối trang là ba thẻ mở rộng: "Giải thích kết quả" liệt kê toàn bộ lập luận bằng ngôn ngữ tự nhiên, "Vết suy diễn" trình bày bảng các luật đã kích hoạt kèm biểu đồ thác nước thể hiện ảnh hưởng của từng luật lên giá (Hình 3.5), "Xe tương tự" hiển thị bảng các tình huống đã truy hồi kèm độ tương tự và giá sau hiệu chỉnh (Hình 3.6).

**Trang Phân tích thị trường** (Hình 3.7) cung cấp bốn chỉ số tổng quan và bốn biểu đồ: phân bố giá, giá trung vị theo phân khúc, đường cong khấu hao theo phân khúc và biểu đồ phân tán quan hệ giữa số km và giá bán.

**Trang Quản trị tri thức** (Hình 3.8) cho phép người quản trị xem toàn bộ tập luật với bộ lọc theo nhóm, xem bảng khung tri thức của 55 phiên bản, và chạy kiểm tra tính nhất quán của cơ sở tri thức. Chức năng kiểm tra nhất quán thực hiện sáu phép kiểm tra: không có mã luật trùng lặp, mọi luật đều có điều kiện, mọi luật đều có hành động, mọi khung phiên bản đều có giá xe mới hợp lệ, mọi hệ số khấu hao đều nằm trong khoảng hợp lý, và cơ sở tình huống đủ lớn để truy hồi. Kết quả chạy thực tế cho thấy cả sáu phép kiểm tra đều đạt (Hình 3.9).""",
        """**Trang Kết quả và giải thích** (Hình 3.4) hiển thị bốn chỉ số chính ở đầu trang gồm giá đề xuất, giá từ luật, giá từ tình huống và độ tin cậy kèm nhãn mức độ; tiếp theo là thanh trực quan thể hiện khoảng giá và các cảnh báo rủi ro nếu có. Phần cuối trang là ba thẻ mở rộng: "Giải thích kết quả" liệt kê lập luận bằng ngôn ngữ tự nhiên, "Vết suy diễn" trình bày bảng luật đã kích hoạt kèm biểu đồ thác nước (Hình 3.5), và "Xe tương tự" hiển thị các tình huống đã truy hồi kèm độ tương tự và giá sau hiệu chỉnh (Hình 3.6).

**Trang Phân tích thị trường** (Hình 3.7) cung cấp bốn chỉ số tổng quan cùng bốn biểu đồ: phân bố giá, giá trung vị theo phân khúc, đường cong khấu hao theo phân khúc và biểu đồ phân tán quan hệ giữa số km và giá bán.

**Trang Quản trị tri thức** (Hình 3.8) cho phép xem toàn bộ tập luật với bộ lọc theo nhóm, xem bảng khung tri thức của 55 phiên bản và chạy kiểm tra tính nhất quán. Chức năng này thực hiện sáu phép kiểm tra: không có mã luật trùng lặp, mọi luật đều có điều kiện và hành động, mọi khung phiên bản đều có giá xe mới hợp lệ, mọi hệ số khấu hao nằm trong khoảng hợp lý, và cơ sở tình huống đủ lớn để truy hồi. Kết quả chạy thực tế cho thấy cả sáu phép kiểm tra đều đạt (Hình 3.9).""",
    ),
    # --- 3.5.1: nén mô tả độ đo ---
    (
        """**MAE (Mean Absolute Error)** là sai số tuyệt đối trung bình, tính bằng trung bình của trị tuyệt đối hiệu giữa giá dự đoán và giá thực. Đơn vị là triệu đồng, cho biết hệ thống lệch bao nhiêu tiền trên một chiếc xe trung bình.

**MAPE (Mean Absolute Percentage Error)** là sai số phần trăm tuyệt đối trung bình. Độ đo này quan trọng hơn MAE trong bài toán định giá, vì sai số 50 triệu trên một chiếc xe 200 triệu nghiêm trọng hơn nhiều so với cùng sai số đó trên một chiếc xe 1,5 tỷ.

**R² (hệ số xác định)** đo tỷ lệ phương sai của giá thực mà mô hình giải thích được, nhận giá trị tối đa bằng 1.

**Tỷ lệ giá thực nằm trong khoảng đề xuất** là độ đo riêng của hệ thống này, đo xem khoảng giá mà hệ thống đưa ra có thực sự chứa giá thị trường hay không. Một hệ thống đưa khoảng giá quá hẹp sẽ có tỷ lệ này thấp; ngược lại khoảng quá rộng thì tỷ lệ cao nhưng mất giá trị sử dụng.

Ngoài ra, thời gian phản hồi trung bình cho một lượt định giá cũng được đo.""",
        """**MAE** là sai số tuyệt đối trung bình, đơn vị triệu đồng, cho biết hệ thống lệch bao nhiêu tiền trên một chiếc xe trung bình. **MAPE** là sai số phần trăm tuyệt đối trung bình – độ đo quan trọng hơn MAE trong bài toán định giá, vì sai số 50 triệu trên một chiếc xe 200 triệu nghiêm trọng hơn nhiều so với cùng sai số đó trên xe 1,5 tỷ. **R²** đo tỷ lệ phương sai của giá thực mà mô hình giải thích được, tối đa bằng 1. **Tỷ lệ giá thực nằm trong khoảng đề xuất** là độ đo riêng của hệ thống, kiểm tra khoảng giá đưa ra có thực sự chứa giá thị trường hay không: khoảng quá hẹp làm tỷ lệ này thấp, còn khoảng quá rộng thì tỷ lệ cao nhưng mất giá trị sử dụng. Thời gian phản hồi trung bình cho một lượt định giá cũng được đo.""",
    ),
    # --- 3.5.3: nén phân tích so sánh ---
    (
        """Kết quả cho thấy hệ lai tốt nhất trên cả ba độ đo. So với phương pháp tốt thứ hai là chỉ dùng luật, hệ lai giảm MAE 6,7% (từ 43,79 xuống 40,86 triệu đồng), giảm MAPE 4,4% tương đối (từ 11,43% xuống 10,93%) và tăng R² từ 0,9055 lên 0,9153.

Điểm đáng chú ý là **hệ lai tốt hơn cả hai thành phần cấu thành nó**. Điều này không hiển nhiên: một tổ hợp của hai phương pháp hoàn toàn có thể nằm giữa hai phương pháp đó về chất lượng. Kết quả này cho thấy hai nguồn tri thức mắc sai số theo những cách khác nhau, nên việc kết hợp giúp triệt tiêu một phần sai số.

Cụ thể, tập luật mô tả tốt xu hướng khấu hao chung nhưng không nắm được đặc thù giữ giá của từng dòng xe cụ thể; ngược lại CBR nắm được đặc thù dòng xe qua các tin rao thực tế nhưng chịu ảnh hưởng mạnh của nhiễu khi số tình huống tương tự ít. Hệ số α thích nghi cho phép hệ thống nghiêng về nguồn đáng tin hơn tùy từng trường hợp.

Mô hình Random Forest đạt kết quả tương đương CBR (MAPE 11,92% so với 12,30%) nhưng kém hơn hệ lai. Quan trọng hơn con số, Random Forest **không cung cấp được lời giải thích nào** cho kết quả của nó, trong khi hệ lai trả về đầy đủ vết suy diễn, danh sách xe tương tự và cảnh báo rủi ro. Đây chính là luận điểm trung tâm của đề tài: trong bài toán định giá tài sản, khả năng giải thích có giá trị ngang với độ chính xác.""",
        """Hệ lai tốt nhất trên cả ba độ đo. So với phương pháp tốt thứ hai là chỉ dùng luật, hệ lai giảm MAE 6,7% (từ 43,79 xuống 40,86 triệu đồng), giảm MAPE từ 11,43% xuống 10,93% và tăng R² từ 0,9055 lên 0,9153.

Điểm đáng chú ý là **hệ lai tốt hơn cả hai thành phần cấu thành nó**. Điều này không hiển nhiên, vì một tổ hợp của hai phương pháp hoàn toàn có thể nằm giữa chúng về chất lượng. Kết quả cho thấy hai nguồn tri thức mắc sai số theo những cách khác nhau nên việc kết hợp triệt tiêu được một phần sai số: tập luật mô tả tốt xu hướng khấu hao chung nhưng không nắm được đặc thù giữ giá của từng dòng xe, còn CBR nắm được đặc thù đó qua tin rao thực tế nhưng chịu ảnh hưởng của nhiễu khi số tình huống tương tự ít. Hệ số α thích nghi cho phép hệ thống nghiêng về nguồn đáng tin hơn tùy trường hợp.

Random Forest đạt kết quả tương đương CBR (MAPE 11,92% so với 12,30%) nhưng kém hơn hệ lai. Quan trọng hơn con số, Random Forest **không cung cấp được lời giải thích nào**, trong khi hệ lai trả về đầy đủ vết suy diễn, danh sách xe tương tự và cảnh báo rủi ro. Đây là luận điểm trung tâm của đề tài: trong định giá tài sản, khả năng giải thích có giá trị ngang với độ chính xác.""",
    ),
    # --- 3.5.4: nén phân tích kịch bản ---
    (
        """**Phân tích KB1 và KB2.** Hai kịch bản này dùng cùng một chiếc xe, chỉ khác ở việc có ngập nước hay không, nên cho phép cô lập tác động của tri thức rủi ro. Kết quả: giá giảm từ 518,4 xuống 456,6 triệu đồng (giảm 11,9%), độ tin cậy giảm mạnh từ 93% xuống 66%, và khoảng giá nới rộng từ 133 triệu lên 215 triệu.

Đây chính xác là hành vi mong muốn. Khi gặp một chiếc xe có lịch sử rủi ro, hệ thống không chỉ hạ giá mà còn **tự nhận biết rằng nó kém chắc chắn hơn** về con số mình đưa ra, và thể hiện sự kém chắc chắn đó bằng khoảng giá rộng hơn. Hai cảnh báo được sinh ra: một từ luật R11 về rủi ro hệ thống điện, một từ luật R25 cảnh báo rằng kết quả từ luật và từ tình huống đã lệch đáng kể – điều dễ hiểu vì trong cơ sở tình huống rất ít xe ngập nước để tham chiếu.

**Phân tích KB3.** Chiếc Hyundai Accent đời 2021 nhưng đã chạy 185.000 km, tương đương hơn 37.000 km mỗi năm. Hệ thống kích hoạt R09 (số km rất cao, nghi xe dịch vụ) và R13 (xe từng đăng ký kinh doanh), đưa ra hai cảnh báo tương ứng và giảm giá xuống 235,9 triệu đồng. Đáng chú ý, độ tin cậy vẫn ở mức cao 88% – hợp lý, vì đây là trường hợp mà tri thức luật mô tả rõ ràng và cơ sở tình huống có đủ xe tương tự để tham chiếu.

**Phân tích KB4.** Chiếc Mercedes C200 đời 2015 kích hoạt đồng thời R21 (phân khúc thanh khoản thấp) và R22 (xe sang quá 8 năm). Khoảng giá 221–370 triệu rộng tới 50,4% giá đề xuất, phản ánh đúng thực tế rằng xe sang đời sâu rất khó định giá chính xác vì phụ thuộc nặng vào tình trạng thực tế và chi phí bảo dưỡng tiềm ẩn.

**Phân tích KB5.** Chiếc Mazda CX-5 từng tai nạn nặng được giảm giá theo luật R12, độ tin cậy hạ xuống 68% và sinh hai cảnh báo, trong đó có cảnh báo R25 về độ lệch giữa hai nguồn tri thức – cùng cơ chế như KB2.

**Nhận xét chung về khả năng giải thích.** Trong cả năm kịch bản, hệ thống đều trả về được: danh sách cụ thể các luật đã kích hoạt kèm hệ số và tác động lên giá, danh sách các xe tương tự dùng làm tham chiếu kèm độ tương tự, cảnh báo rủi ro bằng ngôn ngữ tự nhiên, và độ tin cậy phản ánh mức độ chắc chắn. Hình 3.14 minh họa màn hình kết quả của kịch bản KB2.

Đây là điều mà mô hình Random Forest – dù đạt độ chính xác tương đương – không thể cung cấp. Với một người bán xe đang cân nhắc mức giá, hoặc một nhân viên salon cần giải thích cho khách tại sao định giá như vậy, phần giải thích này có giá trị sử dụng trực tiếp.""",
        """**KB1 và KB2** dùng cùng một chiếc xe, chỉ khác ở việc có ngập nước hay không, nên cô lập được tác động của tri thức rủi ro. Giá giảm từ 518,4 xuống 456,6 triệu đồng (giảm 11,9%), độ tin cậy giảm mạnh từ 93% xuống 66%, khoảng giá nới rộng từ 133 lên 215 triệu. Đây chính xác là hành vi mong muốn: khi gặp xe có lịch sử rủi ro, hệ thống không chỉ hạ giá mà còn **tự nhận biết rằng nó kém chắc chắn hơn** và thể hiện điều đó bằng khoảng giá rộng hơn. Hai cảnh báo được sinh ra: một từ R11 về rủi ro hệ thống điện, một từ R25 báo kết quả hai nguồn lệch đáng kể – dễ hiểu vì cơ sở tình huống có rất ít xe ngập nước để tham chiếu.

**KB3** là chiếc Hyundai Accent đời 2021 đã chạy 185.000 km, tương đương hơn 37.000 km mỗi năm. Hệ thống kích hoạt R09 và R13, sinh hai cảnh báo và giảm giá xuống 235,9 triệu. Độ tin cậy vẫn cao ở mức 88%, hợp lý vì đây là trường hợp tri thức luật mô tả rõ ràng và có đủ xe tương tự tham chiếu.

**KB4** là chiếc Mercedes C200 đời 2015, kích hoạt đồng thời R21 và R22. Khoảng giá 221–370 triệu rộng tới 50,4% giá đề xuất, phản ánh đúng thực tế xe sang đời sâu rất khó định giá vì phụ thuộc nặng vào tình trạng thực tế và chi phí bảo dưỡng tiềm ẩn.

**KB5** là chiếc Mazda CX-5 từng tai nạn nặng, được giảm giá theo R12, độ tin cậy hạ xuống 68% và sinh hai cảnh báo, trong đó có R25 – cùng cơ chế như KB2.

**Nhận xét chung.** Trong cả năm kịch bản, hệ thống đều trả về danh sách luật đã kích hoạt kèm hệ số và tác động, danh sách xe tương tự kèm độ tương tự, cảnh báo rủi ro bằng ngôn ngữ tự nhiên, và độ tin cậy phản ánh mức chắc chắn (Hình 3.14 minh họa kịch bản KB2). Đây là điều mô hình Random Forest không thể cung cấp dù đạt độ chính xác tương đương. Với người bán xe đang cân nhắc mức giá hoặc nhân viên salon cần giải thích cho khách, phần giải thích này có giá trị sử dụng trực tiếp.""",
    ),
    # --- 3.5.5: nén phần nhận xét ---
    (
        """**Về độ chính xác.** Hệ lai đạt MAPE 10,93% trên tập kiểm thử, nghĩa là sai số trung bình khoảng 11% giá xe. Với bài toán định giá xe cũ – nơi ngay cả các chuyên gia cũng thường đưa ra khoảng giá thay vì một con số duy nhất – mức sai số này chấp nhận được cho mục đích tham khảo và sàng lọc ban đầu, nhưng chưa đủ để thay thế thẩm định trực tiếp.

**Về giá trị của việc kết hợp tri thức.** Kết quả thực nghiệm ủng hộ giả thuyết trung tâm của đề tài: hệ lai tốt hơn cả ba phương pháp đơn lẻ trên cả ba độ đo. Cơ chế hệ số α thích nghi tỏ ra hiệu quả trong việc chọn nguồn tri thức đáng tin hơn tùy từng trường hợp cụ thể.

**Về khả năng giải thích.** Đây là ưu điểm rõ rệt nhất của hướng tiếp cận dựa trên tri thức. Hệ thống không chỉ đưa ra con số mà còn trình bày được toàn bộ lập luận dẫn tới con số đó, đồng thời tự đánh giá được mức độ chắc chắn của mình và nới rộng khoảng giá khi thiếu chắc chắn. Năm kịch bản ở mục 3.5.4 cho thấy cơ chế này hoạt động nhất quán.

**Về khả năng xử lý tri thức hiếm.** Các luật R11, R12 xử lý xe ngập nước và tai nạn nặng là ví dụ điển hình cho loại tri thức mà mô hình học máy thuần túy khó học được: những trường hợp này chỉ chiếm 2–4% dữ liệu, quá ít để mô hình học ra quy luật đáng tin, nhưng lại là tri thức mà bất kỳ người làm nghề nào cũng nắm rõ. Việc mã hóa chúng thành luật tường minh cho phép hệ thống xử lý đúng ngay cả khi dữ liệu không đủ.""",
        """**Về độ chính xác.** Hệ lai đạt MAPE 10,93%, nghĩa là sai số trung bình khoảng 11% giá xe. Với bài toán định giá xe cũ – nơi ngay cả chuyên gia cũng thường đưa ra khoảng giá thay vì một con số – mức sai số này chấp nhận được cho mục đích tham khảo và sàng lọc ban đầu, nhưng chưa đủ để thay thế thẩm định trực tiếp.

**Về giá trị của việc kết hợp tri thức.** Kết quả ủng hộ giả thuyết trung tâm của đề tài: hệ lai tốt hơn cả ba phương pháp đơn lẻ trên cả ba độ đo, và cơ chế hệ số α thích nghi tỏ ra hiệu quả trong việc chọn nguồn tri thức đáng tin hơn tùy trường hợp.

**Về khả năng giải thích.** Đây là ưu điểm rõ rệt nhất của hướng tiếp cận dựa trên tri thức. Hệ thống không chỉ đưa ra con số mà còn trình bày toàn bộ lập luận dẫn tới con số đó, tự đánh giá mức độ chắc chắn và nới rộng khoảng giá khi thiếu chắc chắn. Năm kịch bản ở mục 3.5.4 cho thấy cơ chế này hoạt động nhất quán.

**Về khả năng xử lý tri thức hiếm.** Các luật R11, R12 xử lý xe ngập nước và tai nạn nặng là ví dụ điển hình cho loại tri thức mà mô hình học máy thuần túy khó học được: những trường hợp này chỉ chiếm 2–4% dữ liệu, quá ít để học ra quy luật đáng tin, nhưng lại là tri thức mà người làm nghề nào cũng nắm rõ. Mã hóa chúng thành luật tường minh cho phép hệ thống xử lý đúng ngay cả khi dữ liệu không đủ.""",
    ),
]


def main() -> None:
    source_path = SCRATCHPAD / "chuong3.md"
    text = source_path.read_text(encoding="utf-8")
    original_word_count = len(text.split())

    applied_count = 0
    for original_block, condensed_block in CONDENSED_BLOCKS:
        if original_block not in text:
            print(f"  CANH BAO: khong tim thay doan '{original_block[:55]}...'")
            continue

        text = text.replace(original_block, condensed_block)
        applied_count += 1

    output_path = SCRATCHPAD / "chuong3_rut_gon.md"
    output_path.write_text(text, encoding="utf-8")

    final_word_count = len(text.split())
    print(f"Da ap dung {applied_count}/{len(CONDENSED_BLOCKS)} doan rut gon")
    print(f"Chuong 3: {original_word_count:,} tu -> {final_word_count:,} tu "
          f"(giam {(1 - final_word_count / original_word_count) * 100:.0f}%)")


if __name__ == "__main__":
    main()
