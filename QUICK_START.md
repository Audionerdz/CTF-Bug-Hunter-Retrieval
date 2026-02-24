# RAG Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Create Environment Files
```bash
cd /home/kali/Desktop/RAG

# Create .env directory
mkdir -p .env

# Add your Pinecone key
echo "PINECONE_API_KEY=your_key_here" > .env/pinecone.env

# Add your OpenAI key
echo "OPENAI_API_KEY=your_key_here" > .env/openai.env

# Add your Telegram credentials
cat > .env/telegram.env << 'ENVEOF'
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
ENVEOF
```

### 2. Verify Setup
```bash
python3 test_config.py
```

### 3. Test a Query
```bash
python3 src/query_agent.py "SQL injection" --top-k 3
```

## 📚 Common Commands

### Query Pinecone
```bash
# Basic query
python3 src/query_agent.py "RCE techniques"

# With options
python3 src/query_agent.py "LFI" --top-k 10 --machine gavel

# Send to Telegram
python3 src/rag_to_telegram.py "your query" 5
```

### Vectorize Chunks
```bash
# Vectorize a directory
python3 src/vectorize_canonical_openai.py /path/to/chunks

# Vectorize a single file
python3 src/vectorize_canonical_openai.py chunk.md

# Vectorize by folder name (in RAG directory)
python3 src/vectorize_canonical_openai.py default
```

### Telegram Integration
```bash
# Start the bot daemon
python3 src/telegram_bot.py

# Send message
python3 telegram_sender.py "Task completed"

# Send file
python3 telegram_sender.py --file /path/to/file "Caption"
```

## 🐛 Troubleshooting

### "API key not found" error
Check that files exist:
```bash
ls -la /home/kali/Desktop/RAG/.env/
cat /home/kali/Desktop/RAG/.env/pinecone.env
```

### Scripts not found
Make sure you're in the RAG directory:
```bash
cd /home/kali/Desktop/RAG
```

### Module import errors
Install dependencies:
```bash
pip install pinecone openai python-telegram-bot python-dotenv pyyaml
```

## 📖 Full Documentation

- **CONFIGURATION.md** - Complete setup and advanced usage
- **MIGRATION_SUMMARY.md** - What changed in the refactoring
- **config.py** - Configuration module reference

## 🚀 Ready to Go!

Once verified with `test_config.py`, you can:
1. Vectorize your CTF notes
2. Query them with the RAG
3. Receive results on Telegram
4. Build your knowledge base!

Happy hacking! 🎯
