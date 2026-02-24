# RAG System Configuration Guide

## Overview

The RAG system has been refactored to use **centralized configuration** instead of hardcoded paths. All environment files and settings are now managed from within the RAG directory (`/home/kali/Desktop/RAG`).

## Directory Structure

```
/home/kali/Desktop/RAG/
├── config.py                    # Centralized configuration module
├── .env/                        # Environment files directory
│   ├── pinecone.env            # Pinecone API key
│   ├── openai.env              # OpenAI API key
│   └── telegram.env            # Telegram Bot credentials
├── src/
│   ├── query_agent.py
│   ├── vectorize_canonical_openai.py
│   ├── telegram_bot.py
│   ├── query_fast.py
│   └── ... (other scripts)
└── telegram_sender.py
```

## Setup Instructions

### 1. Create Environment Files

Create the `.env/` directory and populate with your API keys:

```bash
# Create directory if it doesn't exist
mkdir -p /home/kali/Desktop/RAG/.env/

# Add your Pinecone API key
echo "PINECONE_API_KEY=your_pinecone_key_here" > /home/kali/Desktop/RAG/.env/pinecone.env

# Add your OpenAI API key
echo "OPENAI_API_KEY=your_openai_key_here" > /home/kali/Desktop/RAG/.env/openai.env

# Add your Telegram credentials
cat > /home/kali/Desktop/RAG/.env/telegram.env << 'EOF'
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
EOF

# Optional: Add Google API key for Gemini support
echo "GOOGLE_API_KEY=your_google_api_key_here" > /home/kali/Desktop/RAG/.env/gemini.env
```

### 2. Verify Configuration

Test the configuration setup:

```bash
cd /home/kali/Desktop/RAG
python3 config.py
```

Expected output:
```
📋 RAG Configuration:
  RAG_ROOT: /home/kali/Desktop/RAG
  ENV_DIR: /home/kali/Desktop/RAG/.env
  INDEX_NAME: rag-canonical-v1-emb3large
  EMBEDDING_MODEL: text-embedding-3-large
  EMBEDDING_DIM: 3072

✅ Configuration initialized at /home/kali/Desktop/RAG
```

## Using the Scripts

All scripts now use the centralized configuration. You can run them from any directory:

### Vectorization

```bash
# Vectorize a directory
python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /path/to/chunks

# Vectorize a specific file
python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /path/to/chunk.md

# Vectorize by simple name (searches in RAG_ROOT)
python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py my_chunks
```

### Querying

```bash
# Query the RAG
python3 /home/kali/Desktop/RAG/src/query_agent.py "your query" --top-k 5

# Query with machine filter
python3 /home/kali/Desktop/RAG/src/query_agent.py "privesc" --machine gavel

# Fast query
python3 /home/kali/Desktop/RAG/src/query_fast.py "SQL injection"

# Query specific chunk
python3 /home/kali/Desktop/RAG/src/query_chunk.py "technique::web::sql::injection::001"
```

### Telegram Bot

```bash
# Start the Telegram bot
python3 /home/kali/Desktop/RAG/src/telegram_bot.py

# Send message to Telegram
python3 /home/kali/Desktop/RAG/telegram_sender.py "Test message"

# Send file to Telegram
python3 /home/kali/Desktop/RAG/telegram_sender.py --file /path/to/file "Caption"
```

### Terminal Chat

```bash
# Start interactive RAG terminal (requires langchain)
python3 /home/kali/Desktop/RAG/src/rag_terminal.py
```

## Configuration Module (config.py)

The `config.py` module provides centralized access to all configuration:

```python
import config

# Get directories
rag_root = config.RAG_ROOT  # /home/kali/Desktop/RAG
env_dir = config.ENV_DIR    # /home/kali/Desktop/RAG/.env
chunk_registry = config.CHUNK_REGISTRY  # /home/kali/Desktop/RAG/chunk_registry.json

# Get API keys
pinecone_key = config.get_pinecone_key()
openai_key = config.get_openai_key()
telegram_token, telegram_chat_id = config.get_telegram_keys()

# Initialize environment
config.init_environment()
```

## Migrating from Old Structure

If you previously used `/root/.openskills/env/`, follow these steps:

1. **Copy your existing env files** to the new location:
   ```bash
   cp /root/.openskills/env/pinecone.env /home/kali/Desktop/RAG/.env/
   cp /root/.openskills/env/openai.env /home/kali/Desktop/RAG/.env/
   cp /root/.openskills/env/telegram.env /home/kali/Desktop/RAG/.env/
   # Optional:
   cp /root/.openskills/env/gemini.env /home/kali/Desktop/RAG/.env/
   ```

2. **Verify the files exist**:
   ```bash
   ls -la /home/kali/Desktop/RAG/.env/
   ```

3. **Test a script** to ensure it works:
   ```bash
   python3 /home/kali/Desktop/RAG/src/query_agent.py "test query" --top-k 3
   ```

## Troubleshooting

### "PINECONE_API_KEY not found"

**Solution**: Create `/home/kali/Desktop/RAG/.env/pinecone.env` with your API key:
```bash
echo "PINECONE_API_KEY=your_key_here" > /home/kali/Desktop/RAG/.env/pinecone.env
```

### "OPENAI_API_KEY not found"

**Solution**: Create `/home/kali/Desktop/RAG/.env/openai.env` with your API key:
```bash
echo "OPENAI_API_KEY=your_key_here" > /home/kali/Desktop/RAG/.env/openai.env
```

### "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found"

**Solution**: Create `/home/kali/Desktop/RAG/.env/telegram.env` with both values:
```bash
cat > /home/kali/Desktop/RAG/.env/telegram.env << 'EOF'
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF
```

### Scripts can't find configuration

**Solution**: Ensure you're running scripts from within the RAG directory or use absolute paths:
```bash
cd /home/kali/Desktop/RAG
python3 src/query_agent.py "your query"
```

## Updated Scripts

The following scripts have been refactored to use centralized configuration:

- ✅ `config.py` - New centralized configuration module
- ✅ `src/query_agent.py` - Uses config.get_pinecone_key(), config.get_openai_key()
- ✅ `src/vectorize_canonical_openai.py` - Uses config.RAG_ROOT, config.CHUNK_REGISTRY
- ✅ `src/telegram_bot.py` - Uses config.get_telegram_keys(), config.INDEX_NAME
- ✅ `src/query_fast.py` - Uses config.RAG_ROOT, config.CHUNK_REGISTRY
- ✅ `src/query_canonical_openai.py` - Uses config.get_pinecone_key(), config.get_openai_key()
- ✅ `src/query_chunk.py` - Uses config.get_pinecone_key()
- ✅ `src/query_gemini.py` - Uses config.ENV_DIR
- ✅ `src/rag_terminal.py` - Uses config.ENV_DIR
- ✅ `src/rag_to_telegram.py` - Uses config.get_pinecone_key(), config.get_openai_key()
- ✅ `src/sync_registry.py` - Uses config.RAG_ROOT, config.CHUNK_REGISTRY
- ✅ `telegram_sender.py` - Uses config.get_telegram_keys()

## Environment File Format

All `.env` files follow the simple `KEY=VALUE` format:

```bash
# Example: pinecone.env
PINECONE_API_KEY=abc123def456ghi789

# Example: openai.env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxx

# Example: telegram.env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=9876543210

# Example: gemini.env
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Benefits of This Approach

✅ **Single Source of Truth**: All configuration in one place  
✅ **Portable**: Everything contained within `/home/kali/Desktop/RAG/`  
✅ **Safe**: No hardcoded paths in scripts  
✅ **Easy to Backup**: Just copy the `.env/` directory  
✅ **Multi-Machine Ready**: Can work from any system  
✅ **Scalable**: Easy to add new configuration options

## Future Enhancements

- Support for environment variable overrides
- Configuration profiles (dev, production, etc.)
- Encrypted credential storage
- Configuration validation and health checks
