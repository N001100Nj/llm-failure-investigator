"""Routing helpers for analyzer execution."""

from __future__ import annotations

from app.models.graph_state import GraphState


def selected_analyzers(state: GraphState) -> list[str]:
    """Return analyzer node names selected by the classifier."""

    mapping = {
        "schema_validation_failure": "schema_validator",
        "hallucination": "hallucination_detector",
        "retrieval_inconsistency": "retrieval_analyzer",
        "tool_execution_failure": "tool_failure_analyzer",
        "low_response_quality": "response_quality_evaluator",
    }
    return [mapping[item] for item in state.get("detected_failures", []) if item in mapping]

