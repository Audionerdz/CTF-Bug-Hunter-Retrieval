#!/bin/bash

# RAG System Aliases Setup Script
# This script automatically adds RAG aliases to your shell configuration

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          RAG System - Alias Setup Script                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Define aliases
ALIASES='
# RAG System Aliases (Updated: GeminiRag instead of rag-chat)
alias vectorize='"'"'python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py'"'"'
alias query='"'"'python3 /home/kali/Desktop/RAG/src/query_fast.py'"'"'
alias rag-query='"'"'python3 /home/kali/Desktop/RAG/src/query_agent.py'"'"'
alias GeminiRag='"'"'python3 /home/kali/Desktop/RAG/src/gemini_rag.py'"'"'
alias pa='"'"'/usr/local/bin/pa'"'"'
alias rag-send='"'"'python3 /home/kali/Desktop/RAG/telegram_sender.py'"'"'
alias rag-bot='"'"'python3 /home/kali/Desktop/RAG/src/telegram_bot.py'"'"'
alias rag-sync='"'"'python3 /home/kali/Desktop/RAG/src/sync_registry.py'"'"'
'

# Detect shell
if [ -f ~/.zshrc ]; then
    echo "📝 Detected: Zsh (~/.zshrc)"
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f ~/.bashrc ]; then
    echo "📝 Detected: Bash (~/.bashrc)"
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "❌ Error: Could not find shell configuration file"
    echo "   Create ~/.zshrc or ~/.bashrc and try again"
    exit 1
fi

echo

# Check if aliases already exist
if grep -q "GeminiRag=" "$SHELL_CONFIG"; then
    echo "⚠️  Aliases already installed in $SHELL_CONFIG"
    echo
    read -p "Do you want to update them? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipped."
        exit 0
    fi
    
    # Remove old aliases first
    echo "🗑️  Removing old aliases..."
    sed -i.bak '/# RAG System Aliases/,/alias rag-sync=/d' "$SHELL_CONFIG"
    echo "✅ Old aliases removed"
fi

# Add aliases
echo "📝 Adding aliases to $SHELL_CONFIG..."
echo "$ALIASES" >> "$SHELL_CONFIG"
echo "✅ Aliases added"

# Reload shell config
echo
echo "🔄 Reloading shell configuration..."
source "$SHELL_CONFIG" 2>/dev/null
echo "✅ Shell configuration reloaded"

# Verify
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Aliases Installed:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
alias | grep -E 'vectorize|query|GeminiRag|pa=|rag-send|rag-bot|rag-sync' || echo "⚠️  Run: source $SHELL_CONFIG"
echo
echo "🎯 Usage:"
echo "   vectorize /path              - Vectorize chunks"
echo "   query \"your query\"          - Quick query"
echo "   rag-query \"query\"           - Query with Telegram"
echo "   GeminiRag                    - Interactive chat with Gemini"
echo "   pa \"query\"                  - Pinecone Assistant CLI"
echo "   rag-send \"message\"          - Send to Telegram"
echo "   rag-bot                      - Start Telegram bot"
echo "   rag-sync                     - Sync chunk registry"
echo
echo "✅ Setup complete!"
echo

