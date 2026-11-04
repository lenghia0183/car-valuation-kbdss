"""Đọc quy định hình thức trình bày và bài tiểu luận mẫu để rút ra chuẩn cần áp dụng."""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.shared import Length

TEMPLATE_DIR = Path(r"C:\Users\PC\Documents\bao-cao\co_so_du_lieu_nang_cao")


def _describe_section(document: Document) -> None:
    section = document.sections[0]
    print("  Kho giay   : "
          f"{section.page_width.cm:.1f} x {section.page_height.cm:.1f} cm")
    print("  Le (T/P/Tr/D): "
          f"{section.left_margin.cm:.2f} / {section.right_margin.cm:.2f} / "
          f"{section.top_margin.cm:.2f} / {section.bottom_margin.cm:.2f} cm")


def _describe_styles(document: Document) -> None:
    normal = document.styles["Normal"]
    size = normal.font.size.pt if normal.font.size else "(ke thua)"
    spacing = normal.paragraph_format.line_spacing
    print(f"  Style Normal: font={normal.font.name}, co chu={size}, gian dong={spacing}")

    for style_name in ["Heading 1", "Heading 2", "Heading 3"]:
        if style_name not in [s.name for s in document.styles]:
            continue
        style = document.styles[style_name]
        size = style.font.size.pt if style.font.size else "(ke thua)"
        print(f"  {style_name:<10}: font={style.font.name}, co chu={size}, "
              f"dam={style.font.bold}")


def dump_text(path: Path, max_paragraphs: int) -> None:
    document = Document(path)

    print(f"\n{'=' * 78}\n{path.name}\n{'=' * 78}")
    _describe_section(document)
    _describe_styles(document)
    print(f"  So doan={len(document.paragraphs)}, so bang={len(document.tables)}")
    print("-" * 78)

    shown = 0
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        style_name = paragraph.style.name
        marker = f"[{style_name}] " if style_name != "Normal" else ""

        # Lấy cỡ chữ và font thực tế của run đầu tiên để biết định dạng trực tiếp.
        detail = ""
        if paragraph.runs:
            run = paragraph.runs[0]
            parts = []
            if run.font.name:
                parts.append(run.font.name)
            if run.font.size:
                parts.append(f"{run.font.size.pt:g}pt")
            if run.bold:
                parts.append("dam")
            if run.italic:
                parts.append("nghieng")
            if parts:
                detail = f"  <{', '.join(parts)}>"

        print(f"{marker}{text[:150]}{detail}")

        shown += 1
        if shown >= max_paragraphs:
            print(f"... (con {len(document.paragraphs) - shown} doan nua)")
            break


def main() -> None:
    file_name = sys.argv[1]
    max_paragraphs = int(sys.argv[2]) if len(sys.argv) > 2 else 120

    dump_text(TEMPLATE_DIR / file_name, max_paragraphs)


if __name__ == "__main__":
    main()
