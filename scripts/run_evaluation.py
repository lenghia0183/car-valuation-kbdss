"""Thực nghiệm và đánh giá: so sánh bốn phương pháp định giá trên cùng tập kiểm thử.

Bốn phương pháp:
  1. Chỉ dùng tập luật sản xuất (suy diễn tiến).
  2. Chỉ dùng lập luận dựa trên tình huống (CBR).
  3. Chỉ dùng mô hình học máy Random Forest (đối chứng).
  4. Hệ lai: kết hợp luật và CBR theo hệ số alpha thích nghi.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from case_based_reasoning import CaseBase, CaseBasedReasoner  # noqa: E402
from knowledge_base import KnowledgeBase  # noqa: E402
from valuation_service import ValuationService, VehicleQuery  # noqa: E402

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

RANDOM_FOREST_FEATURES = [
    "brand", "model", "version", "phan_khuc", "hop_so", "nhien_lieu", "xuat_xu", "khu_vuc",
    "nam_san_xuat", "tuoi_xe", "so_km", "km_moi_nam", "gia_xe_moi",
    "ngap_nuoc", "tai_nan_nang", "xe_dich_vu", "mot_chu_bao_duong_hang",
]
CATEGORICAL_FEATURES = [
    "brand", "model", "version", "phan_khuc", "hop_so", "nhien_lieu", "xuat_xu", "khu_vuc",
]


def mean_absolute_percentage_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(np.abs((actual - predicted) / actual)) * 100.0)


def compute_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    return {
        "MAE": round(float(mean_absolute_error(actual, predicted)), 2),
        "MAPE": round(mean_absolute_percentage_error(actual, predicted), 2),
        "R2": round(float(r2_score(actual, predicted)), 4),
    }


def build_random_forest(train_set: pd.DataFrame) -> tuple[RandomForestRegressor, dict[str, dict]]:
    """Huấn luyện mô hình đối chứng Random Forest với mã hóa thứ tự cho thuộc tính định danh."""
    encoders: dict[str, dict] = {}
    encoded_train = train_set[RANDOM_FOREST_FEATURES].copy()

    for column in CATEGORICAL_FEATURES:
        categories = sorted(train_set[column].astype(str).unique())
        mapping = {category: index for index, category in enumerate(categories)}
        encoders[column] = mapping
        encoded_train[column] = encoded_train[column].astype(str).map(mapping)

    for column in ["ngap_nuoc", "tai_nan_nang", "xe_dich_vu", "mot_chu_bao_duong_hang"]:
        encoded_train[column] = encoded_train[column].astype(int)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=18,
        min_samples_leaf=2,
        random_state=20_261_104,
        n_jobs=1,
    )
    model.fit(encoded_train, train_set["gia"])

    return model, encoders


def encode_for_random_forest(dataset: pd.DataFrame, encoders: dict[str, dict]) -> pd.DataFrame:
    encoded = dataset[RANDOM_FOREST_FEATURES].copy()

    for column, mapping in encoders.items():
        encoded[column] = encoded[column].astype(str).map(mapping).fillna(-1).astype(int)

    for column in ["ngap_nuoc", "tai_nan_nang", "xe_dich_vu", "mot_chu_bao_duong_hang"]:
        encoded[column] = encoded[column].astype(int)

    return encoded


def main() -> None:
    train_set = pd.read_csv(DATA_DIR / "train.csv", encoding="utf-8-sig")
    test_set = pd.read_csv(DATA_DIR / "test.csv", encoding="utf-8-sig")

    knowledge_base = KnowledgeBase()
    case_base = CaseBase(train_set)
    reasoner = CaseBasedReasoner(case_base, k=5, min_similarity=0.55)
    service = ValuationService(knowledge_base, reasoner)

    random_forest, encoders = build_random_forest(train_set)
    encoded_test = encode_for_random_forest(test_set, encoders)

    start_time = time.perf_counter()
    random_forest_predictions = random_forest.predict(encoded_test)
    random_forest_elapsed = time.perf_counter() - start_time

    rule_predictions: list[float] = []
    cbr_predictions: list[float] = []
    hybrid_predictions: list[float] = []
    in_range_flags: list[bool] = []
    confidences: list[float] = []
    range_widths: list[float] = []
    cbr_available_flags: list[bool] = []
    per_row_records: list[dict[str, object]] = []

    hybrid_start = time.perf_counter()

    for _, row in test_set.iterrows():
        query = VehicleQuery(
            brand=row["brand"],
            model=row["model"],
            version=row["version"],
            nam_san_xuat=int(row["nam_san_xuat"]),
            so_km=int(row["so_km"]),
            khu_vuc=row["khu_vuc"],
            xuat_xu=row["xuat_xu"],
            ngap_nuoc=bool(row["ngap_nuoc"]),
            tai_nan_nang=bool(row["tai_nan_nang"]),
            xe_dich_vu=bool(row["xe_dich_vu"]),
            mot_chu_bao_duong_hang=bool(row["mot_chu_bao_duong_hang"]),
        )

        result = service.evaluate(query)
        actual_price = float(row["gia"])

        rule_predictions.append(result.rule_price)
        hybrid_predictions.append(result.suggested_price)
        cbr_predictions.append(result.cbr_price if result.cbr_price is not None else result.rule_price)
        cbr_available_flags.append(result.cbr_price is not None)

        in_range_flags.append(result.price_lower <= actual_price <= result.price_upper)
        confidences.append(result.confidence)
        range_widths.append((result.price_upper - result.price_lower) / result.suggested_price)

        per_row_records.append(
            {
                "case_id": int(row["case_id"]),
                "brand": row["brand"],
                "model": row["model"],
                "phan_khuc": row["phan_khuc"],
                "tuoi_xe": int(row["tuoi_xe"]),
                "gia_thuc_te": actual_price,
                "gia_luat": round(result.rule_price, 1),
                "gia_cbr": round(result.cbr_price, 1) if result.cbr_price is not None else None,
                "gia_de_xuat": round(result.suggested_price, 1),
                "trong_khoang": result.price_lower <= actual_price <= result.price_upper,
                "do_tin_cay": round(result.confidence, 3),
            }
        )

    hybrid_elapsed = time.perf_counter() - hybrid_start

    actual_prices = test_set["gia"].to_numpy(dtype=float)

    results = {
        "Chi dung luat": compute_metrics(actual_prices, np.array(rule_predictions)),
        "Chi dung CBR": compute_metrics(actual_prices, np.array(cbr_predictions)),
        "Chi dung Random Forest": compute_metrics(actual_prices, random_forest_predictions),
        "He lai (luat + CBR)": compute_metrics(actual_prices, np.array(hybrid_predictions)),
    }

    per_row_frame = pd.DataFrame(per_row_records)
    per_row_frame["sai_so_tuyet_doi"] = (
        per_row_frame["gia_de_xuat"] - per_row_frame["gia_thuc_te"]
    ).abs()
    per_row_frame["sai_so_phan_tram"] = (
        per_row_frame["sai_so_tuyet_doi"] / per_row_frame["gia_thuc_te"] * 100.0
    )

    error_by_segment = (
        per_row_frame.groupby("phan_khuc")
        .agg(
            so_xe=("gia_thuc_te", "size"),
            MAE=("sai_so_tuyet_doi", "mean"),
            MAPE=("sai_so_phan_tram", "mean"),
            ty_le_trong_khoang=("trong_khoang", "mean"),
        )
        .round(2)
        .sort_values("so_xe", ascending=False)
    )

    age_bins = [-1, 2, 5, 8, 12, 100]
    age_labels = ["0-2 nam", "3-5 nam", "6-8 nam", "9-12 nam", "tren 12 nam"]
    per_row_frame["nhom_tuoi"] = pd.cut(per_row_frame["tuoi_xe"], bins=age_bins, labels=age_labels)

    error_by_age = (
        per_row_frame.groupby("nhom_tuoi", observed=True)
        .agg(
            so_xe=("gia_thuc_te", "size"),
            MAE=("sai_so_tuyet_doi", "mean"),
            MAPE=("sai_so_phan_tram", "mean"),
            ty_le_trong_khoang=("trong_khoang", "mean"),
        )
        .round(2)
    )

    summary = {
        "so_xe_kiem_thu": len(test_set),
        "so_xe_co_tinh_huong_tuong_tu": int(sum(cbr_available_flags)),
        "ty_le_co_tinh_huong_tuong_tu": round(float(np.mean(cbr_available_flags)), 4),
        "ket_qua_cac_phuong_phap": results,
        "ty_le_gia_thuc_trong_khoang_de_xuat": round(float(np.mean(in_range_flags)), 4),
        "do_tin_cay_trung_binh": round(float(np.mean(confidences)), 4),
        "do_rong_khoang_gia_trung_binh": round(float(np.mean(range_widths)), 4),
        "thoi_gian_he_lai_ms_moi_xe": round(hybrid_elapsed / len(test_set) * 1000.0, 2),
        "thoi_gian_random_forest_ms_moi_xe": round(random_forest_elapsed / len(test_set) * 1000.0, 4),
        "sai_so_theo_phan_khuc": json.loads(error_by_segment.to_json(orient="index")),
        "sai_so_theo_nhom_tuoi": json.loads(error_by_age.to_json(orient="index")),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "evaluation_results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    per_row_frame.to_csv(OUTPUT_DIR / "test_predictions.csv", index=False, encoding="utf-8-sig")

    print(f"So xe kiem thu: {len(test_set):,}")
    print(f"Ty le co tinh huong tuong tu: {summary['ty_le_co_tinh_huong_tuong_tu']:.1%}\n")

    print(f"{'Phuong phap':<26}{'MAE':>10}{'MAPE':>10}{'R2':>10}")
    for method_name, metrics in results.items():
        print(f"{method_name:<26}{metrics['MAE']:>10.2f}{metrics['MAPE']:>9.2f}%{metrics['R2']:>10.4f}")

    print(f"\nTy le gia thuc nam trong khoang de xuat: {summary['ty_le_gia_thuc_trong_khoang_de_xuat']:.1%}")
    print(f"Do tin cay trung binh: {summary['do_tin_cay_trung_binh']:.1%}")
    print(f"Thoi gian dinh gia mot xe: {summary['thoi_gian_he_lai_ms_moi_xe']:.2f} ms")

    print("\nSai so theo phan khuc:")
    print(error_by_segment.to_string())
    print("\nSai so theo nhom tuoi xe:")
    print(error_by_age.to_string())


if __name__ == "__main__":
    main()
