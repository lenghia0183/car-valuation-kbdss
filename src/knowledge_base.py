"""Tải và truy vấn cơ sở tri thức: khung xe (frames) và tập luật sản xuất (rules)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

KB_DIR = Path(__file__).resolve().parent.parent / "kb"


@dataclass(frozen=True)
class VersionFrame:
    """Một khe (slot) cụ thể của khung XE: hãng - dòng - phiên bản."""

    brand: str
    model: str
    version: str
    segment: str
    new_price: float
    transmission: str
    fuel: str
    base_depreciation: float
    liquidity: float
    brand_factor: float
    origin_default: str


class KnowledgeBase:
    """Cơ sở tri thức gồm khung đối tượng xe và tập luật sản xuất."""

    def __init__(self, frames_path: Path | None = None, rules_path: Path | None = None) -> None:
        frames_path = frames_path or KB_DIR / "frames.json"
        rules_path = rules_path or KB_DIR / "rules.json"

        self._frames_raw: dict[str, Any] = json.loads(frames_path.read_text(encoding="utf-8"))
        self._rules_raw: dict[str, Any] = json.loads(rules_path.read_text(encoding="utf-8"))

        self.segments: dict[str, Any] = self._frames_raw["segments"]
        self.brands: dict[str, Any] = self._frames_raw["brands"]
        self.regions: dict[str, Any] = self._frames_raw["regions"]
        self.rules: list[dict[str, Any]] = sorted(
            self._rules_raw["rules"], key=lambda rule: -rule["priority"]
        )

        self._version_frames = self._build_version_frames()

    def _build_version_frames(self) -> dict[tuple[str, str, str], VersionFrame]:
        frames: dict[tuple[str, str, str], VersionFrame] = {}

        for model_entry in self._frames_raw["models"]:
            brand = model_entry["brand"]
            model = model_entry["model"]
            segment_key = model_entry["segment"]
            segment = self.segments[segment_key]
            brand_info = self.brands[brand]

            for version_entry in model_entry["versions"]:
                key = (brand, model, version_entry["version"])
                frames[key] = VersionFrame(
                    brand=brand,
                    model=model,
                    version=version_entry["version"],
                    segment=segment_key,
                    new_price=float(version_entry["new_price"]),
                    transmission=version_entry["transmission"],
                    fuel=version_entry["fuel"],
                    base_depreciation=float(segment["base_depreciation"]),
                    liquidity=float(segment["liquidity"]),
                    brand_factor=float(brand_info["brand_factor"]),
                    origin_default=brand_info["origin_default"],
                )

        return frames

    @property
    def version_frames(self) -> dict[tuple[str, str, str], VersionFrame]:
        return self._version_frames

    def find_version_frame(self, brand: str, model: str, version: str) -> VersionFrame | None:
        return self._version_frames.get((brand, model, version))

    def list_brands(self) -> list[str]:
        return sorted({frame.brand for frame in self._version_frames.values()})

    def list_models(self, brand: str) -> list[str]:
        return sorted({frame.model for frame in self._version_frames.values() if frame.brand == brand})

    def list_versions(self, brand: str, model: str) -> list[str]:
        return [
            frame.version
            for frame in self._version_frames.values()
            if frame.brand == brand and frame.model == model
        ]

    def list_regions(self) -> list[str]:
        return list(self.regions.keys())

    def segment_label(self, segment_key: str) -> str:
        return self.segments[segment_key]["label"]

    def region_factor(self, region: str) -> float:
        return float(self.regions.get(region, {"factor": 1.0})["factor"])

    def rule_count(self) -> int:
        return len(self.rules)
