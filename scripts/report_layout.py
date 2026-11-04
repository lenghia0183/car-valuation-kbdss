"""Các tiện ích định dạng quyển báo cáo theo quy định trình bày của nhà trường.

Quy định lấy từ tệp "HDBTL_Hình thức trình bày quyển tiểu luận.docx" và đối chiếu
với bài tiểu luận mẫu đã nộp:

  - Khổ A4, lề trái 3,5 cm, phải 2,0 cm, trên 2,5 cm, dưới 2,0 cm.
  - Times New Roman cỡ 13, giãn dòng 1,3.
  - Số trang đánh ở giữa, phía trên đầu mỗi trang.
  - Phần đầu đánh số La Mã, thân bài đánh số Ả Rập bắt đầu từ MỞ ĐẦU.
  - Tên bảng đặt phía trên bảng, tên hình đặt phía dưới hình, cả hai in đậm.
"""

from __future__ import annotations

from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(13)
LINE_SPACING = 1.3

MARGIN_LEFT = Cm(3.5)
MARGIN_RIGHT = Cm(2.0)
MARGIN_TOP = Cm(2.5)
MARGIN_BOTTOM = Cm(2.0)


def apply_page_setup(section) -> None:
    """Đặt khổ giấy và lề theo đúng quy định."""
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = MARGIN_LEFT
    section.right_margin = MARGIN_RIGHT
    section.top_margin = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM


def _add_field(paragraph, instruction: str) -> None:
    """Chèn một trường của Word (ví dụ PAGE) vào đoạn văn."""
    run = paragraph.add_run()

    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")

    instruction_element = OxmlElement("w:instrText")
    instruction_element.set(qn("xml:space"), "preserve")
    instruction_element.text = instruction

    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")

    placeholder = OxmlElement("w:t")
    placeholder.text = "1"

    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")

    for element in (begin, instruction_element, separate, placeholder, end):
        run._r.append(element)

    run.font.name = BODY_FONT
    run.font.size = BODY_SIZE


def set_page_numbering(section, number_format: str, start_at: int | None) -> None:
    """Đặt kiểu đánh số trang cho một section.

    `number_format` nhận "lowerRoman" cho phần đầu hoặc "decimal" cho thân bài.
    `start_at` khác None sẽ đánh số lại từ giá trị đó.
    """
    section_properties = section._sectPr

    # Xóa cấu hình đánh số cũ nếu có, tránh ghi đè chồng chất.
    for existing in section_properties.findall(qn("w:pgNumType")):
        section_properties.remove(existing)

    page_number_type = OxmlElement("w:pgNumType")
    page_number_type.set(qn("w:fmt"), number_format)
    if start_at is not None:
        page_number_type.set(qn("w:start"), str(start_at))

    section_properties.append(page_number_type)


def add_page_number_to_header(section) -> None:
    """Đánh số trang ở giữa, phía trên đầu trang."""
    section.header.is_linked_to_previous = False

    header_paragraph = section.header.paragraphs[0]
    header_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_paragraph.paragraph_format.space_after = Pt(0)

    for run in list(header_paragraph.runs):
        run._r.getparent().remove(run._r)

    _add_field(header_paragraph, " PAGE ")


def clear_header(section) -> None:
    """Trang bìa không đánh số trang."""
    section.header.is_linked_to_previous = False

    header_paragraph = section.header.paragraphs[0]
    for run in list(header_paragraph.runs):
        run._r.getparent().remove(run._r)


def start_new_section(document) -> object:
    """Bắt đầu một section mới ở trang mới và áp lại thiết lập trang."""
    section = document.add_section(WD_SECTION.NEW_PAGE)
    apply_page_setup(section)
    return section


def add_caption(document, text: str, keep_with_next: bool) -> None:
    """Thêm dòng tên hình hoặc tên bảng, in đậm và căn giữa.

    `keep_with_next` dùng cho tên bảng, để tên luôn nằm cùng trang với bảng.
    """
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = keep_with_next
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(4)

    run = paragraph.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
