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

## El Comando Más Corto (Usando alias)
```bash
query "tu pregunta aquí"
```

## Ejemplo
```bash
query "cómo hacer un commit"
query "ffuf subdomain fuzzing"
query "vectorizar archivos"
```

## Comando Completo (sin alias)
```bash
query "tu pregunta aquí"
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
- **Usa el alias `query`** si lo tienes configurado (ver ALIASES.md)
- Las comillas son obligatorias alrededor de la pregunta
- Funciona en español e inglés

