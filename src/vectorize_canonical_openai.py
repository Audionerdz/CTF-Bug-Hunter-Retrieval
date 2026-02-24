#!/usr/bin/env python3
"""
CLI wrapper for the Vectorizer.
For programmatic use: from rag import RAG; r = RAG(); r.vectorize(path)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.vectorizer import Vectorizer


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vectorize_canonical_openai.py <path> [OPTIONS]")
        print("  --namespace <ns>  Namespace to vectorize into")
        print("\nModes:")
        print("  Directory:  python3 vectorize_canonical_openai.py /path/to/chunks/")
        print("  File:       python3 vectorize_canonical_openai.py /path/chunk.md")
        print("  Name:       python3 vectorize_canonical_openai.py cheatsheets")
        print("\nExample:")
        print("  python3 vectorize_canonical_openai.py /chunks --namespace cve")
        sys.exit(1)

    path = sys.argv[1]
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

    v = Vectorizer(namespace=namespace)
    v.run(path)


if __name__ == "__main__":
    main()
