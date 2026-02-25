# RAG Framework v2.0

A modular Python framework for **Retrieval-Augmented Generation**. Chunk documents, vectorize them into Pinecone, search with semantic queries, chat with multiple LLM backends, and deliver results to Telegram -- all from a single Python object or CLI aliases.

## Quick Start

```bash
git clone https://github.com/your-username/RAG.git
cd RAG
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Set up your API keys:

```bash
mkdir -p .env
echo "PINECONE_API_KEY=your_key" > .env/pinecone.env
echo "OPENAI_API_KEY=your_key"   > .env/openai.env
```

Then use it:

```python
from rag import RAG
r = RAG()

r.query("LFI exploitation")                    # search
r.chunk("/path/to/file.pdf")                   # chunk a PDF
r.vectorize("/path/to/chunks")                 # upload to Pinecone
r.vectorize("notes.md", domain="web", tags=["exploit"])  # with metadata
r.ingest("/path/to/file.pdf")                  # chunk + vectorize
r.ask("How does SQL injection work?")          # AI-powered answer
r.chat()                                       # interactive chat
r.send(results)                                # send to Telegram
```

## Features

- **7 modular components** -- query, vectorize, chunk, chat, telegram, registry, config
- **3 chat backends** -- Gemini, GPT-4o-mini, Ollama
- **Granular namespace control** -- target specific namespaces at instance or method level
- **Metadata injection** -- add domain, tags, and custom fields to plain markdown at vectorize time
- **PDF chunking** -- RecursiveCharacterTextSplitter with configurable size/overlap
- **Plain markdown support** -- files with or without YAML frontmatter
- **Telegram integration** -- send messages, files, directories, and query results
- **CLI aliases** -- `query`, `vectorize`, `pa`, `stt`, `rag-query`, `GeminiRag`

## Architecture

```
RAG()
 |-- r.query("text")              Search Pinecone (semantic)
 |-- r.query("text", namespace="cve")   Search specific namespace
 |-- r.fetch("chunk_id")          Get specific chunk
 |-- r.chunk("/path.pdf")         Split PDF into chunks
 |-- r.vectorize("/path")         Embed + upload to Pinecone
 |-- r.ingest("/path.pdf")        Chunk + vectorize in one shot
 |-- r.chat()                     Interactive chat (Gemini/GPT/Ollama)
 |-- r.ask("question")            Single Q&A with sources
 |-- r.send("message")            Send to Telegram
 |-- r.stats()                    Index statistics
 |-- r.sync()                     Sync chunk registry
 '-- r.help()                     Show all commands
```

## Namespace Support

Control which namespace to query, vectorize, or chat against:

```python
# Instance level (affects all operations)
r = RAG(namespace="cve")

# Method level (one-off override)
r.query("buffer overflow", namespace="ctf")
r.vectorize("/chunks", namespace="tools")
r.ask("What is XSS?", namespace="technique")
```

Presets: `root`, `cve`, `technique`, `ctf`, `tools`, `payloads`

## CLI Aliases

After running `bash setup_aliases.sh`:

```bash
query "LFI exploitation"                    # quick search
query "RCE" --namespace cve                 # search specific namespace
vectorize /path/to/chunks                   # vectorize
vectorize notes.md --domain web --tags exploit,lfi  # with metadata
pa "search text"                            # Pinecone Assistant CLI
GeminiRag                                   # interactive Gemini chat
rag-query "text" --top-k 10                 # search + save + Telegram
rag-send "message"                          # send to Telegram
stt rag "query"                             # STT: search + send
stt file /path/to/file                      # STT: send file
stt directory /path/to/dir                  # STT: zip + send dir
```

## Project Structure

```
RAG/
 |-- rag/                     Framework package
 |    |-- core.py             RAG() orchestrator
 |    |-- query.py            QueryEngine (Pinecone search)
 |    |-- vectorizer.py       Vectorizer (embed + upsert)
 |    |-- chunker.py          Chunker (PDF/text splitting)
 |    |-- chat.py             Chat (Gemini/GPT/Ollama)
 |    |-- telegram.py         Telegram integration
 |    '-- registry.py         Chunk registry manager
 |-- src/                     CLI script wrappers
 |-- config.py                Centralized configuration
 |-- .env/                    API keys (not committed)
 |-- chunks/                  Generated chunks
 |-- chunk_registry.json      Chunk tracking
 |-- requirements.txt         Python dependencies
 |-- setup_aliases.sh         Shell alias installer
 '-- mkdocs/                  Documentation (MkDocs)
```

## Documentation

Full documentation available in `mkdocs/`:

- [Installation](mkdocs/docs/getting-started/installation.md)
- [Beginner's Guide](mkdocs/docs/getting-started/beginners-guide.md)
- [What is RAG?](mkdocs/docs/rag-fundamentals/what-is-rag.md)
- [Chunking Methodology](mkdocs/docs/chunking-methodology/core-principles.md)
- [Pinecone CLI](mkdocs/docs/pinecone-operations/cli-essentials.md)
- [Telegram Integration](mkdocs/docs/telegram-integration/stt-reference.md)
- [PDF Chunker](mkdocs/docs/pdf-chunker/usage.md)

Build the docs locally:

```bash
pip install mkdocs-material
cd mkdocs && mkdocs serve
```

## Requirements

- Python 3.10+
- Pinecone account (free tier works)
- OpenAI API key
- Optional: Google Gemini API key, Telegram bot token

## License

MIT
