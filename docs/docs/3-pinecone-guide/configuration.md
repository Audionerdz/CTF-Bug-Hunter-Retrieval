# Configuration Guide

Complete Pinecone configuration for production RAG systems.

## Environment Setup

Create `.env` file with all required variables:

```env
# Pinecone
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX=rag-canonical-v1-emb3large
PINECONE_NAMESPACE=default

# OpenAI Embeddings
OPENAI_API_KEY=sk_your_key_here
EMBEDDING_MODEL=text-embedding-3-large

# Vector Configuration
EMBEDDING_DIMENSION=3072
METRIC=cosine

# Optional
LOG_LEVEL=INFO
BATCH_SIZE=100
```

## Index Configuration

Create index with proper settings:

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_xxx")

# Serverless (Recommended for RAG)
pc.create_index(
    name="rag-canonical-v1-emb3large",
    dimension=3072,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Pod-based (For larger deployments)
pc.create_index(
    name="rag-canonical-v1-emb3large",
    dimension=3072,
    metric="cosine",
    spec=PodSpec(
        environment="us-east1-aws",
        pod_type="p1.x1"
    )
)
```

## Namespace Configuration

Organize chunks by namespace:

```python
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_xxx")
index = pc.Index("rag-canonical-v1-emb3large")

# Upsert to specific namespace
index.upsert(
    vectors=vectors,
    namespace="web-security"  # Isolates chunks
)

# Query specific namespace
results = index.query(
    vector=query_vector,
    namespace="web-security",
    top_k=5
)
```

## Metadata Filtering

Add metadata to enable filtering:

```python
vectors = [
    {
        'id': 'concept::web::lfi::001',
        'values': embedding_vector,
        'metadata': {
            'chunk_id': 'concept::web::lfi::001',
            'domain': 'web',
            'chunk_type': 'concept',
            'confidence': 'high',
            'tags': ['lfi', 'web-security']
        }
    }
]

index.upsert(vectors=vectors)
```

Query with filters:

```python
results = index.query(
    vector=query_vector,
    filter={
        'domain': {'$eq': 'web'},
        'confidence': {'$eq': 'high'}
    },
    top_k=5
)
```

## Performance Tuning

For production RAG systems:

| Setting | Recommendation | Reason |
|---------|---|---|
| `metric` | `cosine` | Best for semantic search |
| `dimension` | `3072` | OpenAI text-embedding-3-large |
| `batch_size` | `100-200` | Balance throughput vs latency |
| `top_k` | `5-10` | Retrieve top candidates |
| `pod_type` | `p1.x1` for prod | Better performance |

---

Continue: [Concepts Explained](concepts.md)
