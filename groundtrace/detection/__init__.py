"""Detection module for hallucination and other anomalies in RAG outputs."""

from groundtrace.detection.hallucination import (
    HallucinationDetector,
    detector,
)

__all__ = [
    "HallucinationDetector",
    "detector",
]
