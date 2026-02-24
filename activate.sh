#!/bin/bash

# RAG Virtual Environment Activation
# Activates the local venv bundled with the RAG system

RAG_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$RAG_ROOT/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Activate venv
source "$VENV_PATH/bin/activate"

echo "✅ RAG venv activated"
echo "📍 Location: $VENV_PATH"
echo "🐍 Python: $(python3 --version)"
echo "📦 Pip: $(pip --version)"
