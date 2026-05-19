# Graph Based LLM Failure Investigation System for AI Pipeline Reliability

An automated reliability investigation platform for failed Large Language Model pipeline executions. The system loads JSON traces, validates them with Pydantic, routes analysis through a LangGraph-style workflow, generates root-cause incident reports, stores metrics in SQLite, and indexes reports in ChromaDB and FAISS when those optional services are installed.

## Problem Statement

LLM applications fail in several ways that are hard to debug from a single log line: malformed structured output, hallucinated answers, weak retrieval, tool failures, and low-quality responses. This project provides a production-style MVP for investigating those failures consistently and producing actionable incident reports for AI pipeline reliability.

## Architecture

```text
Failed JSON Trace
      |
      v
Pydantic ExecutionTrace validation
      |
      v
START -> classifier
      |
      +--> schema_validator
      +--> hallucination_detector
      +--> retrieval_analyzer
      +--> tool_failure_analyzer
      +--> response_quality_evaluator
      |
      v
root_cause_synthesizer -> IncidentReport -> END
      |
      +--> SQLite metrics and reports
      +--> ChromaDB report embeddings
      +--> FAISS report embeddings
      +--> Streamlit dashboard
```

The MVP uses deterministic rule-based analysis. LangGraph, ChromaDB, FAISS, and sentence-transformers are supported, but the code includes graceful fallbacks so the core investigation path remains simple to run.

## Features

- JSON trace ingestion and Pydantic validation.
- Dynamic graph routing to specialized investigation nodes.
- Detection of schema validation failures, hallucinations, retrieval inconsistencies, tool execution failures, and low response quality.
- Structured reports with failure type, severity, root cause, recommendation, and investigation summary.
- SQLite report and metrics store.
- ChromaDB and FAISS embedding stores for similarity search.
- Streamlit dashboard with incident browsing, severity distribution, failure counts, and reliability metrics.
- Apache Airflow DAGs for ingestion, analysis, report generation, and benchmarking.
- Docker and Docker Compose deployment.
- Sample traces and benchmark traces from HotpotQA, Natural Questions, TruthfulQA, GSM8K, and synthetic cases.

## Setup

Python 3.11 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For a lighter local demo, you can install only the core packages first:

```powershell
pip install pydantic pytest
```

The optional packages in `requirements.txt` enable LangGraph, Streamlit, ChromaDB, FAISS, sentence-transformers, and Airflow.

## Usage

Run the CLI on a sample trace:

```powershell
python app/main.py app/sample_traces/hallucination.json
```

Run all sample traces:

```powershell
Get-ChildItem app/sample_traces/*.json | ForEach-Object { python app/main.py $_.FullName }
```

Run tests:

```powershell
pytest
```

Start the dashboard:

```powershell
streamlit run dashboard/streamlit_app.py
```

Open the dashboard at `http://localhost:8501`.

## Docker

Build and run the investigation service:

```powershell
docker build -t llm-failure-investigator .
docker run --rm -v ${PWD}:/app llm-failure-investigator
```

Start the composed stack:

```powershell
docker compose up --build
```

Services:

- Investigation service: runs one sample analysis.
- Streamlit dashboard: `http://localhost:8501`.
- Airflow standalone: `http://localhost:8080`.
- Ollama: optional profile with `docker compose --profile ollama up`.

## Trace Format

Each trace should include fields such as:

```json
{
  "trace_id": "example-001",
  "benchmark": "Synthetic",
  "pipeline_name": "rag-agent",
  "prompt": "Question asked to the LLM",
  "response": "Model response",
  "expected_answer": "Ground truth answer",
  "structured_output": {"answer": "value"},
  "expected_schema": {"required": ["answer"]},
  "retrieved_documents": [{"doc_id": "d1", "content": "context"}],
  "tool_calls": [{"name": "calculator", "input": {}, "output": null, "error": "timeout"}],
  "metadata": {}
}
```

## Dashboard Screenshots

Add screenshots here after running the Streamlit dashboard:

- Incident report list.
- Severity distribution chart.
- Failure type count chart.
- Reliability metric cards.

## Airflow DAGs

The `dags/` folder contains:

- `trace_ingestion_dag.py`: scheduled ingestion placeholder.
- `failure_analysis_dag.py`: analyzes pending JSON files in `data/traces`.
- `report_generation_dag.py`: computes reliability metrics.
- `benchmarking_dag.py`: analyzes benchmark traces in `data/benchmarks`.

## YouTube Demo Script

Use this 3-5 minute structure:

1. Introduce the problem: failed LLM pipelines need repeatable investigation, not manual log inspection.
2. Show the architecture diagram and explain classifier-driven routing to specialized analyzers.
3. Run `python app/main.py app/sample_traces/hallucination.json` and point out the generated report fields.
4. Run multiple sample traces and open the Streamlit dashboard to show severity and failure type metrics.
5. Show the Airflow DAG folder and Docker Compose file to demonstrate production-style orchestration.
6. Close with future work: richer semantic evaluation, alerting, CI integration, and human feedback loops.

## Future Work

- Add semantic similarity scoring with cross-encoders.
- Add OpenTelemetry ingestion for real production traces.
- Add Slack or email incident notifications.
- Add analyst feedback labels to improve routing thresholds.
- Add model/provider comparison reports for benchmark runs.
- Expand optional Ollama and Gemini report enrichment.

