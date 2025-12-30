from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, Optional
from .data_models import Resource, Recommendation


class Rule(Protocol):
    rule_id: str
    def evaluate(self, r: Resource) -> Optional[Recommendation]: ...


@dataclass(frozen=True)
class Thresholds:
    downsize_usage_lt: float = 30.0
    stop_usage_lt: float = 5.0


class StopIdleRule:
    rule_id = "R001_STOP_IDLE"

    def __init__(self, t: Thresholds):
        self.t = t

    def evaluate(self, r: Resource) -> Optional[Recommendation]:
        if r.usage_percent < self.t.stop_usage_lt:
            optimized_cost = 0.0
            savings = round(r.cost_per_month - optimized_cost, 2)
            return Recommendation(
                rule_id=self.rule_id,
                action="Stop",
                optimized_cost=optimized_cost,
                savings=savings,
                reason=f"usage_percent < {self.t.stop_usage_lt}",
            )
        return None


class DownsizeRule:
    rule_id = "R002_DOWNSIZE"

    def __init__(self, t: Thresholds):
        self.t = t

    def evaluate(self, r: Resource) -> Optional[Recommendation]:
        if r.usage_percent < self.t.downsize_usage_lt:
            optimized_cost = round(r.cost_per_month * 0.5, 2)
            savings = round(r.cost_per_month - optimized_cost, 2)
            return Recommendation(
                rule_id=self.rule_id,
                action="Downsize",
                optimized_cost=optimized_cost,
                savings=savings,
                reason=f"usage_percent < {self.t.downsize_usage_lt}",
            )
        return None


class RuleEngine:
    def __init__(self, rules: Iterable[Rule]):
        self.rules = list(rules)

    def run(self, r: Resource) -> Recommendation:
        # First-match wins
        for rule in self.rules:
            rec = rule.evaluate(r)
            if rec is not None:
                return rec
        return Recommendation(
            rule_id="R000_KEEP",
            action="Keep",
            optimized_cost=r.cost_per_month,
            savings=0.0,
            reason="no rule matched",
        )
