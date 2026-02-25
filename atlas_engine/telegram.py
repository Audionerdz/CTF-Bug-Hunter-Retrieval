"""
Telegram - Unified Telegram sender for the RAG framework.

Send messages, files, directories, and query results to Telegram.
"""

import os
import sys
import shutil
import tempfile
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class Telegram:
    """Send messages, files, and query results to Telegram."""

    def __init__(self, bot_token=None, chat_id=None):
        if bot_token and chat_id:
            self._token = bot_token
            self._chat_id = chat_id
        else:
            self._token, self._chat_id = config.get_telegram_keys()

        self._base_url = f"https://api.telegram.org/bot{self._token}"

    # ------------------------------------------------------------------
    # Core send methods
    # ------------------------------------------------------------------

    def message(self, text, parse_mode=None):
        """
        Send a text message. Auto-chunks if > 4000 chars.

        Returns:
            list of Telegram API responses.
        """
        url = f"{self._base_url}/sendMessage"
        chunks = [text[i : i + 4000] for i in range(0, len(text), 4000)]

        responses = []
        for chunk in chunks:
            payload = {"chat_id": self._chat_id, "text": chunk}
            if parse_mode:
                payload["parse_mode"] = parse_mode

            try:
                resp = requests.post(url, json=payload).json()
                if not resp.get("ok") and parse_mode:
                    payload.pop("parse_mode", None)
                    resp = requests.post(url, json=payload).json()
                responses.append(resp)
            except Exception as e:
                responses.append({"ok": False, "error": str(e)})

        return responses

    def file(self, file_path, caption=None):
        """
        Send a file as a Telegram document.

        Returns:
            Telegram API response dict.
        """
        file_path = str(file_path)
        if not os.path.isfile(file_path):
            return {"ok": False, "error": f"File not found: {file_path}"}

        size = os.path.getsize(file_path)
        if size > 50 * 1024 * 1024:
            return {"ok": False, "error": f"File too large: {size} bytes (limit 50MB)"}

        url = f"{self._base_url}/sendDocument"
        try:
            with open(file_path, "rb") as f:
                files = {"document": (os.path.basename(file_path), f)}
                data = {"chat_id": self._chat_id}
                if caption:
                    data["caption"] = caption[:1024]
                resp = requests.post(url, data=data, files=files).json()
                return resp
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def directory(self, dir_path, caption="Directory archive"):
        """Compress directory to ZIP and send to Telegram."""
        if not os.path.isdir(dir_path):
            return {"ok": False, "error": f"Not a directory: {dir_path}"}

        dir_name = os.path.basename(os.path.normpath(dir_path))
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, dir_name)
                archive = shutil.make_archive(zip_path, "zip", dir_path)
                return self.file(archive, caption=caption)
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ------------------------------------------------------------------
    # Smart send (auto-detect type)
    # ------------------------------------------------------------------

    def send(self, content, caption=None):
        """
        Smart send - auto-detects content type.

        Args:
            content: str (message or file path), Path, list of query results, or dict.
            caption: optional caption for files.

        Returns:
            Telegram API response(s).
        """
        # Path object
        if isinstance(content, Path):
            content = str(content)

        # String: check if it's a file/directory path
        if isinstance(content, str):
            if os.path.isfile(content):
                return self.file(content, caption=caption)
            elif os.path.isdir(content):
                return self.directory(content, caption=caption)
            else:
                return self.message(content)

        # List of query results
        if isinstance(content, list) and content and isinstance(content[0], dict):
            return self._send_results(content)

        # Fallback: convert to string
        return self.message(str(content))

    def _send_results(self, results):
        """Send query results as formatted Telegram messages."""
        header = f"RAG Query Results: {len(results)} matches\n"
        self.message(header)

        responses = []
        for r in results:
            chunk_id = r.get("chunk_id", "unknown")
            score = r.get("score", 0)
            machine = r.get("machine", "?")
            phase = r.get("phase", "?")
            technique = r.get("technique", "?")
            content = r.get("content", "")[:600]

            msg = (
                f"{r.get('rank', '?')}. {chunk_id}\n"
                f"Score: {score:.4f} | {machine.upper()} | {phase} | {technique}\n\n"
                f"{content}"
            )
            responses.append(self.message(msg))

        return responses

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        masked = self._token[:8] + "..." if self._token else "None"
        return f"Telegram(token={masked}, chat_id={self._chat_id})"
