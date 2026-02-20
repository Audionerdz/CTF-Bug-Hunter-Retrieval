# 🎯 CTF Bug Hunter Retrieval System

**Your competitive edge in CTF knowledge retrieval.**

Instant access to your CTF knowledge base via Telegram bot. Semantic search through your writeups, exploits, and research notes during competitions.

---

## Why This Exists

During CTF competitions, you need instant access to:
- **Exploitation techniques** you've researched
- **Vulnerability notes** from past competitions
- **Writeups and payload references**
- **Team knowledge base**

**CTF Bug Hunter Retrieval** gives you a **Telegram bot** that retrieves relevant information in seconds using AI-powered semantic search.

---

## 🚀 Core Features

✅ **Semantic Search**: Understand intent, not just keywords  
✅ **Instant Access**: Query via Telegram bot (phone, laptop, anywhere)  
✅ **Team Friendly**: Share findings with your CTF team instantly  
✅ **No Setup Hell**: One `setup.sh` command to get running  
✅ **Production-Grade**: Pinecone + OpenAI embeddings (3072D)  
✅ **Easy Vectorization**: Two simple commands for adding notes  
✅ **Modular Architecture**: Scale from single chunks to complete knowledge bases  

---

## Quick Demo

```bash
# Query your knowledge base
/root/.openskills/venv/bin/python3 src/telegram_sender.py "SQL injection in blind contexts"

# Send a file to the team
/root/.openskills/venv/bin/python3 src/send_directory.py /root/exploits/

# Search with Telegram bot (in chat)
/q <your_query>  # Returns instant results
```

---

## Getting Started (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git
cd CTF-Bug-Hunter-Retrieval
```

### 2. Run Automated Setup

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 3. Configure Your API Keys

Edit `.env` with:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_from_@BotFather
TELEGRAM_CHAT_ID=your_chat_id
PINECONE_API_KEY=your_api_key_from_pinecone.io
OPENAI_API_KEY=your_api_key_from_openai.com
```

### 4. Test Installation

```bash
source venv/bin/activate
/root/.openskills/venv/bin/python3 src/telegram_sender.py "Test message from CTF Bug Hunter!"
```

### 5. Start Querying

```bash
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "SQL injection techniques" 5
```

See **[QUICKSTART.md](./QUICKSTART.md)** for detailed guide.

---

## System Architecture

```
┌──────────────────────────────┐
│   Your CTF Notes & Writeups  │
│   (Markdown format)          │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   Vectorizer Script          │
│   (OpenAI 3072D embeddings)  │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│   Pinecone Vector DB         │
│   (Semantic search index)    │
└───────────────┬──────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   ┌─────────┐    ┌──────────┐
   │Telegram │    │Query CLI │
   │   Bot   │    │  (stt)   │
   └─────────┘    └──────────┘
```

---

## Use Cases

### During CTF Competition

1. You find a SQL injection vulnerability
2. Query: `/q "blind sql injection"`
3. Telegram bot returns your past exploits instantly
4. Win time, execute faster → **Competitive advantage**

### Research Mode

1. Add writeups/notes to your knowledge base
2. Vectorize them with modular script
3. Query mid-research to avoid re-discovering techniques

### Team Collaboration

1. Query and retrieve findings
2. Send results via Telegram to team group
3. Share exploits without leaving Telegram app

---

## Documentation

### Quick Start Guides

- **[QUICKSTART.md](./QUICKSTART.md)** - 5 minute setup
- **[INSTALLATION.md](./INSTALLATION.md)** - Detailed installation
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design & data flow

### Complete Knowledge Base

Navigate to `docs/` for comprehensive documentation:

- **Part 1-4**: RAG fundamentals, chunking, Pinecone setup
- **Part 5-6**: Advanced topics, manual operations
- **Part 7**: Telegram integration & script reference
- **Part 8**: Vectorization guides (complete & modular)

### Vectorization Guides

Two essential guides for managing your knowledge base:

1. **[Vectorization Complete Guide](./docs-vectorizer/VECTORIZE_INSTRUCTIONS.md)**
   - Full walkthrough of all vectorization options
   - Chunk structure and YAML frontmatter
   - Auto-registry generation
   - Best practices

2. **[Vectorizer Modular Guide](./docs-vectorizer/VECTORIZER_MODULAR_GUIDE.md)**
   - Directory vectorization
   - Single file vectorization
   - Automatic detection
   - Quick examples

---

## How Vectorization Works

### Step 1: Create/Add Notes

```bash
mkdir /home/kali/ctf-notes
# Create markdown files with YAML frontmatter
```

### Step 2: Vectorize with One Command

```bash
# Option A: OpenAI embeddings (best quality)
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/ctf-notes

# Option B: Free local embeddings
/root/.openskills/venv/bin/python3 /root/.opencode/skills/vectorizer/executables/vectorize_simple.py /home/kali/ctf-notes
```

### Step 3: Query Immediately

```bash
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "your search query" 5
```

**That's it.** Auto-registry, auto-indexing, auto-ready.

---

## Supported Platforms

✅ Linux (Ubuntu, Debian, Kali, Parrot)  
✅ macOS  
⏳ Windows (WSL recommended)  

---

## API Requirements

| Service | Free Tier | Purpose |
|---------|-----------|---------|
| **Pinecone** | 1M vectors | Vector storage & search |
| **OpenAI** | $5 free credits | Text embeddings (3072D) |
| **Telegram** | ✅ Free | Bot delivery |

All services have generous free tiers suitable for CTF use.

---

## Common Commands

```bash
# Telegram CLI wrapper (stt = send-to-telegram)
stt rag "LFI exploitation"                              # Search RAG
stt rag "RCE techniques" 10                            # Top 10 results
stt rag "privesc" 5 facts                              # Machine filter
stt file /root/exploit.py "Exploit script"             # Send file
stt directory /root/loot "Extracted findings"          # Send dir

# Direct Python calls
/root/.openskills/venv/bin/python3 src/telegram_sender.py "message"
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "query"
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /path/to/chunks
```

---

## 📚 Scripts Reference Guide

Need detailed information about what each script does? Check **[SCRIPTS_INDEX.md](./SCRIPTS_INDEX.md)** for:

- **Python Scripts** (9 total): Vectorizers, query engines, Telegram integration
- **Bash Scripts** (4 total): CLI wrappers, automation, bot management
- **Function Reference**: Complete parameters and usage examples
- **Architecture Overview**: How scripts interact in the system
- **Troubleshooting**: Common issues and solutions

Quick lookup for any script in your toolbox. Over 500 lines of reference material.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pinecone'"

```bash
source venv/bin/activate
pip install -r config/requirements.txt
```

### "PINECONE_API_KEY not found"

Edit `.env` and add your Pinecone API key from [pinecone.io](https://www.pinecone.io/)

### "Telegram bot not responding"

See [docs/7-telegram-integration/troubleshooting.md](./docs/docs/7-telegram-integration/troubleshooting.md)

### Vectorizer issues

Check [docs-vectorizer/VECTORIZE_INSTRUCTIONS.md](./docs-vectorizer/VECTORIZE_INSTRUCTIONS.md) for complete troubleshooting

---

## Contributing

Found a bug? Have ideas for improvements?

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m "feat: description"`
4. Push: `git push origin feature/your-idea`
5. Open a Pull Request

---

## License

MIT License - See [LICENSE](./LICENSE) file

---

## Support

- 📖 **Documentation**: `docs/` directory (MkDocs format)
- 🚀 **Quick Start**: [QUICKSTART.md](./QUICKSTART.md)
- 🔧 **Setup Help**: [INSTALLATION.md](./INSTALLATION.md)
- 📡 **Vectorization**: [docs-vectorizer/](./docs-vectorizer/)
- 🐛 **Issues**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions

---

## For the Curious

**What is RAG?** See `docs/docs/1-intro/what-is-rag.md`

**How does semantic search work?** See `docs/docs/3-pinecone-guide/concepts.md`

**Full installation guide?** See `docs/docs/3-pinecone-guide/installation.md`

---

**Built for CTF experts. Used by hackers, security researchers, and red teams.**

**Your knowledge base. Your competitive edge. Activated.**
