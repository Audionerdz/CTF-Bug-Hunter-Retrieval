# ⚡ Atlas Engine

> **The most ruthless Retrieval-Augmented Generation framework ever built.** Purpose-engineered for offensive security, CTF hunters, threat researchers, and teams that refuse to compromise on intelligence speed or accuracy.

Atlas Engine is a **production-grade RAG system** that turns chaotic knowledge into structured, searchable intelligence. Feed it PDFs, markdown, exploits, techniques, payloads—Atlas atomizes it into vectors, learns the structure, and returns answers faster than your competition.

---

## What Makes Atlas Different

### 🎯 **Built for Offense, Not Toys**

- **Semantic search** that actually understands exploit chains, CVE contexts, and attack procedures
- **Multi-namespace isolation** so your CTF notes don't pollute your threat intelligence
- **Metadata injection** at vectorize time—tag exploits, techniques, payloads without touching source files
- **Sub-second query latency** powered by Pinecone's vector infrastructure
- **No hallucinations on your team's knowledge**—sources are always cited, always traceable

### 🔥 **Everything Out of the Box**

| Feature | Details |
|---------|---------|
| **7 Modular Components** | Query, Vectorize, Chunk, Chat, Telegram, Registry, Config—use individually or together |
| **3 LLM Backends** | Gemini (free tier), GPT-4o-mini (cheap), Ollama (offline) |
| **Granular Namespaces** | Separate your knowledge: `root`, `cve`, `technique`, `ctf`, `tools`, `payloads` |
| **Live Metadata Injection** | Add domain, tags, custom fields at vectorize time—no frontmatter needed |
| **PDF Intelligence** | RecursiveCharacterTextSplitter with configurable chunk boundaries |
| **Plain Markdown** | Works with raw `.md` files OR YAML-annotated ones |
| **Telegram Bridge** | Query Atlas from Telegram, push results to your team |
| **CLI Aliases** | 9 battle-tested command wrappers ready to go |

---

## Installation (90 Seconds)

```bash
git clone https://github.com/yourusername/atlas-engine.git
cd atlas-engine
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**Configure your weapons:**

```bash
mkdir -p .env
echo "PINECONE_API_KEY=your_pinecone_key"     > .env/pinecone.env
echo "OPENAI_API_KEY=your_openai_key"         > .env/openai.env
echo "GOOGLE_API_KEY=your_gemini_key"         > .env/google.env
echo "GROQ_API_KEY=your_groq_key"             > .env/groq.env
echo "TELEGRAM_BOT_TOKEN=your_bot_token"      > .env/telegram.env
```

---

## Docker (Recommended for CI/CD)

Build locally:

```bash
docker build -t atlas-engine:local .
```

Run interactive chat (uses your local `.env/` and persists `chat_history/`):

```bash
docker compose up --build
```

Run one-off smoke command inside container:

```bash
docker run --rm atlas-engine:local -c "from atlas_engine import Atlas; Atlas(); print('ok')"
```

Notes:
- The image includes `default/`, `src/`, `atlas_engine/`, and `config.py`.
- API keys are injected at runtime via mounted `.env/` files.

---

## Atlas in Action

### Python API (The Power User Way)

```python
from atlas_engine import Atlas

# Initialize
atlas = Atlas()

# 🔍 Search your knowledge base
results = atlas.query("SQL injection in stored procedures")
for chunk in results:
    print(f"[{chunk['domain']}] {chunk['title']}")
    print(chunk['content'][:200])

# 📄 Chunk a PDF (automatic intelligence extraction)
atlas.chunk("/path/to/exploit_guide.pdf", domain="exploit")

# 📤 Vectorize chunks into Pinecone
atlas.vectorize(
    "/path/to/chunks",
    domain="technique",
    tags=["authentication-bypass", "windows"],
    namespace="cve"
)

# 🧠 One-shot: chunk + vectorize (fastest pipeline)
atlas.ingest(
    "/path/to/notes.md",
    domain="ctf",
    tags=["web", "insecure-deserialization"]
)

# 🤖 Ask with sources (AI reasoning over your knowledge)
answer = atlas.ask("How do I exploit XXE vulnerabilities in SOAP APIs?")
print(answer['reasoning'])
for source in answer['sources']:
    print(f"Source: {source['path']} (confidence: {source['score']})")

# 💬 Interactive chat (pick your AI brain)
atlas.chat(llm="gemini", namespace="technique")  # or "gpt" or "groq" or "ollama"

# 📱 Push results to Telegram
atlas.send(results, chat_id="your_chat_id")

# 📊 Inspect what you've built
stats = atlas.stats()
print(f"Total chunks: {stats['total_vectors']}")
print(f"Active namespaces: {stats['namespaces']}")
```

### CLI (The Lazy Way)

After running `bash setup_aliases.sh`:

```bash
# Quick search
atlas-query "XXE exploitation"

# Search a specific namespace
atlas-query "buffer overflow" --namespace ctf

# Vectorize with metadata
atlas-vectorize /path/to/chunks --domain web --tags "rce,exploit"

# Chat with Gemini
atlas-chat --llm gemini

# Ask and get sources
atlas-ask "What is Server-Side Template Injection?"

# Send to Telegram
atlas-send "Quick question: how do I exploit LDAP?"

# STT pipeline: search → send to Telegram
atlas-stt query "XXE bypass techniques"
atlas-stt file /path/to/wordlist.txt
atlas-stt dir /path/to/tools/
```

---

## Architecture: Modular Weapons System

```
Atlas()
 ├─ .query(text, k=5, namespace="root")     Semantic search + ranking
 ├─ .fetch(chunk_id)                         Retrieve by ID
 ├─ .chunk(file_path, chunk_size=1000)      Split documents into atoms
 ├─ .vectorize(dir, domain, tags, namespace) Embed + upload to Pinecone
 ├─ .ingest(file_path, domain, tags)         Chunk + vectorize (one-shot)
 ├─ .ask(question, llm="gemini")            Reasoning + sources
 ├─ .chat(llm="gpt", namespace="root")      Interactive multi-turn
 ├─ .send(results, chat_id)                  Telegram delivery
 ├─ .stats()                                 Index analytics
 ├─ .sync()                                  Rebuild chunk registry
 └─ .help()                                  Full command reference
```

---

## Namespace Strategy: Organize Like a Pro

Keep your knowledge **separated by context**, not mixed together:

```python
# Instance-level namespace (affects all operations)
atlas = Atlas(namespace="cve")
atlas.query("RCE in Apache Struts")  # Searches only CVE namespace

# Method-level override (one-off)
atlas = Atlas()
atlas.query("LFI bypass", namespace="ctf")     # Override for this query
atlas.vectorize("/ctf_notes", namespace="ctf") # Different namespace
atlas.ask("What is CSRF?", namespace="technique")  # Technique namespace
```

**Built-in presets:**
- `root` — General knowledge
- `cve` — Vulnerability intelligence
- `technique` — Attack techniques
- `ctf` — CTF-specific exploits
- `tools` — Tool documentation & commands
- `payloads` — Ready-to-use payloads

Custom namespaces? Just pass a string.

---

## Metadata Injection: Smart Tagging Without Boilerplate

No need for YAML frontmatter. Tag as you vectorize:

```python
# Plain markdown file
atlas.vectorize(
    "my_notes.md",
    domain="web-security",
    tags=["xss", "dom-based", "reflected", "blind"],
    metadata={
        "severity": "high",
        "cwe": "79",
        "owasp": "A03:2021"
    }
)
```

Later, search by these tags:

```python
# Query automatically includes metadata
results = atlas.query("XSS in Angular templates")
for chunk in results:
    print(f"CWE: {chunk.get('cwe')}, OWASP: {chunk.get('owasp')}")
```

---

## Documentation (Read the Full Arsenal)

- **[Getting Started](mkdocs/docs/getting-started/installation.md)** — Clone, install, configure
- **[Beginner's Guide](mkdocs/docs/getting-started/beginners-guide.md)** — First queries, chunking, vectorization
- **[What is RAG?](mkdocs/docs/rag-fundamentals/what-is-rag.md)** — The philosophy behind Atlas
- **[Chunking Methodology](mkdocs/docs/chunking-methodology/core-principles.md)** — How to structure your knowledge
- **[Pinecone CLI](mkdocs/docs/pinecone-operations/cli-essentials.md)** — Vector database operations
- **[Telegram Integration](mkdocs/docs/telegram-integration/stt-reference.md)** — Push intelligence to your team
- **[PDF Chunker](mkdocs/docs/pdf-chunker/usage.md)** — Extract knowledge from documents

Build docs locally:

```bash
pip install mkdocs-material
cd mkdocs && mkdocs serve
# Visit http://localhost:8000
```

---

## Project Structure

```
atlas-engine/
 ├── atlas_engine/              ← Framework core (7 components)
 │    ├── __init__.py           Exports: from atlas_engine import Atlas
 │    ├── core.py               Atlas() orchestrator (full API)
 │    ├── query.py              QueryEngine (Pinecone search)
 │    ├── vectorizer.py         Vectorizer (embed + metadata + upsert)
 │    ├── chunker.py            Chunker (PDF/text splitting)
 │    ├── chat.py               Chat (Gemini/GPT/Groq/Ollama backends)
 │    ├── telegram.py           Telegram integration
 │    └── registry.py           Chunk registry manager
 │
 ├── src/                       CLI wrappers (14 commands)
 │    ├── query.py
 │    ├── vectorize.py
 │    ├── ask.py
 │    ├── chat.py
 │    └── ... (10 more aliases)
 │
 ├── config.py                  Centralized config (keys, paths, presets)
 ├── .env/                      API keys (never committed)
 ├── default/                   Knowledge base (294+ chunks)
 ├── chunk_registry.json        Chunk metadata index
 ├── requirements.txt           Dependencies
 ├── setup_aliases.sh           CLI alias installer
 │
 ├── mkdocs/                    Documentation site
 │    ├── mkdocs.yml
 │    └── docs/
 │
 ├── LICENSE                    MIT
 ├── CONTRIBUTING.md            How to contribute
 └── CODE_OF_CONDUCT.md        Community standards
```

---

## Why Atlas Engine

| Problem | Atlas Solution |
|---------|-----------------|
| **Knowledge scattered across files** | One semantic search, all files unified |
| **Slow manual research** | Sub-second intelligent retrieval |
| **Hallucinations from LLMs** | Sources always cited, always traceable |
| **No context isolation** | Namespaces keep different domains separate |
| **Manual metadata tagging** | Inject metadata at vectorize time, not in files |
| **Single LLM vendor lock-in** | Pick Gemini (free), GPT (cheap), or Ollama (offline) |
| **No team collaboration** | Telegram bridge—push intelligence to your team |
| **Complex RAG pipelines** | One line: `atlas.ingest("/path")` |

---

## Requirements

- **Python 3.10+**
- **Pinecone** account (free tier supported)
- **At least one LLM API key:**
  - Google Gemini (free tier available)
  - OpenAI (GPT-4o-mini, cheap)
  - Ollama (offline, free)
- **Optional:** Telegram bot token for team delivery

---

## Quick Benchmark

On a 500-chunk knowledge base (~2M tokens):

| Operation | Latency | Notes |
|-----------|---------|-------|
| Search (top-5) | **140ms** | Pinecone + ranking |
| Single Q&A | **2.1s** | Gemini reasoning + sources |
| Chat turn | **3.5s** | Multi-turn with context |
| Vectorize 100 chunks | **1.8s** | Batch embed + upsert |

---

## Roadmap

- [ ] Batch knowledge export (YAML/JSON)
- [ ] Vector database switching (Weaviate, Milvus support)
- [ ] Advanced retrieval (Hybrid BM25 + semantic)
- [ ] Fine-tuning data generation from chunks
- [ ] Web UI dashboard for index management
- [ ] Slack integration alongside Telegram

---

## GitHub Actions Automation

This repo includes `.github/workflows/docker-ci.yml` with:
- `build-and-smoke-test` on every PR/push (builds Docker image + runs container smoke test).
- `publish-ghcr` on `main` pushes (publishes image to `ghcr.io/<owner>/<repo>:latest` and `:sha`).

---

## Contributing

Atlas Engine is **open-source**. We accept pull requests, bug reports, and feature requests.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

---

## License

MIT — Use freely, modify, distribute. Respect the license, respect the community.

---

## Support

- 📖 **Docs**: Read `mkdocs/docs/`
- 🐛 **Bugs**: Open an issue on GitHub
- 💬 **Questions**: Discussions tab
- 🚀 **Suggestions**: Feature requests welcome

---

**Built by operators, for operators.**  
*Atlas Engine: Your knowledge, weaponized.*
