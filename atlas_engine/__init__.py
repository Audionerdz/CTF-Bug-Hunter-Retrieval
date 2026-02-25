"""
Atlas Engine - The most ruthless Retrieval-Augmented Generation framework.

Usage:
    from atlas_engine import Atlas

    atlas = Atlas()
    atlas.query("XXE exploitation")
    atlas.vectorize("/path/to/chunks", domain="web")
    atlas.chat(llm="gemini")
    atlas.send("critical finding detected")
"""

from atlas_engine.core import RAG as Atlas

__all__ = ["Atlas"]
__version__ = "2.0.0"
