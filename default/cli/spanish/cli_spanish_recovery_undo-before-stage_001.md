---
chunk_id: cli::spanish::recovery::undo-before-stage::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, undo, recovery, spanish]
---

## Deshacer Cambios Sin Preparar

```bash
# Ver qué cambió
git status
git diff archivo.md

# Opción 1: Restaurar archivo original
git restore archivo.md

# Opción 2: Usar checkout
git checkout archivo.md

# Descartar TODOS los cambios
git restore .
```
