#!/usr/bin/env python3
"""
Send Directory - Compress a directory to ZIP and send via Telegram

Usage:
  python3 send_directory.py /path/to/directory "Optional caption"
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_sender import TelegramSender


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 send_directory.py /path/to/directory [caption]")
        sys.exit(1)

    dir_path = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else "Directory archive"

    if not os.path.isdir(dir_path):
        print(f"Not a directory: {dir_path}")
        sys.exit(1)

    sender = TelegramSender()
    result = sender.send_directory(dir_path, caption=caption)

    if result.get("ok"):
        print(f"Directory sent: {os.path.basename(dir_path)}")
    else:
        print(f"Failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
