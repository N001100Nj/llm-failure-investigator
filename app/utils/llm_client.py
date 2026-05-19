"""Optional LLM client hooks for future enrichment."""

from __future__ import annotations

from app.utils.settings import Settings


class OptionalLLMClient:
    """Minimal optional LLM facade for Ollama or Gemini-backed extensions."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()

    def enabled(self) -> bool:
        """Return whether an external LLM provider is configured."""

        return self.settings.llm_provider.lower() in {"ollama", "gemini"}

    def summarize(self, prompt: str) -> str:
        """Placeholder summarization hook used only when integrations are added."""

        if not self.enabled():
            return prompt
        return prompt

