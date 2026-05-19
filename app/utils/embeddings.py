"""Embedding helpers with a deterministic fallback."""

from __future__ import annotations

import hashlib
import math


class EmbeddingService:
    """Create text embeddings using sentence-transformers when available."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(model_name)
        except Exception:
            self._model = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return embeddings for texts."""

        if self._model is not None:
            return self._model.encode(texts, normalize_embeddings=True).tolist()
        return [_hash_embedding(text) for text in texts]


def _hash_embedding(text: str, dimensions: int = 384) -> list[float]:
    vector = [0.0] * dimensions
    for token in text.lower().split():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % dimensions
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]

