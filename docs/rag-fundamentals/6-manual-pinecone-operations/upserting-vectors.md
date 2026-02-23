# Upserting Vectors to Pinecone

**Upsert** = **Update** or **Insert**. After embedding your chunks, you need to upload them to a Pinecone index. This guide covers manual upserting methods.

## Prerequisites

- **Embedded vectors**: From [Embedding Chunks Manually](embedding-chunks-manually.md)
- **Pinecone SDK installed**: `pip install pinecone-client`
- **Pinecone API Key**: In `PINECONE_API_KEY` environment variable
- **Existing Index**: Or knowledge to create one

### Verify Setup

```bash
# Check Pinecone API key
echo $PINECONE_API_KEY | head -c 10

# Check Python and SDK
python3 -c "import pinecone; print(pinecone.__version__)"

# List available indices
pa list
```

## Method 1: Upsert via Python SDK (Default Index)

The simplest way: upsert to your default `rag-canonical-v1-emb3large` index.

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to index (default)
index = pc.Index("rag-canonical-v1-emb3large")

# Load your embeddings
with open("facts_embeddings.json") as f:
    vectors = json.load(f)

print(f"Upserting {len(vectors)} vectors...")

# Upsert all vectors
upsert_response = index.upsert(
    vectors=vectors,
    namespace="facts"  # Organize by machine
)

print(f"✓ Upserted {len(vectors)} vectors")
print(f"Response: {upsert_response}")

# Verify
stats = index.describe_index_stats()
print(f"\nIndex Stats:")
print(f"  Total vectors: {stats.total_vector_count}")
print(f"  Namespaces: {stats.namespaces}")
EOF
```

**Output:**
```
Upserting 5 vectors...
✓ Upserted 5 vectors
Response: {'upserted_count': 5}

Index Stats:
  Total vectors: 119
  Namespaces: {'facts': {'vector_count': 110, ...}, 'gavel': {'vector_count': 9}}
```

## Method 2: Upsert to Specific Namespace

Organize vectors by namespace (machine name):

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# FACTS machine vectors
with open("facts_embeddings.json") as f:
    facts_vectors = json.load(f)

# GAVEL machine vectors
gavel_vectors = [
    {
        "id": "gavel_001",
        "values": [0.1, 0.2, ...],  # 3072D embedding
        "metadata": {
            "text": "YAML injection vulnerability",
            "machine": "gavel",
            "technique": "injection"
        }
    }
]

# Upsert FACTS to 'facts' namespace
print("Upserting FACTS vectors...")
facts_response = index.upsert(
    vectors=facts_vectors,
    namespace="facts"
)
print(f"✓ FACTS: {facts_response['upserted_count']} vectors")

# Upsert GAVEL to 'gavel' namespace
print("Upserting GAVEL vectors...")
gavel_response = index.upsert(
    vectors=gavel_vectors,
    namespace="gavel"
)
print(f"✓ GAVEL: {gavel_response['upserted_count']} vectors")

# Check final stats
stats = index.describe_index_stats()
print(f"\nFinal Index Stats:")
for ns, data in stats.namespaces.items():
    print(f"  {ns}: {data['vector_count']} vectors")
EOF
```

## Method 3: Upsert with Batch Processing

For large numbers of vectors, process in batches:

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Load vectors
with open("facts_embeddings.json") as f:
    vectors = json.load(f)

# Batch size (Pinecone recommends 100-1000)
batch_size = 100
namespace = "facts"

print(f"Upserting {len(vectors)} vectors in batches of {batch_size}...")

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i+batch_size]
    
    response = index.upsert(
        vectors=batch,
        namespace=namespace
    )
    
    print(f"  Batch {i//batch_size + 1}: {response['upserted_count']} vectors")

print(f"✓ All batches completed")
EOF
```

## Method 4: Upsert to Custom Index

Create or use a different index:

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to custom index
index = pc.Index("my-custom-index")

# Load vectors
with open("facts_embeddings.json") as f:
    vectors = json.load(f)

# Upsert
response = index.upsert(
    vectors=vectors,
    namespace="custom_namespace"
)

print(f"✓ Upserted to my-custom-index: {response['upserted_count']} vectors")
EOF
```

## Method 5: Upsert with Error Handling

Handle potential failures gracefully:

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

with open("facts_embeddings.json") as f:
    vectors = json.load(f)

try:
    print(f"Upserting {len(vectors)} vectors...")
    
    response = index.upsert(
        vectors=vectors,
        namespace="facts"
    )
    
    if response['upserted_count'] == len(vectors):
        print(f"✓ Success! All {len(vectors)} vectors upserted")
    else:
        print(f"⚠ Warning: Only {response['upserted_count']}/{len(vectors)} upserted")
        
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    print("\nTroubleshooting:")
    print("  1. Check PINECONE_API_KEY")
    print("  2. Verify index exists: pa list")
    print("  3. Verify vector dimension (should be 3072)")
    print("  4. Check internet connection")

EOF
```

## Real-World Example: Complete Workflow

Full workflow from chunks to Pinecone:

```bash
# Step 1: Create chunks
cat > chunks.json << 'EOF'
[
  {
    "id": "chunk_facts_101",
    "text": "SQLi in user login parameter allows database access",
    "machine": "facts",
    "technique": "sql_injection"
  },
  {
    "id": "chunk_facts_102",
    "text": "Union-based SQLi reveals admin credentials",
    "machine": "facts",
    "technique": "sql_injection"
  }
]
EOF

# Step 2: Embed chunks
python3 << 'EMBED'
import os, json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("chunks.json") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
response = client.embeddings.create(model="text-embedding-3-large", input=texts)

vectors = []
for chunk, emb in zip(chunks, response.data):
    vectors.append({
        "id": chunk["id"],
        "values": emb.embedding,
        "metadata": {
            "text": chunk["text"],
            "machine": chunk["machine"],
            "technique": chunk["technique"]
        }
    })

with open("embeddings.json", "w") as f:
    json.dump(vectors, f)

print(f"✓ Embedded {len(vectors)} chunks")
EMBED

# Step 3: Upsert to Pinecone
python3 << 'UPSERT'
import os, json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

with open("embeddings.json") as f:
    vectors = json.load(f)

response = index.upsert(vectors=vectors, namespace="facts")
print(f"✓ Upserted {response['upserted_count']} vectors to Pinecone")

# Step 4: Verify
stats = index.describe_index_stats()
print(f"✓ Total index vectors: {stats.total_vector_count}")
UPSERT

# Step 5: Search to verify
pa "SQLi admin credentials" -m facts -v
```

## Verification Commands

After upserting, verify your vectors:

```bash
# Check index stats
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
print(f"Namespaces:")
for ns, data in stats.namespaces.items():
    print(f"  {ns}: {data['vector_count']} vectors")
EOF

# Search for your vectors
pa "your search query" -v

# Count vectors in namespace
pa "test" -m facts -k 1000 | wc -l
```

## Troubleshooting

### Error: "Index not found"
```bash
# List available indices
pa list

# Create index if needed (see Index Management guide)
```

### Error: "Dimension mismatch"
```bash
# Verify embedding dimension
python3 << 'EOF'
import json
with open("embeddings.json") as f:
    vectors = json.load(f)
    print(f"Vector dimension: {len(vectors[0]['values'])}")
    # Should be 3072 for text-embedding-3-large
EOF
```

### Error: "Invalid vector values"
```bash
# Check for NaN or Infinity
python3 << 'EOF'
import json
import math

with open("embeddings.json") as f:
    vectors = json.load(f)
    
for v in vectors[:3]:
    has_invalid = any(
        math.isnan(x) or math.isinf(x) 
        for x in v["values"]
    )
    print(f"{v['id']}: {'INVALID' if has_invalid else 'OK'}")
EOF
```

### Vectors not searchable
```bash
# Verify namespace
pa "query" -m facts  # Search specific namespace

# Check if vectors were actually upserted
python3 << 'EOF'
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Search for specific vector ID
try:
    result = index.fetch(ids=["chunk_facts_001"], namespace="facts")
    print(f"Vector found: {result}")
except:
    print("Vector not found - may not be upserted")
EOF
```

---

**Next: [Query and search your vectors](querying-searching.md)**
