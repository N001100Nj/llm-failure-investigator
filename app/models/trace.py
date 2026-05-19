"""Execution trace models for failed LLM pipeline runs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class RetrievedDocument(BaseModel):
    """Document returned by a retrieval step."""

    doc_id: str = Field(..., min_length=1)
    content: str
    score: float | None = None
    source: str | None = None


class ToolCall(BaseModel):
    """Tool execution metadata captured during an LLM pipeline run."""

    name: str = Field(..., min_length=1)
    input: dict[str, Any] = Field(default_factory=dict)
    output: Any | None = None
    error: str | None = None
    latency_ms: int | None = Field(default=None, ge=0)


class ExecutionTrace(BaseModel):
    """Validated representation of one failed LLM execution trace."""

    trace_id: str = Field(..., min_length=1)
    benchmark: Literal["HotpotQA", "Natural Questions", "TruthfulQA", "GSM8K", "Synthetic"]
    pipeline_name: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prompt: str
    response: str
    expected_answer: str | None = None
    structured_output: str | dict[str, Any] | list[Any] | None = None
    expected_schema: dict[str, Any] | None = None
    retrieved_documents: list[RetrievedDocument] = Field(default_factory=list)
    tool_calls: list[ToolCall] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

