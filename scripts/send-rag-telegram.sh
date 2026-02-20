#!/bin/bash
# 📱 Telegram Sender for RAG Queries
# Sends RAG query results to Telegram using the proper venv

set -e

RAG_PATH="/home/kali/Desktop/RAG"
VENV_PYTHON="/root/.openskills/venv/bin/python3"

# Function to send RAG query
send_rag_query() {
    local query="$1"
    local top_k="${2:-5}"
    local machine="${3:-}"
    
    if [ ! -f "$VENV_PYTHON" ]; then
        echo "Virtual environment not found at $VENV_PYTHON"
        exit 1
    fi
    
    # Run the RAG script with openskills venv
    (
        cd "$RAG_PATH"
        "$VENV_PYTHON" "rag_to_telegram.py" "$query" "$top_k" "$machine"
    )
}

# Main
if [ $# -lt 1 ]; then
    echo "Usage: send-rag-telegram 'query' [top_k] [machine]"
    echo "Examples:"
    echo "  send-rag-telegram 'LFI exploitation'"
    echo "  send-rag-telegram 'RCE techniques' 10"
    echo "  send-rag-telegram 'privesc' 5 facts"
    exit 1
fi

send_rag_query "$@"
