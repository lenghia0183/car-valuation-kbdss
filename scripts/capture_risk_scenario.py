"""Chụp ảnh màn hình kịch bản xe có rủi ro (xe từng ngập nước) để minh họa cảnh báo."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

APP_URL = "http://localhost:8513"
SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "screenshots"
VIEWPORT = {"width": 1500, "height": 1000}


def _select_dropdown_option(page: Page, combobox_index: int, option_label: str) -> None:
    combobox = page.get_by_role("combobox").nth(combobox_index)
    combobox.scroll_into_view_if_needed()
    combobox.click(force=True)
    page.wait_for_timeout(900)

    page.get_by_role("option", name=option_label, exact=True).first.click(force=True)
    page.wait_for_timeout(2_500)


def capture_risk_scenario() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)

        page.goto(APP_URL, wait_until="networkidle", timeout=90_000)
        page.wait_for_timeout(6_000)

        _select_dropdown_option(page, 0, "Toyota")
        _select_dropdown_option(page, 1, "Fortuner")
        _select_dropdown_option(page, 2, "2.4G AT")

        page.get_by_role("spinbutton").first.fill("2019")
        page.get_by_role("spinbutton").nth(1).fill("96000")

        page.get_by_role("checkbox", name="Xe từng ngập nước").check(force=True)
        page.wait_for_timeout(1_500)

        page.get_by_role("button", name="Định giá").click(force=True)
        page.wait_for_timeout(4_500)

        page.get_by_role("radio", name="Kết quả và giải thích").click(force=True)
        page.wait_for_timeout(3_500)

        page.screenshot(path=SCREENSHOT_DIR / "10_canh_bao_rui_ro.png")
        print("Da chup: 10_canh_bao_rui_ro.png")

        browser.close()


if __name__ == "__main__":
    try:
        capture_risk_scenario()
    except Exception as error:  # noqa: BLE001
        print(f"LOI khi chup anh: {error}", file=sys.stderr)
        raise
