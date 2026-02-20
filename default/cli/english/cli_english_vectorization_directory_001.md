---
chunk_id: cli::english::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directory, batch, english]
---

## Vectorize an Entire Directory

```bash
# Vectorize all files in default/
vectorize /home/kali/Desktop/RAG/default/

# Or with full path
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/

# Vectorize specific subdirectory
vectorize /home/kali/Desktop/RAG/default/network/

# Vectorize entire repo
vectorize /home/kali/Desktop/RAG/

# Output will show chunks created
```
