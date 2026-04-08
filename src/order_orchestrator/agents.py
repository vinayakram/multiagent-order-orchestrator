from __future__ import annotations

import asyncio

from .models import FulfillmentReceipt, InventoryDecision, OrderRequest, RoutePlan


class PlannerAgent:
    def plan(self, order: OrderRequest) -> RoutePlan:
        route_name = "priority-route" if order.customer_tier.lower() == "gold" else "standard-route"
        return RoutePlan(route_name=route_name, requires_manual_review=False)


class InventoryAgent:
    def reserve(self, order: OrderRequest, plan: RoutePlan) -> InventoryDecision:
        warehouse_id = "blr-1" if order.destination_region.lower() == "south" else "mum-2"
        return InventoryDecision(warehouse_id=warehouse_id, available=bool(order.items))


class FulfillmentAgent:
    def __init__(self, dispatch_delay_seconds: float = 0.35) -> None:
        self.dispatch_delay_seconds = dispatch_delay_seconds

    async def dispatch(self, order: OrderRequest, plan: RoutePlan, inventory: InventoryDecision) -> FulfillmentReceipt:
        await asyncio.sleep(self.dispatch_delay_seconds)
        return FulfillmentReceipt(
            dispatch_id=f"dispatch-{order.order_id}",
            route_name=plan.route_name,
            warehouse_id=inventory.warehouse_id,
        )
