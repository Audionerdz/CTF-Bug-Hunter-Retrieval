"""
QueryEngine - Unified search interface for Pinecone RAG index.

Supports:
    - Fast query (vector search + local file content)
    - Filtered query (by machine, domain, phase, etc.)
    - Chunk fetch by ID
    - Formatted output (terminal, markdown, dict)
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class QueryEngine:
    """Unified query interface for the RAG system."""

    def __init__(
        self,
        registry=None,
        pinecone_key=None,
        openai_key=None,
        index_name=None,
        namespace=None,
    ):
        self._pinecone_key = pinecone_key
        self._openai_key = openai_key
        self._pc = None
        self._index = None
        self._openai = None

        # Use provided registry or create one
        from rag.registry import Registry

        self.registry = registry or Registry()

        # Config
        self.index_name = index_name or config.INDEX_NAME
        self.namespace = (
            config.resolve_namespace(namespace) if namespace else config.NAMESPACE
        )
        self.embedding_model = config.EMBEDDING_MODEL
        self.embedding_dim = config.EMBEDDING_DIM

    # ------------------------------------------------------------------
    # Lazy init
    # ------------------------------------------------------------------

    def _ensure_keys(self):
        if not self._pinecone_key:
            self._pinecone_key = config.get_pinecone_key()
        if not self._openai_key:
            self._openai_key = config.get_openai_key()

    def _get_index(self):
        if self._index is None:
            self._ensure_keys()
            from pinecone import Pinecone

            self._pc = Pinecone(api_key=self._pinecone_key)
            self._index = self._pc.Index(self.index_name)
        return self._index

    def _get_openai(self):
        if self._openai is None:
            self._ensure_keys()
            from openai import OpenAI

            self._openai = OpenAI(api_key=self._openai_key)
        return self._openai

    def _embed(self, text):
        """Generate embedding for a query string."""
        client = self._get_openai()
        response = client.embeddings.create(
            model=self.embedding_model, input=text, dimensions=self.embedding_dim
        )
        return response.data[0].embedding

    # ------------------------------------------------------------------
    # Core query
    # ------------------------------------------------------------------

    def search(
        self,
        query,
        top_k=5,
        machine=None,
        domain=None,
        phase=None,
        include_content=True,
        namespace=None,
    ):
        """
        Search the RAG index.

        Args:
            query: search text.
            top_k: number of results.
            machine: filter by machine name.
            domain: filter by domain.
            phase: filter by phase.
            include_content: if True, read full content from local files.
            namespace: namespace to search in (optional, uses instance default if not provided).

        Returns:
            List of result dicts with keys:
                rank, chunk_id, score, machine, domain, phase, technique,
                content, file_path, metadata
        """
        idx = self._get_index()
        embedding = self._embed(query)

        # Resolve namespace
        ns = config.resolve_namespace(namespace) if namespace else self.namespace

        query_params = {
            "vector": embedding,
            "top_k": top_k,
            "include_metadata": True,
            "namespace": ns,
        }

        # Build metadata filter
        filters = {}
        if machine:
            filters["machine"] = {"$eq": machine.lower()}
        if domain:
            filters["domain"] = {"$eq": domain.lower()}
        if phase:
            filters["phase"] = {"$eq": phase.lower()}
        if filters:
            query_params["filter"] = filters

        results = idx.query(**query_params)
        matches = results.get("matches", [])

        output = []
        for i, match in enumerate(matches, 1):
            meta = match.get("metadata", {})
            chunk_id = meta.get("chunk_id", match.get("id", "unknown"))

            # Try to read full content from local filesystem
            content = None
            file_path = None
            if include_content:
                content = self.registry.get_content(chunk_id)
                file_path = self.registry.get(chunk_id)

            if content is None:
                content = meta.get("content", "")

            output.append(
                {
                    "rank": i,
                    "chunk_id": chunk_id,
                    "score": match.get("score", 0),
                    "machine": meta.get("machine", "unknown"),
                    "domain": meta.get("domain", "unknown"),
                    "phase": meta.get("phase", "unknown"),
                    "technique": meta.get("technique", "unknown"),
                    "content": content,
                    "file_path": file_path or "",
                    "metadata": meta,
                }
            )

        return output

    def fetch(self, chunk_id, namespace=None):
        """
        Fetch a specific chunk by ID from Pinecone.

        Args:
            chunk_id: ID of the chunk to fetch.
            namespace: namespace to fetch from (optional, uses instance default if not provided).

        Returns:
            dict with chunk metadata and content, or None.
        """
        idx = self._get_index()

        # Resolve namespace
        ns = config.resolve_namespace(namespace) if namespace else self.namespace

        results = idx.fetch(ids=[chunk_id], namespace=ns)

        if not results or not results.get("vectors"):
            return None

        chunk = results["vectors"].get(chunk_id)
        if not chunk:
            return None

        meta = chunk.get("metadata", {})
        return {
            "chunk_id": chunk_id,
            "metadata": meta,
            "content": meta.get("content", ""),
        }

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def format_terminal(self, results, query=None):
        """Print results to terminal."""
        header = f"\n{'=' * 60}\n"
        if query:
            header += f"Query: '{query}'\n"
        header += f"Results: {len(results)} matches\n{'=' * 60}\n"
        print(header)

        for r in results:
            print(f"{r['rank']}. {r['chunk_id']}")
            print(
                f"   Score: {r['score']:.4f} | {r['machine']} | {r['domain']} | {r['phase']}"
            )
            if r["content"]:
                # Show first 500 chars
                preview = r["content"][:500]
                if len(r["content"]) > 500:
                    preview += "\n   ..."
                print(f"\n{preview}\n")
            print()

    def format_markdown(self, results, query=None, machine=None):
        """Format results as markdown string."""
        lines = [
            "# RAG Query Results\n",
            f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Index:** `{self.index_name}`",
        ]
        if query:
            lines.append(f"**Query:** `{query}`")
        if machine:
            lines.append(f"**Machine:** `{machine}`")
        lines.append(f"**Results:** {len(results)}\n---\n")

        for r in results:
            lines.append(f"### {r['rank']}. {r['chunk_id']}")
            lines.append(f"- **Machine:** {r['machine'].upper()}")
            lines.append(f"- **Phase:** {r['phase']}")
            lines.append(f"- **Technique:** {r['technique']}")
            lines.append(f"- **Score:** {r['score']:.3f}")
            content_safe = r["content"].replace("```", "~~~") if r["content"] else ""
            lines.append(f"\n```\n{content_safe}\n```\n")

        return "\n".join(lines)

    def save_markdown(self, results, query, output_dir=None):
        """Save results as a markdown file. Returns the file path."""
        md = self.format_markdown(results, query=query)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c for c in query if c.isalnum() or c in "-_").rstrip()[:30]
        out_dir = Path(output_dir) if output_dir else config.RAG_ROOT
        filepath = out_dir / f"query_results_{safe_query}_{timestamp}.md"
        filepath.write_text(md, encoding="utf-8")
        print(f"Saved: {filepath}")
        return filepath

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self):
        """Get Pinecone index statistics."""
        idx = self._get_index()
        stats = idx.describe_index_stats()
        total = stats.get("total_vector_count", 0)
        namespaces = stats.get("namespaces", {})

        ns_display = self.namespace if self.namespace else "__default__"
        print(f"\nIndex: {self.index_name}:{ns_display}")
        print(f"  Total vectors: {total}")
        for ns, info in namespaces.items():
            ns_name = ns if ns else "__default__"
            marker = " <-- CURRENT" if ns == self.namespace else ""
            print(f"  {ns_name}: {info.get('vector_count', 0)} vectors{marker}")

        return stats

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        ns_display = self.namespace if self.namespace else "__default__"
        return f"QueryEngine(index={self.index_name}, namespace={ns_display}, registry={self.registry.count()} chunks)"
