---
chunk_id: cli::spanish::recovery::undo-commit::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, reset, undo-commit, spanish]
---

## Deshacer un Commit (Antes de Subir)

```bash
# Opción 1: Mantén cambios, solo deshaz el commit
git reset --soft HEAD~1

# Opción 2: Descarta todo (PERMANENTE)
git reset --hard HEAD~1

# Verifica el historial
git log --oneline -5
```
