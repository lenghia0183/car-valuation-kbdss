"""Sắp xếp lại phần đầu quyển và viết phần MỞ ĐẦU theo đúng quy định trình bày.

Quy định yêu cầu thứ tự: Lời cảm ơn, Mục lục, Danh mục các thuật ngữ và chữ viết tắt,
Danh mục hình vẽ, Danh mục bảng biểu. Sau đó MỞ ĐẦU mở đầu thân bài và được đánh số
trang Ả Rập từ 1, với năm mục đánh số: lý do chọn đề tài, mục tiêu nghiên cứu, đối
tượng và phạm vi, kết quả mong muốn, cấu trúc báo cáo.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

# Phần MỞ ĐẦU viết lại theo đúng năm mục mà quy định yêu cầu, giữ nguyên nội dung
# và số liệu của bản gốc, chỉ tổ chức lại cho khớp cấu trúc.
OPENING_SECTION = """# MỞ ĐẦU

## 1. Lý do lựa chọn đề tài

Cùng với tốc độ tăng trưởng nhanh của số lượng ô tô cá nhân, thị trường xe ô tô đã qua sử dụng tại Việt Nam ngày càng sôi động. Mỗi ngày có rất nhiều tin rao bán xe cũ được đăng trên các sàn trực tuyến như Bonbanh, Chợ Tốt Xe, Oto.com.vn, bên cạnh hoạt động thu mua của các salon và đại lý chính hãng. Tuy nhiên, việc xác định **một mức giá hợp lý** cho một chiếc xe cũ vẫn là bài toán khó: giá xe phụ thuộc đồng thời vào hãng, dòng xe, phiên bản, năm sản xuất, số km đã đi, lịch sử sử dụng, tình trạng thực tế và biến động thị trường.

Trên thực tế, người mua và người bán thường định giá dựa vào cảm tính hoặc so sánh thủ công với một vài tin rao; các salon dựa vào kinh nghiệm của thợ định giá – một dạng **tri thức ẩn** khó chia sẻ, khó kiểm chứng và không nhất quán giữa các cá nhân. Ngược lại, các mô hình học máy thuần túy có thể dự đoán giá khá tốt khi đủ dữ liệu nhưng hoạt động như một "hộp đen": không giải thích được vì sao chiếc xe có mức giá đó, và khó đưa vào những tri thức chuyên gia quan trọng nhưng hiếm gặp trong dữ liệu, chẳng hạn xe từng ngập nước hay tai nạn nặng.

Công nghệ tri thức cung cấp hướng tiếp cận phù hợp cho bài toán này. Bằng cách **hiện hóa tri thức chuyên gia** thành tập luật, **khai thác kinh nghiệm thị trường** dưới dạng cơ sở tình huống và **bổ trợ bằng khai phá dữ liệu**, có thể xây dựng một hệ hỗ trợ quyết định vừa đưa ra khoảng giá đề xuất, vừa giải thích được lý do, vừa cảnh báo rủi ro. Xuất phát từ yêu cầu đó, nhóm lựa chọn đề tài "Hệ hỗ trợ quyết định dựa trên tri thức cho định giá xe ô tô cũ tại thị trường Việt Nam".

## 2. Mục tiêu nghiên cứu

  - Hệ thống hóa cơ sở lý thuyết về tri thức, hệ chuyên gia, lập luận dựa trên tình huống, khai phá dữ liệu và hệ hỗ trợ ra quyết định dựa trên tri thức.
  - Xây dựng cơ sở tri thức cho miền định giá xe ô tô cũ, gồm khung tri thức về hãng – dòng – phiên bản, tập luật khấu hao và điều chỉnh giá, cùng cơ sở tình huống từ dữ liệu tin rao.
  - Thiết kế máy suy diễn lai kết hợp suy diễn tiến trên tập luật với lập luận dựa trên tình huống, có mô hình học máy làm kênh kiểm chứng chéo.
  - Cài đặt sản phẩm demo và đánh giá độ chính xác, khả năng giải thích của hệ thống trên dữ liệu thực nghiệm.

## 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu** của đề tài gồm các phương pháp biểu diễn tri thức bằng khung và luật sản xuất, kỹ thuật suy diễn tiến, lập luận dựa trên tình huống theo chu trình 4R, các kỹ thuật khai phá dữ liệu phục vụ thu nhận tri thức, và kiến trúc hệ hỗ trợ quyết định dựa trên tri thức.

**Phạm vi nghiên cứu** giới hạn ở xe du lịch dưới 9 chỗ đã qua sử dụng, giao dịch tại thị trường Việt Nam. Cơ sở tri thức bao phủ 55 phiên bản thuộc 28 dòng xe của 12 hãng phổ biến. Đề tài không đi sâu vào thẩm định kỹ thuật trực tiếp chiếc xe; các thông tin về tình trạng và lịch sử sử dụng do người dùng khai báo.

## 4. Kết quả mong muốn đạt được của đề tài

  - Một cơ sở tri thức có cấu trúc gồm khung tri thức phân cấp, tập luật sản xuất có độ ưu tiên và cơ sở tình huống từ dữ liệu tin rao.
  - Một hệ thống chạy được, trả về khoảng giá đề xuất kèm mức độ tin cậy, cảnh báo rủi ro và lời giải thích truy vết được tới từng luật.
  - Kết quả đánh giá định lượng cho thấy hệ lai kết hợp hai nguồn tri thức tốt hơn từng phương pháp đơn lẻ.
  - Giao diện web cho phép định giá, xem giải thích, phân tích thị trường và quản trị cơ sở tri thức.

## 5. Cấu trúc báo cáo

Ngoài phần Mở đầu, Kết luận và Tài liệu tham khảo, báo cáo được bố cục thành ba chương:

  - **Chương 1. Tìm hiểu công nghệ tri thức và ứng dụng:** trình bày cơ sở lý thuyết về tri thức, hệ chuyên gia, lập luận dựa trên tình huống, khai phá dữ liệu, hệ hỗ trợ ra quyết định và khảo sát bài toán định giá xe ô tô cũ tại Việt Nam.
  - **Chương 2. Phân tích và thiết kế hệ thống:** phân tích yêu cầu, thiết kế use case, kiến trúc ba tầng, cơ sở tri thức, máy suy diễn và cơ chế ra quyết định.
  - **Chương 3. Thực nghiệm và đánh giá:** trình bày môi trường thực nghiệm, dữ liệu, quá trình cài đặt và kết quả đánh giá hệ thống.
"""


def main() -> None:
    source_text = (SCRATCHPAD / "phan_dau.md").read_text(encoding="utf-8")

    def extract_section(heading: str, text: str) -> str:
        """Lấy nội dung một phần cấp 1 tính từ tiêu đề tới tiêu đề cấp 1 kế tiếp."""
        pattern = rf"^# {re.escape(heading)}$"
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match is None:
            raise ValueError(f"Khong tim thay phan '{heading}'")

        start = match.start()
        following = re.search(r"^# ", text[match.end():], flags=re.MULTILINE)
        end = match.end() + following.start() if following else len(text)

        return text[start:end].rstrip() + "\n"

    acknowledgement = extract_section("LỜI CẢM ƠN", source_text)
    abbreviations = extract_section("DANH MỤC TỪ VIẾT TẮT", source_text)
    figure_list = extract_section("DANH MỤC HÌNH ẢNH", source_text)
    table_list = extract_section("DANH MỤC BẢNG BIỂU", source_text)

    # Đổi tên hai danh mục cho khớp thuật ngữ của quy định trình bày.
    abbreviations = abbreviations.replace(
        "# DANH MỤC TỪ VIẾT TẮT",
        "# DANH MỤC CÁC THUẬT NGỮ, KÝ HIỆU VÀ CÁC CHỮ VIẾT TẮT",
    )
    figure_list = figure_list.replace("# DANH MỤC HÌNH ẢNH", "# DANH MỤC HÌNH VẼ")

    # Lời cảm ơn đứng trước mục lục nên được dựng riêng, phần còn lại đi sau mục lục.
    (SCRATCHPAD / "loi_cam_on.md").write_text(acknowledgement, encoding="utf-8")

    front_matter = "\n".join([abbreviations, figure_list, table_list])
    (SCRATCHPAD / "phan_dau_sau_muc_luc.md").write_text(front_matter, encoding="utf-8")

    (SCRATCHPAD / "mo_dau.md").write_text(OPENING_SECTION, encoding="utf-8")

    for name in ["loi_cam_on.md", "phan_dau_sau_muc_luc.md", "mo_dau.md"]:
        content = (SCRATCHPAD / name).read_text(encoding="utf-8")
        print(f"{name:28} {len(content.split()):>6,} tu")


if __name__ == "__main__":
    main()
