# GroundTrace Roadmap

GroundTrace is intended to stay narrow: local RAG tracing, grounding inspection, and attribution. The roadmap below keeps that focus while making the tool easier to use in notebooks, tests, and team debugging.

## Product Principles

- Local by default: prompts, chunks, and responses stay on the developer machine unless the user exports them.
- Low-friction tracing: existing RAG code should run with minimal or no wrapper code.
- Debugger behavior: tracing should observe user code, not become the runtime.
- Bounded overhead: background work must stay limited and should never block the main RAG path.
- Explainable output: users should be able to tell which retrieval result did or did not support an answer.

## v0.2 - Faster Inner Loop

- Live streaming visualization: show partial output while tokens stream, then replace pending states with final grounding results.
- Inline test helper: provide `assert_grounded(response, chunks, min_score=0.8)` for notebooks, scripts, and tests.
- Session comparison: compare two traces side by side to see how prompts or retriever settings changed grounding.
- Manual annotations: allow users to mark a sentence as confirmed, acceptable, or incorrectly flagged.
- Configurable threshold: expose the semantic similarity threshold at the session and server level.

## v0.3 - Persistence And CI

- SQLite-backed session storage for users who want traces to survive process restarts.
- Self-contained HTML export for sharing one trace without running a server.
- pytest integration that can fail tests when grounding falls below a configured threshold.
- Baseline comparison command for CI pipelines.
- Optional project labels so traces from several local apps can be separated.

## v1.0 - Stable Debugging Surface

- MCP server so editor and agent tools can inspect active traces.
- Plugin entry points for third-party interceptors and attribution methods.
- Token-level attribution for local models where attention data is available.
- Dashboard views for multi-turn conversation trees.
- Better offline model management for air-gapped development environments.
- Hardened shared-dashboard mode for teams that choose to run behind their own network controls.

## Out Of Scope

- Hosted SaaS tracing.
- Prompt management platforms.
- Fine-tuning pipelines.
- Dataset labeling products.
- General LLM evaluation suites.
- Production traffic monitoring without explicit user deployment hardening.
