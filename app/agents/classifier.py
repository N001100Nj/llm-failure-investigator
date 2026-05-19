"""Initial failure classifier for routing the graph."""

from __future__ import annotations

from app.models.graph_state import GraphState


def classify_failures(state: GraphState) -> GraphState:
    """Detect candidate failure types to decide which analyzers should run."""

    trace = state["trace"]
    failures: list[str] = []
    if trace.structured_output is not None or trace.expected_schema:
        failures.append("schema_validation_failure")
    if trace.expected_answer:
        failures.append("hallucination")
        if trace.retrieved_documents:
            failures.append("retrieval_inconsistency")
    if trace.tool_calls:
        failures.append("tool_execution_failure")
    failures.append("low_response_quality")
    return {"detected_failures": sorted(set(failures))}
