"""Airflow DAG for running failure analysis."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from airflow.decorators import dag, task
except Exception:
    dag = task = None


if dag:
    @dag(schedule="@hourly", start_date=datetime(2026, 1, 1), catchup=False, tags=["llm-failures"])
    def failure_analysis_dag():
        @task
        def analyze_pending() -> int:
            from app.main import run

            count = 0
            for path in Path("data/traces").glob("*.json"):
                run(path)
                count += 1
            return count

        analyze_pending()

    failure_analysis_dag()

