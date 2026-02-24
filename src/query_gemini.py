#!/usr/bin/env python3
"""
Query Pinecone using Gemini embeddings (3072 dimensions).

Usage:
    python3 query_gemini.py "your query here" [--top-k 5]

Environment files:
    RAG/.env/gemini.env - Google API key
    RAG/.env/pinecone.env - Pinecone config

Model: gemini-embedding-001 (3072 dimensions) - compatible with rag-canonical-v1-emb3large
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai
from google.genai import types

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

GEMINI_ENV_PATH = str(config.ENV_DIR / "gemini.env")
PINECONE_ENV_PATH = str(config.ENV_DIR / "pinecone.env")

DEFAULT_INDEX = "rag-canonical-v1-emb3large"
DEFAULT_NAMESPACE = ""


def load_env():
    load_dotenv(GEMINI_ENV_PATH)
    load_dotenv(PINECONE_ENV_PATH)

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in gemini.env")

    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY not found in pinecone.env")

    return google_api_key, pinecone_api_key


def get_gemini_embedding(text: str, api_key: str) -> list:
    client = genai.Client(api_key=api_key)

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY", output_dimensionality=3072
        ),
    )

    return result.embeddings[0].values


def query_pinecone(embedding: list, index_name: str, namespace: str, top_k: int = 5):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)

    results = index.query(
        vector=embedding, top_k=top_k, namespace=namespace, include_metadata=True
    )
    return results


def format_results(results) -> str:
    output = []
    output.append(f"\n{'=' * 60}")
    output.append(f"Found {len(results['matches'])} results")
    output.append(f"{'=' * 60}\n")

    for i, match in enumerate(results["matches"], 1):
        metadata = match.get("metadata", {})
        score = match.get("score", 0)

        output.append(f"### Result {i} (Score: {score:.4f})")
        output.append(f"- **chunk_id**: {metadata.get('chunk_id', 'N/A')}")
        output.append(f"- **domain**: {metadata.get('domain', 'N/A')}")
        output.append(f"- **chunk_type**: {metadata.get('chunk_type', 'N/A')}")
        output.append(f"- **tags**: {metadata.get('tags', [])}")

        content = metadata.get("content", "")
        if content:
            preview = content[:800] + "..." if len(content) > 800 else content
            output.append(f"\n**Content:**\n{preview}\n")

        output.append("-" * 40)

    return "\n".join(output)


def list_pinecone_indexes():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indexes = pc.list_indexes()
    print("\n📋 Available Pinecone indexes:")
    for idx in indexes:
        index = pc.Index(idx.name)
        stats = index.describe_index_stats()
        print(
            f"  - {idx.name}: {stats.get('dimension', '?')}D, {stats.get('total_vector_count', 0)} vectors"
        )
        namespaces = stats.get("namespaces", {})
        for ns, info in namespaces.items():
            ns_name = ns if ns else "__default__"
            print(f"      └─ {ns_name}: {info.get('vector_count', 0)} vectors")
    return indexes


def main():
    parser = argparse.ArgumentParser(
        description="Query Pinecone with Gemini embeddings (3072D)"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--top-k", type=int, default=5, help="Number of results (default: 5)"
    )
    parser.add_argument(
        "--index",
        default=DEFAULT_INDEX,
        help=f"Pinecone index (default: {DEFAULT_INDEX})",
    )
    parser.add_argument(
        "--namespace", default=DEFAULT_NAMESPACE, help="Namespace (empty = default)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument(
        "--list-indexes", action="store_true", help="List available indexes"
    )

    args = parser.parse_args()

    google_api_key, pinecone_api_key = load_env()

    if args.list_indexes:
        list_pinecone_indexes()
        return

    if not args.query:
        parser.print_help()
        print("\n📝 Example: python3 query_gemini.py 'LFI exploitation techniques'")
        return

    if args.verbose:
        print(f"\n🔍 Generating embedding with Gemini...")

    embedding = get_gemini_embedding(args.query, google_api_key)

    if args.verbose:
        print(f"   Embedding: {len(embedding)} dimensions")
        print(f"   Index: {args.index}")
        print(f"   Namespace: {args.namespace or '__default__'}")

    print(f'\n🔎 Querying: "{args.query}"')
    results = query_pinecone(embedding, args.index, args.namespace, args.top_k)

    print(format_results(results))


if __name__ == "__main__":
    main()
