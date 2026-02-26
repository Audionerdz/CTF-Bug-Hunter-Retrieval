"""
SemanticCache - Pinecone-based semantic cache for LLM responses.

Uses the existing Pinecone index with a dedicated '__cache__' namespace.
When a query is semantically similar to a cached one (cosine >= threshold),
returns the cached response instantly without calling the LLM.

No external infrastructure required -- reuses existing Pinecone + OpenAI embeddings.

Usage:
    # Automatic via Chat (enabled by default):
    atlas.chat(backend="groq")   # cache active
    atlas.ask("What is LFI?")   # cache miss -> LLM -> cached
    atlas.ask("Explain LFI")    # cache hit -> instant response

    # Direct access:
    atlas.chat_engine.cache.stats()
    atlas.chat_engine.cache.clear()
"""

import hashlib
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# Cache configuration
CACHE_NAMESPACE = "__cache__"
SIMILARITY_THRESHOLD = 0.92  # cosine similarity >= 0.92 = cache hit
CACHE_TTL_DAYS = 30  # metadata field, not enforced by Pinecone


class SemanticCache:
    """Pinecone-based semantic cache for LLM responses."""

    def __init__(self, openai_client, pc_index, threshold=None):
        """
        Args:
            openai_client: OpenAI client for embeddings.
            pc_index: Pinecone index instance.
            threshold: cosine similarity threshold for cache hit (default: 0.92).
        """
        self._openai = openai_client
        self._index = pc_index
        self.threshold = threshold or SIMILARITY_THRESHOLD
        self._hits = 0
        self._misses = 0

    # ==================================================================
    # EMBEDDING
    # ==================================================================

    def _embed(self, text):
        """Generate embedding via OpenAI."""
        response = self._openai.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=text,
            dimensions=config.EMBEDDING_DIM,
        )
        return response.data[0].embedding

    # ==================================================================
    # LOOKUP
    # ==================================================================

    def lookup(self, query):
        """
        Check if a semantically similar query exists in cache.

        Args:
            query: the user query string.

        Returns:
            cached response string if hit, None if miss.
        """
        try:
            embedding = self._embed(query)

            results = self._index.query(
                vector=embedding,
                top_k=1,
                include_metadata=True,
                namespace=CACHE_NAMESPACE,
            )

            matches = results.get("matches", [])
            if matches and matches[0].get("score", 0) >= self.threshold:
                self._hits += 1
                cached = matches[0]["metadata"]
                return {
                    "response": cached.get("response", ""),
                    "sources": cached.get("sources", ""),
                    "backend": cached.get("backend", ""),
                    "score": matches[0]["score"],
                    "original_query": cached.get("query", ""),
                }

            self._misses += 1
            return None

        except Exception:
            # Cache should never break the main flow
            self._misses += 1
            return None

    # ==================================================================
    # STORE
    # ==================================================================

    def store(self, query, response, sources, backend):
        """
        Store a query-response pair in the cache.

        Args:
            query: original query string.
            response: LLM response string.
            sources: comma-separated source IDs.
            backend: backend that generated the response.
        """
        try:
            embedding = self._embed(query)

            # Deterministic ID based on query content
            cache_id = "cache::" + hashlib.md5(query.encode()).hexdigest()[:16]

            self._index.upsert(
                vectors=[
                    {
                        "id": cache_id,
                        "values": embedding,
                        "metadata": {
                            "query": query,
                            "response": response,
                            "sources": sources
                            if isinstance(sources, str)
                            else ",".join(str(s) for s in sources),
                            "backend": backend,
                            "cached_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                        },
                    }
                ],
                namespace=CACHE_NAMESPACE,
            )
        except Exception:
            # Cache store failure is non-fatal
            pass

    # ==================================================================
    # MANAGEMENT
    # ==================================================================

    def clear(self):
        """Clear all cached entries."""
        try:
            self._index.delete(delete_all=True, namespace=CACHE_NAMESPACE)
            self._hits = 0
            self._misses = 0
            print(f"Cache cleared (namespace: {CACHE_NAMESPACE})")
        except Exception as e:
            print(f"Cache clear error: {e}")

    def stats(self):
        """Print cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        print(f"\nSemantic Cache Stats:")
        print(f"  Hits: {self._hits}")
        print(f"  Misses: {self._misses}")
        print(f"  Hit rate: {hit_rate:.1f}%")
        print(f"  Threshold: {self.threshold}")
        print(f"  Namespace: {CACHE_NAMESPACE}")
        return {"hits": self._hits, "misses": self._misses, "hit_rate": hit_rate}

    def __repr__(self):
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return (
            f"SemanticCache(threshold={self.threshold}, "
            f"hits={self._hits}, misses={self._misses}, "
            f"hit_rate={hit_rate:.1f}%)"
        )
