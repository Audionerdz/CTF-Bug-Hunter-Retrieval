---
chunk_id: cli::spanish::tips::commit-often::001
domain: cli
chunk_type: guide
category: best-practices
confidence: high
reuse_level: universal
tags: [tips, workflow, commit-frequency, spanish]
---

## Consejo: Confirma Frecuentemente

```bash
# Confirma cambios pequeños regularmente
git add seccion-1.md
git commit -m "docs: Completar sección 1"

git add seccion-2.md
git commit -m "docs: Completar sección 2"

# Sube todos al final
git push origin main

# Verifica historial
git log --oneline -5
```
