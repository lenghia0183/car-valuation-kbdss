"""Máy suy diễn tiến (forward chaining) trên tập luật sản xuất.

Chu trình nhận dạng - giải quyết xung đột - thực thi:
  1. So khớp: tìm mọi luật có phần điều kiện thỏa mãn bộ nhớ làm việc.
  2. Giải quyết xung đột: sắp theo độ ưu tiên giảm dần, luật đã kích hoạt không lặp lại.
  3. Thực thi: áp dụng hành động, cập nhật bộ nhớ làm việc và ghi vết suy diễn.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from knowledge_base import KnowledgeBase

# Các hàm được phép dùng trong biểu thức hệ số của luật.
_EXPRESSION_FUNCTIONS: dict[str, Any] = {
    "pow": pow,
    "max": max,
    "min": min,
    "abs": abs,
    "exp": math.exp,
    "log": math.log,
}


@dataclass
class FiredRule:
    """Một bản ghi trong vết suy diễn: luật nào đã kích hoạt và tác động ra sao."""

    rule_id: str
    description: str
    label: str
    factor: float | None
    price_before: float
    price_after: float

    @property
    def price_delta(self) -> float:
        return self.price_after - self.price_before


@dataclass
class InferenceResult:
    """Kết quả suy diễn từ tập luật."""

    rule_price: float
    base_price: float
    fired_rules: list[FiredRule] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence_delta: float = 0.0
    working_memory: dict[str, Any] = field(default_factory=dict)

    @property
    def fired_rule_ids(self) -> list[str]:
        return [rule.rule_id for rule in self.fired_rules]


class ConditionEvaluator:
    """Đánh giá phần điều kiện (IF) của một luật trên bộ nhớ làm việc."""

    @staticmethod
    def evaluate(condition: dict[str, Any], working_memory: dict[str, Any]) -> bool:
        fact_name = condition["fact"]
        operator = condition["op"]

        if operator == "exists":
            return working_memory.get(fact_name) is not None

        if fact_name not in working_memory:
            return False

        fact_value = working_memory[fact_name]
        if fact_value is None:
            return False

        expected = condition.get("value")

        if operator == "==":
            return fact_value == expected
        if operator == "!=":
            return fact_value != expected
        if operator == "in":
            return fact_value in expected
        if operator == "not_in":
            return fact_value not in expected

        if not isinstance(fact_value, (int, float)):
            return False

        if operator == "<":
            return fact_value < expected
        if operator == "<=":
            return fact_value <= expected
        if operator == ">":
            return fact_value > expected
        if operator == ">=":
            return fact_value >= expected

        raise ValueError(f"Toán tử không được hỗ trợ trong luật: {operator}")


class ForwardChainingEngine:
    """Máy suy diễn tiến áp dụng tập luật lên bộ nhớ làm việc."""

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self._knowledge_base = knowledge_base

    def run(self, working_memory: dict[str, Any]) -> InferenceResult:
        memory = dict(working_memory)
        base_price = float(memory["gia_xe_moi"])
        memory["gia"] = base_price

        result = InferenceResult(
            rule_price=base_price,
            base_price=base_price,
            working_memory=memory,
        )

        fired_rule_ids: set[str] = set()

        # Suy diễn tiến lặp cho tới khi không còn luật mới nào kích hoạt được.
        while True:
            applicable_rule = self._select_next_rule(memory, fired_rule_ids)
            if applicable_rule is None:
                break

            fired_rule_ids.add(applicable_rule["id"])
            self._execute_rule(applicable_rule, memory, result)

        result.rule_price = memory["gia"]
        result.working_memory = memory
        return result

    def _select_next_rule(
        self, memory: dict[str, Any], fired_rule_ids: set[str]
    ) -> dict[str, Any] | None:
        """Chọn luật ưu tiên cao nhất trong tập xung đột (luật đã chạy bị loại)."""
        for rule in self._knowledge_base.rules:
            if rule["id"] in fired_rule_ids:
                continue
            if self._matches(rule, memory):
                return rule
        return None

    @staticmethod
    def _matches(rule: dict[str, Any], memory: dict[str, Any]) -> bool:
        return all(ConditionEvaluator.evaluate(condition, memory) for condition in rule["if"])

    def _execute_rule(
        self, rule: dict[str, Any], memory: dict[str, Any], result: InferenceResult
    ) -> None:
        for action in rule["then"]:
            action_type = action["type"]

            if action_type == "multiply":
                self._apply_multiply(rule, action, memory, result)
            elif action_type == "flag":
                result.warnings.append(action["value"])
            elif action_type == "confidence":
                result.confidence_delta += float(action["delta"])
            elif action_type == "set":
                memory[action["target"]] = action["value"]
            else:
                raise ValueError(f"Loại hành động không được hỗ trợ: {action_type}")

    def _apply_multiply(
        self,
        rule: dict[str, Any],
        action: dict[str, Any],
        memory: dict[str, Any],
        result: InferenceResult,
    ) -> None:
        factor = self._resolve_factor(action, memory)
        price_before = float(memory["gia"])

        # Luật khấu hao tính trực tiếp từ giá xe mới, không cộng dồn lên giá đang có.
        if rule["group"] == "khau_hao":
            price_after = result.base_price * factor
        else:
            price_after = price_before * factor

        memory["gia"] = price_after

        result.fired_rules.append(
            FiredRule(
                rule_id=rule["id"],
                description=rule["description"],
                label=action.get("label", rule["id"]),
                factor=factor,
                price_before=price_before,
                price_after=price_after,
            )
        )

    @staticmethod
    def _resolve_factor(action: dict[str, Any], memory: dict[str, Any]) -> float:
        if "factor" in action:
            return float(action["factor"])

        expression = action["expr"]
        evaluation_scope = {
            key: value
            for key, value in memory.items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        evaluation_scope.update(_EXPRESSION_FUNCTIONS)

        return float(eval(expression, {"__builtins__": {}}, evaluation_scope))  # noqa: S307
