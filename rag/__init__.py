"""
RAG Framework - Unified interface for vectorization, querying, chat, and Telegram.

Usage:
    from rag import RAG

    r = RAG()
    r.query("LFI exploitation")
    r.vectorize("/path/to/chunks")
    r.chat()
    r.send("hello from RAG")
"""

from rag.core import RAG

__all__ = ["RAG"]
__version__ = "1.0.0"
