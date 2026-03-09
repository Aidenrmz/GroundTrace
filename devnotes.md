# Development Notes

These notes collect engineering details that are easy to forget while changing GroundTrace.

## Compatibility

The import path remains `groundtrace`. Do not rename the package directory casually; that would break examples, tests, and existing users. Rebranding should happen through display strings, docs, server metadata, and the `groundtrace` CLI alias.

## Server Lifecycle

`groundtrace.serve()` starts Uvicorn on a daemon thread. Keep lifecycle state protected by `_server_lock`. `get_session_url()` should use the host and port from the running server instead of assuming the default port.

## Session Isolation

`SessionBus` uses context-local active session tracking. This matters for concurrent async tasks and threaded apps. Avoid replacing it with a process-wide active session variable.

## Interceptors

- Import optional SDKs inside `install()`.
- Store originals before patching.
- Make `install()` and `uninstall()` idempotent.
- Catch errors around event recording.
- Preserve return values and streaming behavior.
- Add tests for extraction helpers and uninstall restoration.

## Attribution Pipeline

The pipeline runs outside the user's request path. Queue size and worker count are intentional limits. If a change increases work per response, document the cost and add tests for backpressure behavior.

## Detection

Sentence-transformers is lazy-loaded. Keep import-time overhead low. If adding a new detector, preserve the public detector interface or introduce a compatibility shim.

## Dashboard

The FastAPI server serves `dashboard/dist` when present. The Vite dev server is only for local frontend development. Any frontend change should pass:

```bash
cd dashboard
npm run build
```

## Documentation

Docs should be written in current GroundTrace wording and should not include personal credits or owner-specific repository URLs. Keep screenshots and videos under `docs/` unless the user asks for new media.

## Release Checks

```bash
python -m pytest tests/ -m "not integration"
python -m pytest tests/ -m integration
cd dashboard && npm run build
```

Run integration tests when touching detection, attribution, model loading, or interceptors. Fast tests are enough for pure documentation or copy-only dashboard changes.
