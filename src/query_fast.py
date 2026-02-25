#!/usr/bin/env python3
"""
CLI wrapper for fast RAG queries.
For programmatic use: from atlas_engine import RAG; r = RAG(); r.query("text")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.query import QueryEngine


def main():
    if len(sys.argv) < 2:
        print("Usage: atlas-query <query> [OPTIONS]")
        print("Options:")
        print("  <number>          Number of results (default: 5)")
        print("  --top <number>    Number of results to return")
        print("  --namespace <ns>  Namespace to search in")
        print("  --full            Show full content (default)")
        print("  --preview <chars> Truncate preview to N characters")
        print("\nExamples:")
        print("  atlas-query 'XXE exploitation'")
        print("  atlas-query 'buffer overflow' 10")
        print("  atlas-query 'RCE' --namespace cve --preview 1000")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = 5
    namespace = None
    max_chars = None  # None = show full content

    # Parse optional arguments
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif arg == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        elif arg == "--preview" and i + 1 < len(args):
            max_chars = int(args[i + 1])
            i += 2
        elif arg == "--full":
            max_chars = None
            i += 1
        elif arg.isdigit():
            top_k = int(arg)
            i += 1
        else:
            i += 1

    engine = QueryEngine(namespace=namespace)
    results = engine.search(query_text, top_k=top_k)
    engine.format_terminal(results, query=query_text, max_chars=max_chars)


if __name__ == "__main__":
    main()
