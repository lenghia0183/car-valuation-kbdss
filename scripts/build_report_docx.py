"""Dựng báo cáo DOCX hoàn chỉnh từ nội dung gốc, nội dung Chương 3 mới và ảnh thực nghiệm.

Bản gốc trên Google Docs đã được sửa phần thân bài theo góp ý của giảng viên (gộp còn
ba chương), nhưng mục lục, danh mục hình/bảng vẫn theo cấu trúc bốn chương cũ và toàn bộ
Chương 3 mới chỉ có tiêu đề. Script này dựng lại tài liệu hoàn chỉnh:

  - giữ nguyên Chương 1 và Chương 2 của bản gốc;
  - thay mục lục và danh mục hình/bảng theo cấu trúc ba chương;
  - thay toàn bộ Chương 3 và Kết luận bằng nội dung viết từ kết quả chạy thật;
  - chèn các biểu đồ và ảnh chụp màn hình vào đúng vị trí.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import report_layout

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
SCREENSHOT_DIR = PROJECT_ROOT / "outputs" / "screenshots"

# Ảnh lấy lại từ bản gốc trên Google Docs: logo trường và các sơ đồ của Chương 1, 2.
ORIGINAL_MEDIA_DIR = PROJECT_ROOT / "source_doc" / "media"
SCHOOL_LOGO = ORIGINAL_MEDIA_DIR / "image1.png"

# Sơ đồ gốc được chèn ngay trước dòng chú thích tương ứng.
ORIGINAL_DIAGRAMS: dict[str, Path] = {
    "Hình 1.1. Kiến trúc tổng quát của hệ chuyên gia": ORIGINAL_MEDIA_DIR / "image3.png",
    "Hình 1.2. Chu trình lập luận dựa trên tình huống (4R)": ORIGINAL_MEDIA_DIR / "image2.png",
    "Hình 1.3. Quy trình khám phá tri thức từ dữ liệu (KDD)": ORIGINAL_MEDIA_DIR / "image4.png",
    "Hình 1.4. Các thành phần của hệ hỗ trợ ra quyết định": ORIGINAL_MEDIA_DIR / "image5.png",
    "Hình 2.1. Biểu đồ use case tổng quát của hệ thống": ORIGINAL_MEDIA_DIR / "image8.png",
    "Hình 2.2. Sơ đồ phân rã chức năng của hệ thống": ORIGINAL_MEDIA_DIR / "image6.png",
    "Hình 2.3. Sơ đồ khối kiến trúc tổng thể của hệ thống": ORIGINAL_MEDIA_DIR / "image9.png",
    "Hình 2.4. Biểu đồ hoạt động của chức năng định giá xe": ORIGINAL_MEDIA_DIR / "image7.png",
    "Hình 2.5. Biểu đồ tuần tự của chức năng định giá xe": ORIGINAL_MEDIA_DIR / "image10.png",
}
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "Bao-cao-BTL-Cong-nghe-tri-thuc.docx"

BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(13)
LINE_SPACING = 1.3

# Ảnh được chèn vào ngay sau đoạn văn có chứa chuỗi khóa tương ứng.
FIGURE_PLACEMENTS: list[tuple[str, Path, str]] = [
    ("Hình 3.1 thể hiện trực quan phân bố này",
     FIGURE_DIR / "hinh_phan_bo_gia.png",
     "Hình 3.1. Phân bố giá xe trong tập dữ liệu sau làm sạch"),
    ("phản ánh đúng thực tế xe sang thanh khoản thấp (Hình 3.2)",
     FIGURE_DIR / "hinh_tin_rao_theo_hang.png",
     "Hình 3.2. Số lượng tin rao theo hãng xe"),
    ("danh sách phiên bản cũng lọc lại tương ứng",
     SCREENSHOT_DIR / "01_trang_dinh_gia.png",
     "Hình 3.3. Trang Định giá – biểu mẫu nhập thông tin xe"),
    ("giá sau hiệu chỉnh (Hình 3.6)",
     SCREENSHOT_DIR / "03_ket_qua_va_giai_thich.png",
     "Hình 3.4. Trang Kết quả và giải thích – các chỉ số chính và khoảng giá"),
    ("__AFTER_FIG_3_4__",
     SCREENSHOT_DIR / "04_vet_suy_dien.png",
     "Hình 3.5. Vết suy diễn – bảng luật đã kích hoạt và biểu đồ thác nước"),
    ("__AFTER_FIG_3_5__",
     SCREENSHOT_DIR / "05_xe_tuong_tu.png",
     "Hình 3.6. Danh sách xe tương tự được truy hồi từ cơ sở tình huống"),
    ("biểu đồ phân tán quan hệ giữa số km và giá bán",
     SCREENSHOT_DIR / "07_phan_tich_thi_truong_day_du.png",
     "Hình 3.7. Trang Phân tích thị trường"),
    ("cả sáu phép kiểm tra đều đạt (Hình 3.9)",
     SCREENSHOT_DIR / "08_quan_tri_tri_thuc.png",
     "Hình 3.8. Trang Quản trị tri thức – tập luật sản xuất"),
    ("__AFTER_FIG_3_8__",
     SCREENSHOT_DIR / "09_kiem_tra_nhat_quan.png",
     "Hình 3.9. Kết quả kiểm tra tính nhất quán của cơ sở tri thức"),
    ("độ phân tán tăng dần theo giá",
     FIGURE_DIR / "hinh_du_doan_vs_thuc_te.png",
     "Hình 3.10. Giá đề xuất so với giá thực tế trên tập kiểm thử"),
    ("Hình 3.11 biểu diễn trực quan so sánh này",
     FIGURE_DIR / "hinh_so_sanh_phuong_phap.png",
     "Hình 3.11. So sánh bốn phương pháp định giá"),
    ("MAPE dao động trong khoảng hẹp",
     FIGURE_DIR / "hinh_sai_so_theo_phan_khuc.png",
     "Hình 3.12. Sai số phần trăm tuyệt đối trung bình theo phân khúc"),
    ("MAE giảm đều theo tuổi xe",
     FIGURE_DIR / "hinh_sai_so_theo_tuoi_xe.png",
     "Hình 3.13. Sai số định giá theo nhóm tuổi xe"),
    ("Hình 3.14 minh họa kịch bản KB2",
     SCREENSHOT_DIR / "10_canh_bao_rui_ro.png",
     "Hình 3.14. Kết quả kịch bản KB2 – xe từng ngập nước với cảnh báo rủi ro"),
]


def _configure_styles(document: Document) -> None:
    normal_style = document.styles["Normal"]
    normal_style.font.name = BODY_FONT
    normal_style.font.size = BODY_SIZE
    normal_style.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)

    paragraph_format = normal_style.paragraph_format
    paragraph_format.line_spacing = LINE_SPACING
    paragraph_format.space_after = Pt(3)
    paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Tiêu đề dùng chữ đen in đậm như bài mẫu, không dùng màu.
    for heading_name, size, alignment in [
        ("Heading 1", Pt(14), WD_ALIGN_PARAGRAPH.CENTER),
        ("Heading 2", Pt(13), WD_ALIGN_PARAGRAPH.LEFT),
        ("Heading 3", Pt(13), WD_ALIGN_PARAGRAPH.LEFT),
    ]:
        style = document.styles[heading_name]
        style.font.name = BODY_FONT
        style.font.size = size
        style.font.bold = True
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        style.paragraph_format.space_before = Pt(8)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.alignment = alignment
        style.paragraph_format.keep_with_next = True


def _configure_page(document: Document) -> None:
    for section in document.sections:
        report_layout.apply_page_setup(section)


def _tighten_toc_styles(document: Document) -> None:
    """Siết giãn dòng của các mức mục lục để mục lục không tràn trang không cần thiết."""
    for level in (1, 2, 3):
        style_name = f"TOC {level}"
        if style_name not in [style.name for style in document.styles]:
            continue

        paragraph_format = document.styles[style_name].paragraph_format
        paragraph_format.line_spacing = 1.15
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)


def _add_table_of_contents_field(document: Document) -> None:
    """Chèn trường mục lục tự động; Word sẽ sinh nội dung khi người dùng cập nhật trường."""
    _tighten_toc_styles(document)

    paragraph = document.add_paragraph()
    run = paragraph.add_run()

    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")

    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    # Chỉ lấy tiêu đề cấp 1 và 2; đưa cả cấp 3 vào làm mục lục dài tới bốn trang.
    instruction.text = r'TOC \o "1-2" \h \z \u'

    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")

    placeholder = OxmlElement("w:t")
    placeholder.text = (
        "Nhấn chuột phải vào đây rồi chọn Update Field để sinh mục lục tự động."
    )

    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")

    for element in (begin, instruction, separate, placeholder, end):
        run._r.append(element)


def _add_caption(document: Document, text: str) -> None:
    """Tên hình đặt phía dưới hình, in đậm theo quy định trình bày."""
    report_layout.add_caption(document, text, keep_with_next=False)


def _resolve_image_width(image_path: Path) -> Cm:
    """Ảnh chụp màn hình rất cao nên để hẹp hơn biểu đồ, tránh chiếm trọn một trang."""
    tall_screenshots = {
        "04_vet_suy_dien.png",
        "07_phan_tich_thi_truong_day_du.png",
    }

    if image_path.name in tall_screenshots:
        return Cm(8.0)
    if image_path.parent.name == "screenshots":
        return Cm(11.0)
    # Sơ đồ gốc của Chương 1 và 2 nhiều chữ nhỏ nên để rộng gần hết khung chữ.
    if image_path.parent.name == "media":
        return Cm(12.0)

    # Biểu đồ ba khung ngang có nhiều nhãn nhỏ nên phải để rộng mới đọc được.
    if image_path.name == "hinh_so_sanh_phuong_phap.png":
        return Cm(15.5)

    return Cm(10.5)


def _add_figure(document: Document, image_path: Path, caption: str) -> None:
    if not image_path.exists():
        print(f"  CANH BAO: khong tim thay anh {image_path.name}")
        return

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(0)

    image_width = _resolve_image_width(image_path)
    paragraph.add_run().add_picture(str(image_path), width=image_width)
    _add_caption(document, caption)


def _apply_inline_formatting(paragraph, text: str) -> None:
    """Chuyển cú pháp **đậm** và *nghiêng* của Markdown thành định dạng của Word."""
    tokens = re.split(r"(\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`)", text)

    for token in tokens:
        if not token:
            continue

        if token.startswith("**") and token.endswith("**"):
            paragraph.add_run(token[2:-2]).bold = True
        elif token.startswith("*") and token.endswith("*"):
            paragraph.add_run(token[1:-1]).italic = True
        elif token.startswith("`") and token.endswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(11)
        else:
            paragraph.add_run(token)


def _repeat_header_row(row) -> None:
    """Đánh dấu một dòng là dòng tiêu đề để Word lặp lại nó ở mỗi trang."""
    row_properties = row._tr.get_or_add_trPr()
    header_marker = OxmlElement("w:tblHeader")
    header_marker.set(qn("w:val"), "true")
    row_properties.append(header_marker)


def _prevent_row_split(row) -> None:
    """Không cho nội dung của một dòng bị cắt làm đôi qua hai trang."""
    row_properties = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    row_properties.append(cant_split)


def _add_markdown_table(document: Document, table_lines: list[str]) -> None:
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in table_lines
        if not re.match(r"^\s*\|[\s:|-]+\|\s*$", line)
    ]

    if not rows:
        return

    column_count = max(len(row) for row in rows)
    table = document.add_table(rows=len(rows), cols=column_count)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Khi bảng bị ngắt sang trang mới, dòng tiêu đề được lặp lại để vẫn đọc được cột.
    _repeat_header_row(table.rows[0])
    for table_row in table.rows:
        _prevent_row_split(table_row)

    for row_index, row_cells in enumerate(rows):
        for column_index in range(column_count):
            cell = table.cell(row_index, column_index)
            cell_text = row_cells[column_index] if column_index < len(row_cells) else ""

            cell_paragraph = cell.paragraphs[0]
            cell_paragraph.paragraph_format.line_spacing = 1.0
            cell_paragraph.paragraph_format.space_after = Pt(1)
            cell_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

            _apply_inline_formatting(cell_paragraph, cell_text)

            for run in cell_paragraph.runs:
                run.font.size = Pt(10)
                if row_index == 0:
                    run.bold = True

    document.add_paragraph().paragraph_format.space_after = Pt(6)


def _render_markdown(document: Document, markdown_text: str, figure_state: dict) -> None:
    lines = markdown_text.split("\n")
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        # Bảng Markdown: gom toàn bộ các dòng liên tiếp bắt đầu bằng dấu gạch đứng.
        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1

            _add_markdown_table(document, table_lines)
            _flush_pending_figures(document, figure_state, table_lines)
            continue

        # Dòng chú thích của một sơ đồ gốc: chèn ảnh trước rồi mới ghi chú thích.
        # Chỉ áp dụng trong thân bài; ở danh mục hình ảnh, các dòng trùng tên
        # phải giữ nguyên dạng liệt kê chứ không chèn ảnh.
        caption_text = stripped.strip("*").strip()
        if figure_state.get("in_body") and caption_text in ORIGINAL_DIAGRAMS:
            _add_figure(document, ORIGINAL_DIAGRAMS[caption_text], caption_text)
            index += 1
            continue

        if re.match(r"^\*{1,2}Bảng \d+\.\d+\..*\*{1,2}$", stripped):
            # Tên bảng đặt phía trên bảng và phải nằm cùng trang với bảng đó.
            report_layout.add_caption(document, stripped.strip("*"), keep_with_next=True)
        elif stripped.startswith("### "):
            document.add_heading(stripped[4:], level=3)
        elif stripped.startswith("## "):
            document.add_heading(stripped[3:], level=2)
        elif stripped.startswith("# "):
            heading_text = stripped[2:]

            # Mỗi phần cấp 1 bắt đầu ở trang mới. Riêng ba danh mục ở phần đầu quyển
            # đều rất ngắn nên để chạy liền nhau, tránh ba trang gần như trống.
            is_short_list = heading_text.startswith("DANH MỤC")
            needs_page_break = (
                figure_state.get("has_written_section")
                and not (is_short_list and figure_state.get("previous_was_short_list"))
            )

            if needs_page_break:
                document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

            document.add_heading(heading_text, level=1)
            figure_state["has_written_section"] = True
            figure_state["previous_was_short_list"] = is_short_list

            # Từ chương đầu tiên trở đi mới là thân bài, nơi ảnh được chèn thật.
            if stripped.startswith("# CHƯƠNG"):
                figure_state["in_body"] = True
        elif stripped.startswith("> "):
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Cm(1.2)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.add_run(stripped[2:])
            run.italic = True
            run.bold = True
        elif stripped.startswith("- ") or stripped.startswith("  - "):
            paragraph = document.add_paragraph(style="List Bullet")
            paragraph.paragraph_format.line_spacing = LINE_SPACING
            _apply_inline_formatting(paragraph, stripped.lstrip("- ").strip())
        elif re.match(r"^\d+\.\s", stripped):
            paragraph = document.add_paragraph(style="List Number")
            paragraph.paragraph_format.line_spacing = LINE_SPACING
            _apply_inline_formatting(paragraph, re.sub(r"^\d+\.\s", "", stripped))
        else:
            paragraph = document.add_paragraph()
            _apply_inline_formatting(paragraph, stripped)

            # Các dòng của danh mục hình ảnh và bảng biểu được xếp sát nhau cho gọn.
            if re.match(r"^(Hình|Bảng) \d+\.\d+\.", stripped):
                paragraph.paragraph_format.line_spacing = 1.15
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

            _flush_pending_figures(document, figure_state, [stripped])

        index += 1


def _flush_pending_figures(document: Document, figure_state: dict, context_lines: list[str]) -> None:
    """Chèn các ảnh có chuỗi khóa khớp với đoạn vừa ghi."""
    context = " ".join(context_lines)

    for placement_index, (anchor, image_path, caption) in enumerate(FIGURE_PLACEMENTS):
        if placement_index in figure_state["inserted"]:
            continue

        if anchor.startswith("__"):
            continue

        if anchor in context:
            _add_figure(document, image_path, caption)
            figure_state["inserted"].add(placement_index)

            # Chèn tiếp các ảnh được neo "ngay sau ảnh trước đó".
            _flush_chained_figures(document, figure_state, placement_index)


def _flush_chained_figures(document: Document, figure_state: dict, previous_index: int) -> None:
    chain_anchors = {
        3: "__AFTER_FIG_3_4__",
        4: "__AFTER_FIG_3_5__",
        7: "__AFTER_FIG_3_8__",
    }

    anchor_name = chain_anchors.get(previous_index)
    if anchor_name is None:
        return

    for placement_index, (anchor, image_path, caption) in enumerate(FIGURE_PLACEMENTS):
        if anchor == anchor_name and placement_index not in figure_state["inserted"]:
            _add_figure(document, image_path, caption)
            figure_state["inserted"].add(placement_index)
            _flush_chained_figures(document, figure_state, placement_index)


def _add_cover_page(document: Document) -> None:
    def centered(text: str, size: int, bold: bool = True, space_after: int = 6):
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_after = Pt(space_after)
        run = paragraph.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        return paragraph

    centered("BỘ CÔNG THƯƠNG", 14)
    centered("TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI", 15, space_after=18)

    # Logo trường lấy từ bản gốc, đặt đúng vị trí như trang bìa của bản gốc.
    if SCHOOL_LOGO.exists():
        logo_paragraph = document.add_paragraph()
        logo_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        logo_paragraph.paragraph_format.space_after = Pt(18)
        logo_paragraph.add_run().add_picture(str(SCHOOL_LOGO), width=Cm(3.6))
    else:
        print(f"  CANH BAO: khong tim thay logo {SCHOOL_LOGO}")

    centered("BÁO CÁO BÀI TẬP LỚN", 20, space_after=12)
    centered("HỌC PHẦN: CÔNG NGHỆ TRI THỨC", 15, space_after=36)

    centered("ĐỀ TÀI", 14, space_after=12)
    centered("HỆ HỖ TRỢ QUYẾT ĐỊNH DỰA TRÊN TRI THỨC", 17)
    centered("CHO ĐỊNH GIÁ XE Ô TÔ CŨ", 17)
    centered("TẠI THỊ TRƯỜNG VIỆT NAM", 17, space_after=48)

    info_table = document.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    info_rows = [
        ("Giảng viên hướng dẫn:", "TS. Nguyễn Văn Thiện"),
        ("Lớp:", ""),
        ("Nhóm:", "4"),
        (
            "Học viên thực hiện:",
            "1. Tạ Quý Dương – 2026700140\n"
            "2. Vũ Thái Dương – 2026700149\n"
            "3. Nguyễn Huy Hoàng – 2026700148\n"
            "4. Lê Công Nghĩa – 2026700142",
        ),
    ]

    for row_index, (label, value) in enumerate(info_rows):
        label_cell = info_table.cell(row_index, 0)
        label_paragraph = label_cell.paragraphs[0]
        label_paragraph.paragraph_format.space_after = Pt(3)
        label_run = label_paragraph.add_run(label)
        label_run.bold = True
        label_run.font.size = Pt(13)

        value_cell = info_table.cell(row_index, 1)
        value_paragraph = value_cell.paragraphs[0]
        value_paragraph.paragraph_format.space_after = Pt(3)
        value_paragraph.paragraph_format.line_spacing = 1.3
        value_run = value_paragraph.add_run(value)
        value_run.font.size = Pt(13)

    empty_paragraph = document.add_paragraph()
    empty_paragraph.paragraph_format.space_before = Pt(36)
    centered("Hà Nội, 2026", 13, bold=False)

    document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def main() -> None:
    document = Document()
    _configure_styles(document)
    _configure_page(document)

    figure_state = {"inserted": set()}

    # --- Section 1: trang bìa, không đánh số trang ---
    _add_cover_page(document)
    report_layout.clear_header(document.sections[0])

    # --- Section 2: phần đầu quyển, đánh số La Mã thường ---
    front_section = report_layout.start_new_section(document)
    report_layout.set_page_numbering(front_section, "lowerRoman", start_at=1)
    report_layout.add_page_number_to_header(front_section)

    # Theo quy định, thứ tự phần đầu là: Lời cảm ơn, Mục lục, rồi các danh mục.
    _render_markdown(
        document, (SCRATCHPAD / "loi_cam_on.md").read_text(encoding="utf-8"), figure_state
    )
    print("  Da ghep: loi_cam_on.md")

    document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # Mục lục tự động. Tiêu đề định dạng thủ công thay vì dùng style Heading 1,
    # để chính nó không bị liệt kê trong mục lục mà nó sinh ra.
    table_of_contents_title = document.add_paragraph()
    table_of_contents_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table_of_contents_title.paragraph_format.space_after = Pt(12)

    title_run = table_of_contents_title.add_run("MỤC LỤC")
    title_run.bold = True
    title_run.font.size = Pt(14)

    _add_table_of_contents_field(document)

    _render_markdown(
        document,
        (SCRATCHPAD / "phan_dau_sau_muc_luc.md").read_text(encoding="utf-8"),
        figure_state,
    )
    print("  Da ghep: phan_dau_sau_muc_luc.md")

    # --- Section 3: thân bài, đánh số Ả Rập lại từ 1 kể từ MỞ ĐẦU ---
    body_section = report_layout.start_new_section(document)
    report_layout.set_page_numbering(body_section, "decimal", start_at=1)
    report_layout.add_page_number_to_header(body_section)

    # Phần cấp 1 đầu tiên của thân bài không cần ngắt trang vì đã sang section mới.
    figure_state["has_written_section"] = False

    body_files = [
        "mo_dau.md",
        "chuong1_rut_gon.md",
        "chuong2_rut_gon.md",
        "chuong3_rut_gon.md",
        "ketluan.md",
        "tai_lieu.md",
    ]

    for markdown_file in body_files:
        source_path = SCRATCHPAD / markdown_file
        if not source_path.exists():
            print(f"  BO QUA: khong tim thay {markdown_file}")
            continue

        _render_markdown(document, source_path.read_text(encoding="utf-8"), figure_state)
        print(f"  Da ghep: {markdown_file}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUTPUT_PATH)

    inserted_count = len(figure_state["inserted"])
    print(f"\nDa chen {inserted_count}/{len(FIGURE_PLACEMENTS)} anh")

    missing = [
        FIGURE_PLACEMENTS[index][2]
        for index in range(len(FIGURE_PLACEMENTS))
        if index not in figure_state["inserted"]
    ]
    for caption in missing:
        print(f"  CHUA CHEN: {caption}")

    print(f"\nDa luu bao cao tai: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
