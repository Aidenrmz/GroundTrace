# Blog Draft: GroundTrace

## Stop Guessing Why RAG Answers Drift

RAG systems fail in a frustrating way: the answer looks confident, the retrieved context looks plausible, and the logs rarely explain how one became the other. A model may ignore the best chunk, over-trust a weak one, or invent a detail that was never retrieved.

GroundTrace is a local debugging dashboard for that gap.

```python
import groundtrace

groundtrace.serve()
```

Run the same RAG pipeline you already have. GroundTrace captures retrieval events and LLM responses, then shows a trace in your browser. The dashboard highlights weakly grounded sentences and ranks the chunks that best explain each part of the answer.

## Why This Matters

Most RAG debugging starts with three disconnected artifacts:

- the user question,
- the retrieved chunks,
- the generated answer.

The missing artifact is the relationship between them. GroundTrace adds that relationship without asking you to move your data into another platform.

## A Small Example

Imagine a support assistant gets this question:

> Can I run the dashboard in Kubernetes?

The retriever returns documentation about local development, Docker images, and dashboard ports. The model answers with a confident claim about a built-in Kubernetes controller. That controller does not exist.

GroundTrace shows the sentence as weakly grounded. The relevant chunks have low similarity, and none of them mention a controller. Now the fix is concrete: update the answer prompt, improve retrieval, or add documentation that states the real deployment boundary.

## What The Dashboard Shows

- live sessions,
- retrieved chunks with original scores,
- generated output split into sentences,
- grounding score,
- chunk attribution weights,
- latency, token, and cost metadata when available.

The view is intentionally small. It is a debugger, not an evaluation platform.

## Local-First By Design

The server binds to localhost by default. Session data is held in process memory and dashboard cache. No hosted account is required, and prompts are not sent to a GroundTrace service.

## Supported Stacks

GroundTrace can observe common Python RAG stacks:

- OpenAI, Anthropic, Gemini, and other `httpx`-based API clients,
- HuggingFace Transformers for local generation,
- LangChain retrievers and chat models,
- ChromaDB, Pinecone, FAISS, Weaviate, and pgvector,
- custom retrievers through a manual event API.

## Try It

```bash
pip install groundtrace
groundtrace serve
```

Or start it from Python:

```python
import groundtrace

groundtrace.serve()
```

The package import, command, product, and dashboard now use GroundTrace naming.
