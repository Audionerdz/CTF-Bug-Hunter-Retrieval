# Common Issues & Solutions

**General troubleshooting guide for Atlas Engine.**

---

## API Keys & Secrets

### "OPENAI_API_KEY not found"

**Cause:** Environment variable not set or .env file missing

**Solution:**

```bash
# Create .env directory
mkdir -p ~/.env

# Add OpenAI key
echo "OPENAI_API_KEY=sk-..." > ~/.env/openai.env

# Verify
cat ~/.env/openai.env
```

### "PINECONE_API_KEY not found"

**Cause:** Pinecone credentials missing

**Solution:**

```bash
# Create Pinecone env
echo "PINECONE_API_KEY=pcn-..." > ~/.env/pinecone.env

# Verify
cat ~/.env/pinecone.env
```

### "API key is invalid or expired"

**Cause:** Key is wrong or no longer valid

**Solution:**

1. Go to https://platform.openai.com/api-keys (OpenAI)
2. Go to https://app.pinecone.io (Pinecone)
3. Generate new key
4. Update .env file:
   ```bash
   echo "OPENAI_API_KEY=new-key" > ~/.env/openai.env
   ```
5. Restart application

### "Permission denied accessing .env files"

**Solution:**

```bash
# Fix permissions
chmod 600 ~/.env/*.env
chmod 755 ~/.env

# Verify
ls -la ~/.env/
```

---

## Python Environment

### "ModuleNotFoundError: No module named 'atlas_engine'"

**Cause:** Virtual environment not activated or dependencies not installed

**Solution:**

```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python3 -c "from atlas_engine import Atlas; print('✅ OK')"
```

### "ModuleNotFoundError: No module named 'langchain'"

**Cause:** Dependencies not installed

**Solution:**

```bash
# Activate venv first
source venv/bin/activate

# Reinstall all
pip install -r requirements.txt --force-reinstall

# Check
pip list | grep langchain
```

### "ImportError in atlas_engine"

**Cause:** Missing import or Python path issue

**Solution:**

```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/atlas:$PYTHONPATH

# Verify
python3 -c "import sys; print(sys.path)"

# Or run from repo root
cd /path/to/atlas
python3 src/gemini_rag.py
```

### "venv: command not found"

**Cause:** Python venv module not installed

**Solution:**

```bash
# Install python3-venv
sudo apt-get install python3-venv

# Then create venv
python3 -m venv venv
source venv/bin/activate
```

---

## Network & Connectivity

### "Connection refused (127.0.0.1:11434)"

**Cause:** Ollama not running (if using Ollama backend)

**Solution:**

```bash
# Start Ollama
ollama serve

# Or run in background
ollama serve &

# Check if running
curl http://localhost:11434/api/tags
```

### "Name or service not known (network error)"

**Cause:** No internet or DNS issue

**Solution:**

```bash
# Check internet
ping google.com

# Check DNS
nslookup api.openai.com

# For VPN/Proxy, set
export https_proxy=http://proxy:port
```

### "Request timeout (API not responding)"

**Cause:** API server slow or network latency

**Solution:**

```bash
# Increase timeout (in code)
# Or retry:
python3 << 'EOF'
import time
from atlas_engine import Atlas

atlas = Atlas()
retries = 3
for i in range(retries):
    try:
        result = atlas.query("test")
        break
    except Exception as e:
        if i < retries - 1:
            time.sleep(2)  # Wait 2 seconds
        else:
            raise
EOF
```

---

## Pinecone Issues

### "Index not found"

**Cause:** Pinecone index doesn't exist

**Solution:**

```bash
# Check existing indexes
# Go to: https://app.pinecone.io

# Create if missing:
# Name: rag-canonical-v1-emb3large
# Dimension: 3072
# Metric: cosine

# Or in code:
from pinecone import Pinecone

pc = Pinecone(api_key="your-key")
pc.create_index("rag-canonical-v1-emb3large", dimension=3072)
```

### "Vector dimension mismatch"

**Cause:** Embedding model generates wrong dimension

**Solution:**

```bash
# Check config.py
grep EMBEDDING_DIM config.py

# Should be: 3072

# Verify in Pinecone:
# Index must also have 3072 dimensions
```

### "Quota exceeded"

**Cause:** Too many API calls or storage full

**Solution:**

```bash
# Check usage: https://app.pinecone.io

# Delete old namespaces
python3 << 'EOF'
from pinecone import Pinecone

pc = Pinecone(api_key="your-key")
idx = pc.Index("rag-canonical-v1-emb3large")

# Delete namespace
idx.delete(delete_all=True, namespace="old-namespace")
EOF
```

---

## Memory & Performance

### "Out of memory" / "MemoryError"

**Cause:** Processing too much data at once

**Solution:**

```bash
# Reduce chunk size
# In vectorizer:
vec = Vectorizer()
vec.batch_size = 10  # Reduce batch

# Or reduce queries
atlas.query("something", top_k=3)  # Instead of top_k=100
```

### "Slow performance / Hanging"

**Cause:** Large embeddings or network latency

**Solution:**

```bash
# Check available memory
free -h

# Monitor process
htop

# Reduce scope
# - Fewer top_k results
# - Smaller namespaces
# - Faster embedding model (if available)
```

---

## File System Issues

### "Permission denied" reading files

**Solution:**

```bash
# Check permissions
ls -la /path/to/file

# Fix permissions
chmod 644 /path/to/file

# Or for directories
chmod 755 /path/to/dir
```

### "File not found"

**Solution:**

```bash
# Check file exists
ls -la /path/to/file

# Use absolute path
python3 -c "from pathlib import Path; print(Path('/your/file').absolute())"
```

### "Disk space full"

**Solution:**

```bash
# Check disk usage
df -h

# Clean up
rm -rf ~/.cache/pip
rm -rf __pycache__

# Or
find . -name "__pycache__" -type d -exec rm -rf {} +
```

---

## Debugging Tips

### Get verbose output

```bash
# Python
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"

# Atlas
export DEBUG=1
python3 src/gemini_rag.py
```

### Test each component

```bash
# Test OpenAI key
python3 -c "from openai import OpenAI; OpenAI(api_key='your-key').models.list()"

# Test Pinecone
python3 -c "from pinecone import Pinecone; Pinecone(api_key='your-key').list_indexes()"

# Test imports
python3 -c "from atlas_engine import Atlas; print('✅')"
```

### Check logs

```bash
# Last 20 lines
tail -20 ~/.logs/atlas.log

# Follow logs
tail -f ~/.logs/atlas.log

# Search logs
grep ERROR ~/.logs/atlas.log
```

---

## Still Broken?

1. Check exact error message
2. Search in relevant guide:
   - [GitHub Actions Errors](./GITHUB_ACTIONS_ERRORS.md)
   - [Docker Issues](./DOCKER_ISSUES.md)
3. Check [GitHub Issues](https://github.com/yourusername/atlas/issues)
4. Post error with full traceback

---

**Last updated:** February 2026
**Atlas Engine Version:** 2.0+
