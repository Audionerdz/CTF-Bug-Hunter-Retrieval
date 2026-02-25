#!/usr/bin/env python3
"""
CLI wrapper for the Query Agent (search + save + telegram).
For programmatic use: from atlas_engine import RAG; r = RAG(); r.query("text")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.query import QueryEngine
from atlas_engine.telegram import Telegram


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_agent.py <query> [OPTIONS]")
        print("  --top-k <n>         Number of results (default: 5)")
        print("  --machine <name>    Filter by machine")
        print("  --namespace <ns>    Namespace to search in")
        print("  --no-telegram       Don't send to Telegram")
        sys.exit(1)

    query = sys.argv[1]
    machine = None
    top_k = 5
    namespace = None
    send_telegram = True

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--machine" and i + 1 < len(args):
            machine = args[i + 1]
            i += 2
        elif args[i] == "--top-k" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        elif args[i] == "--namespace" and i + 1 < len(args):
            namespace = args[i + 1]
            i += 2
        elif args[i] == "--no-telegram":
            send_telegram = False
            i += 1
        else:
            i += 1

    try:
        engine = QueryEngine(namespace=namespace)
        results = engine.search(query, top_k=top_k, machine=machine)
        engine.format_terminal(results, query=query)

        filepath = engine.save_markdown(results, query)

        if send_telegram and filepath:
            tg = Telegram()
            result = tg.file(str(filepath), caption="Query Agent Results")
            if result.get("ok"):
                print(f"Sent to Telegram: {filepath.name}")
            else:
                print(f"Telegram error: {result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
