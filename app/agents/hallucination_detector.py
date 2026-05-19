"""Hallucination detector based on answer overlap."""

from __future__ import annotations

import re

from app.models.graph_state import GraphState
from app.models.report import NodeFinding


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def answer_overlap(response: str, expected_answer: str) -> float:
    """Return token recall of the expected answer within the model response."""

    expected = _tokens(expected_answer)
    if not expected:
        return 1.0
    return len(expected & _tokens(response)) / len(expected)


def analyze_hallucination(state: GraphState) -> GraphState:
    """Flag hallucination when response diverges materially from the expected answer."""

    trace = state["trace"]
    if not trace.expected_answer:
        return {}

    overlap = answer_overlap(trace.response, trace.expected_answer)
    if overlap < 0.6:
        return {
            "findings": [
                NodeFinding(
                    node_name="hallucination_detector",
                    failure_type="hallucination",
                    severity="high" if overlap < 0.3 else "medium",
                    confidence=round(1.0 - overlap, 2),
                    evidence=[f"expected answer token recall={overlap:.2f}", f"expected='{trace.expected_answer}'"],
                    root_cause_hint="The generated answer does not match the expected answer.",
                    recommendation_hint="Add answer grounding checks, strengthen evaluation prompts, and retry with retrieved context citations.",
                )
            ]
        }
    return {}
