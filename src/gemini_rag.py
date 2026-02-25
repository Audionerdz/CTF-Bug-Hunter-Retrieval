#!/usr/bin/env python3
"""
CLI wrapper for interactive Gemini RAG chat.
For programmatic use: from atlas_engine import RAG; r = RAG(); r.chat()
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.chat import Chat


def main():
    import sys

    namespace = None

    # Parse optional arguments
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("Usage: python3 gemini_rag.py [OPTIONS]")
            print("  --namespace <ns>  Namespace to search in")
            sys.exit(0)
        else:
            i += 1

    chat = Chat(namespace=namespace)
    chat.interactive()


if __name__ == "__main__":
    main()
