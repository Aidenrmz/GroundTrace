# Newsletter Pitches

## Pitch 1

GroundTrace is a local RAG debugging dashboard for Python. Add `groundtrace.serve()`, run your existing pipeline, and inspect which retrieved chunks support each generated sentence. It captures common LLM clients and vector databases, highlights weakly grounded output, and keeps trace data on your machine.

## Pitch 2

RAG failures are easier to fix when you can see the path from retrieval to answer. GroundTrace records vector search results and LLM responses, then displays grounding and attribution in a localhost dashboard. It works with popular Python stacks and does not require a hosted account.

## Pitch 3

Most RAG logs stop at "these chunks were retrieved" and "this answer was generated." GroundTrace adds the missing link: sentence-level grounding against the retrieved context. It is built for local development, quick experiments, and regression debugging.

## Pitch 4

If a RAG answer invents a detail, is the retriever missing evidence or did the model ignore it? GroundTrace helps answer that question by mapping generated sentences back to retrieved chunks. Start it with `groundtrace serve` or `groundtrace.serve()`.

## Pitch 5

GroundTrace is a small local tool for inspecting RAG hallucinations. It supports common LLM APIs, LangChain, and vector stores such as ChromaDB, Pinecone, FAISS, Weaviate, and pgvector.
