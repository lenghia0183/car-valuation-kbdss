"""Chụp ảnh màn hình các trang chức năng của ứng dụng bằng Playwright."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

APP_URL = "http://localhost:8513"
SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "screenshots"
VIEWPORT = {"width": 1500, "height": 1000}


def _select_sidebar_page(page: Page, page_label: str) -> None:
    page.get_by_role("radio", name=page_label).click(force=True)
    page.wait_for_timeout(3_000)


def _select_dropdown_option(page: Page, combobox_index: int, option_label: str) -> None:
    """Chọn một giá trị trong selectbox của Streamlit bằng cách gõ để lọc rồi Enter.

    Các selectbox phụ thuộc nhau (hãng → dòng xe → phiên bản) chỉ nạp lại danh sách
    sau một vòng rerun, nên gõ để lọc đáng tin cậy hơn là chờ danh sách hiển thị đủ.
    """
    combobox = page.get_by_role("combobox").nth(combobox_index)
    combobox.scroll_into_view_if_needed()
    combobox.click(force=True)
    page.wait_for_timeout(900)

    page.get_by_role("option", name=option_label, exact=True).first.click(force=True)
    page.wait_for_timeout(2_500)


def _fill_valuation_form(page: Page) -> None:
    """Điền thông tin xe mẫu Toyota Fortuner 2.4G AT và bấm Định giá.

    Chọn xe máy dầu phân khúc SUV hạng D để vết suy diễn kích hoạt nhiều nhóm luật
    (khấu hao, số km, kỹ thuật, thị trường, rủi ro thanh khoản).
    """
    _select_dropdown_option(page, 0, "Toyota")
    _select_dropdown_option(page, 1, "Fortuner")
    _select_dropdown_option(page, 2, "2.4G AT")

    year_input = page.get_by_role("spinbutton").first
    year_input.fill("2019")

    mileage_input = page.get_by_role("spinbutton").nth(1)
    mileage_input.fill("96000")

    # Streamlit bọc input trong một label chặn pointer event, nên phải click cưỡng bức.
    page.get_by_role("checkbox", name="Một chủ, bảo dưỡng hãng đầy đủ").check(force=True)
    page.wait_for_timeout(800)

    page.get_by_role("button", name="Định giá").click(force=True)
    page.wait_for_timeout(4_000)


def capture_all() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)

        page.goto(APP_URL, wait_until="networkidle", timeout=90_000)
        page.wait_for_timeout(6_000)

        # Trang 1: form nhập thông tin xe.
        page.screenshot(path=SCREENSHOT_DIR / "01_trang_dinh_gia.png")
        print("Da chup: 01_trang_dinh_gia.png")

        _fill_valuation_form(page)
        page.screenshot(path=SCREENSHOT_DIR / "02_ket_qua_nhanh.png")
        print("Da chup: 02_ket_qua_nhanh.png")

        # Trang 2: kết quả và giải thích.
        _select_sidebar_page(page, "Kết quả và giải thích")
        page.screenshot(path=SCREENSHOT_DIR / "03_ket_qua_va_giai_thich.png")
        print("Da chup: 03_ket_qua_va_giai_thich.png")

        page.get_by_role("tab", name="Vết suy diễn").click(force=True)
        page.wait_for_timeout(3_000)
        page.screenshot(path=SCREENSHOT_DIR / "04_vet_suy_dien.png", full_page=True)
        print("Da chup: 04_vet_suy_dien.png")

        page.get_by_role("tab", name="Xe tương tự").click(force=True)
        page.wait_for_timeout(2_500)
        page.screenshot(path=SCREENSHOT_DIR / "05_xe_tuong_tu.png")
        print("Da chup: 05_xe_tuong_tu.png")

        # Trang 3: phân tích thị trường.
        _select_sidebar_page(page, "Phân tích thị trường")
        page.wait_for_timeout(3_500)
        page.screenshot(path=SCREENSHOT_DIR / "06_phan_tich_thi_truong.png")
        print("Da chup: 06_phan_tich_thi_truong.png")

        page.screenshot(
            path=SCREENSHOT_DIR / "07_phan_tich_thi_truong_day_du.png", full_page=True
        )
        print("Da chup: 07_phan_tich_thi_truong_day_du.png")

        # Trang 4: quản trị tri thức.
        _select_sidebar_page(page, "Quản trị tri thức")
        page.screenshot(path=SCREENSHOT_DIR / "08_quan_tri_tri_thuc.png")
        print("Da chup: 08_quan_tri_tri_thuc.png")

        page.get_by_role("tab", name="Kiểm tra nhất quán").click(force=True)
        page.wait_for_timeout(2_000)
        page.screenshot(path=SCREENSHOT_DIR / "09_kiem_tra_nhat_quan.png")
        print("Da chup: 09_kiem_tra_nhat_quan.png")

        browser.close()

    print(f"\nTat ca anh da luu tai: {SCREENSHOT_DIR}")


if __name__ == "__main__":
    try:
        capture_all()
    except Exception as error:  # noqa: BLE001
        print(f"LOI khi chup anh: {error}", file=sys.stderr)
        raise
