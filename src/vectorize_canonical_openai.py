#!/usr/bin/env python3
"""
CLI wrapper for the Vectorizer.
For programmatic use: from atlas_engine import RAG; r = RAG(); r.vectorize(path)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.vectorizer import Vectorizer


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vectorize_canonical_openai.py <path> [OPTIONS]")
        print("  --namespace <ns>   Namespace to vectorize into")
        print("  --domain <domain>  Metadata domain (e.g. cve, web, linux)")
        print("  --tags <t1,t2>     Comma-separated tags to inject")
        print("\nModes:")
        print("  Directory:  vectorize /path/to/chunks/")
        print("  File:       vectorize /path/chunk.md")
        print("  Name:       vectorize cheatsheets")
        print("\nExamples:")
        print("  vectorize /chunks --namespace cve")
        print("  vectorize notes.md --domain web --tags exploit,2026")
        sys.exit(1)

    path = sys.argv[1]
    namespace = None
    domain = None
    tags = None

    # Parse optional arguments
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]
            i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            tags = [t.strip() for t in args[i + 1].split(",")]
            i += 2
        else:
            i += 1

    v = Vectorizer(namespace=namespace)
    v.run(path, domain=domain, tags=tags)


if __name__ == "__main__":
    main()
