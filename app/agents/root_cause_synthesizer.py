"""Root-cause synthesis agent."""

from __future__ import annotations

from app.models.graph_state import GraphState
from app.models.report import IncidentReport, NodeFinding


_SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def _primary_finding(findings: list[NodeFinding]) -> NodeFinding | None:
    return max(findings, key=lambda item: (_SEVERITY_RANK[item.severity], item.confidence), default=None)


def synthesize_report(state: GraphState) -> GraphState:
    """Combine node findings into a final incident report."""

    trace = state["trace"]
    findings = list(state.get("findings", []))
    primary = _primary_finding(findings)
    if primary is None:
        report = IncidentReport(
            trace_id=trace.trace_id,
            failure_type="unknown",
            severity="low",
            root_cause="No strong rule-based failure signal was detected.",
            recommendation="Review the trace manually and add task-specific checks if this case is recurring.",
            investigation_summary="The trace was validated and routed through the investigation graph without high-confidence findings.",
            findings=[],
        )
    else:
        report = IncidentReport(
            trace_id=trace.trace_id,
            failure_type=primary.failure_type,
            severity=primary.severity,
            root_cause=primary.root_cause_hint,
            recommendation=primary.recommendation_hint,
            investigation_summary="; ".join(
                f"{finding.node_name} found {finding.failure_type} ({finding.severity}, confidence={finding.confidence:.2f})"
                for finding in findings
            ),
            findings=findings,
        )
    return {"report": report}
