"""Kết xuất một số trang của PDF thành ảnh để kiểm tra bố cục bằng mắt."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "outputs" / "Bao-cao-BTL-Cong-nghe-tri-thuc.pdf"
RENDER_DIR = PROJECT_ROOT / "outputs" / "page_renders"

VIEWER_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<style>body{margin:0;background:#fff}canvas{display:block}</style>
</head><body>
<canvas id="page"></canvas>
<script>
pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

window.renderPage = async function (pdfBase64, pageNumber) {
  const raw = atob(pdfBase64);
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);

  const pdf = await pdfjsLib.getDocument({ data: bytes }).promise;
  const page = await pdf.getPage(pageNumber);
  const viewport = page.getViewport({ scale: 1.6 });

  const canvas = document.getElementById("page");
  canvas.width = viewport.width;
  canvas.height = viewport.height;

  await page.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;
  return { width: canvas.width, height: canvas.height };
};
</script></body></html>
"""


def main() -> None:
    page_numbers = [int(argument) for argument in sys.argv[1:]] or [1, 10, 33, 40]

    RENDER_DIR.mkdir(parents=True, exist_ok=True)

    import base64

    pdf_base64 = base64.b64encode(PDF_PATH.read_bytes()).decode("ascii")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1100, "height": 1500})

        page.set_content(VIEWER_HTML)
        page.wait_for_function("typeof pdfjsLib !== 'undefined'", timeout=30_000)

        for page_number in page_numbers:
            size = page.evaluate(
                "([data, number]) => window.renderPage(data, number)",
                [pdf_base64, page_number],
            )
            page.set_viewport_size(
                {"width": int(size["width"]), "height": int(size["height"])}
            )
            page.wait_for_timeout(600)

            output_path = RENDER_DIR / f"trang_{page_number:02d}.png"
            page.locator("#page").screenshot(path=str(output_path))
            print(f"Da ket xuat trang {page_number} -> {output_path.name}")

        browser.close()


if __name__ == "__main__":
    main()
