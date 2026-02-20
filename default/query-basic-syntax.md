---
chunk_id: rag::query::basic-syntax::001
domain: rag
chunk_type: guide
category: query
confidence: high
reuse_level: universal
tags: [query, canonical, syntax, basic, command]
source_file: query-basic-syntax.md
---

# Query: Sintaxis Básica

## El Comando Completo (Con venv activado)
```bash
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "tu pregunta aquí"
```

## Ejemplo Completo
```bash
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "cómo hacer un commit"
```

## Alternativa (Si ya activaste el venv)
```bash
source /root/.openskills/venv/bin/activate
cd /home/kali/Desktop/RAG
python3 src/query_canonical_openai.py "cómo hacer un commit"
deactivate
```

## Resultado
```
Muestra los 5 chunks más relevantes
Con scores de relevancia (0.0 a 1.0)
```

## Formato de la Pregunta
```
"pregunta en español o inglés"
```

## Importante
- **Ruta completa al venv Python:** `/root/.openskills/venv/bin/python3` (NO usar `python3` del sistema)
- **Ruta completa al script:** `/home/kali/Desktop/RAG/src/query_canonical_openai.py`
- Las comillas son obligatorias alrededor de la pregunta

