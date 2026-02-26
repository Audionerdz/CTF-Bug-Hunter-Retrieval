# Groq, Context Memory & Semantic Cache

This guide covers the new features added to Atlas Engine: Groq backend, conversation memory across all backends, and Pinecone-based semantic cache.

## Quick Start

```bash
cd /home/kali/Desktop/RAG
source venv/bin/activate && python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.chat(backend="groq")
```

That's it. Memory and cache are automatic.

## What Changed

| Feature | Before | Now |
|---|---|---|
| Backends | gemini, gpt, ollama | gemini, gpt, **groq**, ollama |
| Memory | None | Last 3 exchanges (all backends) |
| Cache | None | Semantic cache via Pinecone (all backends) |
| Logging | None | ChatML JSONL for fine-tuning |

## Available Backends

```python
atlas.chat()                    # Gemini (default)
atlas.chat(backend="gpt")      # OpenAI GPT-4o-mini
atlas.chat(backend="groq")     # Groq
atlas.chat(backend="ollama")   # Ollama local
```

## Groq Setup

### 1. Add your API key

Add `GROQ_API_KEY=your_key` to any `.env` file inside `RAG/.env/`. Example:

```bash
echo "GROQ_API_KEY=gsk_your_key_here" >> /home/kali/Desktop/RAG/.env/openai.env
```

### 2. Install dependency

```bash
source venv/bin/activate && pip install langchain-groq
```

### 3. Use it

```python
atlas.ask("What is LFI?", backend="groq")
atlas.chat(backend="groq")
```

### Change the Groq model

Edit this line in `atlas_engine/chat.py` (line 42):

```python
BACKENDS = {
    "gemini": "gemini-2.5-flash",
    "gpt": "gpt-4o-mini",
    "groq": "openai/gpt-oss-20b",   # <-- change this value
    "ollama": "gpt-oss:120b-cloud",
}
```

Replace `"openai/gpt-oss-20b"` with any model from [Groq's model list](https://console.groq.com/docs/models). Examples:

```python
"groq": "llama-3.3-70b-versatile",
"groq": "deepseek-r1-distill-llama-70b",
"groq": "mixtral-8x7b-32768",
```

## Context Memory

All backends now remember the last 3 exchanges (question + answer pairs). You do not need to configure anything.

```
[Pregunta]: What is LFI?
[Respuesta]: LFI allows reading local files...

[Pregunta]: How do I escalate that to RCE?
[Respuesta]: Building on the LFI vector discussed above...
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              It remembers the previous exchange.
```

Memory resets when you create a new `Atlas()` instance or exit Python.

## Semantic Cache

When you ask a question, Atlas checks Pinecone for a semantically similar previous query. If found (cosine similarity >= 0.92), it returns the cached answer instantly without calling the LLM.

```
atlas.ask("What is LFI?")          # MISS -> calls LLM -> caches response
atlas.ask("Explain LFI")           # HIT  -> instant response from cache
                                    #   [CACHE HIT] score=0.9534
```

Cache is stored in your existing Pinecone index under namespace `__cache__`.

### View cache stats

```python
atlas.chat_engine.cache.stats()
```

Output:

```
Semantic Cache Stats:
  Hits: 3
  Misses: 7
  Hit rate: 30.0%
  Threshold: 0.92
  Namespace: __cache__
```

### Check if cache grew after a conversation

```python
atlas.chat_engine.cache.stats()
```

Every question that goes to the LLM gets cached. The `Misses` count tells you how many new entries were added.

### Clear cache

```python
atlas.chat_engine.cache.clear()
```

### Cache shows stats on exit

When you type `exit` in interactive chat, cache stats print automatically:

```
[Pregunta]: exit
Saliendo...

Semantic Cache Stats:
  Hits: 2
  Misses: 5
  Hit rate: 28.6%

Session saved: /home/kali/Desktop/RAG/chat_history/session_groq_20260226_160000_chatml.jsonl
```

## ChatML Fine-Tuning Logs

Every conversation is saved automatically in ChatML/ShareGPT format:

```
RAG/chat_history/session_groq_20260226_160000_chatml.jsonl
RAG/chat_history/session_gpt_20260226_161500_chatml.jsonl
```

Each line is a complete conversation turn compatible with Unsloth fine-tuning:

```json
{
  "conversations": [
    {"from": "system", "value": "Identity: You are Atlas Engine..."},
    {"from": "human", "value": "Context:...\n\nQuestion: What is LFI?"},
    {"from": "gpt", "value": "LFI allows reading local files..."}
  ]
}
```

Use directly with Unsloth:

```python
from unsloth import FastLanguageModel
dataset = load_dataset("json", data_files="chat_history/session_groq_*.jsonl")
```

## Full Pipeline Example

```bash
cd /home/kali/Desktop/RAG
source venv/bin/activate && python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()

# Ask with Groq (first call: cache miss, LLM responds)
response, sources = atlas.ask("How does XXE work?", backend="groq")
print(response)

# Ask similar question (cache hit, instant)
response, sources = atlas.ask("Explain XXE attacks", backend="groq")
print(response)

# Interactive chat with memory
atlas.chat(backend="groq")

# Check cache after conversation
atlas.chat_engine.cache.stats()

# Clear cache if needed
atlas.chat_engine.cache.clear()

exit()
```

## File Reference

| File | Purpose |
|---|---|
| `atlas_engine/chat.py` | All backends, memory, cache integration |
| `atlas_engine/cache.py` | SemanticCache class (Pinecone namespace `__cache__`) |
| `config.py` | `get_groq_key()` reads from `.env/*.env` |
| `.env/openai.env` | Add `GROQ_API_KEY=...` here |
| `chat_history/*.jsonl` | Auto-generated ChatML logs |
