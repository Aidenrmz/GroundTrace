# GroundTrace Context

## Snapshot

GroundTrace is a Python package and local dashboard for tracing RAG pipelines. The package import remains `groundtrace`; the display name is GroundTrace.

## Main Capabilities

- Starts a FastAPI server on localhost.
- Installs optional interceptors for supported LLM SDKs, LangChain, and vector stores.
- Records events in an in-process session bus.
- Runs sentence-level grounding checks in a background attribution pipeline.
- Streams session updates to a React dashboard.
- Keeps recent session data in memory, with browser-side caching for dashboard history.

## Important Paths

```text
groundtrace/__init__.py        public API and server lifecycle
groundtrace/cli.py             console commands
groundtrace/session_bus.py     sessions, event recording, subscriptions
groundtrace/pipeline.py        automatic attribution orchestration
groundtrace/types.py           shared dataclasses
groundtrace/interceptors/      provider and vector store capture
groundtrace/server/            FastAPI app and REST API
dashboard/src/                React dashboard
tests/                        pytest coverage
docs/                         screenshots and demo media
```

## Runtime Flow

1. User calls `groundtrace.serve()` or `groundtrace serve`.
2. Interceptors install for libraries that are present.
3. RAG code runs as usual.
4. Retrieval calls create `VectorQueryEvent` records.
5. LLM calls create request and response records.
6. The attribution pipeline matches responses to retrieved chunks.
7. The server exposes sessions over REST and WebSocket.
8. The dashboard renders output, chunks, and grounding metadata.

## Testing

Fast suite:

```bash
python -m pytest tests/ -m "not integration"
```

Integration suite:

```bash
python -m pytest tests/ -m integration
```

Dashboard:

```bash
cd dashboard
npm run build
```

## Branding Rule

Use GroundTrace in docs, dashboard labels, CLI descriptions, and server metadata. Use `groundtrace` only where the actual Python package, import path, entry point group, or file path requires it.

## Security Assumptions

- Localhost is the default deployment boundary.
- WebSocket origin checks are required.
- Captured prompts and chunks may be sensitive.
- Session memory and browser cache should be treated as private debugging data.
- Do not widen CORS or bind to public interfaces without adding explicit security controls.
