"""Monkey-patch interceptors for LLM providers and vector databases.

This module provides a registry of interceptors that can be installed/uninstalled
to record LLM requests/responses and vector database queries (ChromaDB, Pinecone,
FAISS, Weaviate, pgvector, etc.).
"""

from __future__ import annotations

import threading
from typing import Any

from groundtrace.interceptors.anthropic_patch import AnthropicInterceptor
from groundtrace.interceptors.chroma_patch import ChromaInterceptor
from groundtrace.interceptors.faiss_patch import FAISSInterceptor
from groundtrace.interceptors.gemini_patch import GeminiInterceptor
from groundtrace.interceptors.httpx_transport import HttpxTransportInterceptor
from groundtrace.interceptors.langchain_patch import LangChainInterceptor
from groundtrace.interceptors.openai_patch import OpenAIInterceptor
from groundtrace.interceptors.pgvector_patch import PGVectorInterceptor
from groundtrace.interceptors.pinecone_patch import PineconeInterceptor
from groundtrace.interceptors.transformers_patch import TransformersInterceptor
from groundtrace.interceptors.weaviate_patch import WeaviateInterceptor

# Global registry of all available interceptors
_INTERCEPTORS: dict[str, Any] = {
    "httpx": HttpxTransportInterceptor(),
    "openai": OpenAIInterceptor(),
    "anthropic": AnthropicInterceptor(),
    "gemini": GeminiInterceptor(),
    "langchain": LangChainInterceptor(),
    "chroma": ChromaInterceptor(),
    "pinecone": PineconeInterceptor(),
    "faiss": FAISSInterceptor(),
    "transformers": TransformersInterceptor(),
    "weaviate": WeaviateInterceptor(),
    "pgvector": PGVectorInterceptor(),
}

_lock = threading.Lock()


def install_all() -> list[str]:
    """Install all available interceptors.

    Silently skips interceptors whose libraries are not installed.

    Returns:
        List of names of successfully installed interceptors.
    """
    with _lock:
        installed = []
        for name, interceptor in _INTERCEPTORS.items():
            try:
                interceptor.install()
                if interceptor.is_installed():
                    installed.append(name)
            except Exception:
                # Silently skip if installation fails (e.g., library not installed)
                pass
        return installed


def uninstall_all() -> None:
    """Uninstall all interceptors and restore original functions."""
    with _lock:
        for interceptor in _INTERCEPTORS.values():
            try:
                interceptor.uninstall()
            except Exception:
                # Silently ignore errors during uninstall
                pass


def get_installed() -> list[str]:
    """Return list of currently installed interceptors."""
    with _lock:
        return [name for name, interceptor in _INTERCEPTORS.items() if interceptor.is_installed()]


__all__ = [
    "install_all",
    "uninstall_all",
    "get_installed",
]
