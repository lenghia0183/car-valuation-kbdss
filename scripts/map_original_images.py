"""Xác định mỗi ảnh nhúng trong bản gốc tương ứng với hình nào của báo cáo.

Đọc thứ tự ảnh xuất hiện trong thân tài liệu rồi ghép với dòng chú thích đứng
ngay sau ảnh đó, nhờ vậy biết chắc ảnh nào là logo, ảnh nào là Hình 1.1, 2.1...
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ORIGINAL_DOCX = PROJECT_ROOT / "source_doc" / "Bao-cao-goc-tu-Google-Docs.docx"

WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RELATIONSHIP_NAMESPACE = (
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
)


def _load_relationship_targets(archive: zipfile.ZipFile) -> dict[str, str]:
    """Ánh xạ mã quan hệ (rId) sang tên tệp ảnh."""
    relationships_xml = archive.read("word/_rels/document.xml.rels").decode("utf-8")

    targets: dict[str, str] = {}
    for match in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', relationships_xml):
        relationship_id, target = match.groups()
        if "media/" in target:
            targets[relationship_id] = Path(target).name

    return targets


def main() -> None:
    with zipfile.ZipFile(ORIGINAL_DOCX) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        relationship_targets = _load_relationship_targets(archive)

    # Tách thân tài liệu thành từng đoạn để biết ảnh nằm ở đoạn nào.
    paragraphs = re.findall(r"<w:p[ >].*?</w:p>", document_xml, flags=re.DOTALL)

    records: list[tuple[int, str, str]] = []

    for index, paragraph_xml in enumerate(paragraphs):
        embed_match = re.search(r'r:embed="([^"]+)"', paragraph_xml)
        if embed_match is None:
            continue

        image_name = relationship_targets.get(embed_match.group(1), "?")

        # Chú thích thường nằm ở đoạn ngay sau ảnh.
        caption = ""
        for following_index in range(index + 1, min(index + 4, len(paragraphs))):
            text = "".join(
                re.findall(
                    r"<w:t[^>]*>(.*?)</w:t>",
                    paragraphs[following_index],
                    flags=re.DOTALL,
                )
            ).strip()
            if text:
                caption = text[:85]
                break

        records.append((index, image_name, caption))

    print(f"{'Doan':>6}  {'Tep anh':<16}  Chu thich ngay sau anh")
    print("-" * 95)
    for paragraph_index, image_name, caption in records:
        print(f"{paragraph_index:>6}  {image_name:<16}  {caption}")


if __name__ == "__main__":
    main()
