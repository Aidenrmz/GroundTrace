# GroundTrace Promotion Notes

This document keeps launch copy and positioning snippets in one place. It is intentionally owner-neutral and avoids personal credits.

## One-Line Positioning

GroundTrace is a local dashboard that shows how retrieved chunks support, fail to support, or appear to influence RAG answers.

## Short Description

GroundTrace helps Python developers debug RAG hallucinations without moving prompts or documents into a hosted observability product. Add `groundtrace.serve()` before your existing pipeline, run a query, and inspect a local dashboard with retrieved chunks, highlighted output, grounding scores, and attribution.

## Longer Description

When a RAG answer is wrong, ordinary logs show the question, the retrieved context, and the final text. They usually do not show which chunk supported which sentence or whether a sentence had any retrieved support at all. GroundTrace fills that debugging gap locally. It captures retrieval and generation events from popular Python stacks, runs sentence-level grounding checks in the background, and presents the result in a lightweight dashboard.

## Audience

- Python developers building RAG prototypes.
- Teams debugging customer-support, search, documentation, and agent workflows.
- Engineers who want local trace visibility without a hosted account.
- Test authors who want grounding checks to become part of regression workflows.

## Key Messages

- Local-first RAG trace inspection.
- Minimal application changes.
- Works with common LLM SDKs and vector databases.
- Shows the relationship between answer sentences and retrieved chunks.
- Useful before buying or building a larger observability stack.

## Social Snippets

### Short

RAG logs tell you what happened. GroundTrace helps show why. Start a local dashboard, run your pipeline, and inspect which retrieved chunks support each answer sentence.

### Developer-Focused

```python
import groundtrace
groundtrace.serve()
```

Run the same RAG code. GroundTrace captures retrieval + LLM events and opens a local dashboard for grounding and attribution.

### Debugging-Focused

When a model invents a detail, GroundTrace helps separate retrieval misses from generation drift by mapping answer sentences back to the retrieved chunks.

## Launch Checklist

- README uses GroundTrace branding.
- Screenshots and demo media remain available under `docs/`.
- Python quick start uses the `groundtrace` import.
- Dashboard title and welcome text say GroundTrace.
- No owner-specific GitHub URLs remain in docs.
- Fast tests and dashboard build pass.
- Security notes clearly state localhost-only assumptions.

## Outreach Angles

- "A local first look at RAG hallucinations."
- "Trace the context-to-answer relationship."
- "Debug retrieval and generation together."
- "Small dashboard before large observability."

## Avoid

- Claims that all hallucinations are detected.
- Claims of token-level accuracy where the current default is sentence-level.
- Production monitoring promises without deployment hardening.
- Personal or company attribution in general-purpose project docs.
