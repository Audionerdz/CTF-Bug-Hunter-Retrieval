# rag_to_telegram.py - RAG Integration

**File**: `/home/kali/Desktop/RAG/rag_to_telegram.py`  
**Lines**: 430  
**Class**: `RAGtoTelegram`  
**Purpose**: Query RAG index + send results to Telegram

## Overview

Combines Pinecone RAG search with Telegram delivery. Supports:
- Text message output (chunked results)
- ZIP file output (organized by machine)
- Machine filtering (FACTS, GAVEL)
- Metadata preservation

## Key Functions

### Class: RAGtoTelegram

```python
class RAGtoTelegram:
    # Initialize: Load API keys, connect to Pinecone/OpenAI/Telegram
    def __init__(self):
        self.pinecone_key, self.openai_key = load_keys()
        self.pc = Pinecone(api_key=self.pinecone_key)
        self.index = self.pc.Index(INDEX_NAME)
        self.openai_client = OpenAI(api_key=self.openai_key)
        self.sender = TelegramSender()
        # Load optional chunk registry for full content
        self.chunk_map = {...}  # Maps chunk_id -> file_path
```

### Main Methods

#### get_embedding(text)
Creates 3072D embedding using OpenAI API
```python
response = self.openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=text,
    dimensions=3072
)
```

#### clean_markdown(content)
Removes YAML frontmatter from markdown files
```python
# Input: ---\ntitle: ...\n---\ncontent...
# Output: content...
if content.startswith("---"):
    parts = content.split("---", 2)
    return parts[2].strip()
```

#### query_and_notify(query_text, top_k, machine_filter)
Query RAG and send results as messages
```python
# 1. Generate embedding for query
embedding = self.get_embedding(query_text)

# 2. Query Pinecone
results = self.index.query(
    vector=embedding,
    top_k=top_k,
    include_metadata=True
)

# 3. Send header message
intro = f"🔍 **QUERY RESULT**\n📝 Query: {query_text}..."
self.sender.send_message(intro)

# 4. Send each result
for match in results["matches"]:
    header = self.format_header(match)
    self.sender.send_message(f"{header}\n{content}")
```

#### query_and_notify_zip(query_text, top_k, machine_filter)
Query RAG and send results as ZIP
```python
# 1. Same as above but:
results = self.index.query(...)

# 2. Create ZIP with markdown files
zip_path = create_chunks_zip({
    "matches": matches,
    "query": query_text,
    "chunk_map": self.chunk_map
})

# 3. Send ZIP file
send_zip_to_telegram(zip_path, self.sender)
```

## Usage

### Python Script
```python
from rag_to_telegram import RAGtoTelegram

agent = RAGtoTelegram()

# Send results as messages
agent.query_and_notify(
    "LFI exploitation", 
    top_k=10, 
    machine_filter="facts"
)

# Send results as ZIP
agent.query_and_notify_zip(
    "RCE techniques",
    top_k=20,
    machine_filter="facts"
)
```

### Command Line (via stt)
```bash
# Query and send messages
stt rag "LFI exploitation" 10 facts

# Query and send ZIP
stt rag-zip "RCE techniques" 20 facts

# Query all machines
stt rag "vulnerability" 5
```

## Configuration

```python
# Index settings
INDEX_NAME = "rag-canonical-v1-emb3large"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072

# Environment keys loaded from:
# /root/.openskills/env/pinecone.env
# /root/.openskills/env/openai.env
```

## Output Format

### Message Mode
```
🔍 **QUERY RESULT**

📝 Query: `LFI exploitation`
📊 Results: 3 chunks found
🗄️ Index: rag-canonical-v1-emb3large

#1 ──────────────────────────────
🖥️ **MACHINE: FACTS**
📄 Chunk: `chunk_facts_001`
🎯 Phase: reconnaissance | Technique: enumeration
⭐ Score: 0.891
────────────────────────────
LFI vulnerabilities allow reading arbitrary files...

════════════════════════════

✅ **END OF REPORT**
```

### ZIP Mode
```
RAG_results_LFI_exploitation_20260213_103000.zip
├── INDEX.md
├── FACTS/
│   ├── 001_chunk_facts_001.md
│   ├── 002_chunk_facts_003.md
│   └── 003_chunk_facts_005.md
└── GAVEL/
    └── 001_chunk_gavel_001.md
```

---

**Next: [send_directory.py](send_directory_py.md)**
