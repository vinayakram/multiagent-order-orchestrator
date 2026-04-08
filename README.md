# Multiagent Order Orchestrator

A small AI-style multi-agent workflow that routes an order through planning, inventory, and fulfillment steps.

## Simple client brief

This project simulates how an order platform can use multiple agents to decide how to process an order:
- a planner agent decides the route
- an inventory agent checks stock
- a fulfillment agent prepares dispatch

The seeded bug is production-friendly for a demo:
- the planner-to-fulfillment handoff times out even when the runtime is configured with a larger timeout
- this makes the system look unreliable during busy periods

## Why it is good for the remediation demo

- Easy to explain in business language
- Clearly multi-agent
- Timeout and retry issues are realistic
- Good overlap with the support project for project-selection ambiguity

## Project layout

- `src/order_orchestrator/models.py`
- `src/order_orchestrator/agents.py`
- `src/order_orchestrator/runtime.py`
- `tests/test_runtime.py`

## Seeded issue

The runtime incorrectly caps the fulfillment handoff timeout at `0.2` seconds, even when a larger timeout is configured. A normal downstream delay can therefore fail as a timeout.

## Demo commands

```bash
pytest -q
```
