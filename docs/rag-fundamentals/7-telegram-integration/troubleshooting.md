# Troubleshooting - Common Issues & Solutions

## Issue 1: "Command not found: stt"

**Problem**: `stt` alias not recognized

**Solutions**:

```bash
# Reload shell configuration
source ~/.zshrc  # or ~/.bashrc

# Verify alias exists
alias stt

# Check if script exists
which send-to-telegram
ls -la /usr/local/bin/send-to-telegram

# Check permissions
chmod +x /usr/local/bin/send-to-telegram

# Manually test
/usr/local/bin/send-to-telegram --help
```

## Issue 2: "RAG venv not found"

**Problem**: Virtual environment missing

**Solution**:

```bash
# Check venv exists
ls -la /home/kali/Desktop/RAG/.venv

# Recreate venv if missing
cd /home/kali/Desktop/RAG
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv pinecone-client openai
```

## Issue 3: "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"

**Problem**: Environment variables not set

**Solutions**:

```bash
# Check if telegram.env exists
ls -la /root/.openskills/env/telegram.env

# Load environment variables
source /root/.openskills/env/telegram.env

# Verify they're loaded
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# If file missing, create it
cat > /root/.openskills/env/telegram.env << 'EOF'
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF

# Set permissions
chmod 600 /root/.openskills/env/telegram.env
```

## Issue 4: "Error sending message" / Network timeout

**Problem**: Telegram API unreachable

**Solutions**:

```bash
# Test connectivity
ping api.telegram.org

# Check firewall
sudo ufw status

# Test with curl
curl -X POST \
  https://api.telegram.org/botYOUR_TOKEN/sendMessage \
  -d "chat_id=YOUR_CHAT_ID&text=Test"

# Check for proxy issues
curl -I https://api.telegram.org
```

## Issue 5: "File not found"

**Problem**: Specified file doesn't exist

**Solution**:

```bash
# Verify file path
ls -la /path/to/file

# Check permissions
cat /path/to/file

# Use absolute paths (not relative)
stt file /root/exploit.py "My exploit"  # Good
stt file ~/exploit.py "My exploit"      # May fail
```

## Issue 6: "File is X.X MB. Telegram limit is 50 MB"

**Problem**: File too large for Telegram

**Solutions**:

```bash
# Compress file
gzip -9 /path/to/file      # Reduces size significantly

# Split file
split -b 40M /path/to/file file_chunk_

# Create selective ZIP (exclude large files)
cd /root/loot
zip -r archive.zip . -x "*.iso" "*.vmdk"  # Exclude large files
stt file archive.zip "Loot without large files"

# Check file size first
ls -lh /path/to/file
du -sh /path/to/file
```

## Issue 7: "Missing PINECONE_API_KEY or OPENAI_API_KEY"

**Problem**: API keys for RAG not configured

**Solution**:

```bash
# Load Pinecone key
source /root/.openskills/env/pinecone.env
echo $PINECONE_API_KEY

# Load OpenAI key
source /root/.openskills/env/openai.env
echo $OPENAI_API_KEY

# Test RAG search
stt rag "test query" 3
```

## Issue 8: "No results found for query"

**Problem**: RAG search returned empty

**Solutions**:

```bash
# Try different query
stt rag "vulnerability" 10  # Broader term

# Check with verbose output
stt rag "query" -v

# Verify index exists
pa list

# Check index has data
pa describe rag-canonical-v1-emb3large

# Query all machines
stt rag "privilege escalation"  # Don't specify machine
```

## Issue 9: ZIP file too large

**Problem**: Resulting ZIP exceeds 50MB limit

**Solutions**:

```bash
# Use rag-zip instead of large directories
stt rag-zip "query" 10  # Results only, not whole directory

# Exclude large files before sending
cd /root/loot
zip -r loot.zip . -x "*.bin" "*.iso" -S

# Send multiple smaller ZIPs
tar -czf loot1.tar.gz $(ls | head -5)
tar -czf loot2.tar.gz $(ls | tail -5)
stt file loot1.tar.gz "Part 1"
stt file loot2.tar.gz "Part 2"
```

## Issue 10: Rate limiting errors

**Problem**: "Too many requests" from Telegram API

**Solution**:

```bash
# Add delays between requests
stt message "Message 1"
sleep 2
stt message "Message 2"
sleep 2
stt message "Message 3"

# In scripts
#!/bin/bash
for query in query1 query2 query3; do
    stt rag "$query" 5
    sleep 5  # Wait 5 seconds between queries
done
```

## Issue 11: "File already exists" in /tmp

**Problem**: ZIP file already exists, conflicts occur

**Solution**:

```bash
# Clean up temporary files
rm -f /tmp/*.zip
rm -f /tmp/rag_chunks_*

# Or use cron to clean /tmp periodically
# Add to crontab:
# 0 3 * * * rm -f /tmp/*.zip
```

## Issue 12: Unicode/Emoji not displaying

**Problem**: Emojis appear as boxes or special characters

**Solution**:

```bash
# Check terminal encoding
echo $LANG

# Set UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Add to ~/.bashrc or ~/.zshrc
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
source ~/.bashrc
```

## Issue 13: "broken pipe" or connection errors

**Problem**: Connection drops during large file transfer

**Solution**:

```bash
# Use timeout setting (scripts handle this)
# For large files, consider:
timeout 120 stt file /huge/file.zip "My file"

# Or split into smaller files
split -b 30M /huge/file huge_chunk_
for chunk in huge_chunk_*; do
    stt file "$chunk" "Large file chunk"
done
```

## Debugging Steps

### 1. Check Environment
```bash
# Verify all keys are loaded
echo "Token: $TELEGRAM_BOT_TOKEN"
echo "Chat: $TELEGRAM_CHAT_ID"
echo "Pinecone: $PINECONE_API_KEY"
echo "OpenAI: $OPENAI_API_KEY"
```

### 2. Test Individual Components
```bash
# Test Telegram directly
python3 << 'EOF'
import requests
token = "YOUR_TOKEN"
chat_id = "YOUR_CHAT_ID"
url = f"https://api.telegram.org/bot{token}/sendMessage"
requests.post(url, json={"chat_id": chat_id, "text": "Test"})
EOF

# Test Pinecone
pa list

# Test OpenAI
python3 -c "from openai import OpenAI; c = OpenAI(); r = c.embeddings.create(model='text-embedding-3-large', input='test'); print(len(r.data[0].embedding))"
```

### 3. Enable Verbose Output
```bash
# Run scripts directly with Python for more info
cd /home/kali/Desktop/RAG
python3 telegram_sender.py "test message"
python3 rag_to_telegram.py "test query" 3
python3 send_directory.py /tmp "test"
```

### 4. Check Logs
```bash
# Create wrapper script with logging
#!/bin/bash
STT_LOG="/tmp/stt_debug.log"
echo "[$(date)] Command: $@" >> "$STT_LOG"
/usr/local/bin/send-to-telegram "$@" 2>&1 | tee -a "$STT_LOG"

# View logs
tail -f /tmp/stt_debug.log
```

## Getting Help

If issues persist:

1. Check API key validity
2. Verify network connectivity
3. Review error messages carefully
4. Test individual components
5. Check documentation
6. Review logs and error output

---

**All Issues Covered - You're Ready!**
