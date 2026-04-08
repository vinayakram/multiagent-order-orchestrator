from __future__ import annotations

import asyncio

from .agents import FulfillmentAgent, InventoryAgent, PlannerAgent
from .models import OrderRequest, WorkflowResult


class OrderWorkflowRuntime:
    def __init__(
        self,
        planner: PlannerAgent | None = None,
        inventory: InventoryAgent | None = None,
        fulfillment: FulfillmentAgent | None = None,
        handoff_timeout_seconds: float = 0.6,
        max_attempts: int = 2,
    ) -> None:
        self.planner = planner or PlannerAgent()
        self.inventory = inventory or InventoryAgent()
        self.fulfillment = fulfillment or FulfillmentAgent()
        self.handoff_timeout_seconds = handoff_timeout_seconds
        self.max_attempts = max_attempts

    async def process_order(self, order: OrderRequest) -> WorkflowResult:
        trace = ["planner:started"]
        plan = await self.planner.plan(order)
        trace.append(f"planner:route={plan.route_name}")

        inventory = self.inventory.reserve(order, plan)
        trace.append(f"inventory:warehouse={inventory.warehouse_id}")
        if not inventory.available:
            return WorkflowResult(
                status="blocked",
                route_name=plan.route_name,
                attempt_count=0,
                error="inventory_unavailable",
                trace=trace,
            )

        for attempt in range(1, self.max_attempts + 1):
            trace.append(f"fulfillment:attempt={attempt}")
            try:
                await asyncio.wait_for(
                    self.fulfillment.dispatch(order, plan, inventory),
                    timeout=self.handoff_timeout_seconds,
                )
                trace.append("fulfillment:success")
                return WorkflowResult(
                    status="completed",
                    route_name=plan.route_name,
                    attempt_count=attempt,
                    trace=trace,
                )
            except asyncio.TimeoutError:
                trace.append("fulfillment:timeout")

        return WorkflowResult(
            status="failed",
            route_name=plan.route_name,
            attempt_count=self.max_attempts,
            error="fulfillment_timeout",
            trace=trace,
        )
