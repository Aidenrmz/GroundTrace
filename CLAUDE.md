# GroundTrace Developer Guide

This file is a compact orientation guide for agents and maintainers working in the repository.

## Project Identity

The product name and Python package import are both GroundTrace / `groundtrace`, so code examples should use:

```python
import groundtrace

groundtrace.serve()
```

The dashboard, CLI alias, and user-facing prose should say GroundTrace.

## Useful Commands

```bash
python -m pytest tests/ -m "not integration"
python -m pytest tests/ -m integration
cd dashboard && npm run build
cd dashboard && npm run dev
pip install -e ".[all]"
groundtrace serve
```

## Architecture

```text
interceptors -> SessionBus -> attribution pipeline -> FastAPI API -> React dashboard
```

- `groundtrace/interceptors/`: monkey patches for LLM clients, frameworks, and vector stores.
- `groundtrace/session_bus.py`: thread-safe event store with `ContextVar` session isolation.
- `groundtrace/pipeline.py`: background attribution scheduling with bounded pending work.
- `groundtrace/detection/`: semantic similarity checks for output sentences.
- `groundtrace/attribution/`: perturbation scoring and attention rollout.
- `groundtrace/server/`: FastAPI app, REST models, WebSocket broadcasting, static dashboard serving.
- `dashboard/`: React and TypeScript UI.

## Implementation Patterns

- Optional providers are imported inside `install()` methods.
- Interceptors save original methods and restore them on uninstall.
- `bus.record_*()` calls inside interceptors are wrapped so tracing cannot break user code.
- Session selection is context-local. Do not reintroduce a single global active session ID.
- Attribution work must remain bounded; increase limits only with a clear reason.
- The detector loads sentence-transformers lazily to keep import time low.
- Dashboard API calls should remain relative paths.
- WebSocket Origin enforcement belongs in the app because CORS does not protect WebSockets.

## Known Constraints

- Server sessions are in-memory by default.
- The dashboard can cache summaries in browser storage, but it is not a durable database.
- Streaming token counts are estimates when provider metadata is unavailable.
- `httpx` interception should stay conservative about which hosts are treated as LLM APIs.
- pgvector interception buffers SQLAlchemy rows for vector queries, so avoid capturing huge result sets.
- The dashboard served by FastAPI comes from `dashboard/dist`; rebuild after frontend edits.

## Test Strategy

- Unit tests mock model and provider behavior.
- Integration tests use the real sentence-transformers model.
- Provider interceptors need tests for sync calls, async calls where applicable, extraction failure, and uninstall restoration.
- Server changes need endpoint tests plus a check for security-sensitive behavior when relevant.
- Dashboard changes should at least pass TypeScript and Vite build checks.

## Editing Guidance

- Keep user-facing wording generic and owner-neutral.
- Avoid adding personal acknowledgements or maintainer credits to docs.
- Preserve existing screenshots and video files unless the task explicitly asks to update media.
- Use GroundTrace for display names and `groundtrace` for imports.
