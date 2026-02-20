# Querying and Searching Vectors

Once your vectors are in Pinecone, you can search them using semantic similarity. Learn to query manually using the CLI and Python SDK.

## Quick Search via CLI

The simplest way to search:

```bash
# Basic search (returns top 5)
pa "LFI exploitation"

# More results
pa "RCE techniques" -k 10

# Specific namespace (machine)
pa "privesc" -m facts

# Verbose (show full content)
pa "SQL injection" -v

# Combine options
pa "buffer overflow" -m facts -k 20 -v
```

## Method 1: Search via CLI

### Basic Query

```bash
pa "your query here"
```

**Output:**
```
[1] chunk_facts_001 (score: 0.89)
    LFI vulnerabilities allow reading arbitrary files from the server filesystem
    
[2] chunk_facts_003 (score: 0.87)
    RCE via log poisoning: injecting code into Apache access.log
    
[3] chunk_gavel_001 (score: 0.72)
    YAML injection in configuration parsing leads to code execution
```

### Search with Top-K

Return more results:

```bash
# Top 20 results
pa "authentication bypass" -k 20

# Top 100 results
pa "exploitation" -k 100
```

### Filter by Machine (Namespace)

```bash
# Only FACTS chunks
pa "privilege escalation" -m facts

# Only GAVEL chunks
pa "yaml injection" -m gavel
```

### Verbose Output

Show full metadata and content:

```bash
pa "kernel exploit" -v
```

**Output:**
```
[1] chunk_facts_042 (score: 0.91)
    Metadata: {
        "text": "Kernel exploit CVE-2021-22555 allows privilege escalation",
        "machine": "facts",
        "technique": "privilege_escalation",
        "severity": "critical"
    }
    Full Content: Kernel exploit CVE-2021-22555 allows privilege escalation...
```

## Method 2: Search via Python SDK

### Basic Query

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

# Initialize
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Your query
query = "How to exploit LFI vulnerabilities?"

# Convert query to embedding
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)
query_embedding = query_response.data[0].embedding

# Search
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

# Display results
print(f"Query: {query}\n")
for i, result in enumerate(results['matches'], 1):
    print(f"[{i}] {result['id']} (score: {result['score']:.3f})")
    print(f"    {result['metadata']['text']}\n")

EOF
```

**Output:**
```
Query: How to exploit LFI vulnerabilities?

[1] chunk_facts_001 (score: 0.891)
    LFI vulnerabilities allow reading arbitrary files from the server

[2] chunk_facts_003 (score: 0.867)
    RCE via log poisoning: injecting code into Apache access.log

[3] chunk_facts_005 (score: 0.823)
    Chained LFI + filter bypass = Remote Code Execution
```

### Query with Namespace Filter

Search only specific machine:

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Query embedding
query = "API endpoint exploitation"
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)

# Search in FACTS namespace only
results = index.query(
    vector=query_response.data[0].embedding,
    top_k=10,
    namespace="facts",  # Filter by namespace
    include_metadata=True
)

print(f"Results from FACTS machine:")
for result in results['matches']:
    print(f"- {result['id']}: {result['metadata']['text'][:80]}...")

EOF
```

### Query with Metadata Filtering

Search with additional filters:

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Query
query = "privilege escalation technique"
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)

# Search with filter (Pinecone Pro feature)
# This requires metadata indices to be created
results = index.query(
    vector=query_response.data[0].embedding,
    top_k=5,
    namespace="facts",
    include_metadata=True
)

# Filter results manually if metadata doesn't support server-side filtering
privilege_escalation_results = [
    r for r in results['matches'] 
    if r['metadata'].get('technique') == 'privilege_escalation'
]

print(f"Privilege Escalation techniques:")
for r in privilege_escalation_results:
    print(f"- {r['id']}: {r['metadata']['text']}")

EOF
```

## Method 3: Batch Queries

Search for multiple queries at once:

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Multiple queries
queries = [
    "LFI exploitation",
    "RCE techniques",
    "privilege escalation"
]

# Embed all queries at once
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=queries
)

# Search each query
for query, query_obj in zip(queries, query_response.data):
    results = index.query(
        vector=query_obj.embedding,
        top_k=3,
        include_metadata=True
    )
    
    print(f"\n=== {query} ===")
    for r in results['matches']:
        print(f"[{r['score']:.3f}] {r['metadata']['text'][:100]}")

EOF
```

## Method 4: Semantic Search Variations

### Exact Phrase Search

If you have the exact phrase in metadata:

```bash
# Search for exact phrase
pa "buffer overflow" -v
```

### Similarity Score Threshold

Filter by minimum similarity:

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

query = "security vulnerability"
query_response = openai_client.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)

results = index.query(
    vector=query_response.data[0].embedding,
    top_k=100,
    include_metadata=True
)

# Filter by minimum similarity (0.8 = 80%)
high_confidence = [
    r for r in results['matches'] 
    if r['score'] >= 0.80
]

print(f"Results with >80% similarity:")
for r in high_confidence:
    print(f"[{r['score']:.1%}] {r['metadata']['text'][:80]}...")

EOF
```

### Combine Related Searches

Search for variations:

```bash
pa "LFI" -k 5
pa "Local File Inclusion" -k 5
pa "path traversal" -k 5
```

## Real-World Examples

### Example 1: Troubleshoot a Vulnerability

```bash
# Search your knowledge base
pa "PHP include vulnerability" -m facts -v

# Takes your query, embeds it, searches FACTS namespace, shows results with metadata
```

### Example 2: Find All Exploitation Techniques

```bash
# Multiple related searches
pa "RCE exploitation" -k 20
pa "remote code execution" -k 20
pa "code injection" -k 20
pa "shell access" -k 20
```

### Example 3: Filter Results by Machine

```bash
# Get all results
pa "privesc" -k 50

# Or filter by machine
pa "privilege escalation" -m facts -k 50
pa "privilege escalation" -m gavel -k 50
```

### Example 4: Verify Vector Retrieval

```bash
# Search with verbose output
pa "buffer overflow exploit" -v

# Check:
# 1. Results are relevant
# 2. Scores are high (>0.7)
# 3. Metadata is correct
```

## Similarity Scores Explained

| Score | Meaning | Use Case |
|-------|---------|----------|
| 0.95+ | Near-identical | Exact matches, definitions |
| 0.85-0.94 | Highly relevant | Core concepts, techniques |
| 0.70-0.84 | Relevant | Related concepts |
| 0.50-0.69 | Somewhat related | Distant connections |
| <0.50 | Weakly related | Probably not useful |

For CTF/security research, use results with **>0.75 score**.

## Performance Tips

### Speed Up Queries

```bash
# Smaller top_k = faster search
pa "query" -k 5  # Faster
pa "query" -k 1000  # Slower

# Narrow by namespace
pa "query" -m facts  # Faster (only FACTS vectors)
pa "query"  # Slower (all vectors)
```

### Optimize Search Quality

```bash
# More specific queries = better results
pa "CVE-2021-22555 privilege escalation"  # Better
pa "exploit"  # Too broad

# Use full phrases
pa "local file inclusion via null bytes"  # Better
pa "lfi"  # Less precise
```

## Troubleshooting

### No Results Found

```bash
# Try broader query
pa "vulnerability"  # Instead of "CVE-2024-12345"

# Increase top_k
pa "query" -k 100  # Return more results

# Check namespace
pa "query" -m facts  # Maybe results only in specific namespace
```

### Low Similarity Scores (<0.5)

```bash
# Your query might be too different from indexed text
pa "completely different query" -k 10  # See average scores

# Try synonyms
pa "RCE"  # instead of "remote code execution"
pa "privesc"  # instead of "privilege escalation"
```

### Wrong Results

```bash
# Add more context to query
pa "Ubuntu kernel exploit CVE-2021"  # Better
pa "kernel"  # Too vague

# Use verbose to see scores
pa "query" -v  # See why results rank high/low
```

---

**Next: [Manage vectors](managing-vectors.md) - delete, update, and inspect individual vectors**
