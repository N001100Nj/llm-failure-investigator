"""Tool execution failure analyzer."""

from __future__ import annotations

from app.models.graph_state import GraphState
from app.models.report import NodeFinding


def analyze_tools(state: GraphState) -> GraphState:
    """Inspect tool errors and missing outputs."""

    trace = state["trace"]
    failed = [call for call in trace.tool_calls if call.error or call.output in (None, "")]
    if failed:
        evidence = [f"{call.name}: {call.error or 'empty output'}" for call in failed]
        return {
            "findings": [
                NodeFinding(
                    node_name="tool_failure_analyzer",
                    failure_type="tool_execution_failure",
                    severity="critical" if any(call.error for call in failed) else "medium",
                    confidence=0.92,
                    evidence=evidence,
                    root_cause_hint="One or more external tools failed or returned unusable output.",
                    recommendation_hint="Add timeout handling, typed tool contracts, retries, and fallback behavior for critical tools.",
                )
            ]
        }
    return {}
