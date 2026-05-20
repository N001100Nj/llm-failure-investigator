# Graph Based LLM Failure Investigation System for AI Pipeline Reliability

An automated reliability investigation platform for failed Large Language Model pipeline executions. The system loads JSON traces, validates them with Pydantic, routes analysis through a LangGraph-style workflow, generates root-cause incident reports, stores metrics in SQLite, and indexes reports in ChromaDB and FAISS when those optional services are installed.

## Problem Statement

LLM applications fail in several ways that are hard to debug from a single log line: malformed structured output, hallucinated answers, weak retrieval, tool failures, and low-quality responses. This project provides a production-style MVP for investigating those failures consistently and producing actionable incident reports for AI pipeline reliability.

## Architecture

![Architecture Diagram](logoremover_1779284942198.jpeg)

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

## Demo Video

https://youtu.be/I0PheLGQKN4
