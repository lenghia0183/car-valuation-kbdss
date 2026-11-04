"""Vòng rút gọn cuối cùng: bỏ hai bảng ở Chương 3 trùng nội dung với Chương 2.

Bảng trọng số độ đo tương tự và bảng quy tắc chọn hệ số alpha đã được trình bày đầy đủ
ở phần thiết kế (Bảng 2.6 và Bảng 2.7). Lặp lại chúng ở phần cài đặt không thêm thông tin
mới, chỉ tốn hai trang, nên phần cài đặt chỉ dẫn chiếu ngược về Chương 2.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

REPLACEMENTS: list[tuple[str, str]] = [
    # Bỏ Bảng 3.7, dẫn chiếu về Bảng 2.6.
    (
        """**Truy hồi (Retrieve).** Độ tương tự toàn cục là trung bình có trọng số của tám độ tương tự cục bộ, tổng trọng số bằng 1,0 (Bảng 3.7).

**Bảng 3.7. Trọng số các thuộc tính trong độ đo tương tự**

| Thuộc tính | Trọng số | Hàm tương tự cục bộ |
| :-- | --: | :-- |
| Dòng xe | 0,30 | So sánh bằng (1 nếu giống, 0 nếu khác) |
| Năm sản xuất | 0,22 | Tuyến tính giảm dần, ngưỡng 6 năm |
| Số km | 0,18 | Tuyến tính giảm dần, ngưỡng 120.000 km |
| Phiên bản | 0,12 | So sánh bằng |
| Hộp số | 0,06 | So sánh bằng |
| Nhiên liệu | 0,04 | So sánh bằng |
| Xuất xứ | 0,04 | So sánh bằng |
| Khu vực | 0,04 | So sánh bằng |

Dòng xe có trọng số cao nhất vì quyết định phân khúc giá; năm sản xuất và số km xếp tiếp theo vì quyết định mức khấu hao. Hai thuộc tính số này dùng công thức `max(0, 1 − |chênh lệch| / ngưỡng)`, nghĩa là hai xe chênh 3 năm có độ tương tự về năm sản xuất là 0,5, chênh từ 6 năm trở lên thì bằng 0.

Hệ thống còn áp một ràng buộc cứng: **chỉ các tình huống cùng hãng mới được xét**, tránh so sánh một chiếc Toyota với một chiếc BMW cùng phân khúc nhưng khác hẳn mặt bằng giá. Hệ thống truy hồi k = 5 tình huống vượt ngưỡng tương tự tối thiểu 0,55.""",
        """**Truy hồi (Retrieve).** Độ tương tự toàn cục là trung bình có trọng số của tám độ tương tự cục bộ với bộ trọng số đã trình bày ở Bảng 2.6. Hai thuộc tính số là năm sản xuất và số km dùng công thức `max(0, 1 − |chênh lệch| / ngưỡng)`, nghĩa là hai xe chênh 3 năm có độ tương tự về năm sản xuất bằng 0,5 và chênh từ 6 năm trở lên thì bằng 0. Hệ thống áp thêm ràng buộc cứng **chỉ xét các tình huống cùng hãng**, rồi truy hồi k = 5 tình huống vượt ngưỡng tương tự tối thiểu 0,55.""",
    ),
    # Bỏ Bảng 3.8, dẫn chiếu về Bảng 2.7.
    (
        """**Công thức tổng hợp.** Giá đề xuất là tổ hợp lồi của hai nguồn:

> giá đề xuất = α × giá từ luật + (1 − α) × giá từ CBR

Hệ số α được chọn thích nghi theo số lượng và chất lượng của các tình huống truy hồi được, theo Bảng 3.8.

**Bảng 3.8. Quy tắc chọn hệ số α**

| Điều kiện | α | Diễn giải |
| :-- | --: | :-- |
| Không truy hồi được tình huống nào | 1,00 | Chỉ dùng luật |
| ≥ 5 tình huống, độ tương tự trung bình ≥ 0,80 | 0,35 | Tin tưởng dữ liệu thị trường nhiều hơn |
| ≥ 3 tình huống, độ tương tự trung bình ≥ 0,70 | 0,50 | Cân bằng hai nguồn |
| ≥ 2 tình huống | 0,65 | Nghiêng về luật |
| 1 tình huống | 0,80 | Chủ yếu dùng luật |

Logic đằng sau quy tắc này: khi có nhiều xe rất giống trên thị trường, giá thị trường thực tế đáng tin hơn công thức khấu hao tổng quát; ngược lại khi dữ liệu tham chiếu ít hoặc không giống, tri thức chuyên gia dạng luật trở thành chỗ dựa chính.""",
        """**Công thức tổng hợp.** Giá đề xuất là tổ hợp lồi của hai nguồn:

> giá đề xuất = α × giá từ luật + (1 − α) × giá từ CBR

Hệ số α được chọn thích nghi theo số lượng và độ tương tự trung bình của các tình huống truy hồi được, theo quy tắc đã trình bày ở Bảng 2.7. Logic đằng sau quy tắc này là khi có nhiều xe rất giống trên thị trường thì giá thị trường thực tế đáng tin hơn công thức khấu hao tổng quát; ngược lại khi dữ liệu tham chiếu ít, tri thức chuyên gia dạng luật trở thành chỗ dựa chính.""",
    ),
]

# Hai bảng bị bỏ nên các bảng sau phải đánh số lại.
RENUMBERING: list[tuple[str, str]] = [
    ("Bảng 3.9. So sánh bốn phương pháp", "Bảng 3.7. So sánh bốn phương pháp"),
    ("Bảng 3.9 trình bày kết quả", "Bảng 3.7 trình bày kết quả"),
    ("Bảng 3.10. Kết quả năm kịch bản", "Bảng 3.8. Kết quả năm kịch bản"),
    ("Bảng 3.10 tổng hợp kết quả", "Bảng 3.8 tổng hợp kết quả"),
]


def main() -> None:
    path = SCRATCHPAD / "chuong3_rut_gon.md"
    text = path.read_text(encoding="utf-8")
    before = len(text.split())

    applied = 0
    for original, condensed in REPLACEMENTS:
        if original not in text:
            print(f"  CANH BAO: khong tim thay '{original[:55]}...'")
            continue
        text = text.replace(original, condensed)
        applied += 1

    for original, renumbered in RENUMBERING:
        text = text.replace(original, renumbered)

    path.write_text(text, encoding="utf-8")
    print(f"chuong3_rut_gon.md  {before:>6,} -> {len(text.split()):>6,} tu "
          f"({applied}/{len(REPLACEMENTS)} doan)")

    # Cập nhật danh mục bảng biểu cho khớp cách đánh số mới.
    front_path = SCRATCHPAD / "phan_dau_sau_muc_luc.md"
    front_text = front_path.read_text(encoding="utf-8")

    front_text = re.sub(r"^Bảng 3\.7\..*\n?", "", front_text, flags=re.MULTILINE)
    front_text = re.sub(r"^Bảng 3\.8\..*\n?", "", front_text, flags=re.MULTILINE)
    front_text = front_text.replace(
        "Bảng 3.9. So sánh bốn phương pháp định giá trên tập kiểm thử 584 xe",
        "Bảng 3.7. So sánh bốn phương pháp định giá trên tập kiểm thử 584 xe",
    )
    front_text = front_text.replace(
        "Bảng 3.10. Kết quả năm kịch bản định giá điển hình",
        "Bảng 3.8. Kết quả năm kịch bản định giá điển hình",
    )

    front_path.write_text(front_text, encoding="utf-8")
    print("Da cap nhat danh muc bang bieu")


if __name__ == "__main__":
    main()
