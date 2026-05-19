"""ChromaDB storage for report embeddings."""

from __future__ import annotations

from pathlib import Path

from app.models.report import IncidentReport
from app.utils.embeddings import EmbeddingService


class ChromaReportStore:
    """Persist reports in ChromaDB when installed."""

    def __init__(self, persist_path: str = "data/reports/chroma") -> None:
        self.persist_path = persist_path
        Path(persist_path).mkdir(parents=True, exist_ok=True)
        self.embeddings = EmbeddingService()
        self.collection = None
        try:
            import chromadb

            client = chromadb.PersistentClient(path=persist_path)
            self.collection = client.get_or_create_collection("incident_reports")
        except Exception:
            self.collection = None

    def add_report(self, report: IncidentReport) -> None:
        """Add a report document to ChromaDB if available."""

        if self.collection is None:
            return
        text = f"{report.failure_type} {report.severity} {report.root_cause} {report.recommendation}"
        embedding = self.embeddings.embed([text])[0]
        self.collection.upsert(ids=[report.report_id], documents=[text], embeddings=[embedding], metadatas=[{"trace_id": report.trace_id}])

