#!/usr/bin/env python3
"""
RAG to Telegram - Query Pinecone and send results via Telegram

Usage:
  python3 rag_to_telegram.py "query" [top_k] [machine] [--zip]

Examples:
  python3 rag_to_telegram.py "LFI exploitation"
  python3 rag_to_telegram.py "RCE techniques" 10
  python3 rag_to_telegram.py "privesc" 5 gavel
  python3 rag_to_telegram.py "LFI" 5 --zip
"""

import os
import sys
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_sender import TelegramSender


def load_api_keys():
    """Load Pinecone and OpenAI API keys"""
    keys = {}
    try:
        with open("/root/.openskills/env/pinecone.env", "r") as f:
            for line in f:
                if line.strip().startswith("PINECONE_API_KEY="):
                    keys["pinecone_key"] = line.strip().split("=", 1)[1]
    except FileNotFoundError:
        pass

    try:
        with open("/root/.openskills/env/openai.env", "r") as f:
            for line in f:
                if line.strip().startswith("OPENAI_API_KEY="):
                    keys["openai_key"] = line.strip().split("=", 1)[1]
    except FileNotFoundError:
        pass

    return keys


def query_and_send(query_text, top_k=5, machine_filter=None, send_zip=False):
    """Query Pinecone and send results to Telegram"""
    from pinecone import Pinecone
    from openai import OpenAI

    keys = load_api_keys()
    if not keys.get("pinecone_key") or not keys.get("openai_key"):
        print("Missing API keys")
        sys.exit(1)

    # Initialize
    pc = Pinecone(api_key=keys["pinecone_key"])
    idx = pc.Index("rag-canonical-v1-emb3large")
    client = OpenAI(api_key=keys["openai_key"])
    sender = TelegramSender()

    # Generate embedding
    print(f"Generating embedding for: {query_text}")
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=query_text,
        dimensions=3072,
    )
    embedding = response.data[0].embedding

    # Query Pinecone
    query_params = {
        "vector": embedding,
        "top_k": top_k,
        "include_metadata": True,
    }
    if machine_filter:
        query_params["filter"] = {"machine": {"$eq": machine_filter.lower()}}

    results = idx.query(**query_params)
    matches = results.get("matches", [])

    if not matches:
        sender.send_message(f"No results for: {query_text}")
        print("No results found")
        return

    print(f"Found {len(matches)} results")

    if send_zip:
        # Create ZIP with results
        import tempfile
        import shutil

        tmpdir = tempfile.mkdtemp()
        try:
            for i, match in enumerate(matches, 1):
                meta = match.get("metadata", {})
                chunk_id = meta.get("chunk_id", match.get("id", f"chunk_{i}"))
                content = meta.get("content", "No content")
                safe_id = chunk_id.replace("::", "_")

                filepath = os.path.join(tmpdir, f"{i:02d}_{safe_id}.md")
                with open(filepath, "w") as f:
                    f.write(f"# {chunk_id}\n\n")
                    f.write(f"Score: {match.get('score', 0):.4f}\n")
                    f.write(f"Machine: {meta.get('machine', 'unknown')}\n\n---\n\n")
                    f.write(content)

            safe_query = "".join(c for c in query_text if c.isalnum() or c in "-_ ")[
                :30
            ]
            zip_path = os.path.join(tempfile.gettempdir(), f"rag_{safe_query}")
            archive = shutil.make_archive(zip_path, "zip", tmpdir)

            result = sender.send_document(
                archive, caption=f"RAG: {query_text} ({len(matches)} chunks)"
            )
            if result.get("ok"):
                print(f"ZIP sent: {os.path.basename(archive)}")
            else:
                print(f"Failed to send ZIP: {result}")

            os.remove(archive)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    else:
        # Send results as messages
        header = f"\U0001f50d *RAG Query Results*\n\nQuery: `{query_text}`\nResults: {len(matches)}\n"
        if machine_filter:
            header += f"Machine: {machine_filter}\n"
        sender.send_message(header, parse_mode="Markdown")

        for i, match in enumerate(matches, 1):
            meta = match.get("metadata", {})
            chunk_id = meta.get("chunk_id", match.get("id", "unknown"))
            score = match.get("score", 0)
            content = meta.get("content", "No content available")
            content_preview = content[:600]
            if len(content) > 600:
                content_preview += "..."

            msg = (
                f"*{i}. {chunk_id}*\n"
                f"Score: {score:.4f} | "
                f"{meta.get('machine', '?').upper()} | "
                f"{meta.get('phase', '?')} | "
                f"{meta.get('technique', '?')}\n\n"
                f"{content_preview}"
            )
            try:
                sender.send_message(msg, parse_mode="Markdown")
            except Exception:
                sender.send_message(msg)

    print("Done!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rag_to_telegram.py <query> [top_k] [machine] [--zip]")
        sys.exit(1)

    query_text = sys.argv[1]
    top_k = 5
    machine_filter = None
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
            machine_filter = positional[0]

    if len(positional) >= 2:
        machine_filter = positional[1]

    query_and_send(query_text, top_k, machine_filter, send_zip)


if __name__ == "__main__":
    main()
