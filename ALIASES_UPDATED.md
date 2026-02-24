# Updated RAG Aliases - GeminiRag Renamed

All aliases have been updated with the new naming convention.

## Current Aliases (Use These)

```bash
# Vectorize chunks
alias vectorize='python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'

# Query with results to terminal
alias query='python3 /home/kali/Desktop/RAG/src/query_fast.py'

# Query and send to Telegram
alias rag-query='python3 /home/kali/Desktop/RAG/src/query_agent.py'

# ✨ Interactive RAG with Gemini (RENAMED)
alias GeminiRag='python3 /home/kali/Desktop/RAG/src/gemini_rag.py'

# Send to Telegram
alias rag-send='python3 /home/kali/Desktop/RAG/telegram_sender.py'

# Telegram bot daemon
alias rag-bot='python3 /home/kali/Desktop/RAG/src/telegram_bot.py'

# Sync chunk registry
alias rag-sync='python3 /home/kali/Desktop/RAG/src/sync_registry.py'
```

## Setup Instructions

### For Bash (~/.bashrc)
```bash
cat >> ~/.bashrc << 'ALIASES'
# RAG System Aliases (Updated)
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

### For Zsh (~/.zshrc)
```bash
cat >> ~/.zshrc << 'ALIASES'
# RAG System Aliases (Updated)
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

## Usage Examples

### Previous Way (No Longer Works)
```bash
rag-chat  # ❌ This alias no longer exists
```

### New Way
```bash
# Start interactive RAG with Gemini
GeminiRag

# Then ask questions interactively
```

## What Changed

| Old | New | Status |
|-----|-----|--------|
| `rag-chat` | `GeminiRag` | ✨ Renamed |
| `rag_terminal.py` | `gemini_rag.py` | ✨ Renamed |

All other aliases remain the same.

## Why This Name?

`GeminiRag` better reflects:
- 🔮 The interactive chat nature
- 📱 Powered by Google Gemini LLM
- 🧠 The RAG (Retrieval Augmented Generation) functionality
- 🎯 Clear intent: Gemini-powered RAG interface

## Verification

```bash
# Check alias is set
alias GeminiRag

# Check script exists
ls -la /home/kali/Desktop/RAG/src/gemini_rag.py

# Test it
GeminiRag
```

---

**Updated**: February 24, 2026
