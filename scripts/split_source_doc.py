"""Tách nội dung bản gốc đã tải từ Google Docs thành các tệp Markdown nguồn.

Bản gốc có mục lục và danh mục hình/bảng theo cấu trúc bốn chương cũ, trong khi thân bài
đã được sửa thành ba chương. Script này giữ lại phần thân bài còn dùng được (Chương 1,
Chương 2, lời cảm ơn, lời mở đầu, tài liệu tham khảo) và bỏ phần mục lục lỗi thời cùng
Chương 3 chỉ có tiêu đề.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)
SOURCE_PATH = SCRATCHPAD / "doc.md"

# Danh mục hình ảnh và bảng biểu dựng lại theo cấu trúc ba chương.
# Bản gốc đánh số theo cấu trúc bốn chương cũ nên không dùng lại được.
FIGURE_AND_TABLE_LISTS = """# DANH MỤC HÌNH ẢNH

Hình 1.1. Kiến trúc tổng quát của hệ chuyên gia

Hình 1.2. Chu trình lập luận dựa trên tình huống (4R)

Hình 1.3. Quy trình khám phá tri thức từ dữ liệu (KDD)

Hình 1.4. Các thành phần của hệ hỗ trợ ra quyết định

Hình 2.1. Biểu đồ use case tổng quát của hệ thống

Hình 2.2. Sơ đồ phân rã chức năng của hệ thống

Hình 2.3. Sơ đồ khối kiến trúc tổng thể của hệ thống

Hình 2.4. Biểu đồ hoạt động của chức năng định giá xe

Hình 2.5. Biểu đồ tuần tự của chức năng định giá xe

Hình 3.1. Phân bố giá xe trong tập dữ liệu sau làm sạch

Hình 3.2. Số lượng tin rao theo hãng xe

Hình 3.3. Trang Định giá – biểu mẫu nhập thông tin xe

Hình 3.4. Trang Kết quả và giải thích – các chỉ số chính và khoảng giá

Hình 3.5. Vết suy diễn – bảng luật đã kích hoạt và biểu đồ thác nước

Hình 3.6. Danh sách xe tương tự được truy hồi từ cơ sở tình huống

Hình 3.7. Trang Phân tích thị trường

Hình 3.8. Trang Quản trị tri thức – tập luật sản xuất

Hình 3.9. Kết quả kiểm tra tính nhất quán của cơ sở tri thức

Hình 3.10. Giá đề xuất so với giá thực tế trên tập kiểm thử

Hình 3.11. So sánh bốn phương pháp định giá

Hình 3.12. Sai số phần trăm tuyệt đối trung bình theo phân khúc

Hình 3.13. Sai số định giá theo nhóm tuổi xe

Hình 3.14. Kết quả kịch bản KB2 – xe từng ngập nước với cảnh báo rủi ro

# DANH MỤC BẢNG BIỂU

Bảng 1.1. Sáu mô hình hệ thống thông minh dựa trên tri thức và vai trò trong đề tài

Bảng 1.2. Biểu diễn tri thức miền định giá xe bằng logic vị từ

Bảng 1.3. Các yếu tố ảnh hưởng đến giá xe ô tô cũ

Bảng 2.1. Các tác nhân của hệ thống

Bảng 2.2. Đặc tả use case "Định giá xe"

Bảng 2.3. Công nghệ sử dụng trong hệ thống

Bảng 2.4. Các khe của khung XE

Bảng 2.5. Tập luật định giá xe ô tô cũ

Bảng 2.6. Trọng số và hàm tương tự cục bộ của các thuộc tính

Bảng 2.7. Quy tắc chọn hệ số α

Bảng 2.8. Các luật được kích hoạt trong ví dụ minh họa

Bảng 2.9. Các tình huống tương tự được truy hồi trong ví dụ minh họa

Bảng 2.10. Cấu trúc bảng tình huống (cases)

Bảng 3.1. Môi trường và công cụ cài đặt hệ thống

Bảng 3.2. Mô tả các thuộc tính của bộ dữ liệu

Bảng 3.3. Thống kê mô tả các thuộc tính số

Bảng 3.4. Kết quả các bước làm sạch dữ liệu

Bảng 3.5. Hệ số khấu hao cơ bản và thanh khoản theo phân khúc

Bảng 3.6. Đối chiếu tỷ lệ giữ giá giữa tập luật và dữ liệu

Bảng 3.7. Trọng số các thuộc tính trong độ đo tương tự

Bảng 3.8. Quy tắc chọn hệ số α

Bảng 3.9. So sánh bốn phương pháp định giá trên tập kiểm thử 584 xe

Bảng 3.10. Sai số của hệ lai theo phân khúc

Bảng 3.11. Sai số của hệ lai theo nhóm tuổi xe

Bảng 3.12. Kết quả năm kịch bản định giá điển hình
"""


def _strip_comment_markers(text: str) -> str:
    """Bỏ các thẻ đánh dấu vị trí comment mà Google Docs chèn vào nội dung."""
    text = re.sub(r"<comment_start id=[^>]+>", "", text)
    return re.sub(r"<comment_end id=[^>]+>", "", text)


def _strip_heading_links(text: str) -> str:
    """Bỏ các liên kết nội bộ dạng [nội dung](#heading=...) nhưng giữ lại phần nội dung."""
    return re.sub(r"\[([^\]]*)\]\(#heading=[^)]*\)", r"\1", text)


def _normalize_escapes(text: str) -> str:
    """Bỏ các ký tự thoát của Markdown mà bản xuất Google Docs thêm vào."""
    for escaped, plain in [
        (r"\[", "["), (r"\]", "]"), (r"\!", "!"),
        (r"\.", "."), (r"\-", "-"), (r"\_", "_"),
    ]:
        text = text.replace(escaped, plain)
    return text


def _clean(text: str) -> str:
    text = _strip_comment_markers(text)
    text = _strip_heading_links(text)
    text = _normalize_escapes(text)

    # Bỏ các chỗ đánh dấu ảnh rỗng của bản gốc; ảnh sẽ được chèn lại từ tệp thật.
    text = text.replace("[image]", "")

    # Chuẩn hóa tiêu đề: Google Docs xuất ra dạng "# **Tiêu đề**".
    text = re.sub(r"^(#{1,3})\s*\*{1,3}(.+?)\*{1,3}\s*$", r"\1 \2", text, flags=re.MULTILINE)

    return text


def _align_design_with_implementation(text: str) -> str:
    """Sửa các con số trong phần thiết kế cho khớp với hệ thống đã cài đặt thật.

    Chương 2 được viết ở giai đoạn thiết kế nên nêu một số dự kiến khác với kết quả
    cài đặt cuối cùng (phiên bản Python, quy mô cơ sở tình huống, mô hình đối chứng,
    kho lưu trữ). Giữ nguyên các con số đó sẽ khiến Chương 2 mâu thuẫn với Chương 3.
    """
    replacements: list[tuple[str, str]] = [
        (
            "Xây dựng **cơ sở tình huống** từ dữ liệu tin rao đã làm sạch "
            "(mục tiêu từ 5.000 tình huống trở lên).",
            "Xây dựng **cơ sở tình huống** từ dữ liệu tin rao đã làm sạch "
            "(mục tiêu từ 2.000 tình huống trở lên, bao phủ toàn bộ các dòng xe "
            "có trong khung tri thức).",
        ),
        (
            "**Hiệu năng:** phản hồi dưới 2 giây cho một yêu cầu định giá với "
            "cơ sở tình huống khoảng 10.000 bản ghi.",
            "**Hiệu năng:** phản hồi dưới 2 giây cho một yêu cầu định giá với "
            "cơ sở tình huống khoảng vài nghìn bản ghi.",
        ),
        ("| Ngôn ngữ lập trình | Python 3.11 |", "| Ngôn ngữ lập trình | Python 3.13 |"),
        (
            "| Cơ sở tri thức | JSON (luật, khung), SQLite (tình huống, lịch sử) |",
            "| Cơ sở tri thức | JSON (luật, khung), CSV (cơ sở tình huống) |",
        ),
        (
            "| Học máy | scikit-learn | Huấn luyện Linear Regression, Random Forest |",
            "| Học máy | scikit-learn | Huấn luyện mô hình đối chứng Random Forest |",
        ),
        (
            "cơ sở tình huống và lịch sử định giá (lưu trong SQLite)",
            "cơ sở tình huống (lưu dưới dạng CSV) và lịch sử định giá",
        ),
    ]

    for original, replacement in replacements:
        if original not in text:
            print(f"  CANH BAO: khong tim thay doan can sua: {original[:60]}...")
            continue
        text = text.replace(original, replacement)

    return text


def main() -> None:
    lines = SOURCE_PATH.read_text(encoding="utf-8").split("\n")

    def find_line(predicate, start: int = 0) -> int:
        for index in range(start, len(lines)):
            if predicate(lines[index]):
                return index
        raise ValueError("Khong tim thay dong phu hop")

    # Phần đầu: lấy từ TIÊU ĐỀ "DANH MỤC TỪ VIẾT TẮT" (dòng bắt đầu bằng dấu thăng)
    # chứ không phải dòng cùng tên nằm trong mục lục cũ ở đầu tài liệu.
    abbreviations_start = find_line(
        lambda line: line.startswith("#") and "DANH MỤC TỪ VIẾT TẮT" in line
    )
    chapter_one_start = find_line(lambda line: line.startswith("# **CHƯƠNG 1."))

    front_matter = "\n".join(lines[abbreviations_start:chapter_one_start])

    # Chương 1 và Chương 2: giữ nguyên, kết thúc ngay trước Chương 3.
    chapter_three_start = find_line(lambda line: line.startswith("# **CHƯƠNG 3."))
    chapters_one_two = "\n".join(lines[chapter_one_start:chapter_three_start])

    # Tài liệu tham khảo: từ tiêu đề tới hết tệp.
    references_start = find_line(lambda line: "TÀI LIỆU THAM KHẢO" in line and line.startswith("#"))
    references = "\n".join(lines[references_start:])

    # Mục [12] của bản gốc ghi nguồn dữ liệu là các sàn rao vặt, nhưng thực nghiệm
    # được chạy trên dữ liệu mô phỏng nên phải ghi đúng bản chất.
    references = re.sub(
        r"\[12\][^\n]*",
        "[12] Mặt bằng giá xe mới niêm yết dùng làm tham chiếu cho khung tri thức được "
        "tổng hợp từ bảng giá công bố của các hãng xe tại Việt Nam. Dữ liệu tin rao dùng "
        "trong thực nghiệm là dữ liệu mô phỏng do nhóm sinh ra, xem mục 3.1.2.",
        references,
    )

    chapters_one_two = _align_design_with_implementation(chapters_one_two)

    outputs = {
        "phan_dau.md": FIGURE_AND_TABLE_LISTS + "\n" + front_matter,
        "chuong1_2.md": chapters_one_two,
        "tai_lieu.md": references,
    }

    for filename, content in outputs.items():
        cleaned = _clean(content)
        (SCRATCHPAD / filename).write_text(cleaned, encoding="utf-8")
        print(f"Da tao {filename}: {len(cleaned.splitlines())} dong")


if __name__ == "__main__":
    main()
