"""
Example 2: Anthropic + FAISS
----------------------------
Uses Anthropic for generation and FAISS for local vector search.

Install:
    pip install "groundtrace[anthropic]" faiss-cpu sentence-transformers numpy

Run:
    ANTHROPIC_API_KEY=sk-ant-... python examples/anthropic_faiss.py
"""

import os

import anthropic
import faiss
from sentence_transformers import SentenceTransformer

import groundtrace

groundtrace.serve()

documents = [
    "Python first appeared publicly in 1991 and is now widely used.",
    "Python 3.0 was released in 2008 and is not backwards compatible with Python 2.",
    "Python is known for readable syntax that uses indentation to define code blocks.",
    "The Python Software Foundation manages Python's development and intellectual property.",
    "NumPy, Pandas, and PyTorch are popular Python libraries for data science and ML.",
]

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(documents).astype("float32")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

query = "When did Python first appear publicly?"
query_vec = embed_model.encode([query]).astype("float32")
_distances, indices = index.search(query_vec, k=3)
context = "\n".join(documents[i] for i in indices[0])

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
message = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": f"Answer using only this context:\n{context}\n\nQuestion: {query}",
        }
    ],
)

print(message.content[0].text)
print("\nOpen http://127.0.0.1:7756 to inspect the trace.")
input("\nPress Enter to exit...")
