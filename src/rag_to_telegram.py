#!/usr/bin/env python3
"""
CLI wrapper for query + send to Telegram.
For programmatic use: from atlas_engine import RAG; r = RAG(); r.send(r.query("text"))
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.query import QueryEngine
from atlas_engine.telegram import Telegram


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rag_to_telegram.py <query> [top_k] [machine] [--zip]")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = 5
    machine = None
    send_zip = False

    args = sys.argv[2:]
    positional = []
    for arg in args:
        if arg == "--zip":
            send_zip = True
        else:
            positional.append(arg)

    if len(positional) >= 1:
        try:
            top_k = int(positional[0])
        except ValueError:
            machine = positional[0]
    if len(positional) >= 2:
        machine = positional[1]

    engine = QueryEngine()
    results = engine.search(query_text, top_k=top_k, machine=machine)

    if not results:
        print("No results found.")
        sys.exit(0)

    tg = Telegram()

    if send_zip:
        import tempfile
        import shutil
        import os

        tmpdir = tempfile.mkdtemp()
        try:
            for r in results:
                safe_id = r["chunk_id"].replace("::", "_")
                filepath = os.path.join(tmpdir, f"{r['rank']:02d}_{safe_id}.md")
                with open(filepath, "w") as f:
                    f.write(
                        f"# {r['chunk_id']}\n\nScore: {r['score']:.4f}\n"
                        f"Machine: {r['machine']}\n\n---\n\n{r['content']}"
                    )

            safe_query = "".join(c for c in query_text if c.isalnum() or c in "-_ ")[
                :30
            ]
            zip_path = os.path.join(tempfile.gettempdir(), f"rag_{safe_query}")
            archive = shutil.make_archive(zip_path, "zip", tmpdir)
            tg.file(archive, caption=f"RAG: {query_text} ({len(results)} chunks)")
            os.remove(archive)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    else:
        tg.send(results)

    print("Done!")


if __name__ == "__main__":
    main()
