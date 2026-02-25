# RAG Framework v2.0

A modular Python framework for building **Retrieval-Augmented Generation** systems. Query your knowledge base, chunk PDFs, vectorize documents into Pinecone, chat with multiple LLM backends, and send results to Telegram -- all from a single Python object.

## Quick Start

```python
from rag import RAG

r = RAG()
r.query("LFI exploitation")
r.chunk("/path/to/file.pdf")
r.vectorize("/path/to/chunks")
r.chat()
r.ask("How does SQL injection work?")
```

## What's Inside

| Chapter | What You'll Learn |
|---------|-------------------|
| [Installation](getting-started/installation.md) | Install dependencies, set up API keys, configure aliases |
| [Beginner's Guide](getting-started/beginners-guide.md) | How to use an interactive Python framework (no scripting background needed) |
| [RAG Fundamentals](rag-fundamentals/what-is-rag.md) | What RAG is and how this system works end-to-end |
| [Pinecone Operations](pinecone-operations/cli-essentials.md) | Use the `pa` CLI to manage your vector database |
| [Chunking Methodology](chunking-methodology/core-principles.md) | Design chunks that actually produce good search results |
| [Telegram Integration](telegram-integration/stt-reference.md) | Send queries, files, and directories to Telegram |
| [PDF Chunker](pdf-chunker/usage.md) | Split PDFs into RAG-ready chunks with one command |

## Core Components

```
RAG()
 ├── r.query()       Search the vector database
 ├── r.chunk()       Split PDFs/text into chunks
 ├── r.vectorize()   Embed and upload chunks to Pinecone
 ├── r.ingest()      chunk + vectorize in one shot
 ├── r.chat()        Interactive chat (Gemini, GPT, Ollama)
 ├── r.ask()         Single question, get answer + sources
 ├── r.send()        Send anything to Telegram
 ├── r.fetch()       Get a specific chunk by ID
 ├── r.stats()       Pinecone index statistics
 └── r.help()        Show all available commands
```

## Architecture

```
Raw Documents (PDF, text, markdown)
        |
        v  r.chunk()
Semantic Chunks (.md with YAML frontmatter)
        |
        v  r.vectorize()
Vector Database (Pinecone, 3072D embeddings)
        |
        v  r.query() / r.ask()
Retrieved Context + LLM = Grounded Answers
        |
        v  r.send()
Telegram (results, files, reports)
```
