from __future__ import annotations

import asyncio

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
