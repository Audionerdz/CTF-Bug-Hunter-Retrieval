# ⚡ Quick Start - 5 Minutes

Get CTF Bug Hunter Retrieval running in **5 minutes**. No lengthy configuration.

---

## Step 1: Clone (1 minute)

```bash
git clone https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git
cd CTF-Bug-Hunter-Retrieval
```

---

## Step 2: Setup (2 minutes)

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
- ✅ Create Python virtual environment
- ✅ Install dependencies
- ✅ Create `.env` template (no secrets yet)

---

## Step 3: Get API Keys (1 minute)

You need 4 free API keys. All have generous free tiers.

### Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow the prompts
4. Copy the token

### Telegram Chat ID

1. Open your bot in Telegram
2. Send any message
3. Visit: `https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates`
4. Copy your `chat.id`

### Pinecone API Key

1. Go to [pinecone.io](https://www.pinecone.io/)
2. Sign up (free tier)
3. Copy your API key

### OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/account/billing/overview)
2. Create account or sign in
3. $5 free credits available
4. Copy your API key

---

## Step 4: Configure (1 minute)

Edit `.env`:

```bash
nano .env
```

Paste your 4 keys:

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
PINECONE_API_KEY=YOUR_PINECONE_KEY
OPENAI_API_KEY=YOUR_OPENAI_KEY
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 5: Test (instant)

```bash
source venv/bin/activate
/root/.openskills/venv/bin/python3 src/telegram_sender.py "Testing CTF Bug Hunter!"
```

Check your Telegram chat - you should receive the message!

---

## 🎯 Now You're Ready

### Search Your Knowledge Base

```bash
/root/.openskills/venv/bin/python3 src/rag_to_telegram.py "SQL injection" 5
```

This will:
1. Search for "SQL injection"
2. Return top 5 results to Telegram

### Add Your Notes

See [VECTORIZATION GUIDE](./docs-vectorizer/VECTORIZE_INSTRUCTIONS.md) for adding your CTF notes.

Quick example:

```bash
# Create a note file
mkdir /home/kali/my-ctf-notes
cat > /home/kali/my-ctf-notes/sql-injection_001.md << 'EOF'
---
chunk_id: technique::web::sql::injection::001
domain: web
chunk_type: technique
tags:
  - sql
  - injection
---

# SQL Injection Techniques

Common SQLi payloads and exploitation methods...
EOF

# Vectorize it
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/my-ctf-notes
```

Your notes are now searchable!

---

## 📚 Next Steps

1. **Read full docs**: See [README.md](./README.md)
2. **Learn vectorization**: [VECTORIZE_INSTRUCTIONS.md](./docs-vectorizer/VECTORIZE_INSTRUCTIONS.md)
3. **Explore examples**: [docs-vectorizer/VECTORIZER_MODULAR_GUIDE.md](./docs-vectorizer/VECTORIZER_MODULAR_GUIDE.md)
4. **Join CTF competitions**: Use your knowledge base for instant research

---

## Troubleshooting

**"Module not found"** → `pip install -r config/requirements.txt`

**"API key not found"** → Check `.env` file exists and is correct

**"No results in Telegram"** → Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID

See [README.md#troubleshooting](./README.md#troubleshooting) for more help.

---

**That's it! You're ready for CTF competitions.**

🚀 Start winning with instant knowledge retrieval.
