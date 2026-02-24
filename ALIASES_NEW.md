# Updated RAG Aliases

## Old Aliases (Still Working)

Your existing aliases will continue to work because `/root/.openskills/venv/bin/python3` points to `/usr/bin/python3`:

```bash
alias vectorize='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'
alias rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'
```

✅ These will continue to work as-is.

## Recommended: Simplified Aliases

However, we recommend updating to the **simplified versions** that don't depend on the old venv path:

```bash
# Vectorize chunks
alias vectorize='python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'

# Query with results to terminal
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'

# Query and send to Telegram
alias rag-query='python3 /home/kali/Desktop/RAG/src/query_agent.py'

# ✨ Interactive RAG with Gemini
alias GeminiRag='python3 /home/kali/Desktop/RAG/src/gemini_rag.py'

# Send to Telegram
alias rag-send='python3 /home/kali/Desktop/RAG/telegram_sender.py'

# Telegram bot daemon
alias rag-bot='python3 /home/kali/Desktop/RAG/src/telegram_bot.py'

# Sync chunk registry
alias rag-sync='python3 /home/kali/Desktop/RAG/src/sync_registry.py'
```

### Setup Instructions

**1. Add to your shell config:**

For Bash (`~/.bashrc`):
```bash
cat >> ~/.bashrc << 'ALIASES'
# RAG System Aliases
alias vectorize='python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'
alias rag-query='python3 /home/kali/Desktop/RAG/src/query_agent.py'
alias GeminiRag='python3 /home/kali/Desktop/RAG/src/gemini_rag.py'
alias rag-send='python3 /home/kali/Desktop/RAG/telegram_sender.py'
alias rag-bot='python3 /home/kali/Desktop/RAG/src/telegram_bot.py'
alias rag-sync='python3 /home/kali/Desktop/RAG/src/sync_registry.py'
ALIASES
source ~/.bashrc
```

For Zsh (`~/.zshrc`):
```bash
cat >> ~/.zshrc << 'ALIASES'
# RAG System Aliases
alias vectorize='python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'
alias rag-query='python3 /home/kali/Desktop/RAG/src/query_agent.py'
alias GeminiRag='python3 /home/kali/Desktop/RAG/src/gemini_rag.py'
alias rag-send='python3 /home/kali/Desktop/RAG/telegram_sender.py'
alias rag-bot='python3 /home/kali/Desktop/RAG/src/telegram_bot.py'
alias rag-sync='python3 /home/kali/Desktop/RAG/src/sync_registry.py'
ALIASES
source ~/.zshrc
```

**2. Reload your shell:**
```bash
# For bash
source ~/.bashrc

# For zsh
source ~/.zshrc
```

**3. Verify aliases are loaded:**
```bash
alias | grep -E 'rag|vectorize|query'
```

## Usage Examples

```bash
# Vectorize a directory
vectorize /path/to/chunks

# Quick query
query "SQL injection"

# Query with Telegram integration
rag-query "RCE techniques" --top-k 10 --machine gavel

# Interactive chat
rag-chat

# Send message to Telegram
rag-send "Task completed"

# Send file to Telegram
rag-send --file /path/to/file "Caption"

# Start bot daemon
rag-bot

# Sync chunk registry
rag-sync
```

## Comparison

| Alias | Old Path | New Path | Works? |
|-------|----------|----------|--------|
| `vectorize` | `/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py` | `python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py` | ✅ Both work |
| `query` | `/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py` | `python3 /home/kali/Desktop/RAG/src/query_fast.py` | ✅ Both work |
| `rag-chat` | `/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py` | `python3 /home/kali/Desktop/RAG/src/rag_terminal.py` | ✅ Both work |

## Why Update?

✅ **Simpler** - Don't need to maintain the old venv path  
✅ **Cleaner** - Uses system Python or active venv  
✅ **Future-proof** - Works even if `/root/.openskills/` is removed  
✅ **Portable** - Works on any system with Python 3  

## Troubleshooting

### Aliases not working after update
```bash
# Reload your shell configuration
source ~/.bashrc    # or ~/.zshrc
```

### Command not found
```bash
# Verify alias is set
alias query

# If not set, add it manually
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'
```

### Wrong Python version
```bash
# Check which Python is being used
which python3

# If needed, use explicit Python
/usr/bin/python3 /home/kali/Desktop/RAG/src/query_agent.py "query"
```

## Summary

- ✅ **Old aliases will keep working** (they use system Python via the venv symlink)
- ✅ **New simplified aliases recommended** (no venv path dependency)
- ✅ **Easy migration** (just add the new aliases to your shell config)
