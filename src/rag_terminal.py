#!/usr/bin/env python3
"""
RAG Terminal Chat with LangChain + Pinecone + Gemini.

Interactive terminal interface for querying the CTF/cybersecurity knowledge base.

Usage:
    python3 rag_terminal.py

Environment files (loaded from /root/.openskills/env/):
    - openai.env: OPENAI_API_KEY (for embeddings)
    - gemini.env: GOOGLE_API_KEY (for LLM)
    - pinecone.env: PINECONE_API_KEY (for vector store)

Stack:
    - Embeddings: text-embedding-3-large (3072 dims) via OpenAI
    - LLM: gemini-2.5-flash via Google
    - Vector Store: Pinecone (rag-canonical-v1-emb3large)
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

OPENAI_ENV_PATH = "/root/.openskills/env/openai.env"
GEMINI_ENV_PATH = "/root/.openskills/env/gemini.env"
PINECONE_ENV_PATH = "/root/.openskills/env/pinecone.env"

load_dotenv(OPENAI_ENV_PATH)
load_dotenv(GEMINI_ENV_PATH)
load_dotenv(PINECONE_ENV_PATH)

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMS = 3072
LLM_MODEL = "gemini-2.5-flash"
PINECONE_INDEX_NAME = "rag-canonical-v1-emb3large"
RETRIEVER_K = 4


def load_environment():
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    pinecone_key = os.getenv("PINECONE_API_KEY")

    if not all([openai_key, google_key, pinecone_key]):
        missing = [
            k
            for k, v in {
                "OPENAI_API_KEY": openai_key,
                "GOOGLE_API_KEY": google_key,
                "PINECONE_API_KEY": pinecone_key,
            }.items()
            if not v
        ]
        raise EnvironmentError(f"Faltan variables de entorno: {', '.join(missing)}")

    return openai_key, google_key, pinecone_key


def initialize_components():
    openai_key, google_key, pinecone_key = load_environment()

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMS, openai_api_key=openai_key
    )

    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=google_key)

    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index(PINECONE_INDEX_NAME)

    vectorstore = PineconeVectorStore(
        index=index, embedding=embeddings, text_key="content"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})

    return llm, retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(llm, retriever):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un asistente experto en CTF y ciberseguridad. 
Responde la pregunta usando ÚNICAMENTE el contexto proporcionado.
Si no tienes información suficiente, dilo claramente.

Contexto:
{context}""",
            ),
            ("human", "{input}"),
        ]
    )

    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def format_sources(documents):
    sources = []
    for i, doc in enumerate(documents, 1):
        source = (
            doc.metadata.get("source")
            or doc.metadata.get("chunk_id")
            or doc.metadata.get("domain")
            or "Desconocido"
        )
        sources.append(f"  [{i}] {source}")
    return "\n".join(sources)


def main():
    print("Inicializando sistema RAG...")
    llm, retriever = initialize_components()
    chain, retriever = build_chain(llm, retriever)
    print(
        f"Listo. Índice: {PINECONE_INDEX_NAME} | Recuperando top-{RETRIEVER_K} documentos.\n"
    )
    print("Escribe 'exit' o 'quit' para salir.\n")

    while True:
        try:
            query = input("\n[Pregunta]: ").strip()

            if query.lower() in ["exit", "quit", "salir"]:
                print("Saliendo...")
                break

            if not query:
                continue

            docs = retriever.invoke(query)
            response = chain.invoke(query)

            print(f"\n[Respuesta]:\n{response}")

            print("\n[FUENTES]:")
            print(format_sources(docs))

        except KeyboardInterrupt:
            print("\n\nInterrumpido. Saliendo...")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")


if __name__ == "__main__":
    main()
