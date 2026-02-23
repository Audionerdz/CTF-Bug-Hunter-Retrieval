# Quick Reference - Manual Pinecone Operations

## CLI Commands Cheat Sheet

```bash
# List indices
pa list

# Describe an index
pa describe rag-canonical-v1-emb3large

# Search (query vectors)
pa "your query"
pa "your query" -k 10              # 10 results
pa "your query" -m facts           # FACTS namespace only
pa "your query" -v                 # Verbose output

# Fetch vector
pa fetch --id "chunk_facts_001"

# Delete vector
pa delete --id "chunk_facts_001"

# Delete by file ID
pa delete --file-id "file_12345"

# Help
pa --help
```

## Python SDK Quick Snippets

### Initialize Connection

```python
import os
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")
```

### Embed Text

```python
response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=["your text here"]
)
embedding = response.data[0].embedding
```

### Upsert Vectors

```python
index.upsert(
    vectors=[{
        "id": "vector_id",
        "values": embedding,
        "metadata": {"text": "your text", "machine": "facts"}
    }],
    namespace="facts"
)
```

### Query Vectors

```python
response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=["query text"]
)

results = index.query(
    vector=response.data[0].embedding,
    top_k=5,
    namespace="facts",
    include_metadata=True
)
```

### Fetch Vector

```python
vector = index.fetch(
    ids=["chunk_facts_001"],
    namespace="facts"
)
```

### Delete Vector

```python
index.delete(
    ids=["chunk_facts_001"],
    namespace="facts"
)
```

### Get Index Stats

```python
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")
for ns, data in stats.namespaces.items():
    print(f"  {ns}: {data['vector_count']}")
```

### Create Index

```python
pc.create_index(
    name="my-index",
    dimension=3072,
    metric="cosine"
)
```

### Delete Index

```python
pc.delete_index("my-index")
```

## Common Workflows

### 1. Add New Chunks to RAG

```bash
# 1. Create JSON with chunks
cat > chunks.json << 'EOF'
[{"id": "...", "text": "...", "machine": "facts"}]
EOF

# 2. Embed chunks
python3 << 'EMBED'
# (see Embedding Chunks guide)
EMBED

# 3. Upsert to Pinecone
python3 << 'UPSERT'
# (see Upserting guide)
UPSERT

# 4. Verify with search
pa "your search query" -m facts -v
```

### 2. Search Knowledge Base

```bash
# Quick search
pa "LFI exploitation" -k 10 -v

# Filter by machine
pa "RCE" -m facts

# High recall search
pa "privilege escalation" -k 100
```

### 3. Manage Vectors

```bash
# Fetch vector
pa fetch --id "chunk_facts_001"

# Update metadata (fetch + re-upsert)
python3 << 'EOF'
# (see Managing Vectors guide)
EOF

# Delete vector
pa delete --id "chunk_facts_001"
```

### 4. Index Management

```bash
# List indices
pa list

# Create new index
python3 << 'EOF'
pc.create_index(name="...", dimension=3072)
EOF

# Backup index
python3 << 'EOF'
# (see Real-World Examples guide)
EOF

# Delete index
pa delete-index my-index
```

## Dimension Reference

| Model | Dimension | Use Case |
|-------|-----------|----------|
| text-embedding-3-large | 3072 | High quality, large models |
| text-embedding-3-small | 1536 | Faster, lower cost |
| ada | 1536 | Legacy model |

## Namespace Organization

Your current setup:

```
rag-canonical-v1-emb3large/
  ├── facts/        (105 vectors from FACTS HTB machine)
  └── gavel/        (9 vectors from GAVEL HTB machine)
```

Search by namespace:

```bash
pa "query" -m facts    # Only FACTS
pa "query" -m gavel    # Only GAVEL
pa "query"             # All vectors
```

## Environment Variables

```bash
# Required
echo $PINECONE_API_KEY
echo $OPENAI_API_KEY

# Source if empty
source /root/.openskills/env/pinecone.env
source /root/.openskills/env/openai.env

# Verify
pa --help              # If works, Pinecone is configured
```

## File Structure

```
/root/mkdocs-unified-methodology/docs/6-manual-pinecone-operations/
├── index.md                          (Introduction & overview)
├── pinecone-cli-essentials.md        (CLI installation & commands)
├── embedding-chunks-manually.md      (OpenAI embedding guide)
├── upserting-vectors.md              (Upload to Pinecone)
├── querying-searching.md             (Search operations)
├── managing-vectors.md               (CRUD operations)
├── index-management-manual.md        (Create/delete indices)
├── real-world-examples.md            (Complete workflows)
└── QUICK_REFERENCE.md               (This file!)
```

## Troubleshooting

### CLI Not Found

```bash
which pa
# If not found: /usr/local/bin/pa missing
```

### API Key Issues

```bash
echo $PINECONE_API_KEY | head -c 10
# Should show first 10 chars of your key
```

### Index Not Found

```bash
pa list  # Verify index exists
```

### No Search Results

```bash
# Try broader query
pa "vulnerability" instead of "CVE-2024-12345"

# Increase results
pa "query" -k 100

# Check namespace
pa "query" -m facts
```

### Vector Dimension Mismatch

```bash
# 3072 for text-embedding-3-large
# 1536 for text-embedding-3-small

# Check embedding dimension
python3 << 'EOF'
import json
with open("embeddings.json") as f:
    v = json.load(f)[0]
    print(len(v['values']))  # Should be 3072
EOF
```

## Cost Estimation

Embeddings (text-embedding-3-large):
- **$0.13 per 1M tokens**
- 1 chunk (~500 chars) ≈ 125 tokens ≈ **$0.0000163**
- 1000 chunks ≈ **$0.016**
- 10000 chunks ≈ **$0.16**

Queries: FREE (included)

Storage: ~$30-40/month for Serverless

## Next Steps

1. **Start Here**: [Introduction](index.md)
2. **Learn CLI**: [Pinecone CLI Essentials](pinecone-cli-essentials.md)
3. **Embed Data**: [Embedding Chunks Manually](embedding-chunks-manually.md)
4. **Upload**: [Upserting Vectors](upserting-vectors.md)
5. **Search**: [Querying and Searching](querying-searching.md)
6. **Manage**: [Managing Vectors](managing-vectors.md)
7. **Indices**: [Index Management](index-management-manual.md)
8. **Examples**: [Real-World Examples](real-world-examples.md)

---

**Everything you need for manual Pinecone operations. No scripts required.**
