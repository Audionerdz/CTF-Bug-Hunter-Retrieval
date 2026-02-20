---
chunk_id: rag::query::tips-tricks::001
domain: rag
chunk_type: guide
category: query
confidence: high
reuse_level: universal
tags: [query, tips, tricks, optimization, search-better]
source_file: query-tips-tricks.md
---

# Query: Tips y Tricks

## Natural Language Works
```bash
# ¡Funciona natural!
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "tengo miedo de perder mi trabajo en git"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "¿cómo protejo mis secretos?"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "quiero trabajar con otros sin romper todo"
```

## Multiple Phrasings
```bash
# Mismo concepto, palabras diferentes
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "revert"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "undo"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "ir atrás"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "deshacer cambio"
# Cada uno puede retornar resultados ligeramente diferentes
```

## Be Specific
```bash
# Mejor especificar contexto
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "cómo crear repo privado proyecto nuevo"
# Que
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "crear repo"
```

