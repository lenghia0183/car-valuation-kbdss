"""In toàn bộ số liệu cần thiết để viết chương Thực nghiệm và đánh giá của báo cáo."""

from __future__ import annotations

import io
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main() -> None:
    evaluation = json.loads((OUTPUT_DIR / "evaluation_results.json").read_text(encoding="utf-8"))
    preprocessing = json.loads((OUTPUT_DIR / "preprocessing_stats.json").read_text(encoding="utf-8"))
    dataset = pd.read_csv(DATA_DIR / "listings_clean.csv", encoding="utf-8-sig")

    print("===== TIEN XU LY =====")
    for key, value in preprocessing.items():
        print(f"  {key}: {value}")

    print("\n===== PHAN BO THEO HANG =====")
    print(dataset["brand"].value_counts().to_string())

    print("\n===== PHAN BO THEO PHAN KHUC =====")
    print(dataset["phan_khuc"].value_counts().to_string())

    print("\n===== PHAN BO NAM SAN XUAT =====")
    print(dataset["nam_san_xuat"].value_counts().sort_index().to_string())

    print("\n===== THONG KE MO TA =====")
    numeric_columns = ["gia", "so_km", "tuoi_xe", "km_moi_nam", "ty_le_giu_gia"]
    print(dataset[numeric_columns].describe().round(2).to_string())

    print("\n===== THUOC TINH RUI RO =====")
    for column in ["ngap_nuoc", "tai_nan_nang", "xe_dich_vu", "mot_chu_bao_duong_hang"]:
        print(f"  {column}: {int(dataset[column].sum())} tin ({dataset[column].mean() * 100:.1f}%)")

    print("\n===== THUOC TINH DINH DANH =====")
    for column in ["hop_so", "nhien_lieu", "xuat_xu", "khu_vuc"]:
        print(f"  {column}: {dataset[column].value_counts().to_dict()}")

    print("\n===== KET QUA DANH GIA =====")
    skip_keys = {"sai_so_theo_phan_khuc", "sai_so_theo_nhom_tuoi"}
    print(json.dumps(
        {key: value for key, value in evaluation.items() if key not in skip_keys},
        ensure_ascii=False, indent=2,
    ))

    print("\n===== GIA TRUNG VI THEO PHAN KHUC =====")
    print(dataset.groupby("phan_khuc")["gia"].agg(["count", "median", "mean"]).round(1).to_string())


if __name__ == "__main__":
    main()
