# Changelog

This file summarizes meaningful changes to GroundTrace. The project follows semantic versioning for public Python APIs and dashboard behavior.

## Unreleased

- Updated the user-facing project name to GroundTrace.
- Standardized the console command and package import on `groundtrace`.
- Updated dashboard labels, server metadata, CLI text, storage naming, and documentation.
- Standardized dashboard session-cache naming on the GroundTrace key.
- Made session URLs reflect the host and port used when `serve()` starts the server.
- Rewrote project documentation in new wording and kept existing demo media references.

## 0.1.3 - 2026-03-09

### Added

- Streaming response capture through the `httpx` transport wrapper. Server-sent event chunks are reconstructed after the stream finishes.
- LangChain interception for chat model generation and retriever calls.
- Conversation metadata for multi-step agent traces through `parent_request_id`, `conversation_id`, and `chain_step`.
- More resilient chunk removal for perturbation scoring, including exact-match, prefix, and first-sentence fallbacks.
- First-use model download notices for embedding and attribution models.
- Native pgvector tracing for SQLAlchemy sessions that use vector similarity operators.

### Notes

- The main RAG surfaces are covered without manual instrumentation: common LLM SDKs, ChromaDB, Pinecone, FAISS, Weaviate, LangChain, and pgvector.

## 0.1.2 - 2026-03-09

### Added

- Transport-level `httpx` interception so SDK version changes are less likely to break capture.
- Bounded LIME-style perturbation scoring that uses a fixed sample count.
- Conditional attribution so expensive scoring only runs when weak grounding is detected.
- Attention rollout path for local HuggingFace models.

### Fixed

- Session isolation now uses `contextvars.ContextVar` so concurrent tasks do not share active session state.
- Request body limiting moved to pure ASGI middleware for reliable FastAPI behavior.
- Attribution work is capped with a semaphore before entering the thread pool.
- WebSocket Origin validation is enforced before accepting connections.
- Attention scoring guards against divide-by-zero cases.

## 0.1.1 - 2026-03-09

### Security And Stability

- CORS is restricted to localhost origins.
- Interceptor bookkeeping errors are caught so tracing failures do not crash user code.
- Install and uninstall paths are protected by locks.
- Vector scores are normalized into a safe range.
- Request bodies are limited to one megabyte.
- LLM message inputs tolerate missing or malformed values.

### Dashboard And Runtime Fixes

- Attribution now uses a bounded `ThreadPoolExecutor` rather than spawning one thread per response.
- The in-memory session bus keeps a capped recent history.
- Dashboard rendering handles missing or invalid scores.
- Large sessions are summarized before writing to `localStorage`.
- Polling cadence was relaxed to reduce idle work.

## 0.1.0 - 2026-03-08

### Added

- Initial Python API: `serve()`, `stop()`, `new_session()`, and `get_session_url()`.
- Interceptors for OpenAI, Anthropic, Gemini, HuggingFace Transformers, ChromaDB, Pinecone, FAISS, and Weaviate.
- Sentence-level grounding detection based on semantic similarity.
- Background attribution pipeline connected to the session bus.
- FastAPI server with REST endpoints and WebSocket updates.
- React dashboard for sessions, output highlighting, retrieved chunks, and metadata.
- Manual event API for custom retrievers.
- Unit and integration tests for core types, server behavior, detection, attribution, and interceptors.
