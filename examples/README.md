# GroundTrace Examples

This folder contains small RAG scripts that start the GroundTrace dashboard and then run a representative retrieval + generation flow.

| File | Stack | Purpose |
| --- | --- | --- |
| `openai_chromadb.py` | OpenAI + ChromaDB | Basic cloud LLM and local vector collection |
| `anthropic_faiss.py` | Anthropic + FAISS | Privacy-oriented local search with an API LLM |
| `langchain_rag.py` | LangChain + ChromaDB | Framework-level tracing through LangChain abstractions |

## Run One

```bash
OPENAI_API_KEY=sk-... python examples/openai_chromadb.py
```

Each example:

1. Starts the dashboard at `http://127.0.0.1:7756`.
2. Executes a real retrieval step.
3. Sends the retrieved context to an LLM.
4. Leaves the process alive long enough to inspect the trace in the browser.

The code imports `groundtrace` because that remains the package name. The dashboard and documentation refer to the product as GroundTrace.
