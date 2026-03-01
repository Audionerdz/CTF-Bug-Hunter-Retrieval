#!/usr/bin/env python3
"""
Simple Telegram message sender - sends text/files directly without RAG search.
For programmatic use: from atlas_engine.telegram import Telegram; tg = Telegram(); tg.send("text")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.telegram import Telegram


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 telegram_sender.py <message|file_path|dir_path> [caption]"
        )
        sys.exit(1)

    content = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else None

    tg = Telegram()
    resp = tg.send(content, caption=caption)

    if isinstance(resp, dict) and resp.get("ok"):
        print("✓ Sent to Telegram")
    elif isinstance(resp, list) and resp and resp[0].get("ok"):
        print(f"✓ Sent {len(resp)} messages to Telegram")
    else:
        print("✗ Failed to send")
        print(resp)
        sys.exit(1)


if __name__ == "__main__":
    main()
