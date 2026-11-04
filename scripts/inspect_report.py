"""Kiểm tra cấu trúc báo cáo DOCX đã dựng: tiêu đề, bảng, ảnh và ước lượng số trang."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.shared import Cm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "outputs" / "Bao-cao-BTL-Cong-nghe-tri-thuc.docx"


def main() -> None:
    document = Document(REPORT_PATH)

    headings: list[tuple[str, str]] = []
    paragraph_count = 0
    word_count = 0
    image_count = 0

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if paragraph.style.name.startswith("Heading"):
            headings.append((paragraph.style.name, text))

        if text:
            paragraph_count += 1
            word_count += len(text.split())

        image_count += len(paragraph._p.findall(".//" + "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))

    table_cell_words = 0
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                table_cell_words += len(cell.text.split())

    print(f"Tep: {REPORT_PATH.name}")
    print(f"Kich thuoc: {REPORT_PATH.stat().st_size / 1024 / 1024:.2f} MB\n")

    print(f"So doan van co noi dung: {paragraph_count:,}")
    print(f"So tu trong doan van:    {word_count:,}")
    print(f"So tu trong bang:        {table_cell_words:,}")
    print(f"So bang:                 {len(document.tables)}")
    print(f"So anh:                  {image_count}")

    section = document.sections[0]
    print(f"\nKho giay: {section.page_width.cm:.1f} x {section.page_height.cm:.1f} cm")
    print(f"Le trai/phai/tren/duoi: {section.left_margin.cm:.1f} / {section.right_margin.cm:.1f} / "
          f"{section.top_margin.cm:.1f} / {section.bottom_margin.cm:.1f} cm")

    # Ước lượng thô: mỗi trang A4 với cỡ chữ 13 và giãn dòng 1,4 chứa khoảng 330 từ;
    # mỗi ảnh chiếm khoảng nửa trang.
    estimated_pages = (word_count + table_cell_words) / 330 + image_count * 0.55 + 3
    print(f"\nUoc luong so trang: khoang {estimated_pages:.0f} trang")

    print(f"\n{'=' * 70}\nCAU TRUC TIEU DE\n{'=' * 70}")
    for style_name, text in headings:
        indent = "  " * (int(style_name[-1]) - 1)
        print(f"{indent}{text}")


if __name__ == "__main__":
    main()
