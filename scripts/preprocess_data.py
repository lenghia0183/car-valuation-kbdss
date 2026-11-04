"""Tiền xử lý dữ liệu tin rao: làm sạch, loại ngoại lai, chia tập huấn luyện và kiểm thử."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 20_261_104
TEST_RATIO = 0.20
IQR_MULTIPLIER = 1.5
MIN_GROUP_SIZE_FOR_OUTLIER = 8

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def remove_duplicates(dataset: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Loại tin rao trùng lặp theo bộ thuộc tính nhận dạng xe."""
    identity_columns = ["brand", "model", "version", "nam_san_xuat", "so_km", "khu_vuc", "gia"]
    before = len(dataset)
    cleaned = dataset.drop_duplicates(subset=identity_columns, keep="first")
    return cleaned, before - len(cleaned)


def remove_incomplete_rows(dataset: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Loại tin thiếu thông tin bắt buộc hoặc có giá trị vô lý."""
    required_columns = ["brand", "model", "version", "nam_san_xuat", "so_km", "gia"]
    before = len(dataset)

    cleaned = dataset.dropna(subset=required_columns)
    cleaned = cleaned[(cleaned["gia"] > 30) & (cleaned["so_km"] >= 0) & (cleaned["tuoi_xe"] >= 0)]

    return cleaned, before - len(cleaned)


def remove_outliers_by_group(dataset: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Loại ngoại lai bằng quy tắc IQR, áp dụng riêng cho từng nhóm dòng xe - năm sản xuất."""
    keep_mask = pd.Series(True, index=dataset.index)

    for _, group in dataset.groupby(["model", "nam_san_xuat"], observed=True):
        if len(group) < MIN_GROUP_SIZE_FOR_OUTLIER:
            continue

        first_quartile = group["gia"].quantile(0.25)
        third_quartile = group["gia"].quantile(0.75)
        interquartile_range = third_quartile - first_quartile

        lower_bound = first_quartile - IQR_MULTIPLIER * interquartile_range
        upper_bound = third_quartile + IQR_MULTIPLIER * interquartile_range

        outlier_mask = (group["gia"] < lower_bound) | (group["gia"] > upper_bound)
        keep_mask.loc[group.index[outlier_mask]] = False

    return dataset[keep_mask], int((~keep_mask).sum())


def split_train_test(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Chia tập theo phân tầng dòng xe để phân bố hai tập tương đồng."""
    rng = np.random.default_rng(RANDOM_SEED)
    test_indices: list[int] = []

    for _, group in dataset.groupby("model", observed=True):
        group_size = len(group)
        test_size = max(1, int(round(group_size * TEST_RATIO))) if group_size >= 5 else 0
        if test_size == 0:
            continue
        chosen = rng.choice(group.index.to_numpy(), size=test_size, replace=False)
        test_indices.extend(chosen.tolist())

    test_index = pd.Index(test_indices)
    test_set = dataset.loc[test_index]
    train_set = dataset.drop(index=test_index)

    return train_set, test_set


def main() -> None:
    raw_dataset = pd.read_csv(DATA_DIR / "listings_raw.csv", encoding="utf-8-sig")
    initial_count = len(raw_dataset)

    dataset, duplicate_count = remove_duplicates(raw_dataset)
    dataset, incomplete_count = remove_incomplete_rows(dataset)
    dataset, outlier_count = remove_outliers_by_group(dataset)

    # Chuẩn hóa thuộc tính dẫn xuất sau khi đã làm sạch.
    dataset = dataset.copy()
    dataset["km_moi_nam"] = (dataset["so_km"] / dataset["tuoi_xe"].clip(lower=1)).round(1)
    dataset["ty_le_giu_gia"] = (dataset["gia"] / dataset["gia_xe_moi"]).round(4)

    train_set, test_set = split_train_test(dataset)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset.to_csv(DATA_DIR / "listings_clean.csv", index=False, encoding="utf-8-sig")
    train_set.to_csv(DATA_DIR / "train.csv", index=False, encoding="utf-8-sig")
    test_set.to_csv(DATA_DIR / "test.csv", index=False, encoding="utf-8-sig")

    statistics = {
        "so_tin_ban_dau": initial_count,
        "so_tin_trung_lap_da_loai": duplicate_count,
        "so_tin_thieu_thong_tin_da_loai": incomplete_count,
        "so_tin_ngoai_lai_da_loai": outlier_count,
        "so_tin_sau_lam_sach": len(dataset),
        "ty_le_giu_lai": round(len(dataset) / initial_count, 4),
        "so_tin_huan_luyen": len(train_set),
        "so_tin_kiem_thu": len(test_set),
        "gia_trung_binh": round(float(dataset["gia"].mean()), 1),
        "gia_trung_vi": round(float(dataset["gia"].median()), 1),
        "gia_do_lech_chuan": round(float(dataset["gia"].std()), 1),
        "gia_nho_nhat": round(float(dataset["gia"].min()), 1),
        "gia_lon_nhat": round(float(dataset["gia"].max()), 1),
        "so_km_trung_binh": int(dataset["so_km"].mean()),
        "tuoi_xe_trung_binh": round(float(dataset["tuoi_xe"].mean()), 2),
        "so_hang": int(dataset["brand"].nunique()),
        "so_dong_xe": int(dataset["model"].nunique()),
        "so_phien_ban": int(dataset["version"].nunique()),
    }

    (OUTPUT_DIR / "preprocessing_stats.json").write_text(
        json.dumps(statistics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for key, value in statistics.items():
        print(f"{key}: {value:,}" if isinstance(value, (int, float)) else f"{key}: {value}")


if __name__ == "__main__":
    main()
