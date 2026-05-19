"""Retrieval consistency analyzer."""

from __future__ import annotations

from app.models.graph_state import GraphState
from app.models.report import NodeFinding


def analyze_retrieval(state: GraphState) -> GraphState:
    """Check whether the expected answer appears in retrieved context."""

    trace = state["trace"]
    if not trace.expected_answer or not trace.retrieved_documents:
        return {}

    needle = trace.expected_answer.lower()
    haystack = "\n".join(doc.content for doc in trace.retrieved_documents).lower()
    if needle not in haystack:
        return {
            "findings": [
                NodeFinding(
                    node_name="retrieval_analyzer",
                    failure_type="retrieval_inconsistency",
                    severity="high",
                    confidence=0.88,
                    evidence=[f"expected answer not found in {len(trace.retrieved_documents)} retrieved documents"],
                    root_cause_hint="Retriever failed to supply evidence containing the target answer.",
                    recommendation_hint="Tune retrieval query rewriting, chunking, embedding model, and top-k recall thresholds.",
                )
            ]
        }
    return {}
