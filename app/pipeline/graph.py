"""LangGraph workflow definition with a deterministic fallback executor."""

from __future__ import annotations

from collections.abc import Callable

from app.agents.classifier import classify_failures
from app.agents.hallucination_detector import analyze_hallucination
from app.agents.response_quality_evaluator import analyze_quality
from app.agents.retrieval_analyzer import analyze_retrieval
from app.agents.root_cause_synthesizer import synthesize_report
from app.agents.schema_validator import analyze_schema
from app.agents.tool_failure_analyzer import analyze_tools
from app.models.graph_state import GraphState
from app.models.report import IncidentReport
from app.models.trace import ExecutionTrace
from app.pipeline.router import selected_analyzers


Analyzer = Callable[[GraphState], GraphState]

ANALYZERS: dict[str, Analyzer] = {
    "schema_validator": analyze_schema,
    "hallucination_detector": analyze_hallucination,
    "retrieval_analyzer": analyze_retrieval,
    "tool_failure_analyzer": analyze_tools,
    "response_quality_evaluator": analyze_quality,
}


class InvestigationGraph:
    """Small wrapper exposing an invoke API compatible with LangGraph usage."""

    def invoke(self, state: GraphState) -> GraphState:
        routed = _merge_update(state, classify_failures(state))
        for analyzer_name in selected_analyzers(routed):
            routed = _merge_update(routed, ANALYZERS[analyzer_name](routed))
        return _merge_update(routed, synthesize_report(routed))


def _merge_update(state: GraphState, update: GraphState) -> GraphState:
    """Apply a node's partial state update for the non-LangGraph fallback."""

    if not update:
        return state
    merged: GraphState = {**state, **update}
    if "findings" in update:
        merged["findings"] = [*state.get("findings", []), *update["findings"]]
    return merged


def build_graph() -> object:
    """Build a LangGraph StateGraph when available, otherwise use the local executor."""

    try:
        from langgraph.graph import END, START, StateGraph
    except Exception:
        return InvestigationGraph()

    graph = StateGraph(GraphState)
    graph.add_node("classifier", classify_failures)
    for name, func in ANALYZERS.items():
        graph.add_node(name, func)
    graph.add_node("root_cause_synthesizer", synthesize_report)
    graph.add_edge(START, "classifier")
    graph.add_conditional_edges("classifier", selected_analyzers, {name: name for name in ANALYZERS})
    for name in ANALYZERS:
        graph.add_edge(name, "root_cause_synthesizer")
    graph.add_edge("root_cause_synthesizer", END)
    return graph.compile()


def investigate_trace(trace: ExecutionTrace) -> IncidentReport:
    """Run a trace through the investigation graph and return the final report."""

    result = build_graph().invoke({"trace": trace, "findings": []})
    return result["report"]
