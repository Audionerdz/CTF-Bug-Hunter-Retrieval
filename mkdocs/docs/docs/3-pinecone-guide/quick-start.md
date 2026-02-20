# Quick Start with Pinecone

Get up and running with Pinecone in 15 minutes.

## Prerequisites

- Linux, Mac, or Windows
- Python 3.8+
- Pinecone account (free tier is fine)
- OpenAI account (for embeddings)

## Step 1: Create Your Pinecone Account

1. Visit https://www.pinecone.io/
2. Click "Sign Up"
3. Create account with email
4. Verify email
5. Navigate to API Keys in dashboard
6. Copy your API key (looks like: `pcsk_xxxxxxxxxxxxxx`)

## Step 2: Set Up Your Project

Create directories:

```bash
mkdir -p ~/rag-project/{chunks,scripts,config}
cd ~/rag-project
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install pinecone-client==3.2.1 python-dotenv openai
```

## Step 3: Configure Environment

Create `.env` file in your project:

```bash
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX=rag-canonical-v1-emb3large
```

Replace `your_api_key_here` with your actual API key.

## Step 4: Create Your First Index

Create `scripts/create_index.py`:

```python
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')

pc = Pinecone(api_key=api_key)

# Create index
index_name = "rag-canonical-v1-emb3large"
try:
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"✅ Index '{index_name}' created")
except Exception as e:
    print(f"⚠️ Index may already exist: {e}")
```

Run it:

```bash
python scripts/create_index.py
```

## Step 5: Verify Connection

Create `scripts/test_connection.py`:

```python
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')

pc = Pinecone(api_key=api_key)

# List indexes
indexes = pc.list_indexes()
print(f"✅ Connected! Available indexes: {len(indexes)}")
for idx in indexes:
    print(f"  - {idx['name']}")
```

Run it:

```bash
python scripts/test_connection.py
```

Expected output:

```
✅ Connected! Available indexes: 1
  - rag-canonical-v1-emb3large
```

## Step 6: First Vector Upload

After completing these steps, you have a working Pinecone setup!

## Next Steps

1. Create chunks following the methodology
2. Generate embeddings with OpenAI API
3. Batch upload to Pinecone
4. Build semantic search

---

**Ready to dive deeper?** See [Installation & Setup](installation.md)
