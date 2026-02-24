#!/usr/bin/env python3
"""
CLI wrapper for canonical queries with machine filter.
For programmatic use: from rag import RAG; r = RAG(); r.query("text", machine="gavel")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.query import QueryEngine


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_canonical_openai.py <query> [OPTIONS]")
        print("\nOptions:")
        print("  --top-k <n>         Number of results (default: 5)")
        print("  --machine <name>    Filter by machine")
        print("  --namespace <ns>    Namespace to search in")
        print("\nExamples:")
        print("  python3 query_canonical_openai.py 'RCE PHP'")
        print("  python3 query_canonical_openai.py 'YAML injection' --top-k 10")
        print(
            "  python3 query_canonical_openai.py 'privesc' --machine gavel --namespace cve"
        )
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = 5
    machine = None
    namespace = None

    # Parse optional arguments
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--top-k" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        elif args[i] == "--machine" and i + 1 < len(args):
            machine = args[i + 1]
            i += 2
        elif args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        else:
            i += 1

    engine = QueryEngine(namespace=namespace)
    results = engine.search(query_text, top_k=top_k, machine=machine)
    engine.format_terminal(results, query=query_text)


if __name__ == "__main__":
    main()
