"""Dịch vụ định giá: điều phối máy suy diễn, mô-đun CBR và cơ chế giải thích.

Giá đề xuất là tổ hợp lồi của giá suy diễn từ luật và giá từ lập luận tình huống:
    gia_de_xuat = alpha * gia_luat + (1 - alpha) * gia_cbr
Hệ số alpha được chọn theo số lượng và độ tương tự của các tình huống truy hồi được.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from case_based_reasoning import CaseBasedReasoner, CaseBasedResult, RetrievedCase
from inference_engine import FiredRule, ForwardChainingEngine, InferenceResult
from knowledge_base import KnowledgeBase, VersionFrame

CURRENT_YEAR = date.today().year
BASE_CONFIDENCE = 0.80


@dataclass
class VehicleQuery:
    """Thông tin chiếc xe cần định giá do người dùng khai báo."""

    brand: str
    model: str
    version: str
    nam_san_xuat: int
    so_km: int
    khu_vuc: str
    xuat_xu: str | None = None
    ngap_nuoc: bool = False
    tai_nan_nang: bool = False
    xe_dich_vu: bool = False
    mot_chu_bao_duong_hang: bool = False


@dataclass
class ValuationResult:
    """Kết quả định giá đầy đủ kèm bằng chứng để giải thích."""

    suggested_price: float
    price_lower: float
    price_upper: float
    confidence: float
    rule_price: float
    cbr_price: float | None
    alpha: float
    fired_rules: list[FiredRule]
    retrieved_cases: list[RetrievedCase]
    warnings: list[str]
    frame: VersionFrame
    explanation_lines: list[str] = field(default_factory=list)

    @property
    def confidence_label(self) -> str:
        if self.confidence >= 0.75:
            return "Cao"
        if self.confidence >= 0.55:
            return "Trung bình"
        return "Thấp"


def _resolve_alpha(cbr_result: CaseBasedResult) -> float:
    """Chọn hệ số alpha theo quy tắc trong Bảng 'Quy tắc chọn hệ số α'."""
    if cbr_result.cbr_price is None:
        return 1.0

    case_count = cbr_result.case_count
    mean_similarity = sum(case.similarity for case in cbr_result.retrieved_cases) / case_count

    if case_count >= 5 and mean_similarity >= 0.80:
        return 0.35
    if case_count >= 3 and mean_similarity >= 0.70:
        return 0.50
    if case_count >= 2:
        return 0.65
    return 0.80


class ValuationService:
    """Điều phối toàn bộ quy trình định giá một chiếc xe."""

    def __init__(self, knowledge_base: KnowledgeBase, case_based_reasoner: CaseBasedReasoner) -> None:
        self._knowledge_base = knowledge_base
        self._engine = ForwardChainingEngine(knowledge_base)
        self._case_based_reasoner = case_based_reasoner

    def evaluate(self, query: VehicleQuery) -> ValuationResult:
        frame = self._knowledge_base.find_version_frame(query.brand, query.model, query.version)
        if frame is None:
            raise ValueError(
                f"Không tìm thấy khung tri thức cho xe {query.brand} {query.model} {query.version}"
            )

        cbr_query = self._build_cbr_query(query, frame)
        cbr_result = self._case_based_reasoner.run(cbr_query)

        working_memory = self._build_working_memory(query, frame, cbr_result)
        inference_result = self._engine.run(working_memory)

        # Luật R25 cần biết độ lệch giữa hai nguồn tri thức, nên chạy suy diễn lần hai.
        if cbr_result.cbr_price is not None and inference_result.rule_price > 0:
            deviation = abs(inference_result.rule_price - cbr_result.cbr_price) / inference_result.rule_price
            working_memory["do_lech_luat_cbr"] = deviation
            inference_result = self._engine.run(working_memory)

        alpha = _resolve_alpha(cbr_result)
        suggested_price = self._combine_prices(inference_result, cbr_result, alpha)
        confidence = self._compute_confidence(inference_result, cbr_result)
        price_lower, price_upper = self._compute_price_range(suggested_price, confidence, cbr_result)

        result = ValuationResult(
            suggested_price=suggested_price,
            price_lower=price_lower,
            price_upper=price_upper,
            confidence=confidence,
            rule_price=inference_result.rule_price,
            cbr_price=cbr_result.cbr_price,
            alpha=alpha,
            fired_rules=inference_result.fired_rules,
            retrieved_cases=cbr_result.retrieved_cases,
            warnings=inference_result.warnings,
            frame=frame,
        )
        result.explanation_lines = self._build_explanation(query, result, inference_result)
        return result

    def _build_cbr_query(self, query: VehicleQuery, frame: VersionFrame) -> dict[str, Any]:
        return {
            "brand": query.brand,
            "model": query.model,
            "version": query.version,
            "nam_san_xuat": query.nam_san_xuat,
            "so_km": query.so_km,
            "hop_so": frame.transmission,
            "nhien_lieu": frame.fuel,
            "xuat_xu": query.xuat_xu or frame.origin_default,
            "khu_vuc": query.khu_vuc,
        }

    def _build_working_memory(
        self, query: VehicleQuery, frame: VersionFrame, cbr_result: CaseBasedResult
    ) -> dict[str, Any]:
        vehicle_age = max(0, CURRENT_YEAR - query.nam_san_xuat)
        km_per_year = query.so_km / max(1, vehicle_age)

        return {
            "gia_xe_moi": frame.new_price,
            "tuoi_xe": vehicle_age,
            "so_km": query.so_km,
            "km_moi_nam": km_per_year,
            "hop_so": frame.transmission,
            "nhien_lieu": frame.fuel,
            "phan_khuc": frame.segment,
            "xuat_xu": query.xuat_xu or frame.origin_default,
            "base_depreciation": frame.base_depreciation,
            "liquidity": frame.liquidity,
            "brand_factor": frame.brand_factor,
            "region_factor": self._knowledge_base.region_factor(query.khu_vuc),
            "ngap_nuoc": query.ngap_nuoc,
            "tai_nan_nang": query.tai_nan_nang,
            "xe_dich_vu": query.xe_dich_vu,
            "mot_chu_bao_duong_hang": query.mot_chu_bao_duong_hang,
            "so_tinh_huong_tuong_tu": cbr_result.case_count,
            "he_so_bien_thien": cbr_result.coefficient_of_variation,
        }

    @staticmethod
    def _combine_prices(
        inference_result: InferenceResult, cbr_result: CaseBasedResult, alpha: float
    ) -> float:
        if cbr_result.cbr_price is None:
            return inference_result.rule_price
        return alpha * inference_result.rule_price + (1.0 - alpha) * cbr_result.cbr_price

    @staticmethod
    def _compute_confidence(
        inference_result: InferenceResult, cbr_result: CaseBasedResult
    ) -> float:
        confidence = BASE_CONFIDENCE + inference_result.confidence_delta

        if cbr_result.case_count >= 5:
            confidence += 0.08
        elif cbr_result.case_count >= 3:
            confidence += 0.04

        return float(max(0.20, min(0.98, confidence)))

    @staticmethod
    def _compute_price_range(
        suggested_price: float, confidence: float, cbr_result: CaseBasedResult
    ) -> tuple[float, float]:
        # Độ tin cậy càng thấp thì khoảng giá càng rộng.
        half_width_ratio = 0.10 + (1.0 - confidence) * 0.40

        # Khi các xe tương tự có giá phân tán mạnh, khoảng giá phải nới theo độ phân tán đó.
        if cbr_result.coefficient_of_variation is not None:
            half_width_ratio = max(half_width_ratio, cbr_result.coefficient_of_variation * 1.30)

        half_width_ratio = min(half_width_ratio, 0.35)

        return (
            suggested_price * (1.0 - half_width_ratio),
            suggested_price * (1.0 + half_width_ratio),
        )

    def _build_explanation(
        self, query: VehicleQuery, result: ValuationResult, inference_result: InferenceResult
    ) -> list[str]:
        frame = result.frame
        vehicle_age = max(0, CURRENT_YEAR - query.nam_san_xuat)
        segment_label = self._knowledge_base.segment_label(frame.segment)

        lines = [
            f"Xe {query.brand} {query.model} {query.version} thuộc phân khúc {segment_label}, "
            f"giá xe mới tham chiếu {frame.new_price:,.0f} triệu đồng.",
            f"Xe đã sử dụng {vehicle_age} năm, chạy {query.so_km:,} km "
            f"(trung bình {query.so_km / max(1, vehicle_age):,.0f} km mỗi năm).",
        ]

        for fired_rule in result.fired_rules:
            lines.append(
                f"[{fired_rule.rule_id}] {fired_rule.label}: hệ số {fired_rule.factor:.3f} "
                f"→ {fired_rule.price_after:,.1f} triệu đồng."
            )

        lines.append(
            f"Giá suy diễn từ tập luật: {result.rule_price:,.1f} triệu đồng."
        )

        if result.cbr_price is not None:
            lines.append(
                f"Giá từ {len(result.retrieved_cases)} xe tương tự trong cơ sở tình huống: "
                f"{result.cbr_price:,.1f} triệu đồng."
            )
            lines.append(
                f"Tổng hợp hai nguồn tri thức với α = {result.alpha:.2f} "
                f"→ giá đề xuất {result.suggested_price:,.1f} triệu đồng."
            )
        else:
            lines.append(
                "Không tìm được xe tương tự trong cơ sở tình huống, "
                "kết quả chỉ dựa trên tập luật."
            )

        lines.append(
            f"Khoảng giá đề xuất: {result.price_lower:,.0f} – {result.price_upper:,.0f} triệu đồng, "
            f"độ tin cậy {result.confidence:.0%} ({result.confidence_label})."
        )

        return lines
