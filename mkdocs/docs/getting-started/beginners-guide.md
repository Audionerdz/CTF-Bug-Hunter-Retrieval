# Beginner's Guide: Atlas Engine

Atlas Engine is meant to be used from a single interactive Python session.

## Start a session

```bash
python3
```

From the venv (one line):

```bash
source venv/bin/activate && python3
```


```python
from atlas_engine import Atlas
atlas = Atlas()
```

## Core commands (minimal)

```python
atlas.query("LFI", top_k=3)
atlas.ask("What is LFI?")
atlas.ask("What is LFI?", backend="gpt")
atlas.ask("What is LFI?", backend="ollama")
atlas.chat()
atlas.chat(backend="gpt")
atlas.fetch("technique::web::lfi::path-traversal::001")
atlas.delete("chunk_id::here")
atlas.vectorize("/path/to/chunk.md")
atlas.stats()
atlas.help()
```

Ask vs chat:
- `atlas.ask()` returns one answer immediately.
- `atlas.chat()` starts an interactive session where you keep asking multiple questions.
- Default model for `atlas.ask()` is Gemini unless you pass `backend="gpt"` or `backend="ollama"`.

Notes:
- `atlas.chat()` is interactive; use `atlas.ask()` for a single answer.
- If you do not pass `namespace`, Atlas uses the default namespace automatically.

## Vectorize without frontmatter (manual metadata)

```python
atlas.vectorize(
    "/path/to/notes.md",
    domain="web",
    tags=["pentesting", "injection"],
    metadata={"confidence": 5, "reuse_level": 2}
)
```

## Vectorize from text (one shot)

```python
from atlas_engine import Atlas
atlas = Atlas()

atlas.vectorize_text(
    """
# Injection Surface Checklist (Short)

Use this to quickly map input points during recon.

## Direct Inputs (GET/POST)
* **GET**: `id`, `page`, `q`, `search`, `user`, `order`.
* **POST**: `username`, `email`, `password`, `comment`, `message`.
* **Path**: `/user/1234/profile` -> `1234` is often an internal ID.

## APIs and Headers
* **JSON**: `{ "id": 1, "filter": "..." }`
* **GraphQL**: fields in `query` and `variables`
* **Headers**: `Cookie`, `Authorization`, `Referer`, `X-Forwarded-For`

## Response Signals
* Content changes, time delays, HTTP 500 vs 200, stack traces
""",
    chunk_id="technique::web::recon::injection-surface-mapping::001",
    path="default/web/recon/injection-surface-mapping_001.md",
    domain="web",
    tags=["pentesting", "hunting", "attack-surface", "burp-suite", "injection", "fuzzing", "bug-bounty"],
    metadata={"chunk_type": "technique", "confidence": 5, "reuse_level": 2},
)
```

This example includes metadata via `domain`, `tags`, and `metadata`.

## Chat (different backends)

```python
atlas.chat()                 # default (Gemini)
atlas.chat(backend="gpt")   # OpenAI
atlas.chat(backend="ollama") # local
```

Use flags on the command (before the chat starts):

```bash
atlas-chat --backend gpt
atlas-chat --backend gpt --model gpt-4o-mini
atlas-chat --backend ollama --model llama3
```

Note: `atlas.chat()` is interactive; you do not need `print(answer)` there. For a single answer, use `atlas.ask()`.

## Exit

```python
exit()
```
