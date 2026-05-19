"""Heuristic response quality evaluator."""

from __future__ import annotations

from app.models.graph_state import GraphState
from app.models.report import NodeFinding


def quality_score(response: str) -> float:
    """Score response quality with simple length and specificity heuristics."""

    stripped = response.strip()
    if not stripped:
        return 0.0
    score = 0.4
    if len(stripped.split()) >= 8:
        score += 0.25
    if any(char.isdigit() for char in stripped):
        score += 0.1
    if len(set(stripped.lower().split())) / max(1, len(stripped.split())) > 0.55:
        score += 0.15
    if "i don't know" in stripped.lower() or "cannot answer" in stripped.lower():
        score -= 0.25
    return max(0.0, min(1.0, score))


def analyze_quality(state: GraphState) -> GraphState:
    """Flag very short, evasive, or low-information responses."""

    trace = state["trace"]
    score = quality_score(trace.response)
    if score < 0.55:
        return {
            "findings": [
                NodeFinding(
                    node_name="response_quality_evaluator",
                    failure_type="low_response_quality",
                    severity="medium" if score >= 0.3 else "high",
                    confidence=round(1.0 - score, 2),
                    evidence=[f"quality_score={score:.2f}", f"response_length_words={len(trace.response.split())}"],
                    root_cause_hint="The answer is too terse, evasive, or lacks useful detail.",
                    recommendation_hint="Use response quality gates, minimum evidence requirements, and clearer answer format instructions.",
                )
            ]
        }
    return {}
