# RAG Documentation Index

**Organized documentation for the CTF Bug Hunter Retrieval System.**

---

## Directory Structure

```
docs/
├── README.md                          # This file - Documentation index
├── CLI_CHEATSHEET.md                  # Command-line quick reference
├── CLI_GUIDES_QUICK_ACCESS.md         # Fast access to common guides
├── VECTORIZE_INSTRUCTIONS.md          # Complete vectorization guide
├── VECTORIZER_MODULAR_GUIDE.md        # Modular chunk vectorization
├── guides/                            # Step-by-step setup guides
│   ├── GEMINI_RAG_SETUP.md           # Gemini embeddings setup
│   └── LANGCHAIN_RAG_SETUP_GUIDE.md  # LangChain RAG terminal guide
└── rag-fundamentals/                  # RAG theory and concepts
    ├── index.md                       # MkDocs index
    ├── 1-intro/                       # Introduction to RAG
    ├── 2-chunking-methodology/        # How to chunk documents
    ├── 3-pinecone-guide/              # Pinecone setup and usage
    ├── 4-rag-architecture/            # System architecture
    ├── 5-advanced-topics/             # Advanced configurations
    ├── 6-manual-pinecone-operations/  # Manual vector operations
    └── 7-telegram-integration/        # Telegram bot setup
```

---

## Quick Navigation

### New to RAG? Start Here

| Document | Description | Time |
|----------|-------------|------|
| [rag-fundamentals/1-intro/what-is-rag.md](./rag-fundamentals/1-intro/what-is-rag.md) | What is RAG and why it matters | 5 min |
| [rag-fundamentals/1-intro/overview.md](./rag-fundamentals/1-intro/overview.md) | System overview | 10 min |
| [QUICKSTART.md](../QUICKSTART.md) | Get running in 5 minutes | 5 min |

### Setting Up the System

| Document | What You'll Learn |
|----------|-------------------|
| [guides/LANGCHAIN_RAG_SETUP_GUIDE.md](./guides/LANGCHAIN_RAG_SETUP_GUIDE.md) | Build AI-powered RAG chat with LangChain + Gemini |
| [guides/GEMINI_RAG_SETUP.md](./guides/GEMINI_RAG_SETUP.md) | Configure Gemini embeddings (3072D) |
| [rag-fundamentals/3-pinecone-guide/installation.md](./rag-fundamentals/3-pinecone-guide/installation.md) | Install and configure Pinecone |

### Vectorizing Your Knowledge

| Document | Use Case |
|----------|----------|
| [VECTORIZE_INSTRUCTIONS.md](./VECTORIZE_INSTRUCTIONS.md) | Complete vectorization walkthrough |
| [VECTORIZER_MODULAR_GUIDE.md](./VECTORIZER_MODULAR_GUIDE.md) | Chunk-by-chunk vectorization |
| [rag-fundamentals/2-chunking-methodology/](./rag-fundamentals/2-chunking-methodology/) | How to structure your chunks |

### Telegram Integration

| Document | Description |
|----------|-------------|
| [rag-fundamentals/7-telegram-integration/](./rag-fundamentals/7-telegram-integration/) | Setup Telegram bot for RAG queries |

### Quick Reference

| Document | Purpose |
|----------|---------|
| [CLI_CHEATSHEET.md](./CLI_CHEATSHEET.md) | All CLI commands in one place |
| [CLI_GUIDES_QUICK_ACCESS.md](./CLI_GUIDES_QUICK_ACCESS.md) | Fast access to common operations |

---

## Document Details

### Root Level Documents

#### `CLI_CHEATSHEET.md`
**Purpose:** Command-line reference for all RAG operations.

**Contents:**
- Vectorization commands
- Query commands
- Telegram bot commands
- Environment setup
- Troubleshooting commands

**When to use:** Quick command lookup during operations.

---

#### `CLI_GUIDES_QUICK_ACCESS.md`
**Purpose:** Fast access links to the most common guides.

**Contents:**
- Quick setup links
- Common troubleshooting
- One-liner commands

**When to use:** When you need to find a guide quickly.

---

#### `VECTORIZE_INSTRUCTIONS.md`
**Purpose:** Complete guide to vectorizing your knowledge base.

**Contents:**
- What is vectorization
- Chunk structure (YAML frontmatter)
- Metadata fields explained
- Auto-registry generation
- Best practices
- Troubleshooting

**When to use:** Before adding new documents to Pinecone.

**Key sections:**
- Chunk ID naming conventions
- Required vs optional metadata
- How to run the vectorizer
- Verifying vectorization

---

#### `VECTORIZER_MODULAR_GUIDE.md`
**Purpose:** Guide for vectorizing individual files or directories.

**Contents:**
- Single file vectorization
- Directory vectorization
- Automatic detection
- Quick examples

**When to use:** When adding specific chunks to your knowledge base.

---

### `guides/` Directory

#### `guides/LANGCHAIN_RAG_SETUP_GUIDE.md`
**Purpose:** Step-by-step guide to build an AI-powered RAG terminal chat.

**Stack:**
- LangChain (framework)
- OpenAI embeddings (text-embedding-3-large, 3072D)
- Google Gemini LLM (gemini-2.5-flash)
- Pinecone (vector store)

**What you'll build:**
```
User Question → Embeddings → Pinecone Search → 
Retrieve Documents → Prompt Template → Gemini LLM → 
AI Response + Sources
```

**Contents:**
- Prerequisites
- Dependency installation
- Component initialization
- LCEL chain building
- Interactive terminal interface
- Troubleshooting
- Deployment to another VPS

**When to use:** Setting up the interactive RAG chat system on a new VPS.

---

#### `guides/GEMINI_RAG_SETUP.md`
**Purpose:** Configure Gemini embeddings for Pinecone queries.

**Contents:**
- Google AI API setup
- Gemini embedding model configuration
- Query script setup
- Integration with existing Pinecone index

**When to use:** When you want to use Google's embedding model instead of OpenAI.

---

### `rag-fundamentals/` Directory

MkDocs-structured documentation for learning RAG concepts.

#### `1-intro/`
| File | Description |
|------|-------------|
| `welcome.md` | Welcome message and quick start |
| `what-is-rag.md` | Explanation of RAG concepts |
| `overview.md` | System architecture overview |

#### `2-chunking-methodology/`
| File | Description |
|------|-------------|
| `core-principles.md` | Fundamental chunking principles |
| `chunk-fields.md` | Metadata fields for chunks |
| `chunk-id-examples.md` | Chunk ID naming conventions |
| `manifest-json.md` | Registry format and structure |

#### `3-pinecone-guide/`
| File | Description |
|------|-------------|
| `installation.md` | Pinecone setup |
| `configuration.md` | Index configuration |
| `quick-start.md` | Get started quickly |
| `concepts.md` | Vector database concepts |
| `3072d-setup.md` | High-dimensional setup |
| `index-management.md` | Managing indexes |
| `troubleshooting.md` | Common issues |

#### `4-rag-architecture/`
| File | Description |
|------|-------------|
| `rag-system-architecture.md` | Complete system design |
| `complete-index-guide.md` | Full index management |
| `system-update.md` | Updating the system |

#### `5-advanced-topics/`
| File | Description |
|------|-------------|
| `best-practices.md` | Recommended approaches |
| `faqs.md` | Frequently asked questions |
| `reference-table.md` | Quick reference tables |

#### `6-manual-pinecone-operations/`
| File | Description |
|------|-------------|
| `index.md` | Manual operations index |
| `pinecone-cli-essentials.md` | CLI commands |
| `embedding-chunks-manually.md` | Manual embedding |
| `managing-vectors.md` | Vector operations |
| `index-management-manual.md` | Index management |

#### `7-telegram-integration/`
| File | Description |
|------|-------------|
| Telegram bot setup and configuration |

---

## Learning Path

### Beginner Path

```
1. what-is-rag.md           → Understand RAG
2. overview.md               → See the big picture
3. QUICKSTART.md             → Get hands-on
4. VECTORIZE_INSTRUCTIONS.md → Add your first docs
```

### Intermediate Path

```
1. chunk-id-examples.md      → Structure your chunks
2. pinecone-guide/           → Master Pinecone
3. LANGCHAIN_RAG_SETUP_GUIDE.md → Build AI chat
```

### Advanced Path

```
1. rag-system-architecture.md → Design your system
2. manual-pinecone-operations/ → Advanced operations
3. best-practices.md          → Optimize everything
```

---

## External Resources

- [Pinecone Documentation](https://docs.pinecone.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Google AI Studio](https://aistudio.google.com/)

---

## Contributing

To add new documentation:

1. Place general guides in `docs/guides/`
2. Place conceptual/theoretical content in `docs/rag-fundamentals/`
3. Update this README.md index
4. Follow existing markdown formatting

---

**Last updated:** February 2026
