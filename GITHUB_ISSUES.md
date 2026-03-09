# GroundTrace Issue Backlog

This backlog is written as implementation-ready issue material. It avoids owner-specific references and personal credits.

## Issue 1: Configurable Grounding Threshold

### Problem

The semantic similarity threshold is currently fixed in the detection path. Different domains need different strictness levels.

### Proposal

Add a threshold argument to `serve()` and `new_session()`, store it on the session, and pass it into `HallucinationDetector`.

### Acceptance Criteria

- `groundtrace.serve(hallucination_threshold=0.45)` configures new sessions.
- `groundtrace.new_session(hallucination_threshold=0.5)` overrides the default.
- The dashboard shows the threshold used for each attribution result.
- Tests cover default and custom thresholds.

## Issue 2: Self-Contained Session Export

### Problem

Users need to share a trace without keeping the local server running.

### Proposal

Add an export command that writes one HTML file containing session data and the static dashboard bundle.

### Acceptance Criteria

- `groundtrace export <session-id> --output trace.html` creates a standalone file.
- The file opens without a server.
- Large sessions are size-checked and produce a clear error.
- Exported content includes product version, timestamp, and threshold metadata.

## Issue 3: LiteLLM Interceptor

### Problem

Many applications use LiteLLM as a provider abstraction. Capturing that layer can cover many backends with one integration.

### Proposal

Patch `litellm.completion()` and `litellm.acompletion()` when LiteLLM is installed.

### Acceptance Criteria

- Sync and async calls record request and response events.
- Streaming is either captured or explicitly documented as unsupported.
- Provider and model metadata are extracted when available.
- Tests use mocked LiteLLM functions.

## Issue 4: Live Streaming Dashboard State

### Problem

Streaming responses are reconstructed after completion, but users benefit from seeing partial output while it arrives.

### Proposal

Emit partial response events and render pending analysis states in the output panel.

### Acceptance Criteria

- Partial tokens appear in the selected live session.
- Final attribution replaces pending states.
- UI handles stream interruption gracefully.
- WebSocket payloads remain bounded.

## Issue 5: Prompt And Retriever Comparison

### Problem

Users often change one prompt or retriever setting and need to know whether grounding improved.

### Proposal

Add a two-session comparison view that shows grounding delta, hallucination count delta, chunk overlap, and output differences.

### Acceptance Criteria

- Users can select two sessions from history.
- The view shows clear metrics and sentence-level changes.
- The comparison API returns normalized data for the dashboard.
- Tests cover missing sessions and mismatched session shapes.

## Issue 6: Manual Annotation Layer

### Problem

Semantic similarity can misclassify some sentences. Users need a way to mark those cases.

### Proposal

Allow dashboard annotations on output spans and persist them locally.

### Acceptance Criteria

- Users can mark a sentence as confirmed hallucination, acceptable, or unsure.
- Annotations persist across page reloads.
- Export includes annotations.
- Annotation state does not mutate raw attribution results.

## Issue 7: pytest Assertion Helper

### Problem

RAG quality regressions should be catchable in tests without running the dashboard.

### Proposal

Add `assert_grounded(response, chunks, min_score=0.8)` and improve the existing pytest plugin around it.

### Acceptance Criteria

- Helper works without starting FastAPI.
- Assertion failure lists weakly grounded sentences.
- pytest marker can enforce a minimum score.
- Tests cover pass, fail, timeout, and no-chunk cases.

## Issue 8: SQLite Persistence

### Problem

In-memory sessions disappear on restart and browser cache is not a durable store.

### Proposal

Add optional SQLite persistence behind a `persist` argument.

### Acceptance Criteria

- `groundtrace.serve(persist="./groundtrace.db")` stores sessions.
- Session list merges live and persisted sessions.
- Retention cleanup is configurable.
- Sensitive-data warning appears in docs.

## Issue 9: MCP Server

### Problem

Editor agents and local tools should be able to query active traces without scraping the dashboard.

### Proposal

Expose sessions, hallucinations, and grounding metrics through a Model Context Protocol server.

### Acceptance Criteria

- `python -m groundtrace.mcp_server` starts the server.
- Tools include list sessions, get session, list weakly grounded sentences, and summarize grounding.
- Tests cover tool schemas and sample responses.

## Issue 10: Plugin Entry Points

### Problem

Third-party integrations should not require edits to the core interceptor registry.

### Proposal

Load interceptor classes from package entry points and include them in `install_all()`.

### Acceptance Criteria

- Entry point group is documented.
- Failed plugin imports are logged without breaking install.
- Built-in interceptors keep deterministic order.
- Tests cover duplicate names and failing plugins.

## Issue 11: Better Large Payload Handling

### Problem

Very large prompts, chunks, and outputs can increase memory pressure.

### Proposal

Introduce truncation metadata and explicit display caps while preserving enough text for useful debugging.

### Acceptance Criteria

- Captured fields have configurable size limits.
- Dashboard marks truncated values.
- Attribution receives bounded strings.
- Tests cover boundary sizes.

## Issue 12: Dashboard Accessibility Pass

### Problem

The debugging UI needs better keyboard and screen-reader behavior.

### Proposal

Add semantic buttons, labels, focus states, and keyboard navigation for session and sentence selection.

### Acceptance Criteria

- Main controls are keyboard reachable.
- Selected session and selected sentence state are announced.
- Color is not the only signal for hallucination state.
- TypeScript build passes.
