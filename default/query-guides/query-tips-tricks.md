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
query "tengo miedo de perder mi trabajo en git"
query "¿cómo protejo mis secretos?"
query "quiero trabajar con otros sin romper todo"
```

## Multiple Phrasings
```bash
# Mismo concepto, palabras diferentes
query "revert"
query "undo"
query "ir atrás"
query "deshacer cambio"
# Cada uno puede retornar resultados ligeramente diferentes
```

## Be Specific
```bash
# Mejor especificar contexto
query "cómo crear repo privado proyecto nuevo"
# Que
query "crear repo"
```

