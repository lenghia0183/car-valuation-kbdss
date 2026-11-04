"""Vòng rút gọn cuối: đưa báo cáo về khoảng 55 trang.

Cách cắt ưu tiên: bỏ các bảng mà biểu đồ ngay cạnh đã thể hiện cùng dữ liệu, và nén
các đoạn diễn giải còn dài. Toàn bộ số liệu vẫn còn trong báo cáo, chỉ đổi cách trình
bày từ "vừa bảng vừa biểu đồ" sang "biểu đồ kèm nhận xét có số liệu".
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)


def _remove_table_after_caption(text: str, caption_prefix: str) -> tuple[str, bool]:
    """Xóa dòng tên bảng và toàn bộ bảng Markdown đứng ngay sau nó."""
    lines = text.split("\n")

    caption_index = next(
        (i for i, line in enumerate(lines) if line.strip().strip("*").startswith(caption_prefix)),
        None,
    )
    if caption_index is None:
        return text, False

    # Bảng bắt đầu ở dòng gạch đứng đầu tiên sau tên bảng.
    table_start = caption_index + 1
    while table_start < len(lines) and not lines[table_start].strip().startswith("|"):
        table_start += 1

    if table_start >= len(lines):
        return text, False

    table_end = table_start
    while table_end < len(lines) and lines[table_end].strip().startswith("|"):
        table_end += 1

    del lines[caption_index:table_end]
    return "\n".join(lines), True


CHAPTER_THREE_BLOCKS: list[tuple[str, str]] = [
    (
        """**Sai số theo phân khúc.** Bảng 3.10 và Hình 3.12 trình bày sai số của hệ lai phân rã theo phân khúc.""",
        """**Sai số theo phân khúc.** Hình 3.12 trình bày sai số của hệ lai phân rã theo phân khúc.""",
    ),
    (
        """**Sai số theo tuổi xe.** Bảng 3.11 và Hình 3.13 phân rã sai số theo nhóm tuổi xe.""",
        """**Sai số theo tuổi xe.** Hình 3.13 phân rã sai số theo nhóm tuổi xe.""",
    ),
    (
        """MAPE dao động trong khoảng hẹp từ 9,57% đến 12,19%, cho thấy hệ thống hoạt động khá đồng đều giữa các phân khúc. MAE thì chênh lệch lớn hơn nhiều, từ 18,62 triệu (hatchback hạng A) đến 76,51 triệu (xe sang) – điều này hoàn toàn dự đoán được vì MAE tỷ lệ với mặt bằng giá của phân khúc.""",
        """MAPE dao động trong khoảng hẹp từ 9,57% (SUV hạng B) đến 12,19% (MPV đa dụng), cho thấy hệ thống hoạt động khá đồng đều giữa các phân khúc. MAE chênh lệch lớn hơn nhiều, từ 18,62 triệu (hatchback hạng A) đến 76,51 triệu (xe sang) – điều dự đoán được vì MAE tỷ lệ với mặt bằng giá của phân khúc.""",
    ),
    (
        """MAE giảm đều theo tuổi xe, từ 59,45 triệu ở nhóm xe mới xuống 15,78 triệu ở nhóm trên 12 năm. Đây là hệ quả trực tiếp của việc xe càng cũ càng rẻ.

MAPE lại cho bức tranh khác: nhóm 9–12 năm có MAPE cao nhất (12,54%), còn nhóm trên 12 năm lại thấp nhất (9,01%). Nhóm 9–12 năm khó định giá vì đây là giai đoạn giá xe phụ thuộc nhiều vào tình trạng thực tế của từng chiếc – yếu tố mà hệ thống chỉ nắm được qua khai báo của người dùng. Nhóm trên 12 năm dễ hơn vì giá đã tiệm cận giá trị sử dụng, ít biến động.""",
        """MAE giảm đều theo tuổi xe, từ 59,45 triệu ở nhóm 0–2 năm xuống 15,78 triệu ở nhóm trên 12 năm – hệ quả trực tiếp của việc xe càng cũ càng rẻ. MAPE lại cho bức tranh khác: nhóm 9–12 năm cao nhất (12,54%) còn nhóm trên 12 năm thấp nhất (9,01%). Nhóm 9–12 năm khó định giá vì giá phụ thuộc nhiều vào tình trạng thực tế của từng chiếc, yếu tố mà hệ thống chỉ nắm được qua khai báo của người dùng; nhóm trên 12 năm dễ hơn vì giá đã tiệm cận giá trị sử dụng.""",
    ),
    (
        """**Về hạn chế của dữ liệu – điểm cần nhấn mạnh.** Toàn bộ kết quả ở trên được đo trên dữ liệu mô phỏng, không phải dữ liệu thị trường thật. Điều này đặt ra một giới hạn nghiêm trọng về khả năng ngoại suy: bộ dữ liệu được sinh ra có tham chiếu cùng hệ quy luật khấu hao mà tập luật mô tả, nên tập luật có lợi thế không công bằng so với một tình huống thực tế. Các con số MAE, MAPE và R² ở trên **phản ánh tính đúng đắn của phần cài đặt và tính nhất quán nội tại của hệ thống, chứ chưa chứng minh được độ chính xác trên thị trường thật**.

Để có kết luận vững chắc về độ chính xác thực tế, cần lặp lại toàn bộ thực nghiệm này trên dữ liệu tin rao thu thập hợp pháp từ các sàn giao dịch. Nhóm xác định đây là việc cần làm trước tiên nếu đề tài được phát triển tiếp.

**Về các hạn chế khác.** Thứ nhất, hệ thống phụ thuộc vào thông tin do người dùng khai báo về tình trạng và lịch sử xe; nếu người dùng khai báo sai hoặc giấu thông tin, kết quả sẽ sai theo. Thứ hai, cơ sở tri thức hiện chỉ bao phủ 55 phiên bản của 28 dòng xe phổ biến; các dòng xe ngoài danh sách này chưa định giá được. Thứ ba, các hệ số trong luật được đặt theo kinh nghiệm và chưa qua tối ưu tự động. Thứ tư, hệ thống chưa mô hình hóa yếu tố biến động thị trường theo thời gian, trong khi giá xe cũ chịu ảnh hưởng của chính sách thuế, giá xe mới và chu kỳ kinh tế.""",
        """**Về hạn chế của dữ liệu – điểm cần nhấn mạnh.** Toàn bộ kết quả trên được đo trên dữ liệu mô phỏng, không phải dữ liệu thị trường thật. Vì bộ dữ liệu được sinh có tham chiếu cùng hệ quy luật khấu hao mà tập luật mô tả, tập luật có lợi thế không công bằng so với tình huống thực tế. Các con số MAE, MAPE và R² **phản ánh tính đúng đắn của phần cài đặt và tính nhất quán nội tại của hệ thống, chứ chưa chứng minh được độ chính xác trên thị trường thật**. Để có kết luận vững chắc, cần lặp lại toàn bộ thực nghiệm trên dữ liệu tin rao thu thập hợp pháp từ các sàn giao dịch.

**Về các hạn chế khác.** Hệ thống phụ thuộc vào thông tin người dùng khai báo về tình trạng và lịch sử xe, nếu khai sai thì kết quả sai theo. Cơ sở tri thức mới bao phủ 55 phiên bản của 28 dòng xe phổ biến. Các hệ số trong luật đặt theo kinh nghiệm, chưa qua tối ưu tự động. Hệ thống cũng chưa mô hình hóa biến động thị trường theo thời gian, trong khi giá xe cũ chịu ảnh hưởng của chính sách thuế, giá xe mới và chu kỳ kinh tế.""",
    ),
]

CHAPTER_TWO_BLOCKS: list[tuple[str, str]] = [
    (
        """Các siêu luật điều khiển việc áp dụng tập luật gồm bốn quy tắc. Các luật trong nhóm khấu hao (R01–R05) và nhóm số km theo năm (R06–R09) **loại trừ lẫn nhau** vì điều kiện được thiết kế không giao nhau. Các luật rủi ro R11, R12 có **độ ưu tiên cao** nên được xét trước các luật điều chỉnh kỹ thuật và thị trường. Các luật R23–R25 **không thay đổi giá** mà chỉ hạ độ tin cậy và sinh cảnh báo. Cuối cùng, một luật đã kích hoạt **không được kích hoạt lại** trong cùng một phiên suy diễn, bảo đảm vòng lặp suy diễn kết thúc.

Mỗi luật được lưu trong tệp `rules.json` gồm mã, nhóm, độ ưu tiên, mô tả, phần điều kiện và phần hành động, ví dụ:

> {"id": "R11", "group": "tinh_trang", "priority": 80, "if": [{"fact": "ngap_nuoc", "op": "==", "value": true}], "then": [{"type": "multiply", "factor": 0.70, "label": "Xe từng ngập nước"}, {"type": "flag", "value": "Xe từng ngập nước: rủi ro hỏng hệ thống điện"}, {"type": "confidence", "delta": -0.10}]}

Cách lưu trữ này tách biệt tri thức khỏi mã nguồn: kỹ sư tri thức chỉnh sửa luật qua trang quản trị mà không phải lập trình lại. Mỗi khi tập luật thay đổi, chức năng kiểm tra tính nhất quán sẽ phát hiện các luật trùng mã, luật thiếu điều kiện hoặc thiếu hành động.""",
        """Bốn siêu luật điều khiển việc áp dụng tập luật: các luật trong nhóm khấu hao (R01–R05) và nhóm số km theo năm (R06–R09) **loại trừ lẫn nhau** vì điều kiện không giao nhau; các luật rủi ro R11, R12 có **độ ưu tiên cao** nên được xét trước; các luật R23–R25 **không thay đổi giá** mà chỉ hạ độ tin cậy và sinh cảnh báo; và một luật đã kích hoạt **không được kích hoạt lại** trong cùng phiên suy diễn, bảo đảm vòng lặp kết thúc.

Mỗi luật được lưu trong tệp `rules.json` gồm mã, nhóm, độ ưu tiên, mô tả, phần điều kiện và phần hành động. Cách lưu trữ này tách biệt tri thức khỏi mã nguồn: kỹ sư tri thức chỉnh sửa luật qua trang quản trị mà không phải lập trình lại. Mỗi khi tập luật thay đổi, chức năng kiểm tra tính nhất quán sẽ phát hiện luật trùng mã, luật thiếu điều kiện hoặc thiếu hành động.""",
    ),
    (
        """Ngoài các trọng số trên, hệ thống áp một ràng buộc cứng: chỉ các tình huống **cùng hãng** mới được xét, các tình huống khác hãng bị gán độ tương tự bằng 0. Ràng buộc này tránh so sánh một chiếc xe phổ thông với một chiếc xe sang cùng phân khúc nhưng khác hẳn mặt bằng giá.

Hệ thống chọn k = 5 tình huống có độ tương tự cao nhất và vượt ngưỡng tối thiểu 0,55. Ở bước Reuse, giá của mỗi tình huống được điều chỉnh về điều kiện của truy vấn theo hai bước: chênh lệch tuổi xe hiệu chỉnh với hệ số 7% mỗi năm, chênh lệch số km với hệ số 1,2% cho mỗi 10.000 km và giới hạn biên độ trong khoảng ±15%.""",
        """Hệ thống còn áp một ràng buộc cứng: chỉ các tình huống **cùng hãng** mới được xét, tránh so sánh xe phổ thông với xe sang cùng phân khúc nhưng khác hẳn mặt bằng giá. Hệ thống chọn k = 5 tình huống vượt ngưỡng tương tự 0,55. Ở bước Reuse, giá mỗi tình huống được hiệu chỉnh về điều kiện truy vấn: chênh lệch tuổi xe với hệ số 7% mỗi năm, chênh lệch số km với hệ số 1,2% cho mỗi 10.000 km, giới hạn biên độ ±15%.""",
    ),
]


def _apply_blocks(text: str, blocks: list[tuple[str, str]], label: str) -> tuple[str, int]:
    applied = 0
    for original, condensed in blocks:
        if original not in text:
            print(f"  CANH BAO [{label}]: khong tim thay '{original[:50]}...'")
            continue
        text = text.replace(original, condensed)
        applied += 1
    return text, applied


def main() -> None:
    # --- Chương 3: bỏ hai bảng đã có biểu đồ tương đương, nén phần nhận xét ---
    path_three = SCRATCHPAD / "chuong3_rut_gon.md"
    text_three = path_three.read_text(encoding="utf-8")
    before_three = len(text_three.split())

    text_three, applied_three = _apply_blocks(text_three, CHAPTER_THREE_BLOCKS, "chuong3")

    for caption_prefix in ["Bảng 3.10.", "Bảng 3.11."]:
        text_three, removed = _remove_table_after_caption(text_three, caption_prefix)
        print(f"  {'Da xoa' if removed else 'KHONG xoa duoc'} {caption_prefix}")

    path_three.write_text(text_three, encoding="utf-8")
    print(f"chuong3_rut_gon.md         {before_three:>6,} -> {len(text_three.split()):>6,} tu "
          f"({applied_three}/{len(CHAPTER_THREE_BLOCKS)} doan)")

    # --- Chương 2 ---
    path_two = SCRATCHPAD / "chuong2_rut_gon.md"
    text_two = path_two.read_text(encoding="utf-8")
    before_two = len(text_two.split())

    text_two, applied_two = _apply_blocks(text_two, CHAPTER_TWO_BLOCKS, "chuong2")
    path_two.write_text(text_two, encoding="utf-8")

    print(f"chuong2_rut_gon.md         {before_two:>6,} -> {len(text_two.split()):>6,} tu "
          f"({applied_two}/{len(CHAPTER_TWO_BLOCKS)} doan)")

    # Hai bảng bị bỏ nên phải xóa khỏi danh mục bảng biểu và đánh số lại Bảng 3.12.
    path_front = SCRATCHPAD / "phan_dau_sau_muc_luc.md"
    text_front = path_front.read_text(encoding="utf-8")

    text_front = re.sub(r"^Bảng 3\.10\..*\n?", "", text_front, flags=re.MULTILINE)
    text_front = re.sub(r"^Bảng 3\.11\..*\n?", "", text_front, flags=re.MULTILINE)
    text_front = text_front.replace(
        "Bảng 3.12. Kết quả năm kịch bản định giá điển hình",
        "Bảng 3.10. Kết quả năm kịch bản định giá điển hình",
    )
    path_front.write_text(text_front, encoding="utf-8")

    text_three = path_three.read_text(encoding="utf-8")
    text_three = text_three.replace("Bảng 3.12. Kết quả năm kịch bản", "Bảng 3.10. Kết quả năm kịch bản")
    text_three = text_three.replace("Bảng 3.12 tổng hợp kết quả", "Bảng 3.10 tổng hợp kết quả")
    path_three.write_text(text_three, encoding="utf-8")

    print("Da cap nhat danh muc bang bieu va danh so lai Bang 3.12 -> 3.10")


if __name__ == "__main__":
    main()
