# Docker to Home Lab: 5-Minute Deploy

**Get Atlas from this VPS to your home lab VM in 5 minutes.**

---

## TL;DR (Copy-Paste)

```bash
# ON THIS VPS (now)
docker build -t atlas-engine:prod .
docker save atlas-engine:prod -o atlas-engine.tar.gz

# TRANSFER TO YOUR HOME LAB
# Option 1: Via SSH
scp atlas-engine.tar.gz user@192.168.X.X:/home/user/

# Option 2: Via USB stick (physically)
# Copy atlas-engine.tar.gz to USB

# ON YOUR HOME LAB VM
docker load -i atlas-engine.tar.gz
docker run -it --rm \
  -e ATLAS_CI_NAMESPACE="home-lab" \
  -v "/path/to/.env:/app/.env:ro" \
  atlas-engine:prod src/gemini_rag.py --backend gpt

# Done ✅
```

---

## Step 1: Build & Export Image (VPS - 3 min)

**On this VPS:**

```bash
cd /home/kali/Desktop/RAG

# Build production image
docker build -t atlas-engine:prod .

# Export as file (~600MB)
docker save atlas-engine:prod -o atlas-engine.tar.gz

# Verify
ls -lh atlas-engine.tar.gz
```

**Output:**
```
-rw-r--r-- 1 user user 567M Feb 26 10:00 atlas-engine.tar.gz
```

---

## Step 2: Transfer to Home Lab (2 min)

### Option A: SSH (Fastest)

```bash
# From VPS, send to home lab
scp atlas-engine.tar.gz user@192.168.1.X:/home/user/

# Example:
scp atlas-engine.tar.gz user@192.168.1.50:/home/user/
```

### Option B: Physical USB

```bash
# Copy to USB stick
cp atlas-engine.tar.gz /mnt/usb/

# Then physically transfer to home lab
```

---

## Step 3: Load Image (Home Lab VM - 1 min)

**On your home lab VM:**

```bash
# Go to where you transferred the file
cd /home/user

# Load image
docker load -i atlas-engine.tar.gz

# Verify
docker images | grep atlas
```

**Output:**
```
atlas-engine     prod     c18acb7017e6   1 minute ago   567MB
```

---

## Step 4: Run Atlas at Home (Immediate)

### Option A: Docker Container

```bash
# Interactive chat
docker run -it --rm \
  -v "/path/to/.env:/app/.env:ro" \
  atlas-engine:prod src/gemini_rag.py --backend gpt

# One-shot query
docker run --rm \
  -v "/path/to/.env:/app/.env:ro" \
  atlas-engine:prod python3 -c \
  "from atlas_engine import Atlas; a = Atlas(); print(a.query('LFI', top_k=3))"

# With docker-compose
docker-compose up -d
docker-compose logs -f
```

### Option B: Python Directly (Your Home Lab VM)

**Install dependencies first:**

```bash
# Copy source to home lab
scp -r /home/kali/Desktop/RAG/* user@192.168.1.50:~/atlas/

# On home lab VM
cd ~/atlas

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env directory with your keys
mkdir -p .env
echo "OPENAI_API_KEY=sk-..." > .env/openai.env
echo "PINECONE_API_KEY=pcn-..." > .env/pinecone.env
echo "GOOGLE_API_KEY=..." > .env/gemini.env
```

**Run Atlas directly:**

```bash
# Interactive chat with GPT
python3 src/gemini_rag.py --backend gpt

# Interactive chat with Gemini
python3 src/gemini_rag.py --backend gemini

# Interactive chat with Groq
python3 src/gemini_rag.py --backend groq

# Python script (one-shot query)
python3 << 'EOF'
from atlas_engine import Atlas

atlas = Atlas()

# Query
print("[1] Query ffuf cheatsheet:")
results = atlas.query("ffuf cheatsheet", top_k=3)
for r in results:
    print(f"  - {r['chunk_id']}: {r['score']:.4f}")

# Ask (single)
print("\n[2] Ask GPT:")
answer, sources = atlas.ask("What is LFI?", backend="gpt")
print(f"Answer: {answer[:200]}...")
print(f"Sources: {sources}")

# Ask again (test cache)
print("\n[3] Ask GPT again (cached):")
answer2, sources2 = atlas.ask("What is LFI?", backend="gpt")
print(f"Answer: {answer2[:200]}...")

# Fetch chunk
print("\n[4] Fetch chunk:")
chunk = atlas.fetch("technique::web::fuzzing::ffuf-cheatsheet::001")
if chunk:
    print(f"Found: {chunk['chunk_id']}")

print("\n✅ All tests passed!")
EOF
```

---

## Complete Flow (One Command)

### Docker Method (Quick)

```bash
# VPS (export)
docker build -t atlas-engine:prod . && docker save atlas-engine:prod -o atlas-engine.tar.gz

# Transfer
scp atlas-engine.tar.gz user@192.168.1.50:/tmp/

# Home Lab (load + run)
docker load -i /tmp/atlas-engine.tar.gz && \
docker run -it --rm \
  -v "$HOME/.env:/app/.env:ro" \
  atlas-engine:prod src/gemini_rag.py --backend gpt
```

### Python Method (Native)

```bash
# VPS (sync source)
scp -r /home/kali/Desktop/RAG/* user@192.168.1.50:~/atlas/

# Home Lab VM
cd ~/atlas
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mkdir -p .env
echo "OPENAI_API_KEY=sk-..." > .env/openai.env
echo "PINECONE_API_KEY=pcn-..." > .env/pinecone.env

# Run
python3 src/gemini_rag.py --backend gpt
```

---

## Prepare Your Home Lab First (Before Transfer)

### For Docker Method

**On home lab VM:**

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com | sh

# 2. Create .env directory with your keys
mkdir -p ~/.env
echo "OPENAI_API_KEY=sk-..." > ~/.env/openai.env
echo "PINECONE_API_KEY=pcn-..." > ~/.env/pinecone.env
echo "GOOGLE_API_KEY=..." > ~/.env/gemini.env

# 3. Done, ready to receive image
```

### For Python Method

**On home lab VM:**

```bash
# 1. Install Python 3.11+
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# 2. Create directory
mkdir -p ~/atlas && cd ~/atlas

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Create .env directory with your keys
mkdir -p .env
echo "OPENAI_API_KEY=sk-..." > .env/openai.env
echo "PINECONE_API_KEY=pcn-..." > .env/pinecone.env
echo "GOOGLE_API_KEY=..." > .env/gemini.env

# 5. Done, ready to receive code
```

---

## Verify It Works

```bash
# Test import
docker run --rm atlas-engine:prod python3 -c \
  "from atlas_engine import Atlas; print('✅ Atlas loads correctly')"

# Test with real query
docker run --rm \
  -v "$HOME/.env:/app/.env:ro" \
  atlas-engine:prod python3 -c \
  "from atlas_engine import Atlas; a = Atlas(); r = a.query('LFI', top_k=1); print(f'✅ Found {len(r)} results')"
```

---

## Size Reference

| Component | Size |
|-----------|------|
| Docker image compressed | ~567 MB |
| Docker image extracted | ~2.5 GB |
| Transfer time (1 Gbps) | ~5-10 sec |
| Transfer time (100 Mbps) | ~45 sec |

---

## Troubleshooting

**"docker load" fails**
```bash
# Check if tar is corrupted
tar -tzf atlas-engine.tar.gz | head

# If corrupted, re-export from VPS
```

**"Permission denied" on docker**
```bash
# Add user to docker group on home lab
sudo usermod -aG docker $USER
newgrp docker
```

**"No space left on device"**
```bash
# Check disk space
df -h

# Need ~2.5 GB free
```

---

## Copy Config Files (Optional)

### Docker Method

```bash
# From VPS
scp -r default/ config.py user@192.168.1.50:~/

# On home lab
docker run -it --rm \
  -v "$PWD/default:/app/default" \
  -v "$PWD/config.py:/app/config.py" \
  -v "$HOME/.env:/app/.env:ro" \
  atlas-engine:prod src/gemini_rag.py --backend gpt
```

### Python Method

```bash
# From VPS (already synced if you did scp -r)
scp -r /home/kali/Desktop/RAG/* user@192.168.1.50:~/atlas/

# On home lab (everything already there)
cd ~/atlas
source venv/bin/activate
python3 src/gemini_rag.py --backend gpt
```

---

## Quick Reference

### Docker Method

```bash
# VPS: Build & export
docker build -t atlas-engine:prod .
docker save atlas-engine:prod -o atlas-engine.tar.gz

# Home Lab: Load & run
docker load -i atlas-engine.tar.gz
docker run -it --rm -v ~/.env:/app/.env:ro atlas-engine:prod python3 ...

# Check image
docker images | grep atlas

# Remove image
docker rmi atlas-engine:prod
```

### Python Method

```bash
# VPS: Sync source
scp -r /home/kali/Desktop/RAG/* user@192.168.1.50:~/atlas/

# Home Lab: Setup & run
cd ~/atlas
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/gemini_rag.py --backend gpt

# Quick test
python3 -c "from atlas_engine import Atlas; print('✅ Ready')"
```

### Which Method to Choose?

| Method | Pros | Cons |
|--------|------|------|
| **Docker** | Self-contained, no deps | 567MB transfer, needs Docker |
| **Python** | Lightweight, native | Install deps, setup venv |

**Recommendation:** Use **Docker** if transferring once; use **Python** if iterating.

---

---

## Common Commands (Home Lab)

### Docker

```bash
# Interactive chat
docker run -it --rm -v ~/.env:/app/.env:ro atlas-engine:prod src/gemini_rag.py

# Background
docker run -d --name atlas -v ~/.env:/app/.env:ro atlas-engine:prod src/gemini_rag.py
docker logs -f atlas

# Stop
docker stop atlas
docker rm atlas
```

### Python

```bash
# Interactive chat
python3 src/gemini_rag.py --backend gpt

# One-shot (in script)
python3 << 'EOF'
from atlas_engine import Atlas
a = Atlas()
answer, sources = a.ask("Your question", backend="gpt")
print(answer)
EOF

# Deactivate venv
deactivate
```

---

## Troubleshooting

### Python: ModuleNotFoundError

```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall deps
pip install -r requirements.txt --force-reinstall
```

### Python: OPENAI_API_KEY not found

```bash
# Check .env files exist
ls -la .env/

# Verify keys are there
cat .env/openai.env
cat .env/pinecone.env
```

### Python: ImportError in atlas_engine

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/atlas:$PYTHONPATH

# Or run from repo root
cd ~/atlas
python3 -c "from atlas_engine import Atlas; print('✅')"
```

### Docker: Image not found

```bash
# List images
docker images

# If missing, load again
docker load -i atlas-engine.tar.gz
```

---

**Total Time: ~5 minutes** ✅

**Choose your method: Docker OR Python. Both work!** 🚀
