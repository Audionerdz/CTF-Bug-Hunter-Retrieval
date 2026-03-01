---
chunk_id: cli::spanish::recovery::revert-pushed::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, pushed, github, spanish]
---

## Deshacer Cambios Ya Subidos a GitHub

```bash
# Ve el commit que quieres deshacer
git log --oneline -5

# Crea un nuevo commit que lo revierte
git revert hash-del-commit

# Sube el revert
git push origin main
```
