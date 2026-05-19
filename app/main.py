"""CLI entrypoint for LLM failure investigation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import ValidationError

from app.models.trace import ExecutionTrace
from app.pipeline.graph import investigate_trace
from app.storage.chroma_store import ChromaReportStore
from app.storage.faiss_store import FaissReportStore
from app.storage.sqlite_store import SQLiteStore
from app.utils.logger import get_logger
from app.utils.settings import Settings

logger = get_logger(__name__)


def load_trace(path: str | Path) -> ExecutionTrace:
    """Load and validate a JSON execution trace."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return ExecutionTrace.model_validate(payload)


def run(trace_path: str | Path) -> dict[str, object]:
    """Analyze one trace, persist artifacts, and return a report payload."""

    settings = Settings()
    trace = load_trace(trace_path)
    report = investigate_trace(trace)
    SQLiteStore(settings.sqlite_path).save_report(report)
    ChromaReportStore(settings.chroma_path).add_report(report)
    FaissReportStore(settings.faiss_path).add_report(report)
    output_path = Path("data/reports") / f"{report.report_id}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    logger.info("Saved incident report %s", report.report_id)
    return report.model_dump()


def main() -> None:
    """Run the CLI."""

    parser = argparse.ArgumentParser(description="Investigate a failed LLM execution trace.")
    parser.add_argument("trace_path", help="Path to a failed execution trace JSON file.")
    args = parser.parse_args()
    try:
        report = run(args.trace_path)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise SystemExit(f"Invalid trace: {exc}") from exc
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
