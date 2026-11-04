"""Rút gọn Chương 2 và sửa các chỗ mô tả thiết kế không khớp với hệ thống đã cài đặt.

Chương 2 được viết ở giai đoạn thiết kế. Khi cài đặt, một số lựa chọn đã thay đổi:
tập luật dùng công thức nhân lũy thừa thay cho công thức trừ tuyến tính, bộ trọng số
của độ đo tương tự được đặt lại, và một số thuộc tính dự kiến (màu sắc, số đời chủ,
tình trạng tổng thể) không được đưa vào vì người dùng khó khai báo nhất quán.

Giữ nguyên bảng cũ sẽ khiến Chương 2 mâu thuẫn trực tiếp với Chương 3, nên script này
thay chúng bằng mô tả đúng hệ thống thật, đồng thời nén các đoạn liệt kê dài.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

RULE_TABLE_REPLACEMENT = """### 2.7.3. Tập luật sản xuất

Tri thức định giá của chuyên gia được mô hình hóa theo công thức nhân: lấy giá xe mới làm mốc rồi lần lượt nhân với các hệ số do luật suy ra.

> P_luật = P_mới × K_khấu hao × K_số km × K_tình trạng × K_kỹ thuật × K_thị trường

Mỗi hệ số K bằng 1 nếu không có luật nào trong nhóm tương ứng được kích hoạt. Riêng nhóm khấu hao tính trực tiếp từ giá xe mới theo hàm lũy thừa của tuổi xe, vì mỗi luật khấu hao đã bao gồm toàn bộ quá trình mất giá từ lúc xe mới đến tuổi hiện tại.

Tập luật gồm 25 luật chia thành sáu nhóm, trình bày trong Bảng 2.5. Các hệ số là **giá trị khởi tạo** do nhóm đề xuất dựa trên kinh nghiệm thị trường, được kiểm chứng và hiệu chỉnh bằng dữ liệu ở Chương 3.

*Bảng 2.5. Tập luật định giá xe ô tô cũ*

| **Mã** | **Nhóm** | **Điều kiện (IF)** | **Kết luận (THEN)** |
| :- | :- | :- | :- |
| R01–R05 | Khấu hao | Theo khoảng tuổi xe: dưới 1 năm, 1–3, 3–7, 7–15 và trên 15 năm | Hệ số giữ giá tính lũy thừa từ hệ số khấu hao cơ bản của phân khúc; tốc độ khấu hao giảm dần theo tuổi xe, có sàn 0,08 |
| R06–R09 | Số km | Theo số km bình quân mỗi năm: dưới 8.000; 8.000–15.000; 15.000–25.000; trên 25.000 | Hệ số 1,05 / 1,00 / 0,94 / 0,87; nhóm trên 25.000 km sinh cảnh báo nghi xe chạy dịch vụ |
| R10 | Số km | Tổng số km trên 200.000 | Hệ số 0,92; cảnh báo cần kiểm tra động cơ và hộp số |
| R11 | Tình trạng | Xe từng ngập nước | Hệ số 0,70; cảnh báo rủi ro hệ thống điện; hạ độ tin cậy 0,10 |
| R12 | Tình trạng | Xe từng tai nạn nặng | Hệ số 0,78; cảnh báo kiểm tra khung gầm; hạ độ tin cậy 0,08 |
| R13 | Tình trạng | Xe từng đăng ký kinh doanh vận tải | Hệ số 0,88; cảnh báo thanh khoản thấp hơn xe gia đình |
| R14 | Tình trạng | Một chủ, bảo dưỡng hãng đầy đủ | Hệ số 1,04; tăng độ tin cậy 0,05 |
| R15–R16 | Kỹ thuật | Hộp số tự động (AT, CVT) hoặc hộp số sàn | Hệ số 1,02 với hộp số tự động; 0,96 với hộp số sàn ngoài phân khúc bán tải |
| R17 | Kỹ thuật | Máy dầu ở phân khúc SUV hạng D, bán tải hoặc MPV | Hệ số 1,03 |
| R18 | Kỹ thuật | Nhập khẩu nguyên chiếc | Hệ số 1,03 |
| R19–R20 | Thị trường | Luôn áp dụng theo hãng và khu vực rao bán | Nhân hệ số thương hiệu và hệ số khu vực lấy từ khung tri thức |
| R21 | Thị trường | Chỉ số thanh khoản của phân khúc dưới 0,7 | Hệ số 0,96; cảnh báo thời gian bán trung bình dài hơn |
| R22 | Rủi ro | Xe sang trên 8 năm tuổi | Hệ số 0,90; cảnh báo chi phí bảo dưỡng và phụ tùng cao |
| R23 | Rủi ro | Truy hồi được dưới 3 tình huống tương tự | Hạ độ tin cậy 0,15; cảnh báo ít dữ liệu tham chiếu |
| R24 | Rủi ro | Hệ số biến thiên giá của các xe tương tự trên 0,25 | Hạ độ tin cậy 0,10; cảnh báo giá thị trường phân tán mạnh |
| R25 | Rủi ro | Kết quả từ luật và từ tình huống lệch quá 20% | Hạ độ tin cậy 0,12; cảnh báo mâu thuẫn giữa hai nguồn tri thức |

Các siêu luật điều khiển việc áp dụng tập luật gồm bốn quy tắc. Các luật trong nhóm khấu hao (R01–R05) và nhóm số km theo năm (R06–R09) **loại trừ lẫn nhau** vì điều kiện được thiết kế không giao nhau. Các luật rủi ro R11, R12 có **độ ưu tiên cao** nên được xét trước các luật điều chỉnh kỹ thuật và thị trường. Các luật R23–R25 **không thay đổi giá** mà chỉ hạ độ tin cậy và sinh cảnh báo. Cuối cùng, một luật đã kích hoạt **không được kích hoạt lại** trong cùng một phiên suy diễn, bảo đảm vòng lặp suy diễn kết thúc.

Mỗi luật được lưu trong tệp `rules.json` gồm mã, nhóm, độ ưu tiên, mô tả, phần điều kiện và phần hành động, ví dụ:

> {"id": "R11", "group": "tinh_trang", "priority": 80, "if": [{"fact": "ngap_nuoc", "op": "==", "value": true}], "then": [{"type": "multiply", "factor": 0.70, "label": "Xe từng ngập nước"}, {"type": "flag", "value": "Xe từng ngập nước: rủi ro hỏng hệ thống điện"}, {"type": "confidence", "delta": -0.10}]}

Cách lưu trữ này tách biệt tri thức khỏi mã nguồn: kỹ sư tri thức chỉnh sửa luật qua trang quản trị mà không phải lập trình lại. Mỗi khi tập luật thay đổi, chức năng kiểm tra tính nhất quán sẽ phát hiện các luật trùng mã, luật thiếu điều kiện hoặc thiếu hành động.

"""

SIMILARITY_TABLE_REPLACEMENT = """*Bảng 2.6. Trọng số và hàm tương tự cục bộ của các thuộc tính*

| **Thuộc tính** | **Trọng số wi** | **Độ tương tự cục bộ simi** |
| :- | :- | :- |
| Dòng xe | 0,30 | 1 nếu cùng dòng xe, 0 nếu khác |
| Năm sản xuất | 0,22 | max(0; 1 − \\|Δnăm\\| / 6) |
| Số km | 0,18 | max(0; 1 − \\|Δkm\\| / 120.000) |
| Phiên bản | 0,12 | 1 nếu cùng phiên bản, 0 nếu khác |
| Hộp số | 0,06 | 1 nếu trùng, 0 nếu khác |
| Nhiên liệu | 0,04 | 1 nếu trùng, 0 nếu khác |
| Xuất xứ | 0,04 | 1 nếu trùng, 0 nếu khác |
| Khu vực | 0,04 | 1 nếu trùng, 0 nếu khác |
| **Tổng** | **1,00** |  |

Ngoài các trọng số trên, hệ thống áp một ràng buộc cứng: chỉ các tình huống **cùng hãng** mới được xét, các tình huống khác hãng bị gán độ tương tự bằng 0. Ràng buộc này tránh so sánh một chiếc xe phổ thông với một chiếc xe sang cùng phân khúc nhưng khác hẳn mặt bằng giá.

Hệ thống chọn k = 5 tình huống có độ tương tự cao nhất và vượt ngưỡng tối thiểu 0,55. Ở bước Reuse, giá của mỗi tình huống được điều chỉnh về điều kiện của truy vấn theo hai bước: chênh lệch tuổi xe hiệu chỉnh với hệ số 7% mỗi năm, chênh lệch số km hiệu chỉnh với hệ số 1,2% cho mỗi 10.000 km và giới hạn biên độ trong khoảng ±15%.

"""


def _replace_block(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    """Thay toàn bộ khối văn bản từ dấu mốc đầu tới ngay trước dấu mốc cuối."""
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index == -1 or end_index == -1 or end_index <= start_index:
        print(f"  CANH BAO: khong thay the duoc khoi bat dau bang '{start_marker[:40]}'")
        return text

    return text[:start_index] + replacement + text[end_index:]


def _condense_use_case_list(text: str) -> str:
    """Gộp danh sách 11 use case thành một đoạn mô tả ngắn."""
    start_marker = "**Mô tả chi tiết các use case**"
    end_marker = "Đặc tả chi tiết use case trọng tâm"

    replacement = """**Mô tả các use case**

Hệ thống có mười một use case chia theo ba tác nhân. **Người dùng và chuyên viên định giá** dùng các use case Định giá xe (bao gồm Nhập thông tin xe), Xem giải thích và Xem xe tương tự (hai use case mở rộng của Định giá xe), So sánh kịch bản what-if, và Tra cứu thống kê thị trường. **Chuyên viên định giá** còn dùng Phản hồi giá giao dịch thực tế để hệ thống lưu tình huống mới theo bước Retain của chu trình CBR, và Quản lý cơ sở tình huống. **Quản trị viên tri thức** dùng Quản lý tập luật (bao gồm Kiểm tra mâu thuẫn, trùng lặp luật), Cập nhật dữ liệu thị trường, và Huấn luyện – đánh giá mô hình đối chứng.

"""
    return _replace_block(text, start_marker, end_marker, replacement)


def _condense_function_breakdown(text: str) -> str:
    """Rút gọn phần liệt kê chi tiết chữ ký phương thức của năm nhóm chức năng."""
    start_marker = "**Mô tả chi tiết các nhóm chức năng**"
    end_marker = "## 2.6. Kiến trúc hệ thống"

    replacement = """**Mô tả các nhóm chức năng**

Hệ thống được phân rã thành năm nhóm chức năng. **Định giá xe** là nhóm cốt lõi, gồm kiểm tra tính hợp lệ của đầu vào, suy diễn trên tập luật, truy hồi và điều chỉnh các tình huống tương tự, tổng hợp kết quả thành khoảng giá kèm độ tin cậy, và sinh lời giải thích. **Phân tích thị trường** cung cấp thống kê giá theo hãng và dòng xe, đường cong khấu hao, cùng công cụ so sánh kịch bản. **Quản lý tri thức** cho phép thêm, sửa, xóa luật, kiểm tra tính nhất quán, quản lý khung tri thức và cơ sở tình huống. **Quản lý dữ liệu** thực hiện thu thập, làm sạch, chuẩn hóa tin rao và huấn luyện mô hình đối chứng. **Phản hồi và học từ giao dịch** ghi nhận giá giao dịch thực tế, lưu tình huống mới, theo dõi sai số theo thời gian và gợi ý hiệu chỉnh hệ số luật.

"""
    return _replace_block(text, start_marker, end_marker, replacement)


def _condense_worked_example(text: str) -> str:
    """Rút gọn ví dụ minh họa quá trình suy diễn, giữ lại bảng kết quả."""
    start_marker = "### 2.8.5. Ví dụ minh họa quá trình suy diễn"
    end_marker = "## 2.9. Sơ đồ luồng xử lý"

    replacement = """### 2.8.5. Ví dụ minh họa quá trình suy diễn

Xét một chiếc Toyota Fortuner 2.4G AT đời 2019, đã chạy 96.000 km, rao bán tại Hà Nội, một chủ và bảo dưỡng hãng đầy đủ. Giá xe mới tham chiếu của phiên bản này là 1.170 triệu đồng.

Hệ thống lần lượt thực hiện bốn bước. **Bước một**, tra khung tri thức để xác định xe thuộc phân khúc SUV hạng D với hệ số khấu hao cơ bản 0,120 và chỉ số thanh khoản 0,70; hãng Toyota có hệ số thương hiệu 1,06. **Bước hai**, suy ra các thuộc tính dẫn xuất: tuổi xe 7 năm, số km bình quân 13.714 km mỗi năm. **Bước ba**, chạy suy diễn tiến; bảy luật được kích hoạt theo thứ tự độ ưu tiên giảm dần như Bảng 2.8. **Bước bốn**, mô-đun CBR truy hồi năm chiếc Fortuner 2.4G AT cùng đời, cho giá trung bình có trọng số 507 triệu đồng.

Kết quả tổng hợp với hệ số α = 0,35 cho giá đề xuất 518 triệu đồng, khoảng giá 452–585 triệu và độ tin cậy 93%. Toàn bộ quá trình này được minh họa bằng màn hình thật của hệ thống ở Hình 3.4 và Hình 3.5 trong Chương 3.

*Bảng 2.8. Các luật được kích hoạt trong ví dụ minh họa*

| **Mã luật** | **Tác động** | **Hệ số** | **Giá sau khi áp dụng (triệu VND)** |
| :- | :- | --: | --: |
| R04 | Khấu hao 7–15 năm | 0,399 | 466,6 |
| R07 | Km ở mức trung bình | 1,000 | 466,6 |
| R14 | Một chủ, bảo dưỡng hãng đầy đủ | 1,040 | 485,3 |
| R15 | Hộp số tự động | 1,020 | 495,0 |
| R17 | Máy dầu phân khúc SUV/bán tải | 1,030 | 509,9 |
| R19 | Hệ số thương hiệu Toyota | 1,060 | 540,5 |
| R20 | Hệ số khu vực Hà Nội | 1,000 | 540,5 |

"""
    return _replace_block(text, start_marker, end_marker, replacement)


def main() -> None:
    source_path = SCRATCHPAD / "chuong1_2.md"
    text = source_path.read_text(encoding="utf-8")

    # Tách Chương 2 ra khỏi tệp gộp; Chương 1 đã có bản rút gọn riêng.
    chapter_two_index = text.find("# CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")
    if chapter_two_index == -1:
        raise ValueError("Khong tim thay tieu de Chuong 2")

    chapter_two = text[chapter_two_index:]
    original_word_count = len(chapter_two.split())

    chapter_two = _condense_use_case_list(chapter_two)
    chapter_two = _condense_function_breakdown(chapter_two)

    chapter_two = _replace_block(
        chapter_two,
        "### 2.7.3. Tập luật sản xuất",
        "### 2.7.4. Cơ sở tình huống và độ đo tương tự",
        RULE_TABLE_REPLACEMENT,
    )

    chapter_two = _replace_block(
        chapter_two,
        "*Bảng 2.6. Trọng số và hàm tương tự cục bộ của các thuộc tính*",
        "## 2.8. Thiết kế máy suy diễn",
        SIMILARITY_TABLE_REPLACEMENT,
    )

    chapter_two = _condense_worked_example(chapter_two)

    # Bảng 2.9 không còn được dẫn chiếu sau khi rút gọn ví dụ minh họa.
    chapter_two = re.sub(
        r"\*Bảng 2\.9\..*?\n(\|.*\n)+", "", chapter_two
    )

    output_path = SCRATCHPAD / "chuong2_rut_gon.md"
    output_path.write_text(chapter_two, encoding="utf-8")

    final_word_count = len(chapter_two.split())
    print(f"Chuong 2: {original_word_count:,} tu -> {final_word_count:,} tu "
          f"(giam {(1 - final_word_count / original_word_count) * 100:.0f}%)")


if __name__ == "__main__":
    main()
