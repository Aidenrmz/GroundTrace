# Contributing To GroundTrace

GroundTrace is a local RAG tracing tool. Contributions are most useful when they preserve the core contract: the user's RAG code keeps running, tracing stays local, and attribution work remains bounded.

## Development Setup

```bash
git clone <repository-url>
cd <repository>
pip install -e ".[all]"
```

Install dashboard dependencies:

```bash
cd dashboard
npm install
```

Run fast Python tests:

```bash
python -m pytest tests/ -m "not integration"
```

Run model-backed integration tests:

```bash
python -m pytest tests/ -m integration
```

Build the dashboard:

```bash
cd dashboard
npm run build
```

## Repository Map

```text
groundtrace/                  Python package
  __init__.py                serve(), stop(), new_session(), URL helpers
  session_bus.py             in-process event storage and subscriptions
  pipeline.py                background attribution orchestration
  types.py                   shared dataclasses
  interceptors/              provider, framework, and vector DB patches
  detection/                 grounding detection
  attribution/               perturbation and attention attribution
  server/                    FastAPI app and API models
dashboard/                   React dashboard
examples/                    runnable RAG examples
tests/                       unit and integration coverage
docs/                        screenshots and demo media
```

## Design Rules

- Interceptors must fail closed: never let tracing errors bubble into user code.
- Avoid global mutable state unless it is guarded and session-aware.
- Keep imports lazy for optional integrations.
- Prefer small, provider-specific extraction helpers over fragile string parsing.
- Keep request and session size limits in mind when storing raw text.
- Dashboard code should use relative API paths so it works behind the local FastAPI server.
- User-facing copy should say GroundTrace; Python imports should use `groundtrace`.

## Adding An LLM Interceptor

1. Check whether the provider already uses `httpx`; the transport interceptor may already capture it.
2. Add a module under `groundtrace/interceptors/` only when SDK-level handling is still needed.
3. Inherit from `BaseInterceptor`.
4. Store original methods during `install()`.
5. Restore originals during `uninstall()`.
6. Wrap calls with `try/except` around all `bus.record_*()` calls.
7. Extract model, messages, output text, token counts, latency, and cost when available.
8. Register the interceptor in `groundtrace/interceptors/__init__.py`.
9. Add tests with mocked provider objects.

Minimal shape:

```python
class ProviderInterceptor(BaseInterceptor):
    def install(self) -> None:
        if self._installed:
            return
        try:
            import provider
        except ImportError:
            return
        self._original = provider.Client.create
        provider.Client.create = self._wrap_create(self._original)
        self._installed = True

    def uninstall(self) -> None:
        if not self._installed:
            return
        provider.Client.create = self._original
        self._installed = False
```

## Adding A Vector Store

Patch the method that performs retrieval, then publish a `VectorQueryEvent` with:

- `db_type`
- collection/index name when available
- query text or embedding
- top-k value
- `RetrievedChunk` entries with IDs, text, scores, and metadata

Do not mutate the provider's return shape. If buffering is required, wrap the result so callers can still consume it normally.

## Detection And Attribution Changes

`HallucinationDetector.detect()` is the stable detection entry point. Changes should preserve its return shape: a list of `OutputToken` objects with hallucination flags and chunk attribution weights.

Perturbation code may call LLM providers again, so keep sample counts bounded and make cost visible in docs or UI when a feature triggers extra calls.

## Dashboard Changes

- Run `npm run build` before release packaging.
- Keep colors and spacing restrained; this is a debugging dashboard, not a landing page.
- Do not add explanatory marketing panels inside the app.
- Preserve responsive behavior for the sidebar, output panel, and chunks panel.
- Avoid text overflow in compact controls.

## Pull Request Checklist

- Tests added or updated for changed behavior.
- Fast tests pass.
- Integration tests run when detection, attribution, or provider capture changes.
- Dashboard builds when frontend code changes.
- New docs use GroundTrace branding.
- No personal credits, maintainer names, or owner-specific repository links are introduced.
- Legal notices and third-party license metadata are not removed casually.

## Release Checklist

```bash
python -m pytest tests/ -m "not integration"
python -m pytest tests/ -m integration
cd dashboard && npm run build
```

Then build the Python distribution with the project's packaging tool and inspect the wheel contents before publishing.
