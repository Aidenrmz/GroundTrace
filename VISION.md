# GroundTrace Vision

GroundTrace should make RAG debugging concrete. A developer should be able to run a query, open a local page, and understand whether an answer is supported by retrieved context.

## Target Experience

```python
import groundtrace

groundtrace.serve()
```

Then the existing RAG pipeline runs normally. GroundTrace observes retrieval and generation, records a session, and shows:

- the query,
- the retrieved chunks,
- the generated answer,
- weakly grounded sentences,
- chunk attribution weights,
- useful metadata such as latency and token counts.

## Non-Negotiables

### Local-First

Trace data should stay on the user's machine by default. Hosted workflows are not the core product.

### Low Friction

The tool should work with existing Python stacks. Manual events are available for custom systems, but common frameworks and stores should be automatic.

### Debugger Semantics

GroundTrace observes and explains. It should not become the application framework or require users to restructure their RAG code.

### Bounded Runtime Cost

Attribution runs in the background and stays capped. Slow or failed tracing must not break the host application.

### Honest Grounding

The dashboard should make uncertainty visible. Grounding scores are signals, not proof of factual correctness.

## Core Use Cases

- Find unsupported claims in a generated answer.
- See whether the retriever returned evidence that the model ignored.
- Compare prompt or retriever changes across sessions.
- Capture debugging evidence for a bug report.
- Turn grounding behavior into tests.

## Product Boundaries

GroundTrace is not a prompt registry, red-team platform, vector database, model router, or fine-tuning system. Integrations should help trace RAG behavior, not expand the product into a full LLMOps suite.

## Road To 1.0

1. Make tracing reliable across common providers and stores.
2. Make the dashboard fast and clear for live debugging.
3. Add persistence and export for collaboration.
4. Add test and CI surfaces for regression prevention.
5. Stabilize extension points for custom interceptors and attribution methods.

## Success Criteria

- Setup stays under a few lines for common stacks.
- Traces explain retrieval-to-answer relationships without reading raw logs.
- The dashboard remains useful with no cloud dependency.
- False positives and limitations are documented clearly.
- Users can adopt the tool temporarily during debugging without committing to a platform.
