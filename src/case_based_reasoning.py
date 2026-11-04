"""Lập luận dựa trên tình huống (Case-Based Reasoning) cho bài toán định giá xe cũ.

Chu trình 4R: Retrieve (truy hồi) - Reuse (tái sử dụng) - Revise (hiệu chỉnh) - Retain (lưu giữ).
Độ tương tự toàn cục là trung bình có trọng số của các độ tương tự cục bộ theo từng thuộc tính.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

# Trọng số các thuộc tính trong độ đo tương tự toàn cục (tổng bằng 1.0).
ATTRIBUTE_WEIGHTS: dict[str, float] = {
    "model": 0.30,
    "version": 0.12,
    "nam_san_xuat": 0.22,
    "so_km": 0.18,
    "hop_so": 0.06,
    "nhien_lieu": 0.04,
    "xuat_xu": 0.04,
    "khu_vuc": 0.04,
}

# Khoảng chuẩn hóa cho các thuộc tính số.
YEAR_TOLERANCE = 6.0
KM_TOLERANCE = 120_000.0


@dataclass
class RetrievedCase:
    """Một tình huống tương tự được truy hồi từ cơ sở tình huống."""

    case_id: int
    brand: str
    model: str
    version: str
    nam_san_xuat: int
    so_km: int
    hop_so: str
    khu_vuc: str
    gia: float
    similarity: float
    adjusted_price: float


@dataclass
class CaseBasedResult:
    """Kết quả của mô-đun lập luận dựa trên tình huống."""

    cbr_price: float | None
    retrieved_cases: list[RetrievedCase]
    coefficient_of_variation: float | None

    @property
    def case_count(self) -> int:
        return len(self.retrieved_cases)


def _local_similarity_categorical(query_value: Any, case_value: Any) -> float:
    return 1.0 if query_value == case_value else 0.0


def _local_similarity_numeric(query_value: float, case_value: float, tolerance: float) -> float:
    distance = abs(float(query_value) - float(case_value))
    return float(max(0.0, 1.0 - distance / tolerance))


class CaseBase:
    """Cơ sở tình huống xây dựng từ dữ liệu tin rao đã tiền xử lý."""

    def __init__(self, cases: pd.DataFrame) -> None:
        self._cases = cases.reset_index(drop=True)

    @property
    def size(self) -> int:
        return len(self._cases)

    @property
    def frame(self) -> pd.DataFrame:
        return self._cases

    def _compute_similarities(self, query: dict[str, Any]) -> np.ndarray:
        cases = self._cases

        # Tình huống phải cùng hãng mới được xét, tránh so sánh khác phân khúc thương hiệu.
        same_brand_mask = (cases["brand"] == query["brand"]).to_numpy()

        similarity = np.zeros(len(cases), dtype=float)

        similarity += ATTRIBUTE_WEIGHTS["model"] * (cases["model"] == query["model"]).to_numpy()
        similarity += ATTRIBUTE_WEIGHTS["version"] * (cases["version"] == query["version"]).to_numpy()
        similarity += ATTRIBUTE_WEIGHTS["hop_so"] * (cases["hop_so"] == query["hop_so"]).to_numpy()
        similarity += ATTRIBUTE_WEIGHTS["nhien_lieu"] * (cases["nhien_lieu"] == query["nhien_lieu"]).to_numpy()
        similarity += ATTRIBUTE_WEIGHTS["xuat_xu"] * (cases["xuat_xu"] == query["xuat_xu"]).to_numpy()
        similarity += ATTRIBUTE_WEIGHTS["khu_vuc"] * (cases["khu_vuc"] == query["khu_vuc"]).to_numpy()

        year_distance = np.abs(cases["nam_san_xuat"].to_numpy(dtype=float) - float(query["nam_san_xuat"]))
        similarity += ATTRIBUTE_WEIGHTS["nam_san_xuat"] * np.maximum(0.0, 1.0 - year_distance / YEAR_TOLERANCE)

        km_distance = np.abs(cases["so_km"].to_numpy(dtype=float) - float(query["so_km"]))
        similarity += ATTRIBUTE_WEIGHTS["so_km"] * np.maximum(0.0, 1.0 - km_distance / KM_TOLERANCE)

        return np.where(same_brand_mask, similarity, 0.0)

    def retrieve(
        self, query: dict[str, Any], k: int = 5, min_similarity: float = 0.55
    ) -> list[RetrievedCase]:
        """Truy hồi k tình huống tương tự nhất vượt ngưỡng tương tự tối thiểu."""
        if self.size == 0:
            return []

        similarities = self._compute_similarities(query)
        candidate_indices = np.where(similarities >= min_similarity)[0]

        if candidate_indices.size == 0:
            return []

        top_indices = candidate_indices[np.argsort(-similarities[candidate_indices])][:k]

        retrieved: list[RetrievedCase] = []
        for index in top_indices:
            case_row = self._cases.iloc[int(index)]
            adjusted_price = self._adjust_price(query, case_row)

            retrieved.append(
                RetrievedCase(
                    case_id=int(case_row["case_id"]),
                    brand=str(case_row["brand"]),
                    model=str(case_row["model"]),
                    version=str(case_row["version"]),
                    nam_san_xuat=int(case_row["nam_san_xuat"]),
                    so_km=int(case_row["so_km"]),
                    hop_so=str(case_row["hop_so"]),
                    khu_vuc=str(case_row["khu_vuc"]),
                    gia=float(case_row["gia"]),
                    similarity=float(similarities[index]),
                    adjusted_price=adjusted_price,
                )
            )

        return retrieved

    @staticmethod
    def _adjust_price(query: dict[str, Any], case_row: pd.Series) -> float:
        """Revise: hiệu chỉnh giá tình huống về điều kiện của xe cần định giá."""
        price = float(case_row["gia"])

        # Mỗi năm chênh lệch tuổi xe tương ứng khoảng 7% giá trị.
        year_gap = int(query["nam_san_xuat"]) - int(case_row["nam_san_xuat"])
        price *= (1.0 + 0.07) ** year_gap

        # Mỗi 10.000 km chênh lệch tương ứng khoảng 1.2% giá trị, giới hạn biên độ ±15%.
        km_gap = float(case_row["so_km"]) - float(query["so_km"])
        km_adjustment = max(-0.15, min(0.15, (km_gap / 10_000.0) * 0.012))
        price *= (1.0 + km_adjustment)

        return price


class CaseBasedReasoner:
    """Mô-đun CBR: truy hồi, tái sử dụng và hiệu chỉnh giá từ các tình huống tương tự."""

    def __init__(self, case_base: CaseBase, k: int = 5, min_similarity: float = 0.55) -> None:
        self._case_base = case_base
        self._k = k
        self._min_similarity = min_similarity

    def run(self, query: dict[str, Any]) -> CaseBasedResult:
        retrieved_cases = self._case_base.retrieve(query, k=self._k, min_similarity=self._min_similarity)

        if not retrieved_cases:
            return CaseBasedResult(cbr_price=None, retrieved_cases=[], coefficient_of_variation=None)

        similarities = np.array([case.similarity for case in retrieved_cases])
        adjusted_prices = np.array([case.adjusted_price for case in retrieved_cases])

        # Reuse: giá CBR là trung bình có trọng số theo độ tương tự.
        cbr_price = float(np.average(adjusted_prices, weights=similarities))

        mean_price = float(adjusted_prices.mean())
        coefficient_of_variation = (
            float(adjusted_prices.std() / mean_price) if mean_price > 0 else None
        )

        return CaseBasedResult(
            cbr_price=cbr_price,
            retrieved_cases=retrieved_cases,
            coefficient_of_variation=coefficient_of_variation,
        )
