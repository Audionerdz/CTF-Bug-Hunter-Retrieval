#!/usr/bin/env python3
"""
Telegram Sender - Utility for sending messages, files, and directories to Telegram.

Usage:
  python3 telegram_sender.py "message text"
  python3 telegram_sender.py --file /path/to/file "caption"
  python3 telegram_sender.py --file /path/to/file

Requires:
  - RAG/.env/telegram.env with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
"""

import os
import sys
import json
import shutil
import logging
import tempfile
import requests
from pathlib import Path

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).parent))
import config

logger = logging.getLogger(__name__)


def load_api_keys():
    """Load API keys from centralized config"""
    try:
        telegram_token, telegram_chat_id = config.get_telegram_keys()
        return {"telegram_token": telegram_token, "telegram_chat_id": telegram_chat_id}
    except ValueError as e:
        logger.error(f"Telegram keys error: {e}")
        return {}


class TelegramSender:
    """Send messages, files, and directories to Telegram"""

    def __init__(self, bot_token=None, chat_id=None):
        if bot_token and chat_id:
            self.bot_token = bot_token
            self.chat_id = chat_id
        else:
            keys = load_api_keys()
            self.bot_token = keys.get("telegram_token")
            self.chat_id = keys.get("telegram_chat_id")

        if not self.bot_token or not self.chat_id:
            raise ValueError("Missing Pinecone or OpenAI API keys")

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text, parse_mode=None):
        """Send a text message to Telegram"""
        url = f"{self.base_url}/sendMessage"
        # Telegram has a 4096 char limit per message
        chunks = [text[i : i + 4000] for i in range(0, len(text), 4000)]

        responses = []
        for chunk in chunks:
            payload = {
                "chat_id": self.chat_id,
                "text": chunk,
            }
            if parse_mode:
                payload["parse_mode"] = parse_mode

            try:
                response = requests.post(url, json=payload)
                result = response.json()
                if not result.get("ok"):
                    # Retry without parse_mode if markdown fails
                    if parse_mode:
                        payload.pop("parse_mode", None)
                        response = requests.post(url, json=payload)
                        result = response.json()
                responses.append(result)
                logger.info(f"Response: {result.get('ok')}")
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                responses.append({"ok": False, "error": str(e)})

        return responses

    def send_document(self, file_path, caption=None):
        """Send a file as a document to Telegram"""
        url = f"{self.base_url}/sendDocument"

        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:
            logger.error(f"File too large: {file_size} bytes. Telegram limit is 50 MB.")
            return {"ok": False, "error": "File too large (>50MB)"}

        try:
            with open(file_path, "rb") as f:
                files = {"document": (os.path.basename(file_path), f)}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption[:1024]  # Telegram caption limit

                response = requests.post(url, data=data, files=files)
                result = response.json()
                if result.get("ok"):
                    logger.info(f"Document sent: {os.path.basename(file_path)}")
                else:
                    logger.error(f"Failed to send document: {result}")
                return result
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            return {"ok": False, "error": str(e)}

    def send_directory(self, dir_path, caption="Directory archive"):
        """Compress a directory to ZIP and send it via Telegram"""
        if not os.path.isdir(dir_path):
            logger.error(f"Not a directory: {dir_path}")
            return {"ok": False, "error": "Not a directory"}

        dir_name = os.path.basename(os.path.normpath(dir_path))

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, dir_name)
                archive = shutil.make_archive(zip_path, "zip", dir_path)

                archive_size = os.path.getsize(archive)
                if archive_size > 50 * 1024 * 1024:
                    logger.error(
                        f"ZIP too large: {archive_size / 1024 / 1024:.1f} MB. "
                        "Telegram limit is 50 MB."
                    )
                    return {"ok": False, "error": "ZIP too large (>50MB)"}

                return self.send_document(archive, caption=caption)
        except Exception as e:
            logger.error(f"Error sending directory: {e}")
            return {"ok": False, "error": str(e)}


def main():
    """CLI interface for telegram_sender"""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if len(sys.argv) < 2:
        print("Usage:")
        print('  python3 telegram_sender.py "message text"')
        print('  python3 telegram_sender.py --file /path/to/file "caption"')
        sys.exit(1)

    sender = TelegramSender()

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Usage: python3 telegram_sender.py --file /path/to/file [caption]")
            sys.exit(1)
        file_path = sys.argv[2]
        caption = sys.argv[3] if len(sys.argv) > 3 else None
        result = sender.send_document(file_path, caption=caption)
    else:
        message = sys.argv[1]
        result = sender.send_message(message, parse_mode=None)

    if isinstance(result, list):
        success = all(r.get("ok") for r in result)
    else:
        success = result.get("ok", False)

    if success:
        print("Sent successfully")
    else:
        print(f"Failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
