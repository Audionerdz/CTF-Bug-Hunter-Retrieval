#!/bin/bash

# Atlas Engine - Alias Setup Script
# This script automatically adds Atlas Engine aliases to your shell configuration

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Atlas Engine - Alias Setup Script                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if venv exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "   Creating venv and installing dependencies..."
    python3 -m venv "$SCRIPT_DIR/venv"
    "$SCRIPT_DIR/venv/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
    echo "✅ venv created and dependencies installed"
    echo ""
fi

# Use venv Python
PYTHON="$SCRIPT_DIR/venv/bin/python3"

# Define aliases using venv Python
ALIASES='
# Atlas Engine CLI Aliases (using venv Python)
alias atlas-vectorize='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/vectorize_canonical_openai.py'"'"'
alias atlas-query='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/query_fast.py'"'"'
alias atlas-ask='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/query_agent.py'"'"'
alias atlas-chat='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/gemini_rag.py'"'"'
alias atlas-stt='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/rag_to_telegram.py'"'"'
alias atlas-send='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/rag_to_telegram.py'"'"'
alias atlas-bot='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/telegram_bot.py'"'"'
alias atlas-sync='"'"''"$PYTHON"' '"$SCRIPT_DIR"'/src/sync_registry.py'"'"'
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
if grep -q "atlas-chat=" "$SHELL_CONFIG"; then
    echo "⚠️  Atlas Engine aliases already installed in $SHELL_CONFIG"
    echo
    read -p "Do you want to update them? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipped."
        exit 0
    fi
    
    # Remove old aliases first
    echo "🗑️  Removing old aliases..."
    sed -i.bak '/# Atlas Engine CLI Aliases/,/alias atlas-sync=/d' "$SHELL_CONFIG"
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
echo "✨ Atlas Engine Aliases Installed:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
alias | grep -E 'atlas-' || echo "⚠️  Run: source $SHELL_CONFIG"
echo
echo "🎯 Usage:"
echo "   atlas-vectorize /path              - Vectorize chunks with metadata"
echo "   atlas-query \"your query\"          - Semantic search"
echo "   atlas-ask \"question\"              - Ask with AI reasoning + sources"
echo "   atlas-chat                         - Interactive chat with Gemini/GPT/Ollama"
echo "   atlas-stt query \"text\"            - Search & send to Telegram"
echo "   atlas-stt file /path               - Send file to Telegram"
echo "   atlas-stt dir /path                - Zip & send directory"
echo "   atlas-send \"message\"              - Send to Telegram"
echo "   atlas-bot                          - Start Telegram bot"
echo "   atlas-sync                         - Rebuild chunk registry"
echo
echo "✅ Setup complete! Atlas Engine is ready to hunt."
echo
