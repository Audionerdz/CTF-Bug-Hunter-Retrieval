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
import config

ATLAS_ROOT = str(config.ATLAS_ROOT)
ATLAS_DEFAULT = str(config.ATLAS_DEFAULT)
ATLAS_ENV = str(config.ATLAS_ENV)
ATLAS_REGISTRY = str(config.ATLAS_REGISTRY)

__all__ = [
    "Atlas",
    "ATLAS_ROOT",
    "ATLAS_DEFAULT",
    "ATLAS_ENV",
    "ATLAS_REGISTRY",
]
__version__ = "2.0.0"
