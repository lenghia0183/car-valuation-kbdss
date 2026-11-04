"""Giải mã bản DOCX gốc tải từ Google Docs và trích các ảnh nhúng trong đó.

Bản gốc chứa logo trường ở trang bìa và các sơ đồ của Chương 1, Chương 2 mà bản dựng
lại không có. Script này lấy lại chúng để báo cáo giữ đúng hình thức của bản gốc.
"""

from __future__ import annotations

import base64
import json
import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_PATH = Path(
    r"C:\Users\PC\.claude\projects\d--agent-dev-kit"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\tool-results"
    r"\mcp-claude_ai_Google_Drive-download_file_content-1793809254977.txt"
)

ORIGINAL_DIR = PROJECT_ROOT / "source_doc"
ORIGINAL_DOCX = ORIGINAL_DIR / "Bao-cao-goc-tu-Google-Docs.docx"
EXTRACTED_MEDIA_DIR = ORIGINAL_DIR / "media"


def main() -> None:
    payload = json.loads(DOWNLOAD_PATH.read_text(encoding="utf-8"))

    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    ORIGINAL_DOCX.write_bytes(base64.b64decode(payload["content"]))

    print(f"Tieu de  : {payload['title']}")
    print(f"Kieu tep : {payload['mimeType']}")
    print(f"Da luu   : {ORIGINAL_DOCX} ({ORIGINAL_DOCX.stat().st_size / 1024 / 1024:.2f} MB)")

    # Ảnh nhúng của DOCX nằm trong word/media bên trong tệp nén.
    if EXTRACTED_MEDIA_DIR.exists():
        shutil.rmtree(EXTRACTED_MEDIA_DIR)
    EXTRACTED_MEDIA_DIR.mkdir(parents=True)

    with zipfile.ZipFile(ORIGINAL_DOCX) as archive:
        media_names = [name for name in archive.namelist() if name.startswith("word/media/")]

        for media_name in sorted(media_names):
            target_path = EXTRACTED_MEDIA_DIR / Path(media_name).name
            target_path.write_bytes(archive.read(media_name))

    print(f"\nDa trich {len(media_names)} anh vao {EXTRACTED_MEDIA_DIR}:")
    for image_path in sorted(EXTRACTED_MEDIA_DIR.iterdir()):
        print(f"  {image_path.name:28} {image_path.stat().st_size / 1024:>8.1f} KB")


if __name__ == "__main__":
    main()
