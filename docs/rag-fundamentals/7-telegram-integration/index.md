# Telegram Integration & Scripts (Complete System - Feb 2026)

Complete documentation of all Telegram integration components with line-by-line commented code blocks. Learn how vectors → Pinecone → Telegram Bot work together.

## System Status

✅ **Fully Operational** - 15 chunks vectorized, bot running 24/7, registry auto-generated

**Key Technologies**:
- OpenAI text-embedding-3-large (3072D)
- Pinecone index: `rag-canonical-v1-emb3large`
- chunk_registry.json: 15 chunk_id → file mappings
- Telegram Bot: polling loop + RAG engine integration

## Overview

Your complete RAG+Telegram system includes:

- **Vectorizer** - Generate 3072D embeddings, auto-generate registry
- **chunk_registry.json** - Map chunk_id → local file paths
- **Text messages** - Send updates and notifications
- **Files** - Upload documents, scripts, exploits
- **Directories** - ZIP and send entire folders
- **RAG results** - Send search results as messages or ZIP files
- **Telegram Bot** - 24/7 online, searches Pinecone + reads local files
- **Query Agent** - Hybrid search + markdown reporting

## Architecture (Feb 2026 - Complete Pipeline)

```
┌──────────────────────────────────────────────────────────────┐
│           Complete RAG + Telegram Integration                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  PHASE 1: VECTORIZATION                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  vectorize_canonical_openai.py                       │   │
│  │  ├─ Read chunks (.md with YAML frontmatter)         │   │
│  │  ├─ Generate 3072D embeddings (OpenAI)             │   │
│  │  ├─ Upload to Pinecone                             │   │
│  │  └─ Auto-generate chunk_registry.json              │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  PHASE 2: PINECONE STORAGE                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  rag-canonical-v1-emb3large (3072D cosine)         │   │
│  │  └─ 15 vectors with full metadata + content         │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  PHASE 3: LOCAL MAPPING                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  chunk_registry.json                                 │   │
│  │  └─ Maps: chunk_id → /path/to/file.md              │   │
│  │  └─ Required for local file reading                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  PHASE 4: TELEGRAM BOT (24/7)                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  telegram_bot.py (polling loop)                      │   │
│  │  ├─ Load RAG Engine (Pinecone + Registry)           │   │
│  │  ├─ Listen for messages (/q <query>)               │   │
│  │  ├─ Generate 3072D embedding                        │   │
│  │  ├─ Search Pinecone                                │   │
│  │  ├─ Read files locally via registry               │   │
│  │  └─ Send COMPLETE content to Telegram             │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  PHASE 5: UTILITIES                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  stt (CLI wrapper) - Manual message/file sending     │   │
│  │  telegram_sender.py - Core Telegram API layer       │   │
│  │  query-agent-hybrid.py - Manual search + reporting  │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Telegram Bot API                                    │   │
│  │  https://api.telegram.org/bot...                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                      ↓                                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Your Telegram Mobile Device                         │   │
│  │  /q chmod permissions → Receive full content        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Components (Complete System)

### PHASE 1: Vectorization
#### **vectorize_canonical_openai.py** (The Engine)
- **Location**: `/root/.openskills/vectorize_canonical_openai.py`
- **Lines**: 339 (fully commented)
- **Purpose**: Transform markdown chunks → 3072D vectors → Pinecone + Registry
- **Input**: Any directory with .md files (YAML frontmatter required)
- **Output**: 
  - Pinecone vectors (3072D, index: `rag-canonical-v1-emb3large`)
  - chunk_registry.json (auto-generated, maps chunk_id → file paths)
- **Model**: OpenAI text-embedding-3-large (highest quality)
- **Documentation**: [Vectorizer Complete Guide](vectorizer-complete-guide.md)

### PHASE 2: Local Mapping
#### **chunk_registry.json** (Critical)
- **Location**: `/home/kali/Desktop/RAG/chunk_registry.json`
- **Purpose**: Maps chunk_id → local file paths
- **Auto-generated**: Yes (by vectorizer script)
- **Used by**: Telegram Bot + Query Agent
- **Enables**: Local file reading (complete content, not metadata-only)

### PHASE 3: Telegram Bot (24/7)
#### **telegram_bot.py** (The Server)
- **Location**: `/home/kali/Desktop/RAG/telegram_bot.py`
- **Lines**: 686 (fully integrated)
- **Status**: Running 24/7 in polling loop
- **Purpose**: Handle user queries via Telegram
- **Commands**: `/q`, `/qf`, `/qg`, `/qz`, `/status`, `/help`
- **Flow**: Message → Embedding → Pinecone → Registry → Local files → Telegram
- **Documentation**: [Telegram Bot Daemon](telegram_bot_daemon.md)

### PHASE 4: Utilities & Helpers

#### **1. stt CLI Wrapper** (Bash)
- **File**: `/usr/local/bin/send-to-telegram`
- **Alias**: `stt`
- **Purpose**: User-friendly command-line interface
- **Functions**: Message, file, directory, RAG queries
- **Documentation**: [STT CLI Wrapper](stt-cli-wrapper.md)

#### **2. telegram_sender.py** (Core)
- **Location**: `/home/kali/Desktop/RAG/telegram_sender.py`
- **Purpose**: Low-level Telegram API communication
- **Class**: `TelegramSender`
- **Methods**: send_message, send_document, send_directory
- **Documentation**: [telegram_sender.py](telegram_sender_py.md)

#### **3. rag_to_telegram.py** (RAG Integration)
- **Location**: `/home/kali/Desktop/RAG/rag_to_telegram.py`
- **Purpose**: Query RAG + send results to Telegram
- **Class**: `RAGtoTelegram`
- **Methods**: query_and_notify, query_and_notify_zip
- **Documentation**: [rag_to_telegram.py](rag_to_telegram_py.md)

#### **4. send_directory.py** (Directory Handler)
- **Location**: `/home/kali/Desktop/RAG/send_directory.py`
- **Purpose**: ZIP and send entire directories
- **Class**: `DirectorySender`
- **Methods**: create_zip, send_zip, send_directory
- **Documentation**: [send_directory.py](send_directory_py.md)

#### **5. query-agent-hybrid.py** (Manual Search)
- **Location**: `/root/.opencode/skills/query-agent/executables/query-agent-hybrid.py`
- **Purpose**: Manual RAG search + markdown reporting
- **Usage**: `query-agent-hybrid.py "tu_query" [--top-k 5] [--machine facts]`
- **Features**: Local file reading via registry, optional Telegram sending
- **Documentation**: [Query Agent Integration](query-agent-integration.md)

## Quick Start

### Send a Message
```bash
stt message "Task completed"
```

### Send a File
```bash
stt file /root/exploit.py "Exploit script"
```

### Send a Directory
```bash
stt directory /root/loot "Extracted files"
```

### Search RAG + Send Results
```bash
stt rag "LFI exploitation" 10 facts
```

### Send RAG Results as ZIP
```bash
stt rag-zip "RCE techniques" 20 facts
```

## Configuration

Required environment variables:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Pinecone (for RAG integration)
PINECONE_API_KEY=your_api_key_here

# OpenAI (for embeddings)
OPENAI_API_KEY=your_api_key_here
```

Located in: `/root/.openskills/env/telegram.env`

## Documentation Structure (Complete)

### Core Pipeline
1. **[Vectorizer Complete Guide](vectorizer-complete-guide.md)** - Line-by-line commented script (8 phases)
2. **[Telegram Bot Daemon](telegram_bot_daemon.md)** - 24/7 polling loop + RAG engine integration
3. **[Query Agent Integration](query-agent-integration.md)** - Manual search + reporting

### Supporting Components
4. **[stt CLI Wrapper](stt-cli-wrapper.md)** - Bash script breakdown
5. **[telegram_sender.py](telegram_sender_py.md)** - Core Telegram API class
6. **[rag_to_telegram.py](rag_to_telegram_py.md)** - RAG + Telegram notification integration
7. **[send_directory.py](send_directory_py.md)** - Directory compression & sending

### Guides & Reference
8. **[Usage Examples](usage-examples.md)** - Real-world workflows
9. **[Troubleshooting](troubleshooting.md)** - Common issues & solutions

## Features

✓ **Message Chunking** - Splits long messages (>4096 chars)  
✓ **File Upload** - Supports files up to 50MB  
✓ **ZIP Creation** - Compress directories automatically  
✓ **RAG Integration** - Query knowledge base + send results  
✓ **Metadata Preservation** - Chunk info included in results  
✓ **Error Handling** - Graceful failure with notifications  
✓ **Rate Limiting** - Protection against Telegram API limits  

## Key Statistics (Feb 2026)

| Component | Lines | Status | Purpose |
|-----------|-------|--------|---------|
| vectorize_canonical_openai.py | 339 | ✅ Active | Embedding generation + Pinecone upload + registry generation |
| chunk_registry.json | N/A | ✅ 15 entries | Local file mapping (auto-generated) |
| telegram_bot.py | 686 | ✅ 24/7 | RAG query handler + Telegram interface |
| query-agent-hybrid.py | 369 | ✅ Manual | Hybrid search + reporting + Telegram sending |
| stt CLI | 224 | ✅ Helper | Command-line wrapper |
| telegram_sender.py | 196 | ✅ Helper | Core Telegram API layer |
| rag_to_telegram.py | 430 | ✅ Helper | RAG + notification integration |
| send_directory.py | 151 | ✅ Helper | Directory compression + sending |
| **Total System** | **2,395+** | **✅ Operational** | Complete RAG + Telegram pipeline |

### Data Statistics
- **Vectors in Pinecone**: 15
- **Chunk Registry Entries**: 15
- **Embedding Model**: OpenAI text-embedding-3-large
- **Embedding Dimensions**: 3072D
- **Pinecone Index**: rag-canonical-v1-emb3large
- **Namespace**: __default__
- **Uptime**: 24/7 (polling loop)

## Quick Start (Feb 2026)

### 1. Vectorize Your Chunks
```bash
python3 /root/.openskills/vectorize_canonical_openai.py /path/to/chunks
# Output: 
#   - Vectors uploaded to Pinecone
#   - chunk_registry.json auto-generated (15 chunks)
```

### 2. Verify Bot is Running
```bash
ps aux | grep telegram_bot | grep -v grep
# Should show: /root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py
```

### 3. Query via Telegram
```
/q chmod permissions
# Response: 5 results with complete content (from local files, not truncated)
```

### 4. Manual Query (Optional)
```bash
python3 /root/.opencode/skills/query-agent/executables/query-agent-hybrid.py "LFI techniques"
# Output: markdown file + optional Telegram sending
```

## Learning Path

**Understand the system (in order)**:
1. **[Vectorizer Complete Guide](vectorizer-complete-guide.md)** ← Start here (line-by-line breakdown)
2. **[Telegram Bot Daemon](telegram_bot_daemon.md)** ← How bot processes queries
3. **[Query Agent Integration](query-agent-integration.md)** ← Manual search alternative

**Master the utilities**:
4. **[stt CLI Wrapper](stt-cli-wrapper.md)** - Quick messaging
5. **[telegram_sender.py](telegram_sender_py.md)** - Core API layer
6. **[rag_to_telegram.py](rag_to_telegram_py.md)** - RAG + notifications

**Apply & troubleshoot**:
7. **[Usage Examples](usage-examples.md)** - Real workflows
8. **[Troubleshooting](troubleshooting.md)** - Common issues

---

**Every line of code explained. No magic, just clarity.**
