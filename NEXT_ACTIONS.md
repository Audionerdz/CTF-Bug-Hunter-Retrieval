# Next Actions - RAG System Ready

Your RAG system is **fully operational**. Here's what you can do now:

## ✅ Immediate Actions (Right Now)

### 1. Test Pinecone Connection
```bash
python3 /home/kali/Desktop/RAG/src/query_agent.py "SQL injection" --top-k 3
```
Expected: 3 results about SQL injection techniques

### 2. Send Test Message to Telegram
```bash
python3 /home/kali/Desktop/RAG/telegram_sender.py "RAG system is working!"
```
Expected: Message appears in your Telegram chat

### 3. List Your Registered Chunks
```bash
python3 -c "import json; r=json.load(open('/home/kali/Desktop/RAG/chunk_registry.json')); print(f'Registered chunks: {len(r)}'); [print(f'  - {k}') for k in list(r.keys())[:5]]"
```
Expected: Shows list of registered chunks

## 🔧 Configuration Actions

### 1. Update Your Shell Aliases
```bash
# For Zsh (~/.zshrc)
cat >> ~/.zshrc << 'ALIASES'
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'
alias vectorize='python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias rag-query='python3 /home/kali/Desktop/RAG/src/query_agent.py'
alias rag-send='python3 /home/kali/Desktop/RAG/telegram_sender.py'
alias rag-bot='python3 /home/kali/Desktop/RAG/src/telegram_bot.py'
ALIASES

source ~/.zshrc
```

### 2. Secure Your .env Folder
```bash
# Add to .gitignore
echo ".env/" >> /home/kali/Desktop/RAG/.gitignore

# Restrict permissions (optional)
chmod 700 /home/kali/Desktop/RAG/.env/
```

### 3. Backup Your API Keys
```bash
# Create a backup
cp -r /home/kali/Desktop/RAG/.env/ ~/RAG_env_backup/

# Keep it safe!
```

## 📚 Usage Patterns

### Pattern 1: Quick Search
```bash
# Search your knowledge base
query "RCE in PHP"
query "SQL injection techniques"
query "privilege escalation"
```

### Pattern 2: Vectorize Custom Notes
```bash
# Create a directory with your notes
mkdir /home/kali/Desktop/RAG/my-ctf-notes
cp /path/to/your/notes/*.md /home/kali/Desktop/RAG/my-ctf-notes/

# Vectorize them
vectorize /home/kali/Desktop/RAG/my-ctf-notes

# Query them
query "technique from my notes"
```

### Pattern 3: Telegram Integration
```bash
# Send a query result to Telegram
rag-query "your query" --top-k 5

# Send a file to Telegram
rag-send --file /path/to/exploit.py "Found a 0-day!"

# Start the bot daemon
rag-bot &
```

### Pattern 4: Interactive Chat
```bash
# Start interactive RAG terminal
rag-chat

# Then ask questions interactively
# (requires langchain packages)
```

## 🚀 Advanced Usage

### 1. Filter by Machine/Domain
```bash
# Query only FACTS machine
python3 /home/kali/Desktop/RAG/src/query_agent.py "privesc" --machine facts

# Query only GAVEL machine
python3 /home/kali/Desktop/RAG/src/query_agent.py "web exploitation" --machine gavel
```

### 2. Adjust Top-K Results
```bash
# Get more results
python3 /home/kali/Desktop/RAG/src/query_agent.py "your query" --top-k 20

# Get fewer results
python3 /home/kali/Desktop/RAG/src/query_agent.py "your query" --top-k 3
```

### 3. Vectorize Specific Files
```bash
# Single file
vectorize /path/to/single/chunk.md

# Entire directory recursively
vectorize /path/to/chunks/directory/

# By folder name (searches in RAG root)
vectorize my-ctf-notes
```

### 4. Sync Registry
```bash
# If chunk_registry.json gets out of sync
python3 /home/kali/Desktop/RAG/src/sync_registry.py

# Or sync a specific directory
python3 /home/kali/Desktop/RAG/src/sync_registry.py /path/to/chunks
```

## 🔍 Monitoring & Troubleshooting

### Check Configuration Health
```bash
python3 /home/kali/Desktop/RAG/test_config.py
```

### View All API Keys Status
```bash
ls -la /home/kali/Desktop/RAG/.env/
for f in /home/kali/Desktop/RAG/.env/*.env; do
  echo "=== $(basename $f) ==="
  cat "$f"
done
```

### Debug Script Issues
```bash
# Run with verbose output
python3 -u /home/kali/Desktop/RAG/src/query_agent.py "test" -vv

# Check what config module sees
python3 /home/kali/Desktop/RAG/config.py
```

## 📚 Documentation Reference

When stuck, check:

1. **QUICK_START.md** - Quick reference
2. **CONFIGURATION.md** - Detailed setup
3. **MIGRATION_SUMMARY.md** - What changed
4. **Script docstrings** - `python3 script.py --help`

## 🎯 Workflow Examples

### CTF Notes Processing
```bash
# 1. Create your notes
mkdir /home/kali/Desktop/RAG/ctf-2024
# Add .md files...

# 2. Vectorize
vectorize /home/kali/Desktop/RAG/ctf-2024

# 3. Search during CTF
query "SQL injection in $_GET parameter"

# 4. Share findings
rag-send --file /path/to/exploit "Found vulnerability!"
```

### Knowledge Base Expansion
```bash
# 1. Add new technique documentation
vim /home/kali/Desktop/RAG/chunks/new-technique.md

# 2. Vectorize it
vectorize /home/kali/Desktop/RAG/chunks

# 3. It's immediately searchable
query "new technique"
```

### Telegram Bot Daemon
```bash
# 1. Start bot in background
rag-bot &

# 2. Query from Telegram
# Send: /q SQL injection 10
# Get: Results in Telegram

# 3. Send findings
# Send: /send exploit findings

# 4. Stop when done
pkill -f rag_bot.py
```

## ⚠️ Common Issues & Solutions

### "API key not found" error
**Solution**: Check `.env/` files exist and have content
```bash
cat /home/kali/Desktop/RAG/.env/pinecone.env
```

### Scripts can't find config
**Solution**: Run from RAG directory or use absolute paths
```bash
cd /home/kali/Desktop/RAG
python3 src/query_agent.py "query"
```

### Telegram not working
**Solution**: Verify credentials
```bash
cat /home/kali/Desktop/RAG/.env/telegram.env
# Should have TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

### Chunks not found after vectorizing
**Solution**: Sync the registry
```bash
python3 /home/kali/Desktop/RAG/src/sync_registry.py
```

## 🎉 You're Ready!

Your RAG system is **100% operational**. Start with:

```bash
# Simple test
query "SQL injection"

# More advanced
python3 /home/kali/Desktop/RAG/src/query_agent.py "your research" --top-k 10 --machine gavel

# Full automation
rag-bot &  # Run in background
```

**Happy hacking!** 🚀

---

**Last Updated**: February 24, 2026  
**System Status**: 🟢 Fully Operational  
**Documentation**: Complete
