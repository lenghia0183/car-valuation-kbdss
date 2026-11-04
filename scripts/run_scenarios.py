"""Chạy các kịch bản định giá điển hình để đánh giá khả năng giải thích của hệ thống."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from case_based_reasoning import CaseBase, CaseBasedReasoner  # noqa: E402
from knowledge_base import KnowledgeBase  # noqa: E402
from valuation_service import ValuationService, VehicleQuery  # noqa: E402

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

SCENARIOS: list[tuple[str, str, VehicleQuery]] = [
    (
        "KB1",
        "Xe phổ thông, tình trạng bình thường",
        VehicleQuery(
            brand="Toyota", model="Fortuner", version="2.4G AT",
            nam_san_xuat=2019, so_km=96_000, khu_vuc="Hà Nội",
            mot_chu_bao_duong_hang=True,
        ),
    ),
    (
        "KB2",
        "Xe từng ngập nước",
        VehicleQuery(
            brand="Toyota", model="Fortuner", version="2.4G AT",
            nam_san_xuat=2019, so_km=96_000, khu_vuc="Hà Nội",
            ngap_nuoc=True,
        ),
    ),
    (
        "KB3",
        "Xe có số km bất thường, nghi chạy dịch vụ",
        VehicleQuery(
            brand="Hyundai", model="Accent", version="1.5 AT",
            nam_san_xuat=2021, so_km=185_000, khu_vuc="TP Hồ Chí Minh",
            xe_dich_vu=True,
        ),
    ),
    (
        "KB4",
        "Xe sang đời sâu, phân khúc hiếm dữ liệu",
        VehicleQuery(
            brand="Mercedes-Benz", model="C-Class", version="C200",
            nam_san_xuat=2015, so_km=120_000, khu_vuc="Đà Nẵng",
        ),
    ),
    (
        "KB5",
        "Xe từng tai nạn nặng",
        VehicleQuery(
            brand="Mazda", model="CX-5", version="2.0 Luxury",
            nam_san_xuat=2020, so_km=72_000, khu_vuc="Hải Phòng",
            tai_nan_nang=True,
        ),
    ),
]


def main() -> None:
    train_set = pd.read_csv(DATA_DIR / "train.csv", encoding="utf-8-sig")
    knowledge_base = KnowledgeBase()
    reasoner = CaseBasedReasoner(CaseBase(train_set), k=5, min_similarity=0.55)
    service = ValuationService(knowledge_base, reasoner)

    scenario_records: list[dict[str, object]] = []

    for scenario_id, scenario_name, query in SCENARIOS:
        result = service.evaluate(query)

        scenario_records.append(
            {
                "ma_kich_ban": scenario_id,
                "ten_kich_ban": scenario_name,
                "xe": f"{query.brand} {query.model} {query.version}",
                "nam_san_xuat": query.nam_san_xuat,
                "so_km": query.so_km,
                "khu_vuc": query.khu_vuc,
                "gia_de_xuat": round(result.suggested_price, 1),
                "khoang_gia": f"{result.price_lower:,.0f} - {result.price_upper:,.0f}",
                "do_rong_khoang_phan_tram": round(
                    (result.price_upper - result.price_lower) / result.suggested_price * 100, 1
                ),
                "do_tin_cay": round(result.confidence, 3),
                "muc_do_tin_cay": result.confidence_label,
                "so_luat_kich_hoat": len(result.fired_rules),
                "cac_luat_kich_hoat": ", ".join(result.fired_rule_ids)
                if hasattr(result, "fired_rule_ids")
                else ", ".join(rule.rule_id for rule in result.fired_rules),
                "so_tinh_huong_tuong_tu": len(result.retrieved_cases),
                "so_canh_bao": len(result.warnings),
                "cac_canh_bao": result.warnings,
                "giai_thich": result.explanation_lines,
            }
        )

        print(f"\n{'=' * 78}")
        print(f"{scenario_id} – {scenario_name}")
        print(f"{'=' * 78}")
        print(f"Xe: {query.brand} {query.model} {query.version}, doi {query.nam_san_xuat}, "
              f"{query.so_km:,} km, {query.khu_vuc}")
        print(f"Gia de xuat: {result.suggested_price:,.1f} trieu "
              f"(khoang {result.price_lower:,.0f} - {result.price_upper:,.0f})")
        print(f"Do tin cay: {result.confidence:.1%} ({result.confidence_label})")
        print(f"So luat kich hoat: {len(result.fired_rules)} "
              f"[{', '.join(rule.rule_id for rule in result.fired_rules)}]")
        print(f"So tinh huong tuong tu: {len(result.retrieved_cases)}")

        if result.warnings:
            print("Canh bao:")
            for warning in result.warnings:
                print(f"  - {warning}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "scenario_results.json").write_text(
        json.dumps(scenario_records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\n\nDa luu ket qua kich ban tai: {OUTPUT_DIR / 'scenario_results.json'}")


if __name__ == "__main__":
    main()
