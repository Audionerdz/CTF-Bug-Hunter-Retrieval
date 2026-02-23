---
chunk_id: github::recovery::undo-edited::001
domain: github
chunk_type: technique
---

# Deshacer: Edité un Archivo (Sin `git add`)

## La Situación
```bash
cd /home/kali/Desktop/RAG
nano docs/mi-guia.md
# Edité y ahora me arrepiento
```

## El Comando
```bash
git restore docs/mi-guia.md
```

## Verificar
```bash
git status
# Debería estar limpio
```

## Ejemplo RAG
```bash
cd /home/kali/Desktop/RAG
nano docs/vectorization-guide.md
# ¡Oops! Metí la pata
git restore docs/vectorization-guide.md
# ✅ Volvió al original
```

## Ejemplo Proyecto Nuevo
```bash
cd /home/kali/Desktop/mi-proyecto
nano src/main.py
# No quería esos cambios
git restore src/main.py
# ✅ Listo
```
