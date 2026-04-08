from __future__ import annotations

import asyncio


class DemoLLMClient:
    """Small async LLM wrapper for demo purposes.

    The interface mimics an LLM-backed agent call without requiring network access
    during the demo. Runtime failures still look like real LLM handoff failures
    because the agents await this client and the orchestration layer applies timeouts.
    """

    async def complete(
        self,
        *,
        task: str,
        prompt: str,
        metadata: dict[str, str] | None = None,
        artificial_delay_seconds: float = 0.05,
    ) -> dict[str, str | bool]:
        await asyncio.sleep(artificial_delay_seconds)

        if task == "planner_route":
            route_name = "priority-route" if "customer_tier=gold" in prompt.lower() else "standard-route"
            return {
                "route_name": route_name,
                "requires_manual_review": False,
            }

        if task == "fulfillment_dispatch":
            order_id = (metadata or {}).get("order_id", "unknown")
            route_name = "priority-route" if "priority-route" in prompt else "standard-route"
            warehouse_id = "blr-1" if "warehouse_id=blr-1" in prompt else "mum-2"
            return {
                "dispatch_id": f"dispatch-{order_id}",
                "route_name": route_name,
                "warehouse_id": warehouse_id,
            }

        raise ValueError(f"Unsupported task: {task}")
