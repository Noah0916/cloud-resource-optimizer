from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Resource:
    provider: str
    region: str
    resource_type: str
    sku: str
    cost_per_month: float
    usage_percent: float


@dataclass(frozen=True)
class Recommendation:
    rule_id: str
    action: str                 # "Downsize", "Stop", "Keep"
    optimized_cost: float
    savings: float
    reason: str

