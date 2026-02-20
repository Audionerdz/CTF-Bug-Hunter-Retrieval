#!/usr/bin/env python3
"""
OFFICIAL QUERY AGENT: rag-canonical-v1-emb3large via OpenAI 3072D

Unified query interface for the canonical RAG system.
- Uses OpenAI text-embedding-3-large (3072D)
- Queries root namespace (Pinecone default)
- Supports cross-machine filtering via metadata
- Returns relevance-ranked results

Usage:
  python3 /root/.openskills/query_canonical_openai.py "your query"
  python3 /root/.openskills/query_canonical_openai.py "RCE techniques" 5

  Advanced:
    python3 /root/.openskills/query_canonical_openai.py "privesc" 10 gavel
"""

import sys
import os
from pinecone import Pinecone
from openai import OpenAI

# ============================================================================
# INITIALIZATION
# ============================================================================


def load_api_keys():
    """Load Pinecone and OpenAI API keys"""
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

    if not pinecone_key or not openai_key:
        print("❌ ERROR: API keys not found")
        sys.exit(1)

    return pinecone_key, openai_key


def init_clients(pinecone_key, openai_key):
    """Initialize Pinecone and OpenAI clients"""
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")
    client = OpenAI(api_key=openai_key)
    return idx, client


# ============================================================================
# QUERY EXECUTION
# ============================================================================


def query_rag(idx, client, query_text, top_k=5, machine_filter=None):
    """
    Execute a query against the canonical RAG index

    Args:
        idx: Pinecone index
        client: OpenAI client
        query_text: Search query
        top_k: Number of results
        machine_filter: Optional machine name to filter results

    Returns:
        List of matched vectors with metadata
    """

    # Generate query embedding with OpenAI
    response = client.embeddings.create(
        model="text-embedding-3-large", input=query_text, dimensions=3072
    )

    query_embedding = response.data[0].embedding

    # Query without namespace (uses root)
    # If machine_filter provided, use metadata filter
    if machine_filter:
        results = idx.query(
            vector=query_embedding,
            top_k=top_k,
            filter={"machine": {"$eq": machine_filter}},
            include_metadata=True,
        )
    else:
        results = idx.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    return results["matches"]


def format_results(matches, query_text):
    """Format and display query results"""

    print(f"\n{'=' * 70}")
    print(f"🔍 Query: '{query_text}'")
    print(f"{'=' * 70}")
    print(f"✅ Results: {len(matches)} matches\n")

    if not matches:
        print("No results found.")
        return

    for i, match in enumerate(matches, 1):
        meta = match["metadata"]
        print(f"{i}. {meta['chunk_id']}")
        print(
            f"   Score: {match['score']:.4f} | {meta.get('domain', 'unknown')} | {meta.get('chunk_type', 'unknown')} | {meta.get('confidence', 'unknown')}\n"
        )

        # Print content if available
        if "content" in meta:
            content = meta["content"]
            # Print first 1000 chars or full content if shorter
            if len(content) > 1000:
                print(content[:1000] + "...\n")
            else:
                print(content + "\n")

        print()


# ============================================================================
# MAIN
# ============================================================================


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_canonical_openai.py <query> [top_k] [machine]")
        print("\nExamples:")
        print("  python3 query_canonical_openai.py 'RCE PHP'")
        print("  python3 query_canonical_openai.py 'YAML injection' 10")
        print("  python3 query_canonical_openai.py 'privesc' 5 gavel")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    machine_filter = sys.argv[3] if len(sys.argv) > 3 else None

    # Load and init
    pinecone_key, openai_key = load_api_keys()
    idx, client = init_clients(pinecone_key, openai_key)

    # Execute query
    matches = query_rag(
        idx, client, query_text, top_k=top_k, machine_filter=machine_filter
    )

    # Format and display
    format_results(matches, query_text)


if __name__ == "__main__":
    main()
