"""Airflow DAG for scheduled trace ingestion."""

from __future__ import annotations

from datetime import datetime

try:
    from airflow.decorators import dag, task
except Exception:
    dag = task = None


if dag:
    @dag(schedule="@hourly", start_date=datetime(2026, 1, 1), catchup=False, tags=["llm-failures"])
    def trace_ingestion_dag():
        @task
        def ingest() -> str:
            return "Trace ingestion watches data/traces for JSON execution traces."

        ingest()

    trace_ingestion_dag()

