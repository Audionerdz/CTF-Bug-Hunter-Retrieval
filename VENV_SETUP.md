# RAG Virtual Environment Setup

Your RAG framework now includes a complete, self-contained Python virtual environment with all dependencies pre-installed.

## Location

```
/home/kali/Desktop/RAG/venv/
```

## What's Included

**150 Python packages** including:

### Core Dependencies
- ✅ `pinecone` (7.3.0) - Vector Database
- ✅ `openai` (2.21.0) - OpenAI API
- ✅ `python-telegram-bot` (22.6) - Telegram Integration
- ✅ `langchain` (1.2.10) - LLM Framework
- ✅ `google-genai` (1.64.0) - Google Gemini API
- ✅ `langchain-google-genai` (4.2.1) - Gemini + LangChain
- ✅ `langchain-pinecone` (0.2.13) - Pinecone + LangChain
- ✅ `langchain-openai` (1.1.10) - OpenAI + LangChain

### Data & Processing
- beautifulsoup4
- pyyaml
- python-dotenv
- pandas
- numpy
- requests

### Full List
Run to see all 150 packages:
```bash
/home/kali/Desktop/RAG/venv/bin/pip list
```

## Activation Methods

### Method 1: Use the activation script
```bash
source /home/kali/Desktop/RAG/activate.sh
```

### Method 2: Direct activation
```bash
source /home/kali/Desktop/RAG/venv/bin/activate
```

### Method 3: Use venv Python directly
```bash
/home/kali/Desktop/RAG/venv/bin/python3 script.py
```

## Updated Aliases

### Old (using /root/.openskills/venv)
```bash
alias query='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'
```

### New (using RAG local venv)
```bash
alias query='/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'
```

## Scripts Using Local Venv

Update your aliases to use the local venv:

```bash
# Vectorize with local venv
alias vectorize='/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'

# Query with local venv
alias query='/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py'

# RAG Query with Telegram
alias rag-query='/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/query_agent.py'

# GeminiRag with local venv
alias GeminiRag='/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/gemini_rag.py'

# Telegram Bot with local venv
alias rag-bot='cd /home/kali/Desktop/RAG && nohup /home/kali/Desktop/RAG/venv/bin/python3 src/telegram_bot.py > telegram_bot.log 2>&1 &'
```

## Updating Aliases in ~/.zshrc

Add this to your `~/.zshrc`:

```bash
# RAG Virtual Environment
export RAG_PYTHON="/home/kali/Desktop/RAG/venv/bin/python3"

# RAG System Aliases (using local venv)
alias vectorize="$RAG_PYTHON /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py"
alias query="$RAG_PYTHON /home/kali/Desktop/RAG/src/query_fast.py"
alias rag-query="$RAG_PYTHON /home/kali/Desktop/RAG/src/query_agent.py"
alias GeminiRag="$RAG_PYTHON /home/kali/Desktop/RAG/src/gemini_rag.py"
alias rag-send="$RAG_PYTHON /home/kali/Desktop/RAG/telegram_sender.py"
alias rag-bot="cd /home/kali/Desktop/RAG && nohup $RAG_PYTHON src/telegram_bot.py > telegram_bot.log 2>&1 &"
alias rag-sync="$RAG_PYTHON /home/kali/Desktop/RAG/src/sync_registry.py"

# Activate RAG venv
alias rag-activate="source /home/kali/Desktop/RAG/activate.sh"
```

Then reload:
```bash
source ~/.zshrc
```

## Usage Examples

### With alias
```bash
# Automatically uses local venv
query "SQL injection"
vectorize /path/to/chunks
GeminiRag
```

### Without alias
```bash
# Explicitly use local venv
/home/kali/Desktop/RAG/venv/bin/python3 /home/kali/Desktop/RAG/src/query_fast.py "SQL injection"
```

### Activate and use
```bash
source /home/kali/Desktop/RAG/activate.sh
python3 src/query_agent.py "your query"
```

## Verification

```bash
# Check venv exists
ls -la /home/kali/Desktop/RAG/venv/bin/python3

# Check pip packages
/home/kali/Desktop/RAG/venv/bin/pip list | head -20

# Test activation
source /home/kali/Desktop/RAG/activate.sh
which python3  # Should show RAG venv path
```

## Benefits

✅ **Self-Contained**: RAG framework is 100% independent
✅ **No Dependencies**: Don't need /root/.openskills/venv anymore
✅ **Portable**: Copy entire RAG folder to any system with the venv
✅ **Isolated**: Your RAG venv doesn't affect system Python
✅ **Complete**: All 150 packages included - nothing to install

## Troubleshooting

### "venv: command not found"
Make sure to use the activation script:
```bash
source /home/kali/Desktop/RAG/activate.sh
```

### "ModuleNotFoundError"
Check that venv is properly activated:
```bash
which python3  # Should show /home/kali/Desktop/RAG/venv/bin/python3
```

### Scripts not finding modules
Use explicit venv Python path:
```bash
/home/kali/Desktop/RAG/venv/bin/python3 src/script.py
```

## Migration from /root/.openskills/venv

If you were using `/root/.openskills/venv`, update your aliases:

```bash
# Before
/root/.openskills/venv/bin/python3 script.py

# After
/home/kali/Desktop/RAG/venv/bin/python3 script.py
```

Or use the environment variable approach:
```bash
export RAG_PYTHON="/home/kali/Desktop/RAG/venv/bin/python3"
$RAG_PYTHON script.py
```

---

**Status**: ✅ Local venv with 150 packages installed  
**Updated**: February 24, 2026  
**Size**: ~500MB+ (includes all dependencies)
