# 📚 Scripts Index - Quick Reference

Complete guide to all Python and Bash scripts in CTF Bug Hunter Retrieval System.

---

## 🐍 Python Scripts (`src/`)

### **Core Vectorization & Query**

#### `vectorize_canonical_openai.py`
**Purpose**: Main vectorizer - converts markdown chunks into 3072D embeddings and uploads to Pinecone

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/vectorize_canonical_openai.py <path>
```

**Modes**:
- Directory: `src/vectorize_canonical_openai.py /home/kali/chunks/`
- Single file: `src/vectorize_canonical_openai.py /home/kali/chunk.md`
- Simple name: `src/vectorize_canonical_openai.py cheatsheets`

**What it does**:
1. Reads `.md` files with YAML frontmatter
2. Validates chunk metadata (requires `chunk_id`)
3. Generates 3072D embeddings using OpenAI text-embedding-3-large
4. Uploads vectors to Pinecone index `rag-canonical-v1-emb3large`
5. **Auto-generates** `chunk_registry.json` for local file mapping

**Output**:
- Vectors in Pinecone
- `chunk_registry.json` in `/home/kali/Desktop/RAG/`

**Dependencies**: Pinecone, OpenAI, YAML

---

#### `query_canonical_openai.py`
**Purpose**: RAG query engine - semantic search against Pinecone index

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/query_canonical_openai.py <query> [top_k] [machine]
```

**Examples**:
```bash
# Basic query
/root/.openskills/venv/bin/python3 src/query_canonical_openai.py "RCE PHP"

# With result count
/root/.openskills/venv/bin/python3 src/query_canonical_openai.py "SQL injection" 10

# Filter by machine
/root/.openskills/venv/bin/python3 src/query_canonical_openai.py "privesc" 5 gavel
```

**What it does**:
1. Takes user query and generates 3072D embedding (OpenAI)
2. Searches Pinecone index for similar vectors
3. Returns relevance-ranked results with metadata
4. Supports optional machine filtering

**Output**: Formatted results with chunk_id, score, domain, confidence

**Dependencies**: Pinecone, OpenAI

---

#### `query_chunk.py`
**Purpose**: Fetch specific chunk by chunk_id from Pinecone

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/query_chunk.py <chunk_id>
```

**Example**:
```bash
/root/.openskills/venv/bin/python3 src/query_chunk.py "technique::web::sql::injection::001"
```

**What it does**:
1. Looks up exact chunk by ID in Pinecone
2. Displays metadata and full content
3. Useful for debugging or reviewing specific chunks

**Output**: Chunk metadata + content

**Dependencies**: Pinecone

---

### **Telegram Integration**

#### `telegram_sender.py`
**Purpose**: Core Telegram API wrapper - sends messages, files, and directories

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/telegram_sender.py <message>
/root/.openskills/venv/bin/python3 src/telegram_sender.py --file <path> [caption]
```

**Examples**:
```bash
# Send message
/root/.openskills/venv/bin/python3 src/telegram_sender.py "Task completed"

# Send file with caption
/root/.openskills/venv/bin/python3 src/telegram_sender.py --file /root/exploit.py "SQLi payload"

# Send file without caption
/root/.openskills/venv/bin/python3 src/telegram_sender.py --file /root/notes.txt
```

**What it does**:
1. Loads Telegram credentials from `/root/.openskills/env/telegram.env`
2. Sends text messages (splits >4096 chars automatically)
3. Sends files with optional captions (max 50MB)
4. Handles errors gracefully

**Output**: Telegram bot sends to TELEGRAM_CHAT_ID

**Dependencies**: Telegram Bot API, requests

---

#### `rag_to_telegram.py`
**Purpose**: Query RAG + automatically send results to Telegram

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py <query> [top_k] [machine] [--zip]
```

**Examples**:
```bash
# Query and send to Telegram
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "LFI exploitation"

# Top 10 results
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "RCE techniques" 10

# Filter by machine
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "privesc" 5 gavel

# Send as ZIP file
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "SQL injection" 5 --zip
```

**What it does**:
1. Executes RAG query (semantic search)
2. Formats results
3. Sends to Telegram automatically
4. Optional: compresses results as ZIP

**Output**: Results in Telegram chat

**Dependencies**: Pinecone, OpenAI, telegram_sender.py

---

#### `telegram_bot.py`
**Purpose**: Telegram bot daemon - interactive query interface in Telegram

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/telegram_bot.py
```

**What it does**:
1. Starts polling Telegram for messages
2. Handles `/q <query>` command for RAG searches
3. Loads chunk_registry.json for local file fallback
4. Returns instant results with Telegram formatting

**Commands in Telegram**:
```
/q <query>           - Search RAG (default 5 results)
/q <query> <top_k>   - Specify number of results
/q <query> <top_k> <machine>  - Filter by machine
```

**Output**: Real-time Telegram responses

**Dependencies**: Pinecone, OpenAI, python-telegram-bot, chunk_registry.json

---

#### `query_agent.py`
**Purpose**: Hybrid query agent - search Pinecone + read local files

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/query_agent.py <query> [--top-k N] [--machine NAME]
```

**Examples**:
```bash
# Basic query
/root/.openskills/venv/bin/python3 src/query_agent.py "SQL injection"

# Custom top-k
/root/.openskills/venv/bin/python3 src/query_agent.py "RCE" --top-k 10

# Filter machine
/root/.openskills/venv/bin/python3 src/query_agent.py "privesc" --machine gavel
```

**What it does**:
1. Queries Pinecone index
2. Uses chunk_registry.json to locate local files
3. Reads full content directly from filesystem
4. Generates markdown output
5. Optionally sends to Telegram

**Output**: Formatted results + Telegram (optional)

**Dependencies**: Pinecone, OpenAI, chunk_registry.json

---

#### `send_directory.py`
**Purpose**: ZIP compression + Telegram delivery for directories

**Usage**:
```bash
/root/.openskills/venv/bin/python3 src/send_directory.py <directory> [caption]
```

**Examples**:
```bash
# Send directory with default caption
/root/.openskills/venv/bin/python3 src/send_directory.py /root/loot

# Custom caption
/root/.openskills/venv/bin/python3 src/send_directory.py /root/exploits "Active exploits"
```

**What it does**:
1. Compresses entire directory to ZIP
2. Validates size (<50MB Telegram limit)
3. Sends via Telegram with caption

**Output**: ZIP file in Telegram chat

**Dependencies**: telegram_sender.py

---

## 🔧 Bash Scripts (`scripts/`)

### **CLI Wrappers & Tools**

#### `send-to-telegram.sh` (STT Command)
**Purpose**: Main CLI wrapper - single entry point for all Telegram operations

**Installation** (already linked):
```bash
# Already available as 'stt' command system-wide
stt --help
```

**Usage**:
```bash
stt rag <query> [top_k] [machine]        # Search RAG
stt rag-zip <query> [top_k] [machine]    # RAG as ZIP
stt message "text"                       # Send message
stt file /path/to/file [caption]         # Send file
stt directory /path/to/dir [caption]     # Send directory
stt /path/to/file                        # Send file directly
```

**Examples**:
```bash
stt rag "LFI exploitation"
stt rag "RCE techniques" 10
stt rag "privesc" 5 facts
stt message "Exploitation complete"
stt file /root/payload.py "SQLi payload"
stt directory /root/loot "Captured data"
```

**What it does**:
1. Activates `/root/.openskills/venv` automatically
2. Routes commands to appropriate Python scripts
3. Handles file/directory validation
4. Provides color-coded output

**Features**:
- Full RAG integration
- File/directory compression
- Message handling
- Machine filtering support

---

#### `send-rag-telegram.sh`
**Purpose**: Shortcut for direct RAG → Telegram queries

**Usage**:
```bash
send-rag-telegram <query> [top_k] [machine]
```

**Examples**:
```bash
send-rag-telegram "SQL injection"
send-rag-telegram "RCE techniques" 10
send-rag-telegram "privesc" 5 gavel
```

**What it does**:
1. Faster than `stt rag` - direct call
2. Activates venv and executes rag_to_telegram.py
3. Returns results directly in Telegram

**Use case**: Quick ad-hoc queries during CTF competitions

---

#### `QUICKSTART.sh`
**Purpose**: Interactive quick start guide with environment setup

**Usage**:
```bash
./scripts/QUICKSTART.sh
```

**What it does**:
1. Prints header banner
2. Activates `/root/.openskills/venv`
3. Shows available commands with examples
4. Lists configuration paths
5. Displays index statistics

**Output**: Interactive menu with usage instructions

---

#### `start_bot.sh`
**Purpose**: Launch Telegram bot daemon in background

**Usage**:
```bash
./scripts/start_bot.sh
```

**What it does**:
1. Activates venv
2. Starts `telegram_bot.py` as background process
3. Logs to `telegram_bot.log`
4. Ready for `/q` queries in Telegram

**Output**: Running bot, logs in telegram_bot.log

---

## 📊 Execution Flow Diagram

```
User Input
    ↓
┌─────────────────────────────────────┐
│  CLI Wrapper (send-to-telegram.sh)  │
└─────────────────────────────────────┘
    ↓
    ├─→ [rag] → query_canonical_openai.py → Pinecone
    ├─→ [message] → telegram_sender.py → Telegram API
    ├─→ [file] → telegram_sender.py → Telegram API
    └─→ [directory] → send_directory.py → Telegram API
    
Alternative Direct Flow:
    ↓
┌─────────────────────────────────────┐
│ rag_to_telegram.py                  │
├─────────────────────────────────────┤
│ query_canonical_openai.py (search)  │
│ telegram_sender.py (send)           │
└─────────────────────────────────────┘
    ↓
Telegram Chat
```

---

## 🔐 Configuration Files Required

All scripts load credentials from `/root/.openskills/env/`:

```
/root/.openskills/env/
├── telegram.env      # TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
├── pinecone.env      # PINECONE_API_KEY
└── openai.env        # OPENAI_API_KEY
```

**Template** (use `config/.env.example`):
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
PINECONE_API_KEY=your_pinecone_key
OPENAI_API_KEY=your_openai_key
```

---

## ⚡ Quick Command Reference

### Vectorize Your CTF Notes
```bash
/root/.openskills/venv/bin/python3 src/vectorize_canonical_openai.py /home/kali/ctf-notes
```

### Query Instantly
```bash
stt rag "SQL injection" 5
```

### Query Specific Machine
```bash
stt rag "privesc" 10 gavel
```

### Send File to Team
```bash
stt file /root/exploit.py "Working exploit"
```

### Send Entire Directory
```bash
stt directory /root/loot "Captured credentials"
```

### Interactive Bot
```bash
/root/.openskills/venv/bin/python3 src/telegram_bot.py
# Then in Telegram: /q <query>
```

---

## 📋 Script Dependency Graph

```
telegram_sender.py (base)
    ↑
    ├─ rag_to_telegram.py
    ├─ send_directory.py
    ├─ telegram_bot.py
    └─ query_agent.py

query_canonical_openai.py (search)
    ↑
    ├─ rag_to_telegram.py
    ├─ telegram_bot.py
    ├─ query_agent.py
    └─ send-to-telegram.sh

vectorize_canonical_openai.py (index)
    ↑
    ├─ Updates Pinecone
    ├─ Generates chunk_registry.json
    └─ Used by all query scripts
```

---

## 🎯 Use Cases by Script

| Use Case | Command |
|----------|---------|
| Add notes to knowledge base | `src/vectorize_canonical_openai.py` |
| Quick search during CTF | `stt rag "query"` |
| Search specific machine | `stt rag "query" 5 facts` |
| Get full chunk details | `src/query_chunk.py chunk_id` |
| Send findings to team | `stt file /path` |
| Interactive bot | `src/telegram_bot.py` |
| One-time query | `send-rag-telegram` |
| Setup environment | `scripts/QUICKSTART.sh` |

---

## 🔗 Related Documentation

- **Full Guide**: [README.md](./README.md)
- **Quick Start**: [QUICKSTART.md](./QUICKSTART.md)
- **Vectorization**: [docs-vectorizer/VECTORIZE_INSTRUCTIONS.md](./docs-vectorizer/VECTORIZE_INSTRUCTIONS.md)
- **MkDocs**: [docs/mkdocs.yml](./docs/mkdocs.yml)

---

**Built for CTF players who need instant knowledge retrieval. Every script is designed to save time during competitions.** ⚡
