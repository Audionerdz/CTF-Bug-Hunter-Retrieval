# STT Command - Send To Telegram

The `stt` command is a quick wrapper for sending messages, files, and RAG query results to Telegram.

## Location
```
/home/kali/Desktop/RAG/src/stt
```

## Shell Integration
The `stt` function is defined in `~/.zshrc` and automatically calls the script:

```bash
stt <command> [arguments...]
```

## Available Commands

### RAG Query
Send RAG search results to Telegram:

```bash
stt rag "SQL injection" [top_k] [machine]
stt rag "LFI exploitation"          # Default: top_k=5
stt rag "RCE techniques" 10         # Custom top_k
stt rag "privesc" 5 facts           # Filter by machine (facts/gavel)
```

### Send Message
Send a text message to Telegram:

```bash
stt message "Your message"
stt message "Task completed!"
stt message "Found a vulnerability"
```

### Send File
Send a file with optional caption:

```bash
stt file /path/to/file.py
stt file /path/to/exploit.py "Found RCE"
stt file /home/user/notes.txt "CTF Notes"
```

### Send Directory
Send an entire directory as a ZIP file:

```bash
stt directory /path/to/folder
stt directory /home/user/loot "CTF Loot"
stt directory /home/ctf/notes "Research"
```

### Shortcut: Direct File Send
Send a file by directly specifying its path:

```bash
stt /path/to/file.md
stt /path/to/exploit.py "Vulnerability Found"
```

## Examples

### During CTF
```bash
# Find exploit technique
stt rag "SQL injection in $_GET parameter" 10

# Send findings to Telegram
stt message "Found SQL injection on target.com"

# Send exploit code
stt file /tmp/exploit.py "Working exploit"

# Send entire notes directory
stt directory /home/ctf/notes "All CTF research"
```

### Common Workflows
```bash
# Quick search and send
stt rag "Linux privilege escalation" 5 facts

# Send file with context
stt file /home/user/writeup.md "HTB Writeup"

# Share research
stt directory /research/active "Active research"

# Quick notification
stt message "Script finished successfully"
```

## Technical Details

- **Script Location**: `/home/kali/Desktop/RAG/src/stt`
- **Shell Function**: Defined in `~/.zshrc`
- **Backend**: Uses RAG system scripts (rag_to_telegram.py, telegram_sender.py)
- **Requirements**: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in `.env/telegram.env`

## Related Commands

```bash
# Start Telegram bot daemon
alias telegram-bot-start='cd /home/kali/Desktop/RAG && nohup python3 src/telegram_bot.py > telegram_bot.log 2>&1 &'

# Stop bot
alias telegram-bot-stop='pkill -f "telegram_bot.py"'

# View bot logs
alias telegram-bot-logs='tail -f /home/kali/Desktop/RAG/telegram_bot.log'
```

## Troubleshooting

### "Command not found: stt"
```bash
# Reload shell
source ~/.zshrc

# Or manually source it
source /root/.zshrc
```

### Script not working
```bash
# Check script exists
ls -la /home/kali/Desktop/RAG/src/stt

# Test it
/home/kali/Desktop/RAG/src/stt help
```

### Telegram errors
```bash
# Verify credentials
cat /home/kali/Desktop/RAG/.env/telegram.env

# Test connection
stt message "Test message"
```

## Integration with RAG System

The `stt` command seamlessly integrates with your RAG system:

1. **RAG Queries** → Pinecone search + OpenAI embeddings → Telegram
2. **File Sharing** → Upload files/directories → Telegram
3. **Message Routing** → Custom messages → Telegram

All within the `/home/kali/Desktop/RAG/` ecosystem.

---

**Updated**: February 24, 2026  
**Status**: ✅ Integrated with RAG refactored system
