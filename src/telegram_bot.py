#!/usr/bin/env python3
"""
RAG Telegram Bot - Query via Telegram, receive chunks back
Listens for messages and responds with RAG search results

Commands:
  /q <query> [top_k]     - Search RAG (default 5 results)
  /qf <query> [top_k]    - Search only FACTS
  /qg <query> [top_k]    - Search only GAVEL
  /status                - Show index stats
  /help                  - Show help

Examples:
  /q LFI exploitation           -> 5 results
  /q RCE techniques 10          -> 10 results
  /qf privesc 15                -> 15 results from FACTS
  /qg yaml injection 8          -> 8 results from GAVEL

Direct messages are also treated as queries (with optional top_k at end).

Usage:
  python3 /home/kali/Desktop/RAG/telegram_bot.py
"""

import os
import sys
import json
import shutil
import logging
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from pinecone import Pinecone
from openai import OpenAI

# Import centralized configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# ============================================================================
# CONSTANTS
# ============================================================================

INDEX_NAME = config.INDEX_NAME
EMBEDDING_MODEL = config.EMBEDDING_MODEL
EMBEDDING_DIM = config.EMBEDDING_DIM
DEFAULT_TOP_K = 5
MAX_TOP_K = 50
CHUNK_REGISTRY_PATH = str(config.CHUNK_REGISTRY)

MARKDOWN_SPECIAL_CHARS = [
    "_",
    "*",
    "[",
    "]",
    "(",
    ")",
    "~",
    "`",
    ">",
    "#",
    "+",
    "-",
    "=",
    "|",
    "{",
    "}",
    ".",
    "!",
]

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================================
# API KEYS
# ============================================================================


def load_api_keys():
    """Load API keys from centralized configuration"""
    keys = {}

    try:
        keys["telegram_token"], keys["telegram_chat_id"] = config.get_telegram_keys()
    except ValueError as e:
        logger.error(f"Telegram keys error: {e}")

    try:
        keys["pinecone_key"] = config.get_pinecone_key()
    except ValueError as e:
        logger.error(f"Pinecone key error: {e}")

    try:
        keys["openai_key"] = config.get_openai_key()
    except ValueError as e:
        logger.error(f"OpenAI key error: {e}")

    return keys


# ============================================================================
# ESCAPE MARKDOWN
# ============================================================================


def escape_markdown(text):
    """Escape Telegram MarkdownV2 special characters"""
    for char in MARKDOWN_SPECIAL_CHARS:
        text = text.replace(char, f"\\{char}")
    return text


# ============================================================================
# RAG QUERY ENGINE
# ============================================================================


class RAGQueryEngine:
    """Handles Pinecone queries and chunk retrieval"""

    def __init__(self, pinecone_key, openai_key):
        self.pc = Pinecone(api_key=pinecone_key)
        self.index = self.pc.Index(INDEX_NAME)
        self.openai_client = OpenAI(api_key=openai_key)

        # Load chunk registry
        self.chunk_map = {}
        if os.path.exists(CHUNK_REGISTRY_PATH):
            try:
                with open(CHUNK_REGISTRY_PATH, "r") as f:
                    self.chunk_map = json.load(f)
            except Exception as e:
                logger.error(f"Error loading chunk registry: {e}")

        logger.info(f"RAG Engine initialized: {len(self.chunk_map)} chunks in registry")

    def get_embedding(self, text):
        """Generate 3072D embedding"""
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
            dimensions=EMBEDDING_DIM,
        )
        return response.data[0].embedding

    def extract_body(self, content):
        """Extract body without YAML frontmatter"""
        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            except Exception:
                pass
        return content

    def get_chunk_content(self, chunk_id):
        """Read chunk content from local filesystem"""
        if chunk_id not in self.chunk_map:
            return None

        file_path = self.chunk_map[chunk_id]
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.extract_body(content)
        except Exception as e:
            logger.error(f"Error reading chunk {chunk_id}: {e}")
            return None

    def query(self, query_text, top_k=DEFAULT_TOP_K, machine_filter=None):
        """Search Pinecone and return formatted results"""
        embedding = self.get_embedding(query_text)

        query_params = {
            "vector": embedding,
            "top_k": top_k,
            "include_metadata": True,
        }

        if machine_filter:
            query_params["filter"] = {"machine": {"$eq": machine_filter.lower()}}

        results = self.index.query(**query_params)

        formatted_results = []
        for match in results.get("matches", []):
            metadata = match.get("metadata", {})
            chunk_id = metadata.get("chunk_id", match.get("id", "unknown"))
            score = match.get("score", 0)

            # Try to get content from local filesystem first
            local_content = self.get_chunk_content(chunk_id)

            # Fallback to metadata content
            content = local_content or metadata.get("content", "No content available")

            formatted_results.append(
                {
                    "chunk_id": chunk_id,
                    "score": score,
                    "machine": metadata.get("machine", "unknown"),
                    "domain": metadata.get("domain", "unknown"),
                    "phase": metadata.get("phase", "unknown"),
                    "technique": metadata.get("technique", "unknown"),
                    "confidence": metadata.get("confidence", "unknown"),
                    "content": content,
                    "file_path": metadata.get(
                        "file_path", self.chunk_map.get(chunk_id, "")
                    ),
                }
            )

        return formatted_results

    def get_stats(self):
        """Get index statistics"""
        stats = self.index.describe_index_stats()
        return {
            "total_vectors": stats.get("total_vector_count", 0),
            "namespaces": stats.get("namespaces", {}),
            "dimensions": stats.get("dimension", EMBEDDING_DIM),
        }

    def create_chunks_zip(self, results, query_text):
        """Create a ZIP file with chunk contents"""
        tmpdir = tempfile.mkdtemp()
        try:
            safe_query = "".join(
                c for c in query_text if c.isalnum() or c in ("-", "_", " ")
            ).strip()[:30]

            for i, result in enumerate(results, 1):
                chunk_id = result["chunk_id"].replace("::", "_")
                filename = f"{i:02d}_{chunk_id}.md"
                filepath = os.path.join(tmpdir, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {result['chunk_id']}\n\n")
                    f.write(f"**Score:** {result['score']:.4f}\n")
                    f.write(f"**Machine:** {result['machine']}\n")
                    f.write(f"**Phase:** {result['phase']}\n")
                    f.write(f"**Technique:** {result['technique']}\n\n")
                    f.write("---\n\n")
                    f.write(result["content"])

            zip_path = os.path.join(tempfile.gettempdir(), f"rag_results_{safe_query}")
            archive = shutil.make_archive(zip_path, "zip", tmpdir)
            return archive
        except Exception as e:
            logger.error(f"Error creating ZIP: {e}")
            return None
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


# ============================================================================
# TELEGRAM SENDER (inline for bot use)
# ============================================================================


class TelegramSender:
    """Lightweight inline sender for the bot"""

    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text, parse_mode=None):
        import requests

        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return {"ok": False}

    def send_document(self, file_path, caption=None):
        import requests

        url = f"{self.base_url}/sendDocument"
        try:
            with open(file_path, "rb") as f:
                files = {"document": (os.path.basename(file_path), f)}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption[:1024]
                response = requests.post(url, data=data, files=files)
                return response.json()
        except Exception as e:
            logger.error(f"Send document error: {e}")
            return {"ok": False}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

rag_engine = None
telegram_sender = None


def parse_query_and_topk(text, default_top_k=DEFAULT_TOP_K):
    """Parse query text and optional top_k from end of string"""
    if not text or not text.strip():
        return "", default_top_k

    args = text.strip().split()

    # Check if last word is a number (top_k)
    top_k = default_top_k
    query_text = text.strip()

    if len(args) > 1:
        try:
            potential_k = int(args[-1])
            if 1 <= potential_k <= MAX_TOP_K:
                top_k = potential_k
                query_text = " ".join(args[:-1])
        except ValueError:
            pass

    top_k = min(top_k, MAX_TOP_K)
    return query_text, top_k


def filter_text(text):
    """Extract machine filter from text like [FACTS] or [GAVEL]"""
    machine_filter = None
    if text.startswith("[") and "]" in text:
        bracket_end = text.index("]")
        machine_filter = text[1:bracket_end].upper()
        text = text[bracket_end + 1 :].strip()
    return text, machine_filter


def searching_msg(query_text, top_k, machine_filter=None):
    """Build the 'searching...' status message"""
    msg = f"\U0001f50d {query_text} (top_k={top_k})\n\u23f3 Searching..."
    if machine_filter:
        msg = f"\U0001f50d [{machine_filter}] {query_text} (top_k={top_k})\n\u23f3 Searching..."
    return msg


# ============================================================================
# COMMAND HANDLERS
# ============================================================================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if not rag_engine:
        await update.message.reply_text("RAG engine not initialized")
        return

    stats = rag_engine.get_stats()
    await update.message.reply_text(
        f"\U0001f916 *RAG Telegram Bot*\n\n"
        f"\u2022 Index: `{INDEX_NAME}`\n"
        f"\u2022 Vectors: {stats['total_vectors']}\n"
        f"\u2022 Chunks in Registry: {len(rag_engine.chunk_map)}\n"
        f"\u2022 Model: `{EMBEDDING_MODEL}`\n\n"
        f"Send /help for commands.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "*Commands:*\n"
        "`/q <query> [top_k]` - Search RAG (default 5)\n"
        "`/qf <query> [top_k]` - Search only FACTS\n"
        "`/qg <query> [top_k]` - Search only GAVEL\n"
        "`/status` - Show index stats\n"
        "`/help` - Show this help\n\n"
        "*ZIP Feature:*\n"
        "Add `zip` before your query to get results as a ZIP file.\n"
        "Example: `/q zip LFI exploitation`\n\n"
        "*Examples:*\n"
        "`/q LFI exploitation` - 5 results\n"
        "`/q RCE techniques 10` - 10 results\n"
        "`/qf privesc 15` - 15 from FACTS\n"
        "`/qg yaml injection 8` - 8 from GAVEL\n\n"
        "Direct messages are also treated as queries.",
        parse_mode="Markdown",
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    if not rag_engine:
        await update.message.reply_text("RAG engine not initialized")
        return

    stats = rag_engine.get_stats()
    await update.message.reply_text(
        f"\U0001f4ca *RAG Index Status*\n\n"
        f"\u2022 Index: `{INDEX_NAME}`\n"
        f"\u2022 Total Vectors: {stats['total_vectors']}\n"
        f"\u2022 Chunks in Registry: {len(rag_engine.chunk_map)}\n"
        f"\u2022 Embedding Model: `{EMBEDDING_MODEL}`\n"
        f"\u2022 Dimensions: {EMBEDDING_DIM}\n"
        f"\u2022 Default top\\_k: {DEFAULT_TOP_K}\n"
        f"\u2022 Max top\\_k: {MAX_TOP_K}",
        parse_mode="Markdown",
    )


async def execute_query(update: Update, query_text, top_k, machine_filter=None):
    """Execute a RAG query and send results"""
    if not rag_engine:
        await update.message.reply_text("RAG engine not initialized")
        return

    # Send searching message
    msg = await update.message.reply_text(
        searching_msg(query_text, top_k, machine_filter)
    )

    try:
        results = rag_engine.query(
            query_text, top_k=top_k, machine_filter=machine_filter
        )

        if not results:
            await msg.edit_text(
                f"\U0001f50d {query_text} (top_k={top_k})\n\u274c No results found."
            )
            return

        # Edit searching message with summary
        summary = f"\U0001f50d {query_text} (top_k={top_k})\n"
        if machine_filter:
            summary = f"\U0001f50d [{machine_filter}] {query_text} (top_k={top_k})\n"
        summary += f"\u2705 Results: {len(results)}\n"

        await msg.edit_text(summary)

        # Send each result as separate message(s)
        # Telegram limit is 4096 chars per message
        MAX_MSG = 4000  # leave margin for formatting
        for i, result in enumerate(results, 1):
            header = (
                f"*{i}. {result['chunk_id']}*\n"
                f"Score: {result['score']:.4f} | "
                f"{result['machine'].upper()} | "
                f"{result['phase']} | {result['technique']}\n\n"
            )

            content = result["content"]

            # If header + content fits in one message, send it all
            if len(header) + len(content) <= MAX_MSG:
                full_msg = header + content
                try:
                    await update.message.reply_text(full_msg, parse_mode="Markdown")
                except Exception:
                    await update.message.reply_text(full_msg)
            else:
                # Send header + first part
                first_part = content[: MAX_MSG - len(header)]
                try:
                    await update.message.reply_text(
                        header + first_part, parse_mode="Markdown"
                    )
                except Exception:
                    await update.message.reply_text(header + first_part)

                # Send remaining content in continuation messages
                remaining = content[MAX_MSG - len(header) :]
                part_num = 2
                while remaining:
                    chunk = remaining[:MAX_MSG]
                    remaining = remaining[MAX_MSG:]
                    cont_header = f"_...cont {result['chunk_id']} ({part_num})_\n\n"
                    try:
                        await update.message.reply_text(
                            cont_header + chunk, parse_mode="Markdown"
                        )
                    except Exception:
                        await update.message.reply_text(
                            f"...cont ({part_num})\n\n" + chunk
                        )
                    part_num += 1

    except Exception as e:
        logger.error(f"Query error: {e}")
        await msg.edit_text(f"\U0001f50d {query_text}\n\u274c Error: {str(e)[:200]}")


async def execute_query_zip(update: Update, query_text, top_k, machine_filter=None):
    """Execute a RAG query and send results as ZIP"""
    if not rag_engine:
        await update.message.reply_text("RAG engine not initialized")
        return

    msg = await update.message.reply_text(
        f"\U0001f50d {query_text} (top_k={top_k})\n\u23f3 Searching and creating ZIP..."
    )

    try:
        results = rag_engine.query(
            query_text, top_k=top_k, machine_filter=machine_filter
        )

        if not results:
            await msg.edit_text(f"\U0001f50d {query_text}\n\u274c No results found.")
            return

        zip_path = rag_engine.create_chunks_zip(results, query_text)

        if zip_path and os.path.exists(zip_path):
            await msg.edit_text(
                f"\U0001f50d {query_text} (top_k={top_k})\n"
                f"\u2705 {len(results)} results - sending ZIP..."
            )

            # Send ZIP via bot directly
            with open(zip_path, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename=os.path.basename(zip_path),
                    caption=f"RAG results: {query_text} ({len(results)} chunks)",
                )

            # Cleanup
            try:
                os.remove(zip_path)
            except Exception:
                pass

            await msg.edit_text(
                f"\U0001f50d {query_text} (top_k={top_k})\n"
                f"\U0001f4e6 ZIP sent with {len(results)} chunks"
            )
        else:
            await msg.edit_text(f"\U0001f50d {query_text}\n\u274c Error creating ZIP")

    except Exception as e:
        logger.error(f"Query ZIP error: {e}")
        await msg.edit_text(f"\U0001f50d {query_text}\n\u274c Error: {str(e)[:200]}")


async def query_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /q command - generic query"""
    if not context.args:
        await update.message.reply_text("\u26a0\ufe0f Please provide a query")
        return

    text = " ".join(context.args)

    # Check for zip mode
    if text.lower().startswith("zip "):
        text = text[4:].strip()
        query_text, top_k = parse_query_and_topk(text)
        await execute_query_zip(update, query_text, top_k)
    else:
        query_text, top_k = parse_query_and_topk(text)
        await execute_query(update, query_text, top_k)


async def query_facts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /qf command - query FACTS only"""
    if not context.args:
        await update.message.reply_text("\u26a0\ufe0f Please provide a query")
        return

    text = " ".join(context.args)
    query_text, top_k = parse_query_and_topk(text)
    await execute_query(update, query_text, top_k, machine_filter="facts")


async def query_gavel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /qg command - query GAVEL only"""
    if not context.args:
        await update.message.reply_text("\u26a0\ufe0f Please provide a query")
        return

    text = " ".join(context.args)
    query_text, top_k = parse_query_and_topk(text)
    await execute_query(update, query_text, top_k, machine_filter="gavel")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle plain text messages as queries"""
    if not rag_engine:
        await update.message.reply_text("RAG engine not initialized")
        return

    text = update.message.text
    if not text or not text.strip():
        return

    # Check for machine filter prefix like [FACTS] or [GAVEL]
    text, machine_filter = filter_text(text)

    # Check for zip prefix
    if text.lower().startswith("zip "):
        text = text[4:].strip()
        query_text, top_k = parse_query_and_topk(text)
        await execute_query_zip(update, query_text, top_k, machine_filter)
    else:
        query_text, top_k = parse_query_and_topk(text)
        await execute_query(update, query_text, top_k, machine_filter)


# ============================================================================
# MAIN
# ============================================================================


def main():
    global rag_engine, telegram_sender

    keys = load_api_keys()

    if (
        not keys.get("telegram_token")
        or not keys.get("pinecone_key")
        or not keys.get("openai_key")
    ):
        print("Missing Pinecone or OpenAI API keys")
        sys.exit(1)

    print(f"\U0001f916 RAG Telegram Bot starting...")
    print(f"\U0001f4ca Index: {INDEX_NAME}")
    print(f"\U0001f9e0 Model: {EMBEDDING_MODEL}")

    # Initialize RAG engine
    rag_engine = RAGQueryEngine(keys["pinecone_key"], keys["openai_key"])

    # Initialize inline telegram sender (for non-bot sends)
    telegram_sender = TelegramSender(keys["telegram_token"], keys["telegram_chat_id"])

    print(f"\U0001f4da Chunks: {len(rag_engine.chunk_map)}")
    print(f"\U0001f522 Default top_k: {DEFAULT_TOP_K}, Max: {MAX_TOP_K}")
    print()
    print("Bot is running! Send /start to your bot on Telegram.")
    print("Press Ctrl+C to stop.")

    # Build and run the bot
    app = ApplicationBuilder().token(keys["telegram_token"]).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("q", query_command))
    app.add_handler(CommandHandler("qf", query_facts_command))
    app.add_handler(CommandHandler("qg", query_gavel_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run
    app.run_polling()


if __name__ == "__main__":
    main()
