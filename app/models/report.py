"""Incident report models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


FailureType = Literal[
    "schema_validation_failure",
    "hallucination",
    "retrieval_inconsistency",
    "tool_execution_failure",
    "low_response_quality",
    "unknown",
]

Severity = Literal["low", "medium", "high", "critical"]


class NodeFinding(BaseModel):
    """Finding produced by one investigation node."""

    node_name: str
    failure_type: FailureType
    severity: Severity
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    root_cause_hint: str
    recommendation_hint: str


class IncidentReport(BaseModel):
    """Structured root-cause analysis report."""

    report_id: str = Field(default_factory=lambda: str(uuid4()))
    trace_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    failure_type: FailureType
    severity: Severity
    root_cause: str
    recommendation: str
    investigation_summary: str
    findings: list[NodeFinding] = Field(default_factory=list)

