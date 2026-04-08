from __future__ import annotations

import asyncio

from order_orchestrator.agents import FulfillmentAgent
from order_orchestrator.models import OrderRequest
from order_orchestrator.runtime import OrderWorkflowRuntime


def test_order_workflow_should_complete_when_timeout_budget_is_large_enough() -> None:
    order = OrderRequest(
        order_id="order-101",
        customer_tier="gold",
        items=["book", "charger"],
        destination_region="south",
    )
    runtime = OrderWorkflowRuntime(handoff_timeout_seconds=0.5)

    result = asyncio.run(runtime.process_order(order))

    assert result.status == "completed"
    assert result.attempt_count == 1


def test_handoff_uses_configured_timeout_value() -> None:
    order = OrderRequest(
        order_id="order-202",
        customer_tier="silver",
        items=["console"],
        destination_region="west",
    )
    fulfillment = FulfillmentAgent(downstream_delay_seconds=0.25)
    runtime = OrderWorkflowRuntime(
        fulfillment=fulfillment,
        handoff_timeout_seconds=0.3,
    )

    result = asyncio.run(runtime.process_order(order))

    assert result.status == "completed"
    assert result.attempt_count == 1
