#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Atlas Engine - Alias Verification Test             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

REPO_DIR="/home/kali/Desktop/RAG"

# Test data
declare -A ALIASES=(
    ["atlas-query"]="src/query_fast.py"
    ["atlas-ask"]="src/query_agent.py"
    ["atlas-chat"]="src/gemini_rag.py"
    ["atlas-vectorize"]="src/vectorize_canonical_openai.py"
    ["atlas-stt"]="src/rag_to_telegram.py"
    ["atlas-send"]="src/rag_to_telegram.py"
    ["atlas-bot"]="src/telegram_bot.py"
    ["atlas-sync"]="src/sync_registry.py"
)

PASS=0
FAIL=0

for alias in "${!ALIASES[@]}"; do
    script="${ALIASES[$alias]}"
    full_path="$REPO_DIR/$script"
    
    echo "Testing: $alias"
    echo "  Script: $script"
    
    # Check if file exists
    if [ ! -f "$full_path" ]; then
        echo "  ❌ FAIL - Script not found: $full_path"
        ((FAIL++))
        echo ""
        continue
    fi
    echo "  ✅ Script exists"
    
    # Check if it's readable
    if [ ! -r "$full_path" ]; then
        echo "  ❌ FAIL - Script not readable"
        ((FAIL++))
        echo ""
        continue
    fi
    echo "  ✅ Script readable"
    
    # Check Python syntax
    if ! python3 -m py_compile "$full_path" 2>/dev/null; then
        echo "  ❌ FAIL - Python syntax error"
        ((FAIL++))
        echo ""
        continue
    fi
    echo "  ✅ Python syntax OK"
    
    # Check if imports work (try to import the modules)
    if ! python3 -c "import sys; sys.path.insert(0, '$REPO_DIR'); from atlas_engine import Atlas; print('Import OK')" 2>/dev/null; then
        echo "  ⚠️  Warning - Some dependencies may be missing (expected on first run)"
    else
        echo "  ✅ Atlas Engine imports successfully"
    fi
    
    echo "  ✅ PASS"
    ((PASS++))
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST RESULTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PASSED: $PASS / ${#ALIASES[@]}"
echo "❌ FAILED: $FAIL / ${#ALIASES[@]}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED!"
    echo ""
    echo "To use the aliases, run:"
    echo "  bash setup_aliases.sh"
    echo ""
    echo "Then in a new terminal:"
    echo "  atlas-query 'your search'"
    echo "  atlas-vectorize /path/to/chunks"
    echo "  atlas-chat"
    echo "  atlas-ask 'your question'"
else
    echo "⚠️  Some tests failed. Check the output above."
    exit 1
fi
