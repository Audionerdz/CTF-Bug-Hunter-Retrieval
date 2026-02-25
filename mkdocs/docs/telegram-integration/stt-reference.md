# Telegram Integration

The RAG framework includes full Telegram integration. You can send messages, files, directories, and query results directly from your terminal or from Python.

## Two Ways to Use It

### From the Terminal (stt command)

The `stt` (Send To Telegram) bash command handles everything:

```bash
stt rag "LFI exploitation"
stt message "Task completed"
stt file /path/to/report.md
stt directory /path/to/loot
```

### From Python (framework)

```python
from atlas_engine import Atlas
atlas = Atlas()

atlas.send("Hello from the framework")
atlas.send("/path/to/file.md")
atlas.send(results)  # send query results
```

## STT Command Reference

### Search RAG and Send Results

```bash
stt rag "query" [top_k] [machine]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `"query"` | Yes | -- | Search text |
| `top_k` | No | 5 | Number of results |
| `machine` | No | All | Filter by machine name |

**Examples:**

```bash
# Basic search (5 results, all machines)
stt rag "LFI exploitation"

# 10 results
stt rag "RCE techniques" 10

# Filter by machine
stt rag "privesc" 5 facts

# Specific machine, more results
stt rag "yaml injection" 15 gavel
```

### Search RAG and Send as ZIP

```bash
stt rag-zip "query" [top_k] [machine]
```

Same arguments as `stt rag`, but results are packaged into a ZIP file before sending.

```bash
stt rag-zip "LFI exploitation"
stt rag-zip "RCE techniques" 10
stt rag-zip "privesc" 5 facts
```

### Send a Text Message

```bash
stt message "your text here"
```

The script handles chunking automatically if the message is too long for Telegram's limit.

```bash
stt message "Scan complete. Found 3 open ports."
stt message "Task completed successfully"
```

### Send a File

```bash
stt file /path/to/file [caption]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `/path/to/file` | Yes | File to send |
| `caption` | No | Caption text |

```bash
# Send file without caption
stt file /root/notes.txt

# Send file with caption
stt file /root/exploit.py "Exploit script"

# Shortcut: just pass the file path directly
stt /root/report.md
```

### Send a Directory (as ZIP)

```bash
stt directory /path/to/dir [caption]
```

The directory is automatically compressed into a ZIP file before sending.

```bash
stt directory /root/loot "Extracted files"
stt directory /home/kali/results "Scan results"
```

### Help

```bash
stt help
stt --help
stt -h
```

## Python Framework Methods

### atlas.send() -- Auto-Detect

The `send()` method automatically detects what you're sending:

```python
# Send a text message
atlas.send("Hello from RAG")

# Send a file
atlas.send("/path/to/report.md")

# Send query results (formatted as markdown)
results = atlas.query("LFI", show=False)
atlas.send(results)
```

### rag-send Alias

From the terminal:

```bash
rag-send "Quick message to Telegram"
```

### rag-query Alias (Search + Send)

Searches the RAG index and automatically sends results to Telegram:

```bash
# Search and send
rag-query "LFI exploitation"

# With options
rag-query "RCE" --top-k 10 --machine gavel

# Search but don't send to Telegram
rag-query "privesc" --no-telegram
```

## All Telegram-Related Aliases

| Alias | What It Does |
|-------|--------------|
| `stt rag "query"` | Search RAG, send results |
| `stt rag-zip "query"` | Search RAG, send as ZIP |
| `stt message "text"` | Send text message |
| `stt file /path` | Send a file |
| `stt directory /path` | ZIP and send a directory |
| `stt /path/to/file` | Shortcut: send file directly |
| `rag-send "text"` | Send message (alias) |
| `rag-query "text"` | Search + save + send (alias) |
| `rag-bot` | Start Telegram bot daemon |

## Setup Requirements

Make sure your Telegram env file exists:

```bash
cat /home/kali/Desktop/RAG/.env/telegram.env
# Should contain:
# TELEGRAM_BOT_TOKEN=your_bot_token
# TELEGRAM_CHAT_ID=your_chat_id
```

Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot).
