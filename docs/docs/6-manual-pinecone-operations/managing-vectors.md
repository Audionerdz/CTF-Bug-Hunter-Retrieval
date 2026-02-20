# Managing Vectors

Learn to delete, update, fetch, and inspect individual vectors in your Pinecone indices.

## Fetching (Reading) Vectors

### Fetch by ID via CLI

```bash
# Fetch a specific vector
pa fetch --id "chunk_facts_001"

# Fetch multiple vectors
pa fetch --id "chunk_facts_001" "chunk_facts_002" "chunk_facts_003"
```

### Fetch via Python SDK

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Fetch a single vector
vector = index.fetch(
    ids=["chunk_facts_001"],
    namespace="facts"
)

print(f"Vector ID: {vector['vectors'][0]['id']}")
print(f"Metadata: {vector['vectors'][0]['metadata']}")
print(f"Vector dimension: {len(vector['vectors'][0]['values'])}")

EOF
```

### Fetch Multiple Vectors

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Fetch multiple vectors
ids = ["chunk_facts_001", "chunk_facts_002", "chunk_facts_003"]

vectors = index.fetch(
    ids=ids,
    namespace="facts"
)

print(f"Fetched {len(vectors['vectors'])} vectors:\n")

for v in vectors['vectors']:
    print(f"ID: {v['id']}")
    print(f"  Text: {v['metadata']['text'][:80]}...")
    print(f"  Machine: {v['metadata']['machine']}")
    print()

EOF
```

## Updating Vectors

### Update Vector Metadata

Update metadata without changing the embedding:

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Update metadata for existing vector
# Note: You need the embedding values to update
vector = index.fetch(
    ids=["chunk_facts_001"],
    namespace="facts"
)

# Get the embedding
embedding = vector['vectors'][0]['values']
metadata = vector['vectors'][0]['metadata']

# Update metadata
metadata['status'] = 'verified'
metadata['last_updated'] = '2026-02-13'
metadata['confidence'] = 0.95

# Upsert the updated vector
response = index.upsert(
    vectors=[{
        "id": "chunk_facts_001",
        "values": embedding,
        "metadata": metadata
    }],
    namespace="facts"
)

print(f"✓ Vector updated: {response['upserted_count']} vectors")

# Verify update
updated = index.fetch(
    ids=["chunk_facts_001"],
    namespace="facts"
)
print(f"Updated metadata: {updated['vectors'][0]['metadata']}")

EOF
```

### Batch Update Vectors

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Fetch multiple vectors to update
ids = ["chunk_facts_001", "chunk_facts_002", "chunk_facts_003"]

vectors = index.fetch(
    ids=ids,
    namespace="facts"
)

# Update all of them
updated_vectors = []
for v in vectors['vectors']:
    metadata = v['metadata']
    metadata['reviewed'] = True
    metadata['tags'] = ['lfi', 'exploitation']
    
    updated_vectors.append({
        "id": v['id'],
        "values": v['values'],
        "metadata": metadata
    })

# Upsert all updated vectors
response = index.upsert(
    vectors=updated_vectors,
    namespace="facts"
)

print(f"✓ Updated {response['upserted_count']} vectors")

EOF
```

## Deleting Vectors

### Delete by ID via CLI

```bash
# Delete a single vector
pa delete --id "chunk_facts_001"

# Delete multiple vectors
pa delete --id "chunk_facts_001" "chunk_facts_002" "chunk_facts_003"

# Delete by file ID (if uploaded as file)
pa delete --file-id "file_12345"
```

### Delete via Python SDK

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Delete a single vector
index.delete(
    ids=["chunk_facts_001"],
    namespace="facts"
)

print("✓ Vector deleted: chunk_facts_001")

EOF
```

### Delete Multiple Vectors

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Delete multiple vectors
ids_to_delete = [
    "chunk_facts_001",
    "chunk_facts_002",
    "chunk_facts_003"
]

index.delete(
    ids=ids_to_delete,
    namespace="facts"
)

print(f"✓ Deleted {len(ids_to_delete)} vectors")

# Verify deletion
remaining = index.describe_index_stats()
print(f"Index now has {remaining.total_vector_count} vectors")

EOF
```

### Delete All Vectors in Namespace

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# WARNING: This deletes ALL vectors in the namespace!
index.delete(
    delete_all=True,
    namespace="facts"
)

print("⚠ All vectors in 'facts' namespace deleted!")

# Verify
stats = index.describe_index_stats()
print(f"Remaining vectors: {stats.total_vector_count}")

EOF
```

## Inspecting Vectors

### Get Index Statistics

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

stats = index.describe_index_stats()

print(f"Index: rag-canonical-v1-emb3large")
print(f"Total vectors: {stats.total_vector_count}")
print(f"\nNamespaces:")
for ns, data in stats.namespaces.items():
    print(f"  {ns}: {data['vector_count']} vectors")

EOF
```

### List All Vectors in Namespace

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Note: Pinecone doesn't have a direct "list all vectors" method
# Instead, search for a general query to get vectors
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Broad query to get many vectors
query = "the"  # Common word, returns many results
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)

results = index.query(
    vector=query_response.data[0].embedding,
    top_k=1000,  # Maximum is typically 10000
    namespace="facts",
    include_metadata=True
)

print(f"Found {len(results['matches'])} vectors in 'facts' namespace:")
for r in results['matches']:
    print(f"  {r['id']}: {r['metadata']['text'][:60]}... (score: {r['score']:.3f})")

EOF
```

### Analyze Vector Quality

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Get stats
stats = index.describe_index_stats()

print("=== Index Quality Analysis ===\n")
print(f"Total vectors: {stats.total_vector_count}")

for ns, data in stats.namespaces.items():
    print(f"\nNamespace: {ns}")
    print(f"  Vectors: {data['vector_count']}")
    
    # Check if namespace is empty
    if data['vector_count'] == 0:
        print(f"  ⚠ Empty namespace!")
    elif data['vector_count'] < 10:
        print(f"  ⚠ Very few vectors ({data['vector_count']})")
    else:
        print(f"  ✓ Healthy ({data['vector_count']} vectors)")

EOF
```

## Real-World Examples

### Example 1: Clean Up Old Vectors

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Load IDs of vectors to remove
with open("vectors_to_delete.json") as f:
    delete_list = json.load(f)

print(f"Deleting {len(delete_list)} vectors...")

# Batch delete
batch_size = 100
for i in range(0, len(delete_list), batch_size):
    batch = delete_list[i:i+batch_size]
    index.delete(ids=batch, namespace="facts")
    print(f"  Deleted batch {i//batch_size + 1}")

print("✓ Cleanup complete")

EOF
```

### Example 2: Audit Vector Metadata

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Get sample vectors
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=["test"]
)

results = index.query(
    vector=query_response.data[0].embedding,
    top_k=100,
    namespace="facts",
    include_metadata=True
)

# Analyze metadata
print("=== Metadata Audit ===\n")

metadata_fields = set()
for r in results['matches']:
    metadata_fields.update(r['metadata'].keys())

print(f"Metadata fields found: {sorted(metadata_fields)}\n")

# Check for missing required fields
required_fields = {'text', 'machine', 'source'}
for r in results['matches'][:10]:
    missing = required_fields - set(r['metadata'].keys())
    status = '✓' if not missing else '✗'
    print(f"{status} {r['id']}: {missing if missing else 'Complete'}")

EOF
```

### Example 3: Re-embed and Update Vectors

```bash
python3 << 'EOF'
import os
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Fetch vectors
vectors = index.fetch(
    ids=["chunk_facts_001", "chunk_facts_002"],
    namespace="facts"
)

# Extract text
texts = [v['metadata']['text'] for v in vectors['vectors']]

# Re-embed (if you improved the model or text)
new_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Update vectors with new embeddings
updated = []
for v, new_emb in zip(vectors['vectors'], new_response.data):
    updated.append({
        "id": v['id'],
        "values": new_emb.embedding,
        "metadata": v['metadata']
    })

# Upsert
response = index.upsert(vectors=updated, namespace="facts")
print(f"✓ Re-embedded {response['upserted_count']} vectors")

EOF
```

## Troubleshooting

### Vector Not Found

```bash
# Verify it exists
pa fetch --id "chunk_facts_001"

# If error, vector may have been deleted
# Try with verbose output
pa fetch --id "chunk_facts_001" -v
```

### Metadata Missing

```bash
# Fetch the vector
python3 << 'EOF'
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

v = index.fetch(ids=["chunk_facts_001"], namespace="facts")
print(v['vectors'][0]['metadata'])
EOF
```

### Performance Issues with Large Deletes

```bash
# Delete in smaller batches
python3 << 'EOF'
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

ids = ["id1", "id2", ...]  # Your list

batch_size = 100
for i in range(0, len(ids), batch_size):
    batch = ids[i:i+batch_size]
    index.delete(ids=batch, namespace="facts")
    print(f"Batch {i//batch_size + 1} deleted")
EOF
```

---

**Next: [Index Management](index-management-manual.md) - create, delete, and manage indices**
