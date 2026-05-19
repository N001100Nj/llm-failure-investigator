"""Tests for schema validation analyzer."""

from app.agents.schema_validator import analyze_schema
from app.models.trace import ExecutionTrace


def test_schema_validator_flags_invalid_json() -> None:
    trace = ExecutionTrace(
        trace_id="t-schema",
        benchmark="Synthetic",
        pipeline_name="test",
        prompt="Return JSON",
        response="{bad",
        structured_output="{bad",
        expected_schema={"required": ["answer"]},
    )
    result = analyze_schema({"trace": trace, "findings": []})
    assert result["findings"][0].failure_type == "schema_validation_failure"

