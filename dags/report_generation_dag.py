"""Airflow DAG for report export jobs."""

from __future__ import annotations

from datetime import datetime

try:
    from airflow.decorators import dag, task
except Exception:
    dag = task = None


if dag:
    @dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False, tags=["llm-failures"])
    def report_generation_dag():
        @task
        def summarize_reports() -> dict[str, object]:
            from app.storage.sqlite_store import SQLiteStore

            return SQLiteStore().metrics().model_dump()

        summarize_reports()

    report_generation_dag()

