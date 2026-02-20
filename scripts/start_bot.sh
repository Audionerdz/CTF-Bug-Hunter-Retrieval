#!/bin/bash
# Start the RAG Telegram Bot
# Uses /root/.openskills/venv/ (the working venv with all dependencies)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOT_SCRIPT="$SCRIPT_DIR/telegram_bot.py"
VENV_PYTHON="/root/.openskills/venv/bin/python3"
PID_FILE="/tmp/rag_telegram_bot.pid"
LOG_FILE="$SCRIPT_DIR/telegram_bot.log"

# Check venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Python venv not found at $VENV_PYTHON"
    exit 1
fi

# Check bot script exists
if [ ! -f "$BOT_SCRIPT" ]; then
    echo "ERROR: Bot script not found at $BOT_SCRIPT"
    exit 1
fi

# Kill existing instance if running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Stopping existing bot (PID $OLD_PID)..."
        kill "$OLD_PID"
        sleep 2
    fi
    rm -f "$PID_FILE"
fi

echo "Starting RAG Telegram Bot..."
echo "  Script: $BOT_SCRIPT"
echo "  Python: $VENV_PYTHON"
echo "  Log:    $LOG_FILE"

# Start bot in background
nohup "$VENV_PYTHON" "$BOT_SCRIPT" >> "$LOG_FILE" 2>&1 &
BOT_PID=$!
echo "$BOT_PID" > "$PID_FILE"

echo "  PID:    $BOT_PID"
echo ""
echo "Bot started! Check log: tail -f $LOG_FILE"
