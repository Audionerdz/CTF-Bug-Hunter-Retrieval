---
chunk_id: github::recovery::undo-staged::001
domain: github
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, undo, reset, staged-files, git-add]
source_file: undo-staged-files.md
---

# Deshacer: Preparé Cambios (Con `git add`)

## La Situación
```bash
nano archivo1.md
nano archivo2.md
git add .
# ¡Oops! No quería preparar eso
```

## El Comando
```bash
git reset
# Deshacer TODOS los preparados
```

## Para UN archivo
```bash
git reset archivo1.md
```

## Verificar
```bash
git status
# Dice: "Changes not staged for commit"
# Los archivos siguen editados, puedes seguir
```

## Ejemplo RAG
```bash
cd /home/kali/Desktop/RAG
nano docs/README.md
git add docs/README.md
# ¡No quería preparar!
git reset docs/README.md
# ✅ Sigue editado, sin preparar
```

## Ejemplo Proyecto Nuevo
```bash
cd /home/kali/Desktop/mi-proyecto
git add .
# Preparé todo por error
git reset
# ✅ Todo sin preparar
```

