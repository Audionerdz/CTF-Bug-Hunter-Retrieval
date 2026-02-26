#!/usr/bin/env python3
"""
Centralized configuration for RAG system.
All scripts should import from this module instead of hardcoding paths.
"""

import os
import sys
from pathlib import Path

# ============================================================================
# BASE DIRECTORIES
# ============================================================================

# RAG Root directory (where this script is located)
RAG_ROOT = Path(__file__).parent.resolve()
ATLAS_ROOT = RAG_ROOT

# Environment files directory
ENV_DIR = RAG_ROOT / ".env"
ATLAS_ENV = ENV_DIR

# Chunk registry file
CHUNK_REGISTRY = RAG_ROOT / "chunk_registry.json"
ATLAS_REGISTRY = CHUNK_REGISTRY

# Default directory for all chunks (generated or otherwise)
CHUNKS_DIR = RAG_ROOT / "default"
DEFAULT_CHUNKS_DIR = CHUNKS_DIR
ATLAS_DEFAULT = CHUNKS_DIR

# ============================================================================
# PINECONE CONFIGURATION
# ============================================================================

# Default index and namespace
INDEX_NAME = "rag-canonical-v1-emb3large"
NAMESPACE = ""  # Empty string = root namespace (__default__)

# Namespace presets for organization
NAMESPACE_PRESETS = {
    "root": "",  # Root namespace
    "cve": "cve",  # CVE/vulnerability namespace
    "technique": "technique",  # Security techniques
    "ctf": "ctf",  # CTF-specific content
    "tools": "tools",  # Security tools
    "payloads": "payloads",  # Exploit payloads
}

# ============================================================================
# EMBEDDING CONFIGURATION
# ============================================================================

EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072

# ============================================================================
# API KEY LOADING
# ============================================================================


def _load_env_file(filename):
    """Load key-value pairs from an env file in RAG_ROOT/.env/"""
    env_path = ENV_DIR / filename

    if not env_path.exists():
        return {}

    env_vars = {}
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"⚠️  Warning: Error loading {filename}: {e}", file=sys.stderr)

    return env_vars


def get_pinecone_key():
    """Get Pinecone API key from .env/pinecone.env"""
    env_vars = _load_env_file("pinecone.env")
    key = env_vars.get("PINECONE_API_KEY")

    if not key:
        raise ValueError(
            f"PINECONE_API_KEY not found in {ENV_DIR}/pinecone.env\n"
            f"Create this file in {ENV_DIR}/ with:\n"
            f"  PINECONE_API_KEY=your_key_here"
        )

    return key


def get_openai_key():
    """Get OpenAI API key from .env/openai.env"""
    env_vars = _load_env_file("openai.env")
    key = env_vars.get("OPENAI_API_KEY")

    if not key:
        raise ValueError(
            f"OPENAI_API_KEY not found in {ENV_DIR}/openai.env\n"
            f"Create this file in {ENV_DIR}/ with:\n"
            f"  OPENAI_API_KEY=your_key_here"
        )

    return key


def get_telegram_keys():
    """Get Telegram keys from .env/telegram.env"""
    env_vars = _load_env_file("telegram.env")

    token = env_vars.get("TELEGRAM_BOT_TOKEN")
    chat_id = env_vars.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError(
            f"TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in {ENV_DIR}/telegram.env\n"
            f"Create this file in {ENV_DIR}/ with:\n"
            f"  TELEGRAM_BOT_TOKEN=your_token\n"
            f"  TELEGRAM_CHAT_ID=your_chat_id"
        )

    return token, chat_id


# ============================================================================
# INITIALIZATION
# ============================================================================


def resolve_namespace(namespace_name):
    """
    Resolve namespace name to actual namespace string.

    Args:
        namespace_name: preset name (e.g. "cve", "ctf") or full namespace string

    Returns:
        Actual namespace string (empty string = root)
    """
    if namespace_name is None:
        return NAMESPACE
    if namespace_name in NAMESPACE_PRESETS:
        return NAMESPACE_PRESETS[namespace_name]
    return str(namespace_name)


def init_environment():
    """Initialize environment and check dependencies"""
    # Create .env directory if it doesn't exist
    ENV_DIR.mkdir(parents=True, exist_ok=True)

    # Create chunk directories if they don't exist
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    return {
        "RAG_ROOT": str(RAG_ROOT),
        "ENV_DIR": str(ENV_DIR),
        "INDEX_NAME": INDEX_NAME,
        "NAMESPACE": NAMESPACE,
        "NAMESPACE_PRESETS": list(NAMESPACE_PRESETS.keys()),
        "EMBEDDING_MODEL": EMBEDDING_MODEL,
        "EMBEDDING_DIM": EMBEDDING_DIM,
    }


if __name__ == "__main__":
    # Print configuration when run directly
    config = init_environment()
    print("\n📋 RAG Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print(f"\n✅ Configuration initialized at {RAG_ROOT}")
