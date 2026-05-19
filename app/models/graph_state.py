"""State passed between LangGraph nodes."""

from __future__ import annotations

from operator import add
from typing import Annotated, TypedDict

from app.models.report import IncidentReport, NodeFinding
from app.models.trace import ExecutionTrace


class GraphState(TypedDict, total=False):
    """Typed graph state for an investigation run."""

    trace: ExecutionTrace
    detected_failures: list[str]
    findings: Annotated[list[NodeFinding], add]
    report: IncidentReport
