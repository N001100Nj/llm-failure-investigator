"""Airflow DAG for scheduled benchmark analysis."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    from airflow.decorators import dag, task
except Exception:
    dag = task = None


if dag:
    @dag(schedule="@weekly", start_date=datetime(2026, 1, 1), catchup=False, tags=["llm-failures", "benchmarks"])
    def benchmarking_dag():
        @task
        def run_benchmarks() -> int:
            from app.main import run

            count = 0
            for path in Path("data/benchmarks").glob("*.json"):
                run(path)
                count += 1
            return count

        run_benchmarks()

    benchmarking_dag()

