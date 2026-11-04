"""Sinh bộ dữ liệu tin rao xe ô tô cũ mô phỏng thị trường Việt Nam.

LƯU Ý QUAN TRỌNG: Đây là dữ liệu MÔ PHỎNG, không phải dữ liệu thu thập thực tế từ
Bonbanh hay Chợ Tốt Xe. Dữ liệu được sinh theo quy luật khấu hao và biến động giá
quan sát được trên thị trường, có thêm nhiễu ngẫu nhiên để mô phỏng sự phân tán của
giá rao bán. Mục đích là cho phép chạy và đánh giá toàn bộ pipeline của hệ thống.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from knowledge_base import KnowledgeBase  # noqa: E402

RANDOM_SEED = 20_261_104
TARGET_LISTING_COUNT = 3_000
CURRENT_YEAR = date.today().year
OLDEST_YEAR = CURRENT_YEAR - 14

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _sample_year(rng: np.random.Generator) -> int:
    """Tin rao tập trung ở xe 3-8 năm tuổi, thưa dần ở xe quá mới hoặc quá cũ."""
    age = int(np.clip(rng.gamma(shape=3.4, scale=1.7), 0, CURRENT_YEAR - OLDEST_YEAR))
    return CURRENT_YEAR - age


def _sample_mileage(rng: np.random.Generator, age: int) -> int:
    """Số km bám quanh 13.000 km/năm, có đuôi dài cho xe chạy dịch vụ."""
    mean_km_per_year = rng.normal(loc=13_000, scale=4_200)
    mean_km_per_year = max(2_500.0, mean_km_per_year)

    if rng.random() < 0.07:  # xe chạy dịch vụ
        mean_km_per_year *= rng.uniform(1.8, 2.6)

    mileage = mean_km_per_year * max(age, 0.4)
    return int(np.clip(mileage, 500, 480_000))


def _depreciation_ratio(age: float, base_depreciation: float) -> float:
    """Tỷ lệ giữ giá theo tuổi xe, khớp với nhóm luật khấu hao R01-R05."""
    if age < 1:
        return 0.90
    if age < 3:
        return 0.90 * (1 - base_depreciation) ** age
    if age < 7:
        return 0.90 * (1 - base_depreciation) ** 3 * (1 - base_depreciation * 0.85) ** (age - 3)
    if age < 15:
        return (
            0.90
            * (1 - base_depreciation) ** 3
            * (1 - base_depreciation * 0.85) ** 4
            * (1 - base_depreciation * 0.65) ** (age - 7)
        )
    return max(
        0.08,
        0.90
        * (1 - base_depreciation) ** 3
        * (1 - base_depreciation * 0.85) ** 4
        * (1 - base_depreciation * 0.65) ** 8
        * 0.96 ** (age - 15),
    )


def _mileage_factor(km_per_year: float, total_km: int) -> float:
    if km_per_year < 8_000:
        factor = 1.05
    elif km_per_year <= 15_000:
        factor = 1.00
    elif km_per_year <= 25_000:
        factor = 0.94
    else:
        factor = 0.87

    if total_km > 200_000:
        factor *= 0.92

    return factor


def generate_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    knowledge_base = KnowledgeBase()

    version_frames = list(knowledge_base.version_frames.values())
    region_names = knowledge_base.list_regions()
    region_weights = np.array([0.27, 0.31, 0.12, 0.10, 0.07, 0.13])
    region_weights = region_weights / region_weights.sum()

    # Dòng xe phổ thông có nhiều tin rao hơn xe sang.
    popularity = np.array(
        [1.0 / (1.0 + 2.5 * (frame.new_price / 1_000.0) ** 1.4) for frame in version_frames]
    )
    popularity = popularity / popularity.sum()

    # Mỗi dòng xe có một hệ số giữ giá riêng, cố định theo dòng, mà tập luật chỉ mô tả
    # được ở mức hãng và phân khúc. Đây là phần tri thức mà lập luận dựa trên tình huống
    # nắm bắt được còn luật tổng quát thì không.
    model_keys = sorted({(frame.brand, frame.model) for frame in version_frames})
    model_specific_effects = {
        key: float(rng.lognormal(mean=0.0, sigma=0.075)) for key in model_keys
    }

    records: list[dict[str, object]] = []

    for listing_index in range(TARGET_LISTING_COUNT):
        frame = version_frames[int(rng.choice(len(version_frames), p=popularity))]

        year = _sample_year(rng)
        age = CURRENT_YEAR - year
        mileage = _sample_mileage(rng, age)
        km_per_year = mileage / max(1, age)

        region = str(rng.choice(region_names, p=region_weights))

        is_flooded = bool(rng.random() < 0.025)
        had_major_accident = bool(rng.random() < 0.045)
        was_commercial = bool(rng.random() < 0.09 or km_per_year > 26_000)
        single_owner_full_service = bool(rng.random() < 0.22)

        origin = frame.origin_default
        if rng.random() < 0.10:
            origin = "nhap_khau" if origin == "lap_rap" else "lap_rap"

        price = frame.new_price * _depreciation_ratio(age, frame.base_depreciation)
        price *= _mileage_factor(km_per_year, mileage)

        if is_flooded:
            price *= 0.70
        if had_major_accident:
            price *= 0.78
        if was_commercial:
            price *= 0.88
        if single_owner_full_service:
            price *= 1.04

        if frame.transmission in {"AT", "CVT"}:
            price *= 1.02
        elif frame.segment != "pickup":
            price *= 0.96

        if frame.fuel == "dau" and frame.segment in {"suv_d", "pickup", "mpv"}:
            price *= 1.03
        if origin == "nhap_khau":
            price *= 1.03

        price *= frame.brand_factor
        price *= knowledge_base.region_factor(region)

        if frame.liquidity < 0.7:
            price *= 0.96
        if frame.segment == "luxury" and age > 8:
            price *= 0.90

        # Hiệu ứng riêng của từng dòng xe mà tập luật tổng quát không mô tả được:
        # mức độ ưa chuộng thực tế, chi phí phụ tùng, tin đồn về lỗi vặt.
        price *= model_specific_effects[(frame.brand, frame.model)]

        # Hiệu ứng theo đời xe: các năm có bản nâng cấp giữa vòng đời giữ giá tốt hơn.
        price *= 1.0 + 0.035 * np.sin(year * 1.7)

        # Nhiễu thị trường: kỳ vọng của người bán, trang bị thêm, mức độ thương lượng.
        price *= float(rng.lognormal(mean=0.0, sigma=0.115))

        records.append(
            {
                "case_id": listing_index + 1,
                "brand": frame.brand,
                "model": frame.model,
                "version": frame.version,
                "phan_khuc": frame.segment,
                "nam_san_xuat": year,
                "tuoi_xe": age,
                "so_km": mileage,
                "km_moi_nam": round(km_per_year, 1),
                "hop_so": frame.transmission,
                "nhien_lieu": frame.fuel,
                "xuat_xu": origin,
                "khu_vuc": region,
                "ngap_nuoc": is_flooded,
                "tai_nan_nang": had_major_accident,
                "xe_dich_vu": was_commercial,
                "mot_chu_bao_duong_hang": single_owner_full_service,
                "gia_xe_moi": frame.new_price,
                "gia": round(float(price), 1),
            }
        )

    return pd.DataFrame.from_records(records)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    dataset = generate_dataset()

    output_path = DATA_DIR / "listings_raw.csv"
    dataset.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Da sinh {len(dataset):,} tin rao mo phong -> {output_path}")
    print(f"Khoang gia: {dataset['gia'].min():,.0f} - {dataset['gia'].max():,.0f} trieu VND")
    print(f"So dong xe: {dataset['model'].nunique()}, so phien ban: {dataset['version'].nunique()}")
    print(f"Nam san xuat: {dataset['nam_san_xuat'].min()} - {dataset['nam_san_xuat'].max()}")


if __name__ == "__main__":
    main()
