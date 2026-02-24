#!/usr/bin/env python3
"""
CLI wrapper for fetching a specific chunk by ID.
For programmatic use: from rag import RAG; r = RAG(); r.fetch("chunk_id")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.query import QueryEngine


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_chunk.py <chunk_id> [OPTIONS]")
        print("  --namespace <ns>  Namespace to fetch from")
        print("\nExample: python3 query_chunk.py technique::linux::compression::001")
        print("         python3 query_chunk.py chunk_id --namespace cve")
        sys.exit(1)

    chunk_id = sys.argv[1]
    namespace = None

    # Parse optional arguments
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        else:
            i += 1

    engine = QueryEngine(namespace=namespace)
    result = engine.fetch(chunk_id)

    if result:
        meta = result["metadata"]
        print(f"\nChunk: {chunk_id}")
        print("=" * 60)
        for k, v in meta.items():
            if k == "content":
                continue
            print(f"  {k}: {v}")
        content = result.get("content", "")
        if content:
            print(f"\nContent ({len(content)} chars):")
            print("-" * 60)
            print(content)
    else:
        print(f"Chunk not found: {chunk_id}")


if __name__ == "__main__":
    main()
