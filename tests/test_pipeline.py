"""End-to-end pipeline tests."""

from app.models.trace import ExecutionTrace
from app.pipeline.graph import investigate_trace


def test_pipeline_generates_incident_report() -> None:
    trace = ExecutionTrace(
        trace_id="t-pipeline",
        benchmark="Natural Questions",
        pipeline_name="rag",
        prompt="Who wrote Hamlet?",
        response="Charles Dickens wrote Hamlet.",
        expected_answer="William Shakespeare",
        retrieved_documents=[{"doc_id": "d1", "content": "Hamlet is a tragedy.", "score": 0.8}],
    )
    report = investigate_trace(trace)
    assert report.trace_id == "t-pipeline"
    assert report.failure_type in {"hallucination", "retrieval_inconsistency"}
    assert report.findings

