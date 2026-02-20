# Pinecone Installation & Setup Guide

Complete step-by-step guide for setting up Pinecone from scratch.

## 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Text editor
- Internet connection
- Pinecone account (https://www.pinecone.io/)
- OpenAI account (for embeddings)

## 2. Create Pinecone Account

Visit https://www.pinecone.io/ and:

1. Click "Sign Up"
2. Use email or GitHub to create account
3. Verify email address
4. Accept terms of service
5. Access dashboard

## 3. Get Your API Key

From Pinecone dashboard:

1. Click on your profile (top right)
2. Navigate to "API Keys"
3. You'll see your default API key
4. Copy it safely (don't share!)

Format: `pcsk_xxxxxxxxxxxxxxxxxxxx`

## 4. Create Project Directories

```bash
mkdir -p ~/rag-system/{env,logs,chunks,scripts,pinecone}
cd ~/rag-system
```

## 5. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python3 -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

## 6. Install Required Packages

```bash
pip install --upgrade pip
pip install pinecone-client==3.2.1
pip install python-dotenv==1.0.0
pip install openai
pip install pydantic
pip install requests
pip install pyyaml
```

Verify installation:

```bash
pip list | grep -E "pinecone|openai|dotenv"
```

## 7. Create Configuration Files

### Create .env file

```bash
cat > .env << 'EOF'
# Pinecone Configuration
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_PROJECT=default

# OpenAI Configuration
OPENAI_API_KEY=your_openai_key_here

# Pinecone Index
PINECONE_INDEX=rag-canonical-v1-emb3large
PINECONE_NAMESPACE=default

# Vector Configuration
EMBEDDING_DIMENSION=3072
EMBEDDING_MODEL=text-embedding-3-large
METRIC=cosine
EOF
```

Replace with actual keys:
- `your_api_key_here` → Your Pinecone API key
- `your_openai_key_here` → Your OpenAI API key

**IMPORTANT:** Add `.env` to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

Never commit your API keys!

## 8. Test the Installation

Create `scripts/test_install.py`:

```python
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("Checking environment...")
api_key = os.getenv('PINECONE_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')

if api_key:
    print(f"✅ Pinecone API Key: {api_key[:10]}...***")
else:
    print("❌ Pinecone API Key not found")

if openai_key:
    print(f"✅ OpenAI API Key: {openai_key[:10]}...***")
else:
    print("❌ OpenAI API Key not found")

# Try importing libraries
try:
    from pinecone import Pinecone
    print("✅ Pinecone library imported")
except ImportError:
    print("❌ Pinecone library not found")

try:
    from openai import OpenAI
    print("✅ OpenAI library imported")
except ImportError:
    print("❌ OpenAI library not found")

print("\n✅ Installation successful!")
```

Run it:

```bash
python scripts/test_install.py
```

Expected output:

```
Checking environment...
✅ Pinecone API Key: pcsk_xxxx***
✅ OpenAI API Key: sk-xxxx***
✅ Pinecone library imported
✅ OpenAI library imported

✅ Installation successful!
```

## 9. Create Pinecone Index

Create `scripts/create_index.py`:

```python
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('PINECONE_INDEX')

pc = Pinecone(api_key=api_key)

# Check if index exists
indexes = [i['name'] for i in pc.list_indexes()]

if index_name in indexes:
    print(f"✅ Index '{index_name}' already exists")
else:
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"✅ Index created successfully")

# Verify
index = pc.Index(index_name)
stats = index.describe_index_stats()
print(f"   Total vectors: {stats['total_vector_count']}")
```

Run it:

```bash
python scripts/create_index.py
```

## 10. Verify Pinecone Connection

Create `scripts/verify_connection.py`:

```python
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('PINECONE_INDEX')

try:
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    stats = index.describe_index_stats()
    
    print("✅ CONNECTION SUCCESSFUL!")
    print(f"   Index: {index_name}")
    print(f"   Dimension: 3072")
    print(f"   Metric: cosine")
    print(f"   Vectors: {stats['total_vector_count']}")
    print(f"   Status: Ready")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run it:

```bash
python scripts/verify_connection.py
```

## 11. Final Directory Structure

You should have:

```
~/rag-system/
├── .env
├── .env.template
├── .gitignore
├── venv/
├── chunks/
├── scripts/
│   ├── test_install.py
│   ├── create_index.py
│   └── verify_connection.py
├── pinecone/
├── env/
└── logs/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pinecone'"

Activate virtual environment:
```bash
source venv/bin/activate
```

### "PINECONE_API_KEY not found"

Check `.env` file exists and contains API key.

### "Failed to connect to Pinecone"

- Verify API key is correct
- Check internet connection
- Ensure Pinecone account is active

### "Index already exists"

The index was created previously. Use it as-is.

## Next Steps

Now that installation is complete:

1. Read [Configuration Guide](configuration.md)
2. Learn [Pinecone Concepts](concepts.md)
3. Start chunking your knowledge using [Chunking Methodology](../2-chunking-methodology/guia-madre.md)

---

**Continue:** [Configuration Guide](configuration.md)
