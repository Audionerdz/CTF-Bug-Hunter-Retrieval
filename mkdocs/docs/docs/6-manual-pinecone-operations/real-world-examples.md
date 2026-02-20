# Real-World Examples

Complete, copy-paste workflows using your actual FACTS and GAVEL machine data.

## Example 1: Add New FACTS Machine Chunks

You've finished a new FACTS machine exploit and want to add it to the knowledge base.

### Step 1: Prepare Your Chunks

```bash
cat > facts_new_exploit.json << 'EOF'
[
  {
    "id": "chunk_facts_106",
    "text": "Unauthenticated RCE via PHP unserialize() in user_data parameter",
    "machine": "facts",
    "technique": "rce",
    "source": "FACTS HTB Machine",
    "date": "2026-02-13",
    "severity": "critical"
  },
  {
    "id": "chunk_facts_107",
    "text": "Gadget chain exploitation using Laravel framework internals",
    "machine": "facts",
    "technique": "deserialization",
    "source": "FACTS HTB Machine",
    "date": "2026-02-13",
    "severity": "critical"
  },
  {
    "id": "chunk_facts_108",
    "text": "POP chain leading to system() command execution",
    "machine": "facts",
    "technique": "rce",
    "source": "FACTS HTB Machine",
    "date": "2026-02-13",
    "severity": "critical"
  }
]
EOF
```

### Step 2: Embed the Chunks

```bash
python3 << 'EOF'
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load chunks
with open("facts_new_exploit.json") as f:
    chunks = json.load(f)

# Extract text
texts = [c["text"] for c in chunks]

print(f"Embedding {len(chunks)} new chunks...")

# Create embeddings
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Build vectors
vectors = []
for chunk, emb in zip(chunks, response.data):
    vectors.append({
        "id": chunk["id"],
        "values": emb.embedding,
        "metadata": {
            "text": chunk["text"],
            "machine": chunk["machine"],
            "technique": chunk["technique"],
            "source": chunk["source"],
            "severity": chunk["severity"],
            "date": chunk["date"]
        }
    })

with open("facts_new_vectors.json", "w") as f:
    json.dump(vectors, f)

print(f"✓ Embedded {len(vectors)} chunks")

EOF
```

### Step 3: Upsert to Pinecone

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Load vectors
with open("facts_new_vectors.json") as f:
    vectors = json.load(f)

# Upsert to FACTS namespace
response = index.upsert(
    vectors=vectors,
    namespace="facts"
)

print(f"✓ Upserted {response['upserted_count']} vectors to FACTS namespace")

# Verify
stats = index.describe_index_stats()
facts_count = stats.namespaces.get("facts", {}).get("vector_count", 0)
print(f"✓ FACTS now has {facts_count} total vectors")

EOF
```

### Step 4: Test the New Chunks

```bash
# Search for your new exploit
pa "PHP unserialize gadget chain" -m facts -v

# Should find your new chunks with high scores!
```

**Output:**
```
[1] chunk_facts_106 (score: 0.94)
    Unauthenticated RCE via PHP unserialize() in user_data parameter
    Metadata: {
        "severity": "critical",
        "technique": "rce",
        "date": "2026-02-13"
    }

[2] chunk_facts_107 (score: 0.91)
    Gadget chain exploitation using Laravel framework internals
```

---

## Example 2: Organize GAVEL Machine Knowledge

GAVEL has only 9 vectors. Let's add comprehensive YAML injection notes.

### Create Comprehensive GAVEL Knowledge Base

```bash
python3 << 'EOF'
import os
import json
from openai import OpenAI
from pinecone import Pinecone

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# GAVEL chunks
gavel_chunks = [
    {
        "id": "gavel_010",
        "text": "YAML anchors and aliases enable arbitrary object instantiation",
        "technique": "yaml_injection"
    },
    {
        "id": "gavel_011",
        "text": "YAML type tags like !!python/object/apply execute code",
        "technique": "yaml_injection"
    },
    {
        "id": "gavel_012",
        "text": "PyYAML.load() is unsafe - use safe_load() instead",
        "technique": "secure_coding"
    },
    {
        "id": "gavel_013",
        "text": "RCE via YAML config parsing in application initialization",
        "technique": "rce"
    },
    {
        "id": "gavel_014",
        "text": "Merging malicious YAML configs through environment variables",
        "technique": "exploitation"
    }
]

# Embed all
texts = [c["text"] for c in gavel_chunks]
response = openai.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Create vectors
vectors = []
for chunk, emb in zip(gavel_chunks, response.data):
    vectors.append({
        "id": chunk["id"],
        "values": emb.embedding,
        "metadata": {
            "text": chunk["text"],
            "machine": "gavel",
            "technique": chunk["technique"],
            "source": "GAVEL HTB Machine"
        }
    })

# Upsert to GAVEL namespace
response = index.upsert(vectors=vectors, namespace="gavel")
print(f"✓ Upserted {response['upserted_count']} GAVEL vectors")

# Check new total
stats = index.describe_index_stats()
gavel_count = stats.namespaces.get("gavel", {}).get("vector_count", 0)
print(f"✓ GAVEL now has {gavel_count} total vectors")

EOF
```

### Search Your GAVEL Knowledge

```bash
# Find YAML injection techniques
pa "YAML object instantiation RCE" -m gavel -k 10 -v

# Should return your comprehensive YAML knowledge!
```

---

## Example 3: Merge All Machines into One Index

Export all machines and reorganize them.

### Step 1: Export Current Index

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Query all vectors (use broad query)
all_vectors = []

for machine in ["facts", "gavel"]:
    # Search for common word to get all vectors
    response = openai.embeddings.create(
        model="text-embedding-3-large",
        input=["the"]
    )
    
    results = index.query(
        vector=response.data[0].embedding,
        top_k=10000,
        namespace=machine,
        include_metadata=True
    )
    
    for r in results['matches']:
        all_vectors.append({
            "id": r['id'],
            "metadata": r['metadata']
        })

print(f"Exported {len(all_vectors)} vectors from all machines")

# Save
with open("all_vectors_export.json", "w") as f:
    json.dump(all_vectors, f)

EOF
```

### Step 2: Reorganize and Re-upsert

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone
from openai import OpenAI

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load exported vectors
with open("all_vectors_export.json") as f:
    all_vectors = json.load(f)

# Extract texts and re-embed
texts = [v["metadata"]["text"] for v in all_vectors]

print(f"Re-embedding {len(texts)} vectors...")

response = openai.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

# Prepare final vectors
final_vectors = []
for v, emb in zip(all_vectors, response.data):
    final_vectors.append({
        "id": v["id"],
        "values": emb.embedding,
        "metadata": v["metadata"]
    })

# Save
with open("all_vectors_final.json", "w") as f:
    json.dump(final_vectors, f)

print(f"✓ Prepared {len(final_vectors)} vectors for new index")

EOF
```

---

## Example 4: Cross-Machine Search

Search across all machines and analyze results.

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Query
query = "privilege escalation techniques"

response = openai.embeddings.create(
    model="text-embedding-3-large",
    input=[query]
)

# Search all machines
results = index.query(
    vector=response.data[0].embedding,
    top_k=20,
    include_metadata=True
)

# Organize by machine
machines = {}
for r in results['matches']:
    machine = r['metadata'].get('machine', 'unknown')
    if machine not in machines:
        machines[machine] = []
    machines[machine].append(r)

# Display
print(f"Query: {query}\n")
for machine, results in machines.items():
    print(f"=== {machine.upper()} ===")
    for r in results:
        print(f"[{r['score']:.3f}] {r['metadata']['text'][:80]}...")
    print()

EOF
```

---

## Example 5: Backup and Restore

Create a backup of your entire index.

### Backup

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone
from openai import OpenAI
from datetime import datetime

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Get all vectors
all_vectors = []
for machine in ["facts", "gavel"]:
    response = openai.embeddings.create(
        model="text-embedding-3-large",
        input=["the"]
    )
    
    results = index.query(
        vector=response.data[0].embedding,
        top_k=10000,
        namespace=machine,
        include_metadata=True
    )
    
    for r in results['matches']:
        all_vectors.append({
            "id": r['id'],
            "values": r['values'],
            "metadata": r['metadata'],
            "namespace": machine
        })

# Save backup
timestamp = datetime.now().isoformat()
backup_file = f"rag-backup-{timestamp}.json"

with open(backup_file, "w") as f:
    json.dump({
        "timestamp": timestamp,
        "total_vectors": len(all_vectors),
        "vectors": all_vectors
    }, f)

print(f"✓ Backed up {len(all_vectors)} vectors")
print(f"✓ Saved to {backup_file}")

EOF
```

### Restore

```bash
python3 << 'EOF'
import os
import json
from pinecone import Pinecone

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

# Load backup
backup_file = "rag-backup-2026-02-13T10:30:00.json"

with open(backup_file) as f:
    backup = json.load(f)

vectors = backup['vectors']

# Restore by namespace
by_namespace = {}
for v in vectors:
    ns = v.pop('namespace')
    if ns not in by_namespace:
        by_namespace[ns] = []
    by_namespace[ns].append(v)

# Upsert each namespace
for ns, vecs in by_namespace.items():
    response = index.upsert(vectors=vecs, namespace=ns)
    print(f"✓ Restored {response['upserted_count']} vectors to {ns}")

EOF
```

---

## Example 6: Quality Audit

Check the quality of your indexed vectors.

```bash
python3 << 'EOF'
import os
from openai import OpenAI
from pinecone import Pinecone

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

print("=== RAG Index Quality Audit ===\n")

# Check index stats
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")

# Test searches on each machine
test_queries = [
    ("FACTS", "facts", ["LFI", "RCE", "exploitation", "privilege escalation"]),
    ("GAVEL", "gavel", ["YAML", "injection", "config", "parsing"])
]

for label, machine, keywords in test_queries:
    print(f"\n{label} Machine:")
    print(f"  Vectors: {stats.namespaces.get(machine, {}).get('vector_count', 0)}")
    
    # Test each keyword
    hits = {}
    for kw in keywords:
        response = openai.embeddings.create(
            model="text-embedding-3-large",
            input=[kw]
        )
        
        results = index.query(
            vector=response.data[0].embedding,
            top_k=1,
            namespace=machine,
            include_metadata=True
        )
        
        if results['matches']:
            hits[kw] = results['matches'][0]['score']
    
    print(f"  Keyword coverage: {len(hits)}/{len(keywords)}")
    for kw, score in hits.items():
        status = "✓" if score > 0.7 else "⚠"
        print(f"    {status} {kw}: {score:.3f}")

print("\n✓ Audit complete!")

EOF
```

---

## Quick Command Reference

```bash
# Search both machines
pa "your query" -k 10

# Search only FACTS
pa "your query" -m facts

# Search only GAVEL
pa "your query" -m gavel

# Verbose output
pa "your query" -v

# High recall search
pa "your query" -k 100

# Add new chunks - see Example 1 above

# Verify upsert - use pa command

# Backup your index - see Example 5 above

# Audit quality - see Example 6 above
```

---

**You now have complete knowledge of manual Pinecone operations. Explore, experiment, and build!**
