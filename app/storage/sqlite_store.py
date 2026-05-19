"""SQLite persistence for incident reports and metrics."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.models.metrics import ReliabilityMetrics
from app.models.report import IncidentReport


class SQLiteStore:
    """Simple SQLite repository for incident reports."""

    def __init__(self, db_path: str | Path = "data/reports/incidents.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS incident_reports (
                    report_id TEXT PRIMARY KEY,
                    trace_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    failure_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    root_cause TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    investigation_summary TEXT NOT NULL,
                    findings_json TEXT NOT NULL
                )
                """
            )

    def save_report(self, report: IncidentReport) -> None:
        """Insert or replace an incident report."""

        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO incident_reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report.report_id,
                    report.trace_id,
                    report.created_at.isoformat(),
                    report.failure_type,
                    report.severity,
                    report.root_cause,
                    report.recommendation,
                    report.investigation_summary,
                    json.dumps([finding.model_dump() for finding in report.findings], default=str),
                ),
            )

    def list_reports(self) -> list[dict[str, str]]:
        """Return reports as dictionaries for dashboard use."""

        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM incident_reports ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def metrics(self) -> ReliabilityMetrics:
        """Compute reliability metrics from stored reports."""

        reports = self.list_reports()
        failure_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        for report in reports:
            failure_counts[report["failure_type"]] = failure_counts.get(report["failure_type"], 0) + 1
            severity_counts[report["severity"]] = severity_counts.get(report["severity"], 0) + 1
        total = len(reports)
        critical = severity_counts.get("critical", 0)
        high_or_critical = critical + severity_counts.get("high", 0)
        return ReliabilityMetrics(
            total_incidents=total,
            failure_type_counts=failure_counts,
            severity_counts=severity_counts,
            critical_rate=critical / total if total else 0.0,
            high_or_critical_rate=high_or_critical / total if total else 0.0,
        )

