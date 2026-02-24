#!/usr/bin/env python3
"""
CLI wrapper for fast RAG queries.
For programmatic use: from rag import RAG; r = RAG(); r.query("text")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.query import QueryEngine


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_fast.py <query> [OPTIONS]")
        print("  [top_k]           Number of results (default: 5)")
        print("  --namespace <ns>  Namespace to search in")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = 5
    namespace = None

    # Parse optional arguments
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
        elif arg.isdigit():
            top_k = int(arg)

    engine = QueryEngine(namespace=namespace)
    results = engine.search(query_text, top_k=top_k)
    engine.format_terminal(results, query=query_text)


if __name__ == "__main__":
    main()
