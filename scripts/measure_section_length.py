"""Đo độ dài từng phần của báo cáo để biết phần nào cần rút gọn."""

from __future__ import annotations

from pathlib import Path

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "outputs" / "Bao-cao-BTL-Cong-nghe-tri-thuc.docx"

WORDS_PER_PAGE = 330
PAGES_PER_FIGURE = 0.55


def main() -> None:
    document = Document(REPORT_PATH)

    body_elements = list(document.element.body)
    table_index = 0

    sections: list[dict] = []
    current: dict | None = None

    tables = document.tables

    for element in body_elements:
        tag = element.tag.split("}")[-1]

        if tag == "tbl":
            if current is not None and table_index < len(tables):
                table = tables[table_index]
                table_words = sum(
                    len(cell.text.split()) for row in table.rows for cell in row.cells
                )
                current["words"] += table_words
                current["tables"] += 1
            table_index += 1
            continue

        if tag != "p":
            continue

        # Dò tiêu đề cấp 1 để chia phần.
        style_element = element.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr"
        )
        style_name = ""
        if style_element is not None:
            style_reference = style_element.find(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle"
            )
            if style_reference is not None:
                style_name = style_reference.get(
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", ""
                )

        text = "".join(element.itertext()).strip()

        if style_name == "Heading1":
            current = {"title": text, "words": 0, "figures": 0, "tables": 0}
            sections.append(current)
            continue

        if current is None:
            continue

        current["words"] += len(text.split())
        current["figures"] += len(
            element.findall(
                ".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
            )
        )

    print(f"{'Phan':<48}{'So tu':>9}{'Anh':>6}{'Bang':>6}{'~Trang':>9}")
    print("-" * 78)

    total_pages = 0.0
    for section in sections:
        estimated_pages = section["words"] / WORDS_PER_PAGE + section["figures"] * PAGES_PER_FIGURE
        total_pages += estimated_pages
        print(
            f"{section['title'][:46]:<48}{section['words']:>9,}"
            f"{section['figures']:>6}{section['tables']:>6}{estimated_pages:>9.1f}"
        )

    print("-" * 78)
    print(f"{'TONG':<48}{sum(s['words'] for s in sections):>9,}"
          f"{sum(s['figures'] for s in sections):>6}"
          f"{sum(s['tables'] for s in sections):>6}{total_pages:>9.1f}")


if __name__ == "__main__":
    main()
