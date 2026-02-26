# Beginner's Guide: Atlas Engine

Atlas Engine is meant to be used from a single interactive Python session.

## Start a session

```bash
python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()
```

## Core commands (minimal)

```python
atlas.query("LFI", top_k=3)
atlas.ask("What is LFI?")
atlas.chat()
atlas.chat(backend="gpt")
atlas.fetch("technique::web::lfi::path-traversal::001")
atlas.delete("chunk_id::here")
atlas.vectorize("/path/to/chunk.md")
atlas.stats()
atlas.help()
```

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

## Exit

```python
exit()
```
