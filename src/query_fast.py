#!/usr/bin/env python3
"""
FAST QUERY: Pinecone search + local file reading
Shows content from filesystem via chunk_registry
"""

import sys
import json
from pathlib import Path
from pinecone import Pinecone
from openai import OpenAI

RAG_ROOT = Path("/home/kali/Desktop/RAG")
CHUNK_REGISTRY = RAG_ROOT / "chunk_registry.json"


def load_api_keys():
    """Load API keys"""
    with open("/root/.openskills/env/pinecone.env") as f:
        pinecone_key = None
        for line in f:
            if "PINECONE_API_KEY=" in line:
                pinecone_key = line.split("=")[1].strip()
                break

    with open("/root/.openskills/env/openai.env") as f:
        openai_key = None
        for line in f:
            if "OPENAI_API_KEY=" in line:
                openai_key = line.split("=")[1].strip()
                break

    return pinecone_key, openai_key


def get_chunk_content(chunk_id):
    """Read chunk content from filesystem"""
    try:
        with open(CHUNK_REGISTRY) as f:
            registry = json.load(f)

        if chunk_id not in registry:
            return None

        chunk_path = Path(registry[chunk_id])
        if not chunk_path.exists():
            return None

        with open(chunk_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract content after frontmatter
        parts = content.split("---", 2)
        if len(parts) > 2:
            return parts[2].strip()
        return content
    except:
        return None


def query_rag(idx, client, query_text, top_k=5):
    """Query Pinecone"""
    response = client.embeddings.create(
        model="text-embedding-3-large", input=query_text, dimensions=3072
    )
    query_embedding = response.data[0].embedding
    results = idx.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return results["matches"]


def format_results(matches, query_text):
    """Display results with content"""
    print(f"\n{'=' * 70}")
    print(f"🔍 Query: '{query_text}'")
    print(f"{'=' * 70}")
    print(f"✅ Results: {len(matches)} matches\n")

    if not matches:
        print("No results found.")
        return

    for i, match in enumerate(matches, 1):
        meta = match["metadata"]
        chunk_id = meta["chunk_id"]

        print(f"{i}. {chunk_id}")
        print(
            f"   Score: {match['score']:.4f} | {meta.get('domain', 'unknown')} | {meta.get('chunk_type', 'unknown')}\n"
        )

        # Read content from filesystem
        content = get_chunk_content(chunk_id)
        if content:
            print(content)
        else:
            print("[Content not available]")

        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_fast.py <query> [top_k]")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    # Load and init
    pinecone_key, openai_key = load_api_keys()
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")
    client = OpenAI(api_key=openai_key)

    # Execute query
    matches = query_rag(idx, client, query_text, top_k=top_k)

    # Format and display
    format_results(matches, query_text)


if __name__ == "__main__":
    main()
