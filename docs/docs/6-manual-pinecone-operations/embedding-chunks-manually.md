# Embedding Chunks Manually

Before upserting vectors to Pinecone, you must first **embed your chunks** using the OpenAI API. This guide shows how to create 3072-dimensional embeddings for your text chunks.

## Prerequisites

- **OpenAI API Key**: Set in `OPENAI_API_KEY` environment variable
- **Python 3.9+**: With `openai` library installed
- **Your chunks**: In JSON or structured format

### Verify Setup

```bash
# Check OpenAI API key
echo $OPENAI_API_KEY | head -c 10

# Check Python and openai library
python3 --version
python3 -c "import openai; print(openai.__version__)"
```

If the library is missing:
```bash
pip install openai
```

## Method 1: Quick Embedding via Python CLI

Embed a single piece of text immediately:

```bash
python3 << 'EOF'
import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your text
text = "Local File Inclusion (LFI) allows attackers to include files from the server"

# Create embedding
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=text
)

# Extract embedding
embedding = response.data[0].embedding

print(f"Text: {text}")
print(f"Embedding dimension: {len(embedding)}")
print(f"First 10 values: {embedding[:10]}")
EOF
```

**Output:**
```
Text: Local File Inclusion (LFI) allows attackers to include files from the server
Embedding dimension: 3072
First 10 values: [0.034, -0.012, 0.045, -0.023, ...]
```

## Method 2: Embed Multiple Chunks (Batch)

Create embeddings for multiple chunks at once:

```bash
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Your chunks (from FACTS machine for example)
chunks = [
    {
        "id": "chunk_facts_001",
        "text": "LFI vulnerabilities allow reading arbitrary files",
        "source": "FACTS HTB",
        "machine": "facts"
    },
    {
        "id": "chunk_facts_002",
        "text": "RCE through PHP include() function exploitation",
        "source": "FACTS HTB",
        "machine": "facts"
    },
    {
        "id": "chunk_facts_003",
        "text": "Bypass PHP filters with null bytes and encoding",
        "source": "FACTS HTB",
        "machine": "facts"
    }
]

# Extract just the text for embedding
texts = [chunk["text"] for chunk in chunks]

print(f"Embedding {len(chunks)} chunks...")

# Create embeddings for all chunks at once
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Combine chunks with their embeddings
vectors = []
for chunk, embedding_obj in zip(chunks, response.data):
    embedding = embedding_obj.embedding
    vectors.append({
        "id": chunk["id"],
        "values": embedding,
        "metadata": {
            "text": chunk["text"],
            "source": chunk["source"],
            "machine": chunk["machine"]
        }
    })

print(f"Created {len(vectors)} vectors")
print(f"Sample vector:")
print(f"  ID: {vectors[0]['id']}")
print(f"  Dimension: {len(vectors[0]['values'])}")
print(f"  Metadata: {vectors[0]['metadata']}")

# Save for later upserting
with open("embeddings.json", "w") as f:
    json.dump(vectors, f, indent=2)
print("\nEmbeddings saved to embeddings.json")
EOF
```

**Output:**
```
Embedding 3 chunks...
Created 3 vectors
Sample vector:
  ID: chunk_facts_001
  Dimension: 3072
  Metadata: {'text': 'LFI vulnerabilities...', 'source': 'FACTS HTB', 'machine': 'facts'}

Embeddings saved to embeddings.json
```

## Method 3: Embed from a JSON File

If your chunks are already in a JSON file:

```bash
# Example chunk file structure
cat > chunks.json << 'EOF'
[
  {
    "id": "chunk_facts_004",
    "text": "Use /proc/self/environ to read environment variables",
    "machine": "facts",
    "source": "FACTS HTB"
  },
  {
    "id": "chunk_facts_005",
    "text": "Chained LFI + filter bypass = Remote Code Execution",
    "machine": "facts",
    "source": "FACTS HTB"
  }
]
EOF

# Now embed them
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load chunks from file
with open("chunks.json") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

print(f"Embedding {len(chunks)} chunks from file...")

# Create embeddings
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Create vector objects
vectors = []
for chunk, embedding_obj in zip(chunks, response.data):
    vectors.append({
        "id": chunk["id"],
        "values": embedding_obj.embedding,
        "metadata": {
            "text": chunk["text"],
            "machine": chunk["machine"],
            "source": chunk["source"]
        }
    })

# Save
with open("embeddings_output.json", "w") as f:
    json.dump(vectors, f)

print(f"✓ Embedded {len(vectors)} chunks")
print(f"✓ Saved to embeddings_output.json")
EOF
```

## Method 4: Embed with Custom Metadata

Add rich metadata for better searchability:

```bash
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chunk with metadata
chunk = {
    "id": "chunk_gavel_001",
    "text": "YAML injection in configuration parsing",
    "machine": "gavel",
    "source": "GAVEL HTB",
    "technique": "injection",
    "severity": "high",
    "tags": ["yaml", "config", "injection", "rce"],
    "date_added": "2026-02-13"
}

# Create embedding
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=[chunk["text"]]
)

# Vector with full metadata
vector = {
    "id": chunk["id"],
    "values": response.data[0].embedding,
    "metadata": {
        "text": chunk["text"],
        "machine": chunk["machine"],
        "source": chunk["source"],
        "technique": chunk["technique"],
        "severity": chunk["severity"],
        "tags": chunk["tags"],
        "date_added": chunk["date_added"]
    }
}

print(json.dumps(vector, indent=2))
EOF
```

## Real-World Example: Embed FACTS Chunks

Let's embed actual FACTS machine exploration chunks:

```bash
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Real FACTS HTB chunks
facts_chunks = [
    {
        "id": "facts_001",
        "text": "Nmap scan reveals Apache 2.4.41 on port 80 and SSH on port 22",
        "machine": "facts",
        "technique": "reconnaissance"
    },
    {
        "id": "facts_002",
        "text": "curl -I http://target shows PHP application with include parameter",
        "machine": "facts",
        "technique": "reconnaissance"
    },
    {
        "id": "facts_003",
        "text": "LFI vulnerability: ?include=../../../etc/passwd",
        "machine": "facts",
        "technique": "exploitation"
    },
    {
        "id": "facts_004",
        "text": "RCE via log poisoning: injecting code into Apache access.log",
        "machine": "facts",
        "technique": "exploitation"
    },
    {
        "id": "facts_005",
        "text": "Privilege escalation using sudo -l and kernel exploit",
        "machine": "facts",
        "technique": "privilege_escalation"
    }
]

texts = [chunk["text"] for chunk in facts_chunks]

print(f"Embedding {len(facts_chunks)} FACTS chunks...")

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

vectors = []
for chunk, embedding_obj in zip(facts_chunks, response.data):
    vectors.append({
        "id": chunk["id"],
        "values": embedding_obj.embedding,
        "metadata": {
            "text": chunk["text"],
            "machine": chunk["machine"],
            "technique": chunk["technique"]
        }
    })

with open("facts_embeddings.json", "w") as f:
    json.dump(vectors, f, indent=2)

print(f"✓ Created {len(vectors)} embeddings")
print(f"✓ Saved to facts_embeddings.json")
print(f"\nReady to upsert to Pinecone!")
EOF
```

## Cost Estimation

The embedding model `text-embedding-3-large` costs:
- **$0.13 per 1 million tokens**

For reference:
- 1 chunk (~500 chars) = ~125 tokens
- 1000 chunks = ~125,000 tokens = ~$0.016
- 10,000 chunks = ~1.25 million tokens = ~$0.16

## Troubleshooting

### Error: "Invalid API Key"
```bash
# Verify key
echo $OPENAI_API_KEY

# If empty, load it
source /root/.openskills/env/openai.env
echo $OPENAI_API_KEY | head -c 10
```

### Error: "Model not found"
```bash
# Verify model name is exactly: text-embedding-3-large
python3 << 'EOF'
import openai
print(openai.__version__)
EOF
```

### Rate Limiting
```bash
# If you get rate limit errors, add delay between requests
import time
time.sleep(1)  # Wait 1 second between API calls
```

---

**Next: [Upsert your embeddings to Pinecone](upserting-vectors.md)**
