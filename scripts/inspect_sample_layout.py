"""Khảo sát chi tiết cách bài mẫu trình bày hình, bảng, đánh số trang và ngắt phần."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document

SAMPLE_PATH = Path(
    r"C:\Users\PC\Documents\bao-cao\co_so_du_lieu_nang_cao"
    r"\Le_Cong_Nghia_2026700142_Tieu_luan_CSDL_Nang_cao_De_tai_11_Quan_ly_phim_MongoDB.docx"
)


def main() -> None:
    document = Document(SAMPLE_PATH)

    print(f"So section (phan dinh dang trang): {len(document.sections)}")
    for index, section in enumerate(document.sections):
        print(f"  Section {index}: bat dau kieu={section.start_type}, "
              f"khac trang dau={section.different_first_page_header_footer}")

        header_text = " | ".join(p.text.strip() for p in section.header.paragraphs if p.text.strip())
        footer_text = " | ".join(p.text.strip() for p in section.footer.paragraphs if p.text.strip())
        header_xml = section.header.paragraphs[0]._p.xml if section.header.paragraphs else ""

        has_page_field = "PAGE" in header_xml
        print(f"    Header: '{header_text}' (co truong so trang: {has_page_field})")
        print(f"    Footer: '{footer_text}'")

    print(f"\n{'=' * 78}\nCAC DONG CHU THICH HINH VA BANG\n{'=' * 78}")

    paragraphs = document.paragraphs
    for index, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        if not re.match(r"^(Hình|Bảng)\s+\d+\.\d+", text):
            continue

        alignment = paragraph.alignment
        run_detail = ""
        if paragraph.runs:
            run = paragraph.runs[0]
            flags = []
            if run.bold:
                flags.append("dam")
            if run.italic:
                flags.append("nghieng")
            if run.font.size:
                flags.append(f"{run.font.size.pt:g}pt")
            run_detail = f"  <{', '.join(flags)}>" if flags else ""

        print(f"[{alignment}] {text[:95]}{run_detail}")

    print(f"\n{'=' * 78}\nKET LUAN CHUONG VA PHAN CUOI\n{'=' * 78}")
    for paragraph in paragraphs:
        text = paragraph.text.strip()
        if re.match(r"^(Kết luận Chương|KẾT LUẬN|TÀI LIỆU|PHỤ LỤC|MỞ ĐẦU|CHƯƠNG)", text):
            print(f"[{paragraph.style.name}] {text[:95]}")


if __name__ == "__main__":
    main()
