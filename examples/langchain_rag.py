"""
Example 3: LangChain LCEL RAG Pipeline
--------------------------------------
GroundTrace observes the retriever and LLM calls inside a LangChain pipeline
without adding LangChain-specific code to the application path.

Install:
    pip install "groundtrace[openai]" langchain langchain-openai langchain-community chromadb

Run:
    OPENAI_API_KEY=sk-... python examples/langchain_rag.py
"""

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import groundtrace

groundtrace.serve()

docs = [
    Document(page_content="Quantum computing uses qubits instead of classical bits. Qubits can exist in superposition."),
    Document(page_content="Shor's algorithm can factor large integers exponentially faster than classical computers."),
    Document(page_content="Quantum entanglement allows qubits to be correlated regardless of physical distance."),
    Document(page_content="IBM, Google, and IonQ are leading companies in quantum hardware development."),
    Document(page_content="Quantum error correction is a major challenge; current qubits are noisy and prone to errors."),
]

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template(
    "Answer based only on this context:\n{context}\n\nQuestion: {question}"
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question = "What makes quantum computers faster than classical ones?"
answer = chain.invoke(question)

print(answer)
print("\nOpen http://127.0.0.1:7756 to inspect the trace.")
input("\nPress Enter to exit...")
