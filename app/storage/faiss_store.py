"""FAISS storage for report embeddings with JSON fallback."""

from __future__ import annotations

import json
from pathlib import Path

from app.models.report import IncidentReport
from app.utils.embeddings import EmbeddingService


class FaissReportStore:
    """Persist report embeddings in FAISS when installed."""

    def __init__(self, index_path: str = "data/reports/faiss.index", metadata_path: str = "data/reports/faiss_metadata.json") -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.embeddings = EmbeddingService()

    def add_report(self, report: IncidentReport) -> None:
        """Add a report to FAISS, or a JSON metadata fallback if FAISS is unavailable."""

        text = f"{report.failure_type} {report.severity} {report.root_cause} {report.recommendation}"
        vector = self.embeddings.embed([text])[0]
        try:
            import faiss
            import numpy as np

            array = np.array([vector], dtype="float32")
            if self.index_path.exists():
                index = faiss.read_index(str(self.index_path))
            else:
                index = faiss.IndexFlatIP(array.shape[1])
            index.add(array)
            faiss.write_index(index, str(self.index_path))
        except Exception:
            records = []
            if self.metadata_path.exists():
                records = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            records.append({"report_id": report.report_id, "trace_id": report.trace_id, "text": text, "embedding_preview": vector[:8]})
            self.metadata_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

