"""Tests for hallucination detection."""

from app.agents.hallucination_detector import analyze_hallucination, answer_overlap
from app.models.trace import ExecutionTrace


def test_answer_overlap_detects_mismatch() -> None:
    assert answer_overlap("Paris is the capital of France", "Berlin") == 0.0


def test_hallucination_detector_flags_wrong_answer() -> None:
    trace = ExecutionTrace(
        trace_id="t-hallucination",
        benchmark="TruthfulQA",
        pipeline_name="test",
        prompt="What is the capital of France?",
        response="The capital is Berlin.",
        expected_answer="Paris",
    )
    result = analyze_hallucination({"trace": trace, "findings": []})
    assert result["findings"][0].failure_type == "hallucination"

