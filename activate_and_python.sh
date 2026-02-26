#!/bin/bash
# Activate venv and start Python REPL

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
exec python3 "$@"
