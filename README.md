# Hệ hỗ trợ quyết định dựa trên tri thức cho định giá xe ô tô cũ

Bài tập lớn học phần **Công nghệ tri thức** – Nhóm 4, chương trình đào tạo thạc sĩ Hệ thống
thông tin, Trường Đại học Công nghiệp Hà Nội.

Hệ thống kết hợp **suy diễn tiến trên tập luật sản xuất** với **lập luận dựa trên tình huống
(CBR)** để định giá xe ô tô đã qua sử dụng. Khác với mô hình học máy thuần túy, hệ thống trả
về không chỉ một con số mà còn khoảng giá, mức độ tin cậy, cảnh báo rủi ro và lời giải thích
truy vết được tới từng luật đã kích hoạt.

**Kết quả chính:** trên tập kiểm thử 584 xe, hệ lai đạt MAPE 10,93% và R² 0,9153 – tốt hơn cả
ba phương pháp đơn lẻ là chỉ dùng luật, chỉ dùng CBR và chỉ dùng Random Forest.

| Thành phần | Quy mô |
| :-- | :-- |
| Khung tri thức | 10 phân khúc, 12 hãng, 28 dòng xe, 55 phiên bản |
| Tập luật sản xuất | 25 luật chia 6 nhóm |
| Cơ sở tình huống | 2.344 tin rao |
| Báo cáo | 57 trang, 23 hình, 20 bảng |

> **Lưu ý về dữ liệu:** bộ dữ liệu trong `data/` là **dữ liệu mô phỏng**, không phải dữ liệu
> thu thập thật từ Bonbanh hay Chợ Tốt Xe. Dữ liệu được sinh theo quy luật khấu hao quan sát
> được trên thị trường cộng nhiễu ngẫu nhiên, nhằm chạy và đánh giá được toàn bộ pipeline.
> Mục 3.1.2 và phần Kết luận của báo cáo phân tích rõ giới hạn này.

## Yêu cầu môi trường

- Python 3.13 (đã kiểm chứng trên 3.13.6)
- Các thư viện: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `streamlit`, `plotly`,
  `playwright`, `python-docx`

Cài đặt:

```bash
py -m pip install numpy pandas scikit-learn matplotlib streamlit plotly playwright python-docx
py -m playwright install chromium
```

## Cấu trúc thư mục

| Thư mục | Nội dung |
| :-- | :-- |
| `kb/` | Cơ sở tri thức: `frames.json` (khung hãng – dòng xe – phiên bản), `rules.json` (25 luật sản xuất) |
| `src/` | Tầng xử lý tri thức và giao diện web |
| `scripts/` | Các kịch bản chuẩn bị dữ liệu, đánh giá, sinh biểu đồ và dựng báo cáo |
| `data/` | Dữ liệu tin rao thô, đã làm sạch, tập huấn luyện và kiểm thử |
| `outputs/` | Kết quả thực nghiệm, biểu đồ, ảnh chụp màn hình và báo cáo |

### Các mô-đun chính trong `src/`

| Tệp | Trách nhiệm |
| :-- | :-- |
| `knowledge_base.py` | Nạp và truy vấn khung tri thức, tập luật |
| `inference_engine.py` | Máy suy diễn tiến: so khớp, giải quyết xung đột, thực thi, lưu vết |
| `case_based_reasoning.py` | Chu trình CBR: truy hồi k-NN, hiệu chỉnh và tái sử dụng giá |
| `valuation_service.py` | Điều phối toàn bộ quy trình định giá, tổng hợp và giải thích |
| `app.py` | Giao diện web Streamlit bốn trang chức năng |

## Chạy lại toàn bộ thực nghiệm

Thực hiện theo đúng thứ tự sau:

```bash
# 1. Sinh bộ dữ liệu mô phỏng 3.000 tin rao
py scripts/generate_dataset.py

# 2. Làm sạch, loại ngoại lai, chia tập huấn luyện và kiểm thử
py scripts/preprocess_data.py

# 3. Đánh giá bốn phương pháp trên cùng tập kiểm thử
py scripts/run_evaluation.py

# 4. Chạy năm kịch bản định giá điển hình
py scripts/run_scenarios.py

# 5. Sinh các biểu đồ dùng trong báo cáo
py scripts/generate_figures.py
```

Kết quả được ghi vào `outputs/evaluation_results.json`, `outputs/scenario_results.json`,
`outputs/test_predictions.csv` và `outputs/figures/`.

## Chạy giao diện web

```bash
py -m streamlit run src/app.py
```

Ứng dụng mở tại `http://localhost:8501` với bốn trang: Định giá, Kết quả và giải thích,
Phân tích thị trường, Quản trị tri thức.

## Chụp lại ảnh màn hình

Ứng dụng phải đang chạy ở cổng 8513 trước khi chạy hai kịch bản chụp ảnh:

```bash
py -m streamlit run src/app.py --server.port 8513 --server.headless true
py scripts/capture_screenshots.py      # 9 ảnh các trang chức năng
py scripts/capture_risk_scenario.py    # ảnh kịch bản xe ngập nước
```

## Dựng lại báo cáo

```bash
py scripts/split_source_doc.py     # tách nội dung gốc thành các tệp Markdown
py scripts/condense_chapter2.py    # rút gọn Chương 2
py scripts/condense_chapter3.py    # rút gọn Chương 3 vòng một
py scripts/condense_round_two.py   # rút gọn vòng hai
py scripts/build_report_docx.py    # dựng DOCX kèm ảnh

# Cập nhật mục lục tự động, đếm trang và xuất PDF (cần Microsoft Word)
powershell -ExecutionPolicy Bypass -File scripts/finalize_with_word.ps1
```

Báo cáo nằm tại `outputs/Bao-cao-BTL-Cong-nghe-tri-thuc.docx` và bản PDF cùng tên.

## Kết quả thực nghiệm

Trên tập kiểm thử 584 xe:

| Phương pháp | MAE (triệu VND) | MAPE (%) | R² |
| :-- | --: | --: | --: |
| Chỉ dùng luật | 43,79 | 11,43 | 0,9055 |
| Chỉ dùng CBR | 45,43 | 12,30 | 0,8930 |
| Chỉ dùng Random Forest | 45,39 | 11,92 | 0,8931 |
| **Hệ lai (luật + CBR)** | **40,86** | **10,93** | **0,9153** |

Tỷ lệ giá thực nằm trong khoảng đề xuất: 81,85%. Thời gian định giá một xe: khoảng 6–10 ms
tùy tải máy.

## Tái lập kết quả

Mọi kịch bản đều cố định hạt giống ngẫu nhiên (`RANDOM_SEED = 20261104`), nên chạy lại
theo đúng thứ tự ở trên sẽ cho đúng các con số trong báo cáo.
