from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OrderRequest:
    order_id: str
    customer_tier: str
    items: list[str]
    destination_region: str


@dataclass
class RoutePlan:
    route_name: str
    requires_manual_review: bool = False


@dataclass
class InventoryDecision:
    warehouse_id: str
    available: bool


@dataclass
class FulfillmentReceipt:
    dispatch_id: str
    route_name: str
    warehouse_id: str


@dataclass
class WorkflowResult:
    status: str
    route_name: str
    attempt_count: int
    error: str = ""
    trace: list[str] = field(default_factory=list)
