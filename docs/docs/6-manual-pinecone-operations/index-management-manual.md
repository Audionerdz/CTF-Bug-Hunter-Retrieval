# Index Management

Learn to create, delete, inspect, and configure Pinecone indices manually.

## List Indices

### Via CLI

```bash
pa list
```

**Output:**
```
Name                                    Dimension  Vectors
rag-canonical-v1-emb3large             3072       114
my-test-index                          1536       42
```

### Via Python SDK

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# List all indices
indices = pc.list_indexes()

print("Available Indices:\n")
for index_info in indices:
    print(f"  Name: {index_info.name}")
    print(f"  Dimension: {index_info.dimension}")
    print(f"  Status: {index_info.status}")
    print()

EOF
```

## Describe an Index

### Via CLI

```bash
pa describe rag-canonical-v1-emb3large
```

**Output:**
```
Name:        rag-canonical-v1-emb3large
Status:      Ready
Dimension:   3072
Vectors:     114
Metric:      Cosine
Namespaces:  facts, gavel
```

### Via Python SDK

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Get index description
description = index.describe_index_stats()

print("Index Details:")
print(f"  Total vectors: {description.total_vector_count}")
print(f"  Namespaces:")
for ns, data in description.namespaces.items():
    print(f"    {ns}: {data['vector_count']} vectors")

EOF
```

## Create a New Index

### Method 1: Create Index for text-embedding-3-large (3072D)

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create index
index_name = "my-rag-index"

pc.create_index(
    name=index_name,
    dimension=3072,  # For text-embedding-3-large
    metric="cosine",  # Cosine similarity
    spec={
        "serverless": {
            "cloud": "aws",
            "region": "us-east-1"
        }
    }
)

print(f"✓ Index '{index_name}' created")
print("Waiting for index to be ready...")

# Check status
import time
while True:
    indices = pc.list_indexes()
    index_info = next((i for i in indices if i.name == index_name), None)
    if index_info and index_info.status == "Ready":
        print(f"✓ Index is ready!")
        break
    time.sleep(1)

EOF
```

### Method 2: Create Index with Custom Specification

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create a custom index
pc.create_index(
    name="my-custom-index",
    dimension=3072,
    metric="cosine",
    spec={
        "serverless": {
            "cloud": "aws",
            "region": "us-east-1"
        }
    },
    tags=["rag", "custom"]
)

print("✓ Custom index created")

EOF
```

### Method 3: Create Index for Different Embedding Model

For other models with different dimensions:

```bash
# text-embedding-3-small = 1536 dimensions
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

pc.create_index(
    name="small-embedding-index",
    dimension=1536,  # text-embedding-3-small
    metric="cosine"
)

print("✓ Small embedding index created")

EOF

# For custom models, adjust dimension accordingly
```

## Verify Index Creation

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

indices = pc.list_indexes()

print("Current Indices:")
for idx in indices:
    print(f"  {idx.name}: {idx.dimension}D, {idx.status}")

EOF
```

## Delete an Index

### Via CLI

```bash
# Delete index (WARNING: No confirmation!)
pa delete-index my-test-index
```

### Via Python SDK

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Delete index (WARNING: This deletes ALL vectors in the index!)
index_name = "my-test-index"

pc.delete_index(index_name)

print(f"✓ Index '{index_name}' deleted")

# Verify deletion
remaining = pc.list_indexes()
print(f"Remaining indices: {[i.name for i in remaining]}")

EOF
```

## Real-World Workflow: Build Index from Scratch

Complete workflow to create and populate a new index:

```bash
# Step 1: Create the index
python3 << 'EOF'
import os
from pinecone import Pinecone
import time

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("Creating index 'facts-knowledge-base'...")

pc.create_index(
    name="facts-knowledge-base",
    dimension=3072,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
)

# Wait for ready
while True:
    indices = pc.list_indexes()
    if any(i.name == "facts-knowledge-base" and i.status == "Ready" for i in indices):
        print("✓ Index ready!")
        break
    print("Waiting for index to initialize...")
    time.sleep(2)

EOF

# Step 2: Embed your chunks
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create chunks
chunks = [
    {
        "id": "chunk_1",
        "text": "LFI vulnerabilities in PHP applications",
        "machine": "facts",
        "technique": "lfi"
    },
    {
        "id": "chunk_2",
        "text": "RCE via log poisoning exploit",
        "machine": "facts",
        "technique": "rce"
    },
    {
        "id": "chunk_3",
        "text": "Privilege escalation using kernel exploits",
        "machine": "facts",
        "technique": "privesc"
    }
]

# Embed
texts = [c["text"] for c in chunks]
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Create vectors
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

with open("vectors.json", "w") as f:
    json.dump(vectors, f)

print(f"✓ Created {len(vectors)} embeddings")

EOF

# Step 3: Upsert to the new index
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("facts-knowledge-base")

with open("vectors.json") as f:
    vectors = json.load(f)

response = index.upsert(vectors=vectors, namespace="facts")
print(f"✓ Upserted {response['upserted_count']} vectors")

EOF

# Step 4: Verify
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("facts-knowledge-base")

stats = index.describe_index_stats()
print(f"Index Stats:")
print(f"  Total vectors: {stats.total_vector_count}")
print(f"  Namespaces: {list(stats.namespaces.keys())}")

EOF

# Step 5: Test search
pa "privilege escalation" -k 5 -v
# Note: May need to configure the pa command to use this index
```

## Switch Default Index

By default, `pa` searches `rag-canonical-v1-emb3large`. To use a different index, you need to update your configuration:

### Via Environment Variable

```bash
# Set default index
export PINECONE_INDEX="my-custom-index"

# Now searches use this index
pa "your query"
```

### Via CLI Assistant Selection

```bash
# Use specific assistant/index
pa -a "my-assistant" "query"
```

## Monitor Index Growth

Track how your index grows over time:

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

stats = index.describe_index_stats()

print("=== Index Growth Report ===\n")
print(f"Index: rag-canonical-v1-emb3large")
print(f"Total vectors: {stats.total_vector_count}")
print(f"\nNamespace Breakdown:")

total = sum(data['vector_count'] for data in stats.namespaces.values())

for ns, data in stats.namespaces.items():
    count = data['vector_count']
    percentage = (count / total * 100) if total > 0 else 0
    print(f"  {ns}: {count:>4} vectors ({percentage:>5.1f}%)")

print(f"\nTotal: {total} vectors")

EOF
```

## Best Practices

| Practice | Why |
|----------|-----|
| Use 3072D for large models | Better semantic understanding |
| Use 1536D for faster queries | Trade quality for speed |
| Organize by namespace | Easy filtering by machine/topic |
| Name indices clearly | Easy to identify later |
| Monitor growth | Catch issues early |
| Backup metadata | Can re-embed if needed |

## Troubleshooting

### Index Creation Fails

```bash
# Check API key
echo $PINECONE_API_KEY | head -c 10

# Check available quota
# (Pinecone dashboard or error message)

# Try with simpler spec
python3 << 'EOF'
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

pc.create_index(
    name="simple-index",
    dimension=3072,
    metric="cosine"
)
EOF
```

### Index Stuck in Initializing State

```bash
# This sometimes happens - wait a bit longer
python3 << 'EOF'
import time
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

while True:
    indices = pc.list_indexes()
    idx = next((i for i in indices if i.name == "my-index"), None)
    
    if idx:
        print(f"Status: {idx.status}")
        if idx.status == "Ready":
            print("✓ Ready!")
            break
    
    time.sleep(5)
EOF
```

### Can't Delete Index

```bash
# Make sure no code is using it
# Then try deletion
pa delete-index my-index

# Or via SDK
python3 << 'EOF'
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pc.delete_index("my-index")
EOF
```

---

**Next: [Real-World Examples](real-world-examples.md) - complete workflows with FACTS and GAVEL**
