"""Sinh các biểu đồ dùng trong báo cáo từ kết quả thực nghiệm thật."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

PRIMARY_COLOR = "#1f4e79"
ACCENT_COLOR = "#c55a11"
FIGURE_DPI = 150

SEGMENT_LABELS = {
    "hatchback_a": "Hatchback hạng A",
    "sedan_b": "Sedan hạng B",
    "sedan_c": "Sedan hạng C",
    "sedan_d": "Sedan hạng D",
    "suv_b": "SUV hạng B",
    "suv_c": "SUV hạng C",
    "suv_d": "SUV hạng D",
    "mpv": "MPV đa dụng",
    "pickup": "Bán tải",
    "luxury": "Xe sang",
}


def _configure_font() -> None:
    """Chọn font hỗ trợ tiếng Việt có dấu."""
    plt.rcParams["font.family"] = ["Segoe UI", "Arial", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.autolayout"] = False


def _save(figure: plt.Figure, filename: str) -> None:
    output_path = FIGURE_DIR / filename
    figure.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Da tao: {filename}")


def plot_price_distribution(dataset: pd.DataFrame) -> None:
    figure, axes = plt.subplots(figsize=(9, 5))

    axes.hist(dataset["gia"], bins=45, color=PRIMARY_COLOR, edgecolor="white", alpha=0.9)
    axes.axvline(
        dataset["gia"].median(),
        color=ACCENT_COLOR,
        linestyle="--",
        linewidth=2,
        label=f"Trung vị: {dataset['gia'].median():,.0f} triệu",
    )

    axes.set_xlabel("Giá rao bán (triệu VND)")
    axes.set_ylabel("Số tin rao")
    axes.set_title("Phân bố giá xe trong tập dữ liệu sau làm sạch")
    axes.legend()
    axes.grid(axis="y", alpha=0.3)

    _save(figure, "hinh_phan_bo_gia.png")


def plot_listings_by_brand(dataset: pd.DataFrame) -> None:
    counts = dataset["brand"].value_counts().sort_values()

    figure, axes = plt.subplots(figsize=(9, 5.5))
    axes.barh(counts.index, counts.to_numpy(), color=PRIMARY_COLOR)

    for index, value in enumerate(counts.to_numpy()):
        axes.text(value + 4, index, str(value), va="center", fontsize=9)

    axes.set_xlabel("Số tin rao")
    axes.set_title("Số lượng tin rao theo hãng xe")
    axes.grid(axis="x", alpha=0.3)

    _save(figure, "hinh_tin_rao_theo_hang.png")


def plot_depreciation_curves(dataset: pd.DataFrame) -> None:
    figure, axes = plt.subplots(figsize=(9, 5.5))

    featured_segments = ["sedan_b", "suv_c", "mpv", "suv_d", "luxury"]

    for segment_key in featured_segments:
        segment_data = dataset[dataset["phan_khuc"] == segment_key]
        if segment_data.empty:
            continue

        curve = segment_data.groupby("tuoi_xe")["ty_le_giu_gia"].mean().sort_index()
        axes.plot(curve.index, curve.to_numpy(), marker="o", linewidth=2, label=SEGMENT_LABELS[segment_key])

    axes.set_xlabel("Tuổi xe (năm)")
    axes.set_ylabel("Tỷ lệ giữ giá so với xe mới")
    axes.set_title("Đường cong khấu hao theo phân khúc")
    axes.legend()
    axes.grid(alpha=0.3)

    _save(figure, "hinh_duong_cong_khau_hao.png")


def plot_method_comparison(evaluation: dict) -> None:
    results = evaluation["ket_qua_cac_phuong_phap"]
    method_labels = {
        "Chi dung luat": "Chỉ dùng luật",
        "Chi dung CBR": "Chỉ dùng CBR",
        "Chi dung Random Forest": "Chỉ dùng Random Forest",
        "He lai (luat + CBR)": "Hệ lai (luật + CBR)",
    }

    names = [method_labels[key] for key in results]
    mae_values = [results[key]["MAE"] for key in results]
    mape_values = [results[key]["MAPE"] for key in results]
    r2_values = [results[key]["R2"] for key in results]

    figure, axes_list = plt.subplots(1, 3, figsize=(14, 4.8))

    for axes, values, title, unit in zip(
        axes_list,
        [mae_values, mape_values, r2_values],
        ["MAE (triệu VND)", "MAPE (%)", "Hệ số xác định R²"],
        ["{:.2f}", "{:.2f}%", "{:.4f}"],
        strict=True,
    ):
        # Phương pháp tốt nhất được tô màu nhấn.
        best_index = values.index(max(values)) if "R²" in title else values.index(min(values))
        colors = [ACCENT_COLOR if index == best_index else PRIMARY_COLOR for index in range(len(values))]

        bars = axes.bar(range(len(values)), values, color=colors)
        axes.set_xticks(range(len(names)))
        axes.set_xticklabels(names, rotation=22, ha="right", fontsize=9)
        axes.set_title(title)
        axes.grid(axis="y", alpha=0.3)

        for bar, value in zip(bars, values, strict=True):
            axes.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                unit.format(value),
                ha="center",
                va="bottom",
                fontsize=9,
            )

    figure.suptitle("So sánh bốn phương pháp định giá trên cùng tập kiểm thử", fontsize=13)
    _save(figure, "hinh_so_sanh_phuong_phap.png")


def plot_error_by_segment(evaluation: dict) -> None:
    segment_errors = evaluation["sai_so_theo_phan_khuc"]

    frame = pd.DataFrame(segment_errors).T
    frame.index = [SEGMENT_LABELS.get(key, key) for key in frame.index]
    frame = frame.sort_values("MAPE")

    figure, axes = plt.subplots(figsize=(9, 5.5))
    bars = axes.barh(frame.index, frame["MAPE"], color=PRIMARY_COLOR)

    for bar, value, count in zip(bars, frame["MAPE"], frame["so_xe"], strict=True):
        axes.text(
            value + 0.12, bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}% (n={int(count)})", va="center", fontsize=9,
        )

    axes.set_xlabel("MAPE (%)")
    axes.set_title("Sai số phần trăm tuyệt đối trung bình theo phân khúc")
    axes.set_xlim(0, frame["MAPE"].max() * 1.30)
    axes.grid(axis="x", alpha=0.3)

    _save(figure, "hinh_sai_so_theo_phan_khuc.png")


def plot_predicted_vs_actual(predictions: pd.DataFrame) -> None:
    figure, axes = plt.subplots(figsize=(7.2, 7))

    axes.scatter(
        predictions["gia_thuc_te"], predictions["gia_de_xuat"],
        alpha=0.42, s=22, color=PRIMARY_COLOR, edgecolors="none",
    )

    max_price = max(predictions["gia_thuc_te"].max(), predictions["gia_de_xuat"].max()) * 1.03
    axes.plot([0, max_price], [0, max_price], color=ACCENT_COLOR, linestyle="--", linewidth=2, label="Dự đoán hoàn hảo")

    axes.set_xlabel("Giá thực tế (triệu VND)")
    axes.set_ylabel("Giá hệ thống đề xuất (triệu VND)")
    axes.set_title("Giá đề xuất so với giá thực tế trên tập kiểm thử")
    axes.legend()
    axes.grid(alpha=0.3)
    axes.set_xlim(0, max_price)
    axes.set_ylim(0, max_price)

    _save(figure, "hinh_du_doan_vs_thuc_te.png")


def plot_error_by_age(evaluation: dict) -> None:
    age_errors = evaluation["sai_so_theo_nhom_tuoi"]
    frame = pd.DataFrame(age_errors).T

    age_order = ["0-2 nam", "3-5 nam", "6-8 nam", "9-12 nam", "tren 12 nam"]
    age_labels = ["0-2 năm", "3-5 năm", "6-8 năm", "9-12 năm", "Trên 12 năm"]
    frame = frame.reindex([key for key in age_order if key in frame.index])

    figure, axes_left = plt.subplots(figsize=(9, 5))

    bars = axes_left.bar(range(len(frame)), frame["MAE"], color=PRIMARY_COLOR, alpha=0.85, label="MAE (triệu VND)")
    axes_left.set_ylabel("MAE (triệu VND)", color=PRIMARY_COLOR)
    axes_left.set_xticks(range(len(frame)))
    axes_left.set_xticklabels(age_labels[: len(frame)])
    axes_left.tick_params(axis="y", labelcolor=PRIMARY_COLOR)

    for bar, value in zip(bars, frame["MAE"], strict=True):
        axes_left.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f"{value:.1f}", ha="center", fontsize=9, color=PRIMARY_COLOR,
        )

    axes_right = axes_left.twinx()
    axes_right.plot(
        range(len(frame)), frame["MAPE"], color=ACCENT_COLOR,
        marker="o", linewidth=2.4, label="MAPE (%)",
    )
    axes_right.set_ylabel("MAPE (%)", color=ACCENT_COLOR)
    axes_right.tick_params(axis="y", labelcolor=ACCENT_COLOR)
    axes_right.set_ylim(0, frame["MAPE"].max() * 1.45)

    for index, value in enumerate(frame["MAPE"]):
        axes_right.text(index, value + 0.45, f"{value:.2f}%", ha="center", fontsize=9, color=ACCENT_COLOR)

    axes_left.set_xlabel("Nhóm tuổi xe")
    axes_left.set_title("Sai số định giá theo nhóm tuổi xe")
    axes_left.grid(axis="y", alpha=0.25)

    _save(figure, "hinh_sai_so_theo_tuoi_xe.png")


def main() -> None:
    _configure_font()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_csv(DATA_DIR / "listings_clean.csv", encoding="utf-8-sig")
    evaluation = json.loads((OUTPUT_DIR / "evaluation_results.json").read_text(encoding="utf-8"))
    predictions = pd.read_csv(OUTPUT_DIR / "test_predictions.csv", encoding="utf-8-sig")

    plot_price_distribution(dataset)
    plot_listings_by_brand(dataset)
    plot_depreciation_curves(dataset)
    plot_method_comparison(evaluation)
    plot_error_by_segment(evaluation)
    plot_predicted_vs_actual(predictions)
    plot_error_by_age(evaluation)

    print(f"\nTat ca bieu do da luu tai: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
