"""Giao diện web của hệ hỗ trợ quyết định định giá xe ô tô cũ.

Bốn trang chức năng: Định giá, Kết quả và giải thích, Phân tích thị trường, Quản trị tri thức.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from case_based_reasoning import CaseBase, CaseBasedReasoner  # noqa: E402
from knowledge_base import KnowledgeBase  # noqa: E402
from valuation_service import ValuationService, VehicleQuery  # noqa: E402

DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = PROJECT_ROOT / "kb"

PRIMARY_COLOR = "#1f4e79"
ACCENT_COLOR = "#c55a11"

st.set_page_config(
    page_title="Hệ hỗ trợ quyết định định giá xe ô tô cũ",
    page_icon="🚗",
    layout="wide",
)


@st.cache_resource
def load_system() -> tuple[KnowledgeBase, ValuationService, pd.DataFrame]:
    knowledge_base = KnowledgeBase()
    train_set = pd.read_csv(DATA_DIR / "train.csv", encoding="utf-8-sig")
    case_base = CaseBase(train_set)
    reasoner = CaseBasedReasoner(case_base, k=5, min_similarity=0.55)
    service = ValuationService(knowledge_base, reasoner)
    return knowledge_base, service, train_set


@st.cache_data
def load_clean_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "listings_clean.csv", encoding="utf-8-sig")


@st.cache_data
def load_rules() -> list[dict]:
    return json.loads((KB_DIR / "rules.json").read_text(encoding="utf-8"))["rules"]


knowledge_base, valuation_service, train_set = load_system()

SEGMENT_LABELS = {key: value["label"] for key, value in knowledge_base.segments.items()}


def render_valuation_page() -> None:
    st.title("🚗 Định giá xe ô tô cũ")
    st.caption(
        "Hệ hỗ trợ quyết định dựa trên tri thức – kết hợp suy diễn trên luật "
        "và lập luận dựa trên tình huống"
    )

    # Không dùng st.form vì ba danh sách chọn hãng - dòng xe - phiên bản phụ thuộc nhau
    # và phải lọc lại ngay khi người dùng đổi lựa chọn ở cấp trên.
    st.subheader("Thông tin xe")

    column_left, column_middle, column_right = st.columns(3)

    with column_left:
        brand = st.selectbox("Hãng xe", knowledge_base.list_brands(), key="brand_select")
        model = st.selectbox("Dòng xe", knowledge_base.list_models(brand), key=f"model_{brand}")
        version = st.selectbox(
            "Phiên bản",
            knowledge_base.list_versions(brand, model),
            key=f"version_{brand}_{model}",
        )

    with column_middle:
        year = st.number_input(
            "Năm sản xuất", min_value=2010, max_value=2026, value=2020, step=1
        )
        mileage = st.number_input(
            "Số km đã đi", min_value=0, max_value=500_000, value=60_000, step=1_000
        )
        region = st.selectbox("Khu vực rao bán", knowledge_base.list_regions())

    with column_right:
        origin = st.selectbox(
            "Xuất xứ",
            ["Theo mặc định của hãng", "lap_rap", "nhap_khau"],
            format_func=lambda value: {
                "Theo mặc định của hãng": "Theo mặc định của hãng",
                "lap_rap": "Lắp ráp trong nước",
                "nhap_khau": "Nhập khẩu nguyên chiếc",
            }[value],
        )
        st.markdown("**Tình trạng và lịch sử**")
        is_flooded = st.checkbox("Xe từng ngập nước")
        had_accident = st.checkbox("Xe từng tai nạn nặng")
        was_commercial = st.checkbox("Từng đăng ký kinh doanh vận tải")
        single_owner = st.checkbox("Một chủ, bảo dưỡng hãng đầy đủ")

    submitted = st.button("Định giá", type="primary", use_container_width=True)

    if submitted:
        query = VehicleQuery(
            brand=brand,
            model=model,
            version=version,
            nam_san_xuat=int(year),
            so_km=int(mileage),
            khu_vuc=region,
            xuat_xu=None if origin == "Theo mặc định của hãng" else origin,
            ngap_nuoc=is_flooded,
            tai_nan_nang=had_accident,
            xe_dich_vu=was_commercial,
            mot_chu_bao_duong_hang=single_owner,
        )
        st.session_state["valuation_result"] = valuation_service.evaluate(query)
        st.session_state["valuation_query"] = query
        st.success("Đã định giá xong. Xem chi tiết ở trang **Kết quả và giải thích**.")

    if "valuation_result" in st.session_state:
        result = st.session_state["valuation_result"]
        st.divider()
        st.subheader("Kết quả nhanh")

        metric_left, metric_middle, metric_right = st.columns(3)
        metric_left.metric("Giá đề xuất", f"{result.suggested_price:,.0f} triệu")
        metric_middle.metric(
            "Khoảng giá", f"{result.price_lower:,.0f} – {result.price_upper:,.0f}"
        )
        metric_right.metric(
            "Độ tin cậy", f"{result.confidence:.0%}", delta=result.confidence_label
        )

        for warning_message in result.warnings:
            st.warning(warning_message)


def render_result_page() -> None:
    st.title("📊 Kết quả và giải thích")

    if "valuation_result" not in st.session_state:
        st.info("Chưa có kết quả định giá. Hãy nhập thông tin xe ở trang **Định giá**.")
        return

    result = st.session_state["valuation_result"]
    query = st.session_state["valuation_query"]

    st.subheader(f"{query.brand} {query.model} {query.version} – đời {query.nam_san_xuat}")

    metric_columns = st.columns(4)
    metric_columns[0].metric("Giá đề xuất", f"{result.suggested_price:,.0f} tr")
    metric_columns[1].metric("Giá từ luật", f"{result.rule_price:,.0f} tr")
    metric_columns[2].metric(
        "Giá từ tình huống",
        f"{result.cbr_price:,.0f} tr" if result.cbr_price is not None else "Không có",
    )
    metric_columns[3].metric("Độ tin cậy", f"{result.confidence:.0%}", result.confidence_label)

    # Thanh trực quan thể hiện khoảng giá.
    range_figure = go.Figure()
    range_figure.add_trace(
        go.Scatter(
            x=[result.price_lower, result.price_upper],
            y=[0, 0],
            mode="lines",
            line={"color": PRIMARY_COLOR, "width": 18},
            name="Khoảng giá đề xuất",
        )
    )
    range_figure.add_trace(
        go.Scatter(
            x=[result.suggested_price],
            y=[0],
            mode="markers+text",
            marker={"color": ACCENT_COLOR, "size": 22, "symbol": "diamond"},
            text=[f"{result.suggested_price:,.0f} tr"],
            textposition="top center",
            name="Giá đề xuất",
        )
    )
    range_figure.update_layout(
        height=190,
        showlegend=False,
        yaxis={"visible": False, "range": [-0.6, 0.6]},
        xaxis={"title": "Giá (triệu VND)"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title="Khoảng giá đề xuất",
    )
    st.plotly_chart(range_figure, use_container_width=True)

    if result.warnings:
        st.subheader("⚠️ Cảnh báo rủi ro")
        for warning_message in result.warnings:
            st.warning(warning_message)

    explanation_tab, rules_tab, cases_tab = st.tabs(
        ["Giải thích kết quả", "Vết suy diễn", "Xe tương tự"]
    )

    with explanation_tab:
        for line in result.explanation_lines:
            st.markdown(f"- {line}")

    with rules_tab:
        st.markdown("**Các luật đã được kích hoạt trong quá trình suy diễn tiến:**")

        rule_frame = pd.DataFrame(
            [
                {
                    "Mã luật": fired.rule_id,
                    "Tác động": fired.label,
                    "Hệ số": round(fired.factor, 3),
                    "Giá trước (tr)": round(fired.price_before, 1),
                    "Giá sau (tr)": round(fired.price_after, 1),
                    "Chênh lệch (tr)": round(fired.price_delta, 1),
                }
                for fired in result.fired_rules
            ]
        )
        st.dataframe(rule_frame, use_container_width=True, hide_index=True)

        waterfall_figure = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["absolute"] + ["relative"] * len(result.fired_rules),
                x=["Giá xe mới"] + [fired.rule_id for fired in result.fired_rules],
                y=[result.fired_rules[0].price_before if result.fired_rules else 0]
                + [fired.price_delta for fired in result.fired_rules],
                text=["Gốc"] + [fired.label for fired in result.fired_rules],
                connector={"line": {"color": "#999999"}},
                increasing={"marker": {"color": "#2e7d32"}},
                decreasing={"marker": {"color": "#c62828"}},
                totals={"marker": {"color": PRIMARY_COLOR}},
            )
        )
        waterfall_figure.update_layout(
            title="Ảnh hưởng của từng luật lên giá xe",
            height=430,
            yaxis={"title": "Giá (triệu VND)"},
            margin={"l": 20, "r": 20, "t": 60, "b": 20},
        )
        st.plotly_chart(waterfall_figure, use_container_width=True)

    with cases_tab:
        if not result.retrieved_cases:
            st.info("Không tìm được xe tương tự trong cơ sở tình huống.")
        else:
            st.markdown(
                f"**{len(result.retrieved_cases)} xe tương tự nhất** được truy hồi "
                "từ cơ sở tình huống:"
            )
            case_frame = pd.DataFrame(
                [
                    {
                        "Mã": case.case_id,
                        "Xe": f"{case.brand} {case.model} {case.version}",
                        "Đời": case.nam_san_xuat,
                        "Số km": f"{case.so_km:,}",
                        "Khu vực": case.khu_vuc,
                        "Giá rao (tr)": round(case.gia, 1),
                        "Giá sau hiệu chỉnh (tr)": round(case.adjusted_price, 1),
                        "Độ tương tự": f"{case.similarity:.3f}",
                    }
                    for case in result.retrieved_cases
                ]
            )
            st.dataframe(case_frame, use_container_width=True, hide_index=True)


def render_market_page() -> None:
    st.title("📈 Phân tích thị trường")

    dataset = load_clean_dataset()

    summary_columns = st.columns(4)
    summary_columns[0].metric("Số tin rao", f"{len(dataset):,}")
    summary_columns[1].metric("Giá trung bình", f"{dataset['gia'].mean():,.0f} tr")
    summary_columns[2].metric("Giá trung vị", f"{dataset['gia'].median():,.0f} tr")
    summary_columns[3].metric("Số dòng xe", f"{dataset['model'].nunique()}")

    left_column, right_column = st.columns(2)

    with left_column:
        distribution_figure = px.histogram(
            dataset,
            x="gia",
            nbins=45,
            title="Phân bố giá xe trên thị trường",
            labels={"gia": "Giá (triệu VND)", "count": "Số tin rao"},
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        distribution_figure.update_layout(height=390, yaxis_title="Số tin rao")
        st.plotly_chart(distribution_figure, use_container_width=True)

    with right_column:
        segment_frame = (
            dataset.groupby("phan_khuc")["gia"].median().reset_index().sort_values("gia")
        )
        segment_frame["phan_khuc"] = segment_frame["phan_khuc"].map(SEGMENT_LABELS)

        segment_figure = px.bar(
            segment_frame,
            x="gia",
            y="phan_khuc",
            orientation="h",
            title="Giá trung vị theo phân khúc",
            labels={"gia": "Giá trung vị (triệu VND)", "phan_khuc": ""},
            color_discrete_sequence=[ACCENT_COLOR],
        )
        segment_figure.update_layout(height=390)
        st.plotly_chart(segment_figure, use_container_width=True)

    st.subheader("Đường cong khấu hao theo phân khúc")

    depreciation_frame = (
        dataset.groupby(["phan_khuc", "tuoi_xe"])["ty_le_giu_gia"].mean().reset_index()
    )
    depreciation_frame["phan_khuc"] = depreciation_frame["phan_khuc"].map(SEGMENT_LABELS)

    depreciation_figure = px.line(
        depreciation_frame,
        x="tuoi_xe",
        y="ty_le_giu_gia",
        color="phan_khuc",
        markers=True,
        title="Tỷ lệ giữ giá theo tuổi xe",
        labels={
            "tuoi_xe": "Tuổi xe (năm)",
            "ty_le_giu_gia": "Tỷ lệ giữ giá so với xe mới",
            "phan_khuc": "Phân khúc",
        },
    )
    depreciation_figure.update_layout(height=470)
    st.plotly_chart(depreciation_figure, use_container_width=True)

    st.subheader("Quan hệ giữa số km đã đi và giá bán")

    scatter_figure = px.scatter(
        dataset.sample(min(1_200, len(dataset)), random_state=42),
        x="so_km",
        y="gia",
        color="phan_khuc",
        opacity=0.6,
        labels={
            "so_km": "Số km đã đi",
            "gia": "Giá rao bán (triệu VND)",
            "phan_khuc": "Phân khúc",
        },
    )
    scatter_figure.update_layout(height=450)
    st.plotly_chart(scatter_figure, use_container_width=True)


def render_knowledge_admin_page() -> None:
    st.title("🧠 Quản trị cơ sở tri thức")

    rules = load_rules()

    summary_columns = st.columns(4)
    summary_columns[0].metric("Số luật sản xuất", len(rules))
    summary_columns[1].metric("Số khung phiên bản", len(knowledge_base.version_frames))
    summary_columns[2].metric("Số tình huống", f"{len(train_set):,}")
    summary_columns[3].metric("Số hãng xe", len(knowledge_base.list_brands()))

    rules_tab, frames_tab, consistency_tab = st.tabs(
        ["Tập luật sản xuất", "Khung tri thức", "Kiểm tra nhất quán"]
    )

    with rules_tab:
        group_names = sorted({rule["group"] for rule in rules})
        selected_group = st.selectbox("Lọc theo nhóm luật", ["Tất cả"] + group_names)

        visible_rules = (
            rules if selected_group == "Tất cả"
            else [rule for rule in rules if rule["group"] == selected_group]
        )

        rules_frame = pd.DataFrame(
            [
                {
                    "Mã": rule["id"],
                    "Nhóm": rule["group"],
                    "Ưu tiên": rule["priority"],
                    "Mô tả": rule["description"],
                    "Số điều kiện": len(rule["if"]),
                    "Số hành động": len(rule["then"]),
                }
                for rule in visible_rules
            ]
        )
        st.dataframe(rules_frame, use_container_width=True, hide_index=True, height=430)

    with frames_tab:
        frames_frame = pd.DataFrame(
            [
                {
                    "Hãng": frame.brand,
                    "Dòng xe": frame.model,
                    "Phiên bản": frame.version,
                    "Phân khúc": SEGMENT_LABELS[frame.segment],
                    "Giá xe mới (tr)": frame.new_price,
                    "Hộp số": frame.transmission,
                    "Nhiên liệu": frame.fuel,
                    "Hệ số thương hiệu": frame.brand_factor,
                }
                for frame in knowledge_base.version_frames.values()
            ]
        )
        st.dataframe(frames_frame, use_container_width=True, hide_index=True, height=430)

    with consistency_tab:
        st.markdown("**Kết quả kiểm tra tính nhất quán của cơ sở tri thức**")

        rule_ids = [rule["id"] for rule in rules]
        duplicate_ids = {rule_id for rule_id in rule_ids if rule_ids.count(rule_id) > 1}

        checks = [
            ("Không có mã luật trùng lặp", not duplicate_ids),
            ("Mọi luật đều có ít nhất một điều kiện", all(rule["if"] for rule in rules)),
            ("Mọi luật đều có ít nhất một hành động", all(rule["then"] for rule in rules)),
            (
                "Mọi khung phiên bản đều có giá xe mới hợp lệ",
                all(frame.new_price > 0 for frame in knowledge_base.version_frames.values()),
            ),
            (
                "Mọi phân khúc đều có hệ số khấu hao trong khoảng hợp lý",
                all(
                    0.05 <= segment["base_depreciation"] <= 0.25
                    for segment in knowledge_base.segments.values()
                ),
            ),
            (
                "Cơ sở tình huống đủ lớn để truy hồi",
                len(train_set) >= 500,
            ),
        ]

        for check_name, passed in checks:
            if passed:
                st.success(f"✓ {check_name}")
            else:
                st.error(f"✗ {check_name}")


PAGES = {
    "Định giá": render_valuation_page,
    "Kết quả và giải thích": render_result_page,
    "Phân tích thị trường": render_market_page,
    "Quản trị tri thức": render_knowledge_admin_page,
}


def main() -> None:
    with st.sidebar:
        st.markdown("### Hệ hỗ trợ quyết định\n#### Định giá xe ô tô cũ")
        st.caption("Học phần Công nghệ tri thức – Nhóm 4")
        st.divider()
        selected_page = st.radio("Chức năng", list(PAGES.keys()), label_visibility="collapsed")
        st.divider()
        st.caption(
            f"Cơ sở tri thức: {knowledge_base.rule_count()} luật, "
            f"{len(knowledge_base.version_frames)} khung phiên bản, "
            f"{len(train_set):,} tình huống."
        )

    PAGES[selected_page]()


main()
