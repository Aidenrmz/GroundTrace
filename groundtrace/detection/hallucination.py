"""Grounding detection module for GroundTrace.

Compares generated sentences against retrieved chunks with sentence embeddings.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from groundtrace.branding import PRODUCT_NAME
from groundtrace.types import OutputToken, RetrievedChunk


_model: Optional[SentenceTransformer] = None


def _get_model() -> SentenceTransformer:
    """Lazy-load the sentence-transformers model as a singleton."""
    global _model
    if _model is None:
        import sys
        from pathlib import Path

        cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model_cached = any(
            (cache_dir / directory).exists()
            for directory in [
                model_name.replace("/", "--"),
                f"models--{model_name.replace('/', '--')}",
            ]
        )

        if not model_cached:
            print(
                f"\033[33m[{PRODUCT_NAME}] Downloading all-MiniLM-L6-v2 "
                "(~90MB) for grounding detection; one-time download...\033[0m",
                file=sys.stderr,
            )

        _model = SentenceTransformer("all-MiniLM-L6-v2")

        if not model_cached:
            print(f"\033[32m[{PRODUCT_NAME}] Model ready.\033[0m", file=sys.stderr)

    return _model


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


def _split_sentences(text: str) -> list[tuple[str, int, int]]:
    """Split text into simple sentence spans."""
    if not text:
        return []

    sentences = []
    current_pos = 0

    parts = text.split(". ")
    for index, part in enumerate(parts):
        if not part.strip():
            current_pos += len(part) + 2
            continue

        sentence = part + "." if index < len(parts) - 1 else part
        if index == len(parts) - 1 and part.endswith("."):
            sentence = part

        start_pos = current_pos
        end_pos = start_pos + len(sentence)
        sentences.append((sentence.strip(), start_pos, end_pos))
        current_pos = end_pos + 2

    return sentences


class HallucinationDetector:
    """Detect weakly grounded output sentences."""

    HALLUCINATION_THRESHOLD: float = 0.4

    def detect(
        self,
        output_text: str,
        chunks: list[RetrievedChunk],
    ) -> list[OutputToken]:
        """
        Detect weak grounding in output text.

        Args:
            output_text: The LLM output text to analyze.
            chunks: Retrieved chunks from the vector store.

        Returns:
            OutputToken objects with grounding metadata.
        """
        if not output_text or not output_text.strip():
            return []

        if not chunks:
            sentences = _split_sentences(output_text)
            return [
                OutputToken(
                    text=sentence,
                    position=position,
                    is_hallucinated=True,
                    hallucination_score=1.0,
                    chunk_attributions={},
                )
                for position, (sentence, _, _) in enumerate(sentences)
            ]

        model = _get_model()
        sentences = _split_sentences(output_text)
        if not sentences:
            return []

        sentence_texts = [sentence for sentence, _, _ in sentences]
        sentence_embeddings = model.encode(sentence_texts, convert_to_numpy=True)

        chunk_texts = [chunk.text for chunk in chunks]
        chunk_embeddings = model.encode(chunk_texts, convert_to_numpy=True)

        output_tokens: list[OutputToken] = []

        for position, (sentence, _start_pos, _end_pos) in enumerate(sentences):
            sent_embedding = sentence_embeddings[position]
            max_similarity = 0.0
            top_chunks: dict[str, float] = {}
            similarities: list[tuple[str, float]] = []

            for chunk, chunk_emb in zip(chunks, chunk_embeddings):
                similarity = _cosine_similarity(sent_embedding, chunk_emb)
                similarities.append((chunk.chunk_id, similarity))
                max_similarity = max(max_similarity, similarity)

            is_hallucinated = max_similarity < self.HALLUCINATION_THRESHOLD
            hallucination_score = 1.0 - max_similarity if is_hallucinated else 0.0

            if not is_hallucinated:
                similarities.sort(key=lambda item: item[1], reverse=True)
                for chunk_id, similarity in similarities[:3]:
                    top_chunks[chunk_id] = similarity

            output_tokens.append(
                OutputToken(
                    text=sentence,
                    position=position,
                    is_hallucinated=is_hallucinated,
                    hallucination_score=hallucination_score,
                    chunk_attributions=top_chunks,
                )
            )

        return output_tokens


detector = HallucinationDetector()
