"""Reliability metrics models."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ReliabilityMetrics(BaseModel):
    """Aggregated reliability metrics derived from incident reports."""

    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_incidents: int = 0
    failure_type_counts: dict[str, int] = Field(default_factory=dict)
    severity_counts: dict[str, int] = Field(default_factory=dict)
    critical_rate: float = 0.0
    high_or_critical_rate: float = 0.0

