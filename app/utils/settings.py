"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime configuration."""

    sqlite_path: str = os.getenv("SQLITE_PATH", "data/reports/incidents.db")
    chroma_path: str = os.getenv("CHROMA_PATH", "data/reports/chroma")
    faiss_path: str = os.getenv("FAISS_PATH", "data/reports/faiss.index")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    llm_provider: str = os.getenv("LLM_PROVIDER", "none")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")

