---
chunk_id: cli::english::query::how-to-query::001
domain: cli
chunk_type: guide
category: search
confidence: high
reuse_level: universal
tags: [query, search, semantic, english]
---

## How to Query Your Knowledge Base

```bash
# Question in English
python3 src/query_canonical_openai.py "how to revert a commit"

# Question in Spanish
python3 src/query_canonical_openai.py "cómo subir a github"

# General query
python3 src/query_canonical_openai.py "git workflow"
```
