from __future__ import annotations

from .llm_client import DemoLLMClient
from .models import FulfillmentReceipt, InventoryDecision, OrderRequest, RoutePlan


class PlannerAgent:
    def __init__(self, llm: DemoLLMClient | None = None) -> None:
        self.llm = llm or DemoLLMClient()

    async def plan(self, order: OrderRequest) -> RoutePlan:
        prompt = (
            "Decide the order route for a customer tier and destination.\n"
            f"customer_tier={order.customer_tier}\n"
            f"destination_region={order.destination_region}\n"
            f"item_count={len(order.items)}"
        )
        response = await self.llm.complete(
            task="planner_route",
            prompt=prompt,
            metadata={"order_id": order.order_id},
        )
        return RoutePlan(
            route_name=response["route_name"],
            requires_manual_review=response.get("requires_manual_review", False),
        )


class InventoryAgent:
    def reserve(self, order: OrderRequest, plan: RoutePlan) -> InventoryDecision:
        warehouse_id = "blr-1" if order.destination_region.lower() == "south" else "mum-2"
        return InventoryDecision(warehouse_id=warehouse_id, available=bool(order.items))


class FulfillmentAgent:
    def __init__(self, llm: DemoLLMClient | None = None, downstream_delay_seconds: float = 0.35) -> None:
        self.llm = llm or DemoLLMClient()
        self.downstream_delay_seconds = downstream_delay_seconds

    async def dispatch(self, order: OrderRequest, plan: RoutePlan, inventory: InventoryDecision) -> FulfillmentReceipt:
        prompt = (
            "Create a fulfillment dispatch decision.\n"
            f"order_id={order.order_id}\n"
            f"route_name={plan.route_name}\n"
            f"warehouse_id={inventory.warehouse_id}"
        )
        response = await self.llm.complete(
            task="fulfillment_dispatch",
            prompt=prompt,
            metadata={"order_id": order.order_id},
            artificial_delay_seconds=self.downstream_delay_seconds,
        )
        return FulfillmentReceipt(
            dispatch_id=response["dispatch_id"],
            route_name=response["route_name"],
            warehouse_id=response["warehouse_id"],
        )
