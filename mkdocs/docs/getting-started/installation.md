# Installation

This guide walks you through setting up the Atlas Engine from scratch.

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/RAG.git
cd RAG
export ATLAS_ROOT="$(pwd)"
```

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt. Every time you open a new terminal, activate it again with:

```bash
source "$ATLAS_ROOT/venv/bin/activate"
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs everything the framework needs:

| Package | What It Does |
|---------|--------------|
| `pinecone-client` | Vector database (stores and searches embeddings) |
| `openai` | Embedding generation + GPT chat backend |
| `google-generativeai` | Gemini chat backend |
| `langchain` + extensions | Document loading, text splitting, chain orchestration |
| `langchain-pinecone` | Pinecone vector store for LangChain |
| `python-telegram-bot` | Telegram message/file delivery |
| `requests` | HTTP requests (Ollama backend, Telegram API) |
| `python-dotenv` | Environment variable loading |

## 4. Set Up API Keys

The framework reads API keys from `.env/` files inside the repo. Create the directory and files:

```bash
mkdir -p "$ATLAS_ROOT/.env"
```

### Pinecone (Required)

```bash
echo "PINECONE_API_KEY=your_pinecone_key_here" > "$ATLAS_ROOT/.env/pinecone.env"
```

Get your key from [Pinecone Console](https://app.pinecone.io/) > API Keys.

### OpenAI (Required)

```bash
echo "OPENAI_API_KEY=your_openai_key_here" > "$ATLAS_ROOT/.env/openai.env"
```

Get your key from [OpenAI Platform](https://platform.openai.com/api-keys).

### Google Gemini (Optional - needed for Gemini chat backend)

```bash
echo "GOOGLE_API_KEY=your_google_key_here" > "$ATLAS_ROOT/.env/gemini.env"
```

Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Telegram (Optional - needed for Telegram integration)

```bash
cat > "$ATLAS_ROOT/.env/telegram.env" << 'EOF'
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF
```

Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram.

### Verify Keys

Quick check that everything is in place:

```bash
ls "$ATLAS_ROOT/.env/"
# Should show: pinecone.env  openai.env  gemini.env  telegram.env
```

## 5. Install Shell Aliases

Aliases let you run framework commands directly from anywhere in your terminal.

```bash
bash "$ATLAS_ROOT/setup_aliases.sh"
```

This adds the following aliases to your shell:

| Alias | Command | What It Does |
|-------|---------|--------------|
| `atlas-vectorize` | `atlas-vectorize /path/to/chunks` | Vectorize markdown chunks into Pinecone |
| `atlas-query` | `atlas-query "your search text"` | Quick semantic search |
| `atlas-ask` | `atlas-ask "question"` | Ask with AI reasoning + sources |
| `atlas-chat` | `atlas-chat --backend gpt` | Interactive chat with chosen backend |
| `atlas-stt` | `atlas-stt query "text"` | Search & send to Telegram |
| `atlas-send` | `atlas-send "message"` | Send message to Telegram |
| `atlas-bot` | `atlas-bot` | Start Telegram bot daemon |
| `atlas-sync` | `atlas-sync` | Sync chunk registry with filesystem |

After running the script, reload your shell:

```bash
source ~/.zshrc   # or source ~/.bashrc
```

## 6. Verify Installation

Open Python and test:

```bash
python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()
```

You should see:

```
Atlas Engine v2.0
  Index: rag-canonical-v1-emb3large:__default__
  Chunks: 0
  Root: /path/to/RAG
```

If you see this, the framework is ready.

Type `atlas.help()` to see all available commands.

## Common Flags Reference

These flags work across most CLI scripts:

| Flag | Used In | Example |
|------|---------|---------|
| `--namespace <ns>` | All query/vectorize scripts | `query "LFI" --namespace cve` |
| `--top-k <n>` | Query scripts | `rag-query "RCE" --top-k 10` |
| `--machine <name>` | Query scripts | `rag-query "privesc" --machine gavel` |
| `--domain <domain>` | Vectorize script | `vectorize notes.md --domain web` |
| `--tags <t1,t2>` | Vectorize script | `vectorize notes.md --tags exploit,lfi` |
| `--no-telegram` | `rag-query` | `rag-query "text" --no-telegram` |

### Namespace Presets

When using `--namespace`, you can use these preset names:

| Preset | Namespace | Description |
|--------|-----------|-------------|
| `root` | `__default__` | Default namespace |
| `cve` | `cve` | CVE and vulnerability data |
| `technique` | `technique` | Security techniques |
| `ctf` | `ctf` | CTF-specific content |
| `tools` | `tools` | Security tools |
| `payloads` | `payloads` | Exploit payloads |

Examples:

```bash
query "buffer overflow" --namespace cve
vectorize /path/to/chunks --namespace ctf
vectorize notes.md --domain web --tags exploit,lfi
```
