#!/usr/bin/env python3
"""
Recover missing chunks from Pinecone metadata
"""

import json
from pathlib import Path
from pinecone import Pinecone

RAG_ROOT = Path("/home/kali/Desktop/RAG")
DEFAULT_DIR = RAG_ROOT / "default"

# Load API keys
with open("/root/.openskills/env/pinecone.env") as f:
    pinecone_key = None
    for line in f:
        if "PINECONE_API_KEY=" in line:
            pinecone_key = line.split("=")[1].strip()
            break

pc = Pinecone(api_key=pinecone_key)
index = pc.Index("rag-canonical-v1-emb3large")

# Fetch all metadata
print("🔍 Fetching metadata from Pinecone...")
stats = index.describe_index_stats()
print(f"Total vectors: {stats.total_vector_count}")

# Query all vectors (get metadata only)
results = index.query(vector=[0] * 3072, top_k=10000, include_metadata=True)

missing_chunks = {}
for match in results["matches"]:
    chunk_id = match["metadata"].get("chunk_id")
    content = match["metadata"].get("content", "")

    if not chunk_id:
        continue

    missing_chunks[chunk_id] = content

print(f"\n📦 Found {len(missing_chunks)} chunks in Pinecone")

# Create missing files
created = 0
for chunk_id, content in missing_chunks.items():
    # Parse chunk_id to create path
    parts = chunk_id.replace("technique::", "").split("::")

    if len(parts) < 2:
        continue

    # Last part is usually the number (001, 002)
    number = parts[-1] if parts[-1].isdigit() else "001"
    base_name = parts[-2] if len(parts) > 1 else parts[0]
    category_parts = parts[:-2] if len(parts) > 2 else []

    # Create directory structure
    file_path = DEFAULT_DIR / "/".join(category_parts) / f"{base_name}_{number}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create frontmatter
    frontmatter = f"""---
chunk_id: {chunk_id}
domain: {category_parts[0] if category_parts else "unknown"}
chunk_type: technique
---

{content}
"""

    file_path.write_text(frontmatter, encoding="utf-8")
    created += 1
    print(f"✅ Created: {file_path}")

print(f"\n🎉 Created {created} chunk files from Pinecone")
