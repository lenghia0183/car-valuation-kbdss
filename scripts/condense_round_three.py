"""Vòng rút gọn thứ ba: đưa báo cáo về dưới 50 trang theo quy định trình bày.

Đồng thời bổ sung phần giới thiệu đầu mỗi chương mà quy định yêu cầu
("Phần giới thiệu chương: giới thiệu nội dung dự định trình bày, khoảng 3 đến 5 câu").
"""

from __future__ import annotations

import re
from pathlib import Path

SCRATCHPAD = Path(
    r"C:\Users\PC\AppData\Local\Temp\claude\df9978ac714d187d"
    r"\be072046-c45a-4bb6-b703-844aabe2f2d7\scratchpad"
)

# Phần giới thiệu chèn ngay sau tiêu đề chương.
CHAPTER_INTRODUCTIONS: dict[str, str] = {
    "chuong1_rut_gon.md": (
        "Chương 1 trình bày nền tảng lý thuyết của đề tài. Chương bắt đầu từ các khái niệm "
        "cơ bản về dữ liệu, thông tin, tri thức và cơ sở tri thức, sau đó đi sâu vào hệ chuyên "
        "gia với cách biểu diễn tri thức bằng khung và luật sản xuất cùng kỹ thuật suy diễn. "
        "Tiếp theo, chương giới thiệu lập luận dựa trên tình huống, các kỹ thuật khai phá dữ "
        "liệu phục vụ thu nhận tri thức, và kiến trúc hệ hỗ trợ ra quyết định dựa trên tri thức. "
        "Phần cuối chương khảo sát bài toán định giá xe ô tô cũ tại Việt Nam và chỉ ra hạn chế "
        "của các phương pháp định giá hiện có, làm cơ sở cho hướng tiếp cận của đề tài."
    ),
    "chuong2_rut_gon.md": (
        "Chương 2 chuyển từ lý thuyết sang thiết kế cụ thể cho bài toán định giá xe ô tô cũ. "
        "Chương bắt đầu bằng việc giới thiệu đề tài, xác định mục tiêu và phân tích yêu cầu "
        "chức năng cũng như phi chức năng của hệ thống. Tiếp đó, chương trình bày biểu đồ use "
        "case, sơ đồ phân rã chức năng và kiến trúc ba tầng của hệ thống. Phần trọng tâm của "
        "chương là thiết kế cơ sở tri thức gồm khung tri thức, tập luật sản xuất và cơ sở tình "
        "huống, cùng thiết kế máy suy diễn, cơ chế tổng hợp kết quả và giải thích."
    ),
    "chuong3_rut_gon.md": (
        "Chương 3 trình bày quá trình cài đặt và đánh giá hệ thống đã thiết kế ở Chương 2. "
        "Chương mô tả môi trường thực nghiệm, bộ dữ liệu sử dụng và quy trình tiền xử lý, sau "
        "đó trình bày việc xây dựng cơ sở tri thức và cài đặt các thành phần của hệ thống. "
        "Phần cuối chương so sánh bốn phương pháp định giá trên cùng tập kiểm thử, phân tích "
        "sai số theo phân khúc và tuổi xe, đánh giá khả năng giải thích qua các kịch bản điển "
        "hình, và nêu những hạn chế rút ra từ thực nghiệm."
    ),
}

CONDENSED_BLOCKS: dict[str, list[tuple[str, str]]] = {
    "chuong2_rut_gon.md": [
        (
            """Đề tài "Hệ hỗ trợ quyết định dựa trên tri thức cho định giá xe ô tô cũ tại thị trường Việt Nam" xây dựng một hệ thống giúp người mua, người bán và chuyên viên định giá xác định khoảng giá hợp lý cho một chiếc xe ô tô đã qua sử dụng. Thay vì chỉ đưa ra một con số, hệ thống trả về **khoảng giá đề xuất**, **mức độ tin cậy**, **các cảnh báo rủi ro** và **lời giải thích** gồm các luật đã được áp dụng và những chiếc xe tương tự làm căn cứ.

Hệ thống được thiết kế theo kiến trúc lai gồm ba kênh suy luận. Kênh thứ nhất là **máy suy diễn luật** mô phỏng cách chuyên gia định giá: lấy giá xe mới làm mốc rồi áp dụng các luật khấu hao theo tuổi xe, số km và các luật điều chỉnh theo hãng, đặc điểm kỹ thuật, lịch sử, tình trạng. Kênh thứ hai là **mô-đun CBR** truy hồi các xe tương tự trong cơ sở tình huống và điều chỉnh giá của chúng về điều kiện của xe cần định giá. Kênh thứ ba là **mô hình Random Forest** huấn luyện trên dữ liệu thị trường, dùng để kiểm chứng chéo. Bộ tổng hợp hợp nhất kết quả của các kênh thành quyết định cuối cùng.""",
            """Đề tài xây dựng một hệ thống giúp người mua, người bán và chuyên viên định giá xác định khoảng giá hợp lý cho xe ô tô đã qua sử dụng. Thay vì chỉ đưa ra một con số, hệ thống trả về **khoảng giá đề xuất**, **mức độ tin cậy**, **các cảnh báo rủi ro** và **lời giải thích** gồm các luật đã áp dụng cùng những xe tương tự làm căn cứ.

Hệ thống theo kiến trúc lai gồm ba kênh suy luận: **máy suy diễn luật** mô phỏng cách chuyên gia định giá, lấy giá xe mới làm mốc rồi áp dụng các luật khấu hao và điều chỉnh; **mô-đun CBR** truy hồi các xe tương tự trong cơ sở tình huống rồi hiệu chỉnh giá về điều kiện của xe cần định giá; và **mô hình Random Forest** huấn luyện trên dữ liệu thị trường để kiểm chứng chéo. Bộ tổng hợp hợp nhất kết quả thành quyết định cuối cùng.""",
        ),
        (
            """**Mô tả các use case**

Hệ thống có mười một use case chia theo ba tác nhân. **Người dùng và chuyên viên định giá** dùng các use case Định giá xe (bao gồm Nhập thông tin xe), Xem giải thích và Xem xe tương tự (hai use case mở rộng của Định giá xe), So sánh kịch bản what-if, và Tra cứu thống kê thị trường. **Chuyên viên định giá** còn dùng Phản hồi giá giao dịch thực tế để hệ thống lưu tình huống mới theo bước Retain của chu trình CBR, và Quản lý cơ sở tình huống. **Quản trị viên tri thức** dùng Quản lý tập luật (bao gồm Kiểm tra mâu thuẫn, trùng lặp luật), Cập nhật dữ liệu thị trường, và Huấn luyện – đánh giá mô hình đối chứng.""",
            """Hệ thống có mười một use case chia theo ba tác nhân. **Người dùng và chuyên viên định giá** dùng Định giá xe (bao gồm Nhập thông tin xe), Xem giải thích và Xem xe tương tự (hai use case mở rộng), So sánh kịch bản what-if và Tra cứu thống kê thị trường. **Chuyên viên định giá** còn dùng Phản hồi giá giao dịch thực tế theo bước Retain của chu trình CBR và Quản lý cơ sở tình huống. **Quản trị viên tri thức** dùng Quản lý tập luật (bao gồm Kiểm tra mâu thuẫn, trùng lặp luật), Cập nhật dữ liệu thị trường và Huấn luyện – đánh giá mô hình đối chứng.""",
        ),
        (
            """**Mô tả các nhóm chức năng**

Hệ thống được phân rã thành năm nhóm chức năng. **Định giá xe** là nhóm cốt lõi, gồm kiểm tra tính hợp lệ của đầu vào, suy diễn trên tập luật, truy hồi và điều chỉnh các tình huống tương tự, tổng hợp kết quả thành khoảng giá kèm độ tin cậy, và sinh lời giải thích. **Phân tích thị trường** cung cấp thống kê giá theo hãng và dòng xe, đường cong khấu hao, cùng công cụ so sánh kịch bản. **Quản lý tri thức** cho phép thêm, sửa, xóa luật, kiểm tra tính nhất quán, quản lý khung tri thức và cơ sở tình huống. **Quản lý dữ liệu** thực hiện thu thập, làm sạch, chuẩn hóa tin rao và huấn luyện mô hình đối chứng. **Phản hồi và học từ giao dịch** ghi nhận giá giao dịch thực tế, lưu tình huống mới, theo dõi sai số theo thời gian và gợi ý hiệu chỉnh hệ số luật.""",
            """Hệ thống phân rã thành năm nhóm chức năng. **Định giá xe** là nhóm cốt lõi, gồm kiểm tra đầu vào, suy diễn trên tập luật, truy hồi và hiệu chỉnh tình huống tương tự, tổng hợp thành khoảng giá kèm độ tin cậy và sinh lời giải thích. **Phân tích thị trường** cung cấp thống kê giá, đường cong khấu hao và công cụ so sánh kịch bản. **Quản lý tri thức** cho phép thêm, sửa, xóa luật, kiểm tra tính nhất quán và quản lý khung tri thức, cơ sở tình huống. **Quản lý dữ liệu** thu thập, làm sạch, chuẩn hóa tin rao và huấn luyện mô hình đối chứng. **Phản hồi và học từ giao dịch** ghi nhận giá giao dịch thực tế, lưu tình huống mới và gợi ý hiệu chỉnh hệ số luật.""",
        ),
    ],
    "chuong3_rut_gon.md": [
        (
            """Cần nói rõ ngay về bản chất của bộ dữ liệu này: **đây là dữ liệu mô phỏng, không phải dữ liệu thu thập trực tiếp từ các sàn rao vặt**. Bộ dữ liệu được sinh ra bằng cách lấy giá xe mới niêm yết của 55 phiên bản thuộc 28 dòng xe làm giá gốc, sau đó áp dụng quy luật khấu hao theo tuổi xe, điều chỉnh theo số km đã đi, tình trạng xe, cấu hình kỹ thuật và khu vực, cuối cùng cộng thêm hai thành phần nhiễu: một hệ số riêng cố định cho từng dòng xe (mô phỏng mức độ ưa chuộng thực tế mà tập luật tổng quát không nắm được) và một nhiễu ngẫu nhiên phân phối log-chuẩn với độ lệch chuẩn 11,5% (mô phỏng kỳ vọng khác nhau của người bán, trang bị thêm và biên độ thương lượng).

Lý do sử dụng dữ liệu mô phỏng là việc thu thập dữ liệu thật ở quy mô vài nghìn tin rao đòi hỏi quyền truy cập hợp pháp vào dữ liệu của các sàn rao vặt, điều nằm ngoài phạm vi và thời lượng của một bài tập lớn học phần. Việc dùng dữ liệu mô phỏng cho phép chạy và đánh giá đầy đủ toàn bộ quy trình của hệ thống, nhưng cũng đặt ra một giới hạn quan trọng mà mục 3.5.5 và phần Kết luận sẽ phân tích kỹ.""",
            """Cần nói rõ ngay về bản chất của bộ dữ liệu: **đây là dữ liệu mô phỏng, không phải dữ liệu thu thập trực tiếp từ các sàn rao vặt**. Dữ liệu được sinh bằng cách lấy giá xe mới niêm yết của 55 phiên bản làm giá gốc, áp dụng quy luật khấu hao theo tuổi xe, điều chỉnh theo số km, tình trạng, cấu hình kỹ thuật và khu vực, cuối cùng cộng hai thành phần nhiễu: một hệ số riêng cố định cho từng dòng xe và một nhiễu log-chuẩn với độ lệch chuẩn 11,5% mô phỏng kỳ vọng khác nhau của người bán.

Lý do dùng dữ liệu mô phỏng là thu thập dữ liệu thật ở quy mô vài nghìn tin rao đòi hỏi quyền truy cập hợp pháp vào dữ liệu của các sàn, nằm ngoài phạm vi của một bài tập lớn. Cách làm này cho phép chạy và đánh giá đầy đủ toàn bộ quy trình, nhưng đặt ra giới hạn quan trọng mà mục 3.5.5 và phần Kết luận sẽ phân tích kỹ.""",
        ),
        (
            """**Mức phân khúc** định nghĩa 10 phân khúc, mỗi phân khúc có hai khe quan trọng: `base_depreciation` là hệ số khấu hao cơ bản mỗi năm và `liquidity` là chỉ số thanh khoản. Bảng 3.5 trình bày các giá trị này.""",
            """**Mức phân khúc** định nghĩa 10 phân khúc, mỗi phân khúc có hai khe quan trọng là hệ số khấu hao cơ bản mỗi năm và chỉ số thanh khoản (Bảng 3.5).""",
        ),
        (
            """Các giá trị này phản ánh một quy luật quen thuộc của thị trường xe cũ Việt Nam: xe phổ thông cỡ nhỏ và SUV đô thị giữ giá tốt nhất (khấu hao 9–10% mỗi năm, thanh khoản cao), còn xe sang mất giá nhanh nhất (15% mỗi năm) và khó bán nhất (thanh khoản 0,45).

**Mức hãng** định nghĩa 12 hãng, mỗi hãng có khe `brand_factor` thể hiện mức độ giữ giá của thương hiệu và `origin_default` là xuất xứ mặc định. Toyota có hệ số cao nhất (1,06), phản ánh uy tín giữ giá trên thị trường xe cũ; VinFast và BMW có hệ số thấp nhất (0,90).""",
            """Các giá trị này phản ánh quy luật quen thuộc của thị trường xe cũ Việt Nam: xe phổ thông cỡ nhỏ và SUV đô thị giữ giá tốt nhất, còn xe sang mất giá nhanh nhất và khó bán nhất.

**Mức hãng** định nghĩa 12 hãng với hệ số thể hiện mức giữ giá của thương hiệu và xuất xứ mặc định. Toyota có hệ số cao nhất (1,06), phản ánh uy tín giữ giá trên thị trường xe cũ; VinFast và BMW thấp nhất (0,90).""",
        ),
        (
            """Về mã hóa, cần phân biệt hai nhánh xử lý khác nhau:

  - **Máy suy diễn và mô-đun CBR không cần mã hóa.** Chúng làm việc trực tiếp trên giá trị gốc dạng chuỗi, vì điều kiện của luật so sánh trực tiếp (`hop_so == "MT"`) và độ đo tương tự cục bộ cho thuộc tính định danh cũng so sánh bằng trực tiếp.
  - **Mô hình Random Forest cần mã hóa.** Tám thuộc tính định danh (`brand`, `model`, `version`, `phan_khuc`, `hop_so`, `nhien_lieu`, `xuat_xu`, `khu_vuc`) được mã hóa thứ tự, mỗi giá trị được gán một số nguyên. Bảng mã hóa được xây dựng **chỉ từ tập huấn luyện**; giá trị chưa từng xuất hiện trong tập huấn luyện được gán giá trị −1 khi áp lên tập kiểm thử. Bốn thuộc tính luận lý được chuyển thành 0 và 1.

Việc xây dựng bảng mã hóa chỉ từ tập huấn luyện là cần thiết để tránh rò rỉ thông tin từ tập kiểm thử sang quá trình huấn luyện.""",
            """Về mã hóa, máy suy diễn và mô-đun CBR làm việc trực tiếp trên giá trị gốc dạng chuỗi nên không cần mã hóa. Riêng mô hình Random Forest cần mã hóa thứ tự tám thuộc tính định danh và chuyển bốn thuộc tính luận lý thành 0 và 1. Bảng mã hóa được xây dựng **chỉ từ tập huấn luyện**, giá trị lạ trong tập kiểm thử được gán −1, nhằm tránh rò rỉ thông tin từ tập kiểm thử sang quá trình huấn luyện.""",
        ),
        (
            """Một điểm quan trọng về vai trò của tập huấn luyện trong hệ thống này: tập huấn luyện vừa được dùng để huấn luyện mô hình Random Forest đối chứng, vừa **chính là cơ sở tình huống** của mô-đun CBR. Tập kiểm thử được dùng chung cho cả bốn phương pháp, bảo đảm so sánh công bằng.""",
            """Tập huấn luyện vừa dùng để huấn luyện Random Forest, vừa **chính là cơ sở tình huống** của mô-đun CBR. Tập kiểm thử dùng chung cho cả bốn phương pháp, bảo đảm so sánh công bằng.""",
        ),
        (
            """Thực nghiệm được thiết kế để trả lời hai câu hỏi: hệ thống định giá chính xác đến đâu, và việc kết hợp hai nguồn tri thức có thực sự tốt hơn từng nguồn riêng lẻ hay không.

Bốn phương pháp được so sánh trên cùng tập kiểm thử 584 xe:

1. **Chỉ dùng luật** – lấy kết quả suy diễn tiến trên tập 25 luật, tương ứng α = 1.
2. **Chỉ dùng CBR** – lấy kết quả từ mô-đun lập luận tình huống, tương ứng α = 0.
3. **Chỉ dùng Random Forest** – mô hình học máy đối chứng.
4. **Hệ lai** – kết hợp luật và CBR với α thích nghi theo Bảng 3.8.

Bốn độ đo được sử dụng:""",
            """Thực nghiệm trả lời hai câu hỏi: hệ thống định giá chính xác đến đâu, và việc kết hợp hai nguồn tri thức có thực sự tốt hơn từng nguồn riêng lẻ hay không. Bốn phương pháp được so sánh trên cùng tập kiểm thử 584 xe: chỉ dùng luật (α = 1), chỉ dùng CBR (α = 0), chỉ dùng Random Forest, và hệ lai kết hợp luật với CBR theo α thích nghi. Bốn độ đo được sử dụng:""",
        ),
        (
            """Trên toàn bộ 584 xe của tập kiểm thử, hệ lai đạt MAE 40,86 triệu đồng, MAPE 10,93% và R² 0,9153. Tỷ lệ giá thực nằm trong khoảng đề xuất đạt 81,85%, với độ rộng khoảng giá trung bình bằng 36,29% giá đề xuất. Độ tin cậy trung bình mà hệ thống tự đánh giá là 87,17%.

Cả 584 xe đều truy hồi được tình huống tương tự, xác nhận độ phủ của cơ sở tình huống là đủ cho tập kiểm thử này.

Về thời gian phản hồi, hệ lai mất trung bình khoảng 6–10 mili-giây cho một lượt định giá tùy theo tải của máy, bao gồm cả truy hồi tình huống, hai lần chạy suy diễn và sinh lời giải thích. Mức này đáp ứng rất thoải mái yêu cầu phi chức năng về thời gian phản hồi dưới 2 giây đã đặt ra ở mục 2.3.3.

Hình 3.10 biểu diễn quan hệ giữa giá đề xuất và giá thực tế trên toàn tập kiểm thử. Các điểm bám khá sát đường chéo, cho thấy hệ thống không có thiên lệch hệ thống về phía định giá cao hoặc thấp. Độ phân tán tăng dần theo giá, phù hợp với thực tế là xe đắt tiền có biên độ dao động giá lớn hơn.""",
            """Trên toàn bộ 584 xe của tập kiểm thử, hệ lai đạt MAE 40,86 triệu đồng, MAPE 10,93% và R² 0,9153. Tỷ lệ giá thực nằm trong khoảng đề xuất đạt 81,85%, độ rộng khoảng giá trung bình bằng 36,29% giá đề xuất, độ tin cậy trung bình hệ thống tự đánh giá là 87,17%. Cả 584 xe đều truy hồi được tình huống tương tự, xác nhận độ phủ của cơ sở tình huống là đủ.

Về thời gian phản hồi, hệ lai mất trung bình khoảng 6–10 mili-giây cho một lượt định giá, đáp ứng rất thoải mái yêu cầu dưới 2 giây ở mục 2.3.3.

Hình 3.10 biểu diễn quan hệ giữa giá đề xuất và giá thực tế. Các điểm bám khá sát đường chéo, cho thấy hệ thống không thiên lệch về phía định giá cao hoặc thấp; độ phân tán tăng dần theo giá, phù hợp với thực tế xe đắt tiền có biên độ dao động lớn hơn.""",
        ),
    ],
}


def _insert_chapter_introduction(text: str, introduction: str) -> str:
    """Chèn đoạn giới thiệu ngay sau tiêu đề chương (dòng cấp 1 đầu tiên)."""
    match = re.search(r"^# .+$", text, flags=re.MULTILINE)
    if match is None:
        print("  CANH BAO: khong tim thay tieu de chuong")
        return text

    insert_at = match.end()
    return text[:insert_at] + "\n\n" + introduction + text[insert_at:]


def main() -> None:
    for file_name, introduction in CHAPTER_INTRODUCTIONS.items():
        path = SCRATCHPAD / file_name
        text = path.read_text(encoding="utf-8")
        original_word_count = len(text.split())

        applied = 0
        for original, condensed in CONDENSED_BLOCKS.get(file_name, []):
            if original not in text:
                print(f"  CANH BAO [{file_name}]: khong tim thay '{original[:50]}...'")
                continue
            text = text.replace(original, condensed)
            applied += 1

        # Chỉ chèn giới thiệu nếu chưa có, tránh chèn lặp khi chạy lại.
        if "Chương 1 trình bày nền tảng" not in text and "Chương 2 chuyển từ" not in text \
                and "Chương 3 trình bày quá trình" not in text:
            text = _insert_chapter_introduction(text, introduction)

        path.write_text(text, encoding="utf-8")

        final_word_count = len(text.split())
        total_blocks = len(CONDENSED_BLOCKS.get(file_name, []))
        print(f"{file_name:26} {original_word_count:>6,} -> {final_word_count:>6,} tu "
              f"({applied}/{total_blocks} doan nen, da them gioi thieu chuong)")


if __name__ == "__main__":
    main()
