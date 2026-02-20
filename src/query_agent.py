#!/usr/bin/env python3
"""
Query Agent - Hybrid Architecture + Telegram
Search Pinecone + read local files from /home/kali/Desktop/RAG/

This is a standalone CLI tool. For the full hybrid agent, see:
  /root/.opencode/skills/query-agent/executables/query-agent-hybrid.py

Usage:
  python3 query_agent.py "query" [--top-k N] [--machine NAME] [--no-telegram]
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Configuration
INDEX_NAME = "rag-canonical-v1-emb3large"
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072
RAG_ROOT = Path("/home/kali/Desktop/RAG")
CHUNK_REGISTRY = RAG_ROOT / "chunk_registry.json"


def load_api_keys():
    """Load API keys from env files"""
    pinecone_key = None
    openai_key = None

    try:
        with open("/root/.openskills/env/pinecone.env", "r") as f:
            for line in f:
                if line.strip().startswith("PINECONE_API_KEY="):
                    pinecone_key = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass

    try:
        with open("/root/.openskills/env/openai.env", "r") as f:
            for line in f:
                if line.strip().startswith("OPENAI_API_KEY="):
                    openai_key = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass

    if not pinecone_key:
        print("PINECONE_API_KEY not found")
        sys.exit(1)
    if not openai_key:
        print("OPENAI_API_KEY not found")
        sys.exit(1)

    return pinecone_key, openai_key


class QueryAgent:
    """Query agent that searches Pinecone and reads content locally"""

    def __init__(self):
        from pinecone import Pinecone
        from openai import OpenAI

        self.pinecone_key, self.openai_key = load_api_keys()
        self.pc = Pinecone(api_key=self.pinecone_key)
        self.index = self.pc.Index(INDEX_NAME)
        self.openai_client = OpenAI(api_key=self.openai_key)

        # Load chunk registry
        if CHUNK_REGISTRY.exists():
            with open(CHUNK_REGISTRY) as f:
                self.chunk_map = json.load(f)
        else:
            self.chunk_map = {}
            print(f"Warning: chunk_registry.json not found at {CHUNK_REGISTRY}")

        print(f"Connected to: {INDEX_NAME}")
        print(f"Local root: {RAG_ROOT}")
        print(f"Registered chunks: {len(self.chunk_map)}")

    def get_embedding(self, text):
        """Generate 3072D embedding"""
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=text, dimensions=EMBEDDING_DIM
        )
        return response.data[0].embedding

    def extract_body(self, content):
        """Extract body without YAML frontmatter"""
        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            except Exception:
                pass
        return content

    def read_chunk_locally(self, chunk_id):
        """Read chunk from filesystem via registry"""
        if chunk_id not in self.chunk_map:
            return None, f"Not in registry: {chunk_id}"
        file_path = self.chunk_map[chunk_id]
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.extract_body(content), file_path
        except Exception as e:
            return None, f"Error: {e}"

    def query(self, user_query, top_k=5, machine_filter=None):
        """Search Pinecone and read content locally"""
        print(f"\nSearching: {user_query}")
        print(f"  Top-K: {top_k}")
        if machine_filter:
            print(f"  Machine: {machine_filter}")

        embedding = self.get_embedding(user_query)
        query_params = {"vector": embedding, "top_k": top_k, "include_metadata": True}
        if machine_filter:
            query_params["filter"] = {"machine": machine_filter.lower()}

        results = self.index.query(**query_params)
        print(f"\nFound {len(results['matches'])} results")

        responses = []
        for i, match in enumerate(results["matches"], 1):
            metadata = match["metadata"]
            chunk_id = metadata.get("chunk_id", match["id"])
            score = match["score"]

            content, file_path = self.read_chunk_locally(chunk_id)
            if not content:
                content = metadata.get("content", "No content")

            responses.append(
                {
                    "rank": i,
                    "chunk_id": chunk_id,
                    "machine": metadata.get("machine", "unknown"),
                    "phase": metadata.get("phase", "unknown"),
                    "technique": metadata.get("technique", "unknown"),
                    "domain": metadata.get("domain", "unknown"),
                    "score": score,
                    "file_path": file_path
                    if isinstance(file_path, str) and os.path.exists(file_path)
                    else "",
                    "content": content[:1000],
                    "content_full": content,
                    "content_length": len(content),
                }
            )
            print(f"\n  {i}. {chunk_id} (score: {score:.3f})")

        return responses

    def format_response(self, results, query=None, machine_filter=None):
        """Format results as Markdown"""
        if not results:
            return "No results found."

        output = [
            "# Query Agent Results\n",
            f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Index:** `{INDEX_NAME}`\n",
        ]
        if query:
            output.append(f"**Query:** `{query}`\n")
        if machine_filter:
            output.append(f"**Machine:** `{machine_filter}`\n")
        output.append(f"**Results:** {len(results)}\n---\n")

        for r in results:
            output.append(f"### {r['rank']}. {r['chunk_id']}")
            output.append(f"- **Machine:** {r['machine'].upper()}")
            output.append(f"- **Phase:** {r['phase']}")
            output.append(f"- **Technique:** {r['technique']}")
            output.append(f"- **Score:** {r['score']:.3f}")
            content_safe = r["content_full"].replace("```", "~~~")
            output.append(f"\n```\n{content_safe}\n```\n")

        return "\n".join(output)

    def save_markdown(self, content, query):
        """Save markdown to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c for c in query if c.isalnum() or c in "-_").rstrip()[:30]
        filepath = RAG_ROOT / f"query_results_{safe_query}_{timestamp}.md"
        try:
            filepath.write_text(content, encoding="utf-8")
            print(f"\nSaved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving: {e}")
            return None

    def send_to_telegram(self, markdown_path):
        """Send markdown file to Telegram"""
        sys.path.insert(0, str(RAG_ROOT))
        from telegram_sender import TelegramSender as TS

        try:
            sender = TS()
            result = sender.send_document(
                str(markdown_path), caption="Query Agent Results"
            )
            if result.get("ok"):
                print(f"Sent to Telegram: {markdown_path.name}")
                return True
            else:
                print(f"Telegram error: {result}")
                return False
        except Exception as e:
            print(f"Telegram error: {e}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query_agent.py <query> [OPTIONS]")
        print("  --top-k <n>         Number of results (default: 5)")
        print("  --machine <name>    Filter by machine")
        print("  --no-telegram       Don't send to Telegram")
        sys.exit(1)

    query = sys.argv[1]
    machine = None
    top_k = 5
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
        elif args[i] == "--no-telegram":
            send_telegram = False
            i += 1
        else:
            i += 1

    try:
        agent = QueryAgent()
        results = agent.query(query, top_k=top_k, machine_filter=machine)
        md = agent.format_response(results, query=query, machine_filter=machine)
        filepath = agent.save_markdown(md, query)
        if send_telegram and filepath:
            agent.send_to_telegram(filepath)
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
