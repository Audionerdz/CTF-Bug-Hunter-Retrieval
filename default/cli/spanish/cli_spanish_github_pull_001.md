---
chunk_id: cli::spanish::github::pull::001
domain: cli
chunk_type: guide
category: github
confidence: high
reuse_level: universal
tags: [git, pull, fetch, download, spanish]
---

## Descargar Cambios desde GitHub

```bash
# Obtén lo último sin fusionar
git fetch origin

# Ve qué cambió
git log HEAD..origin/main --oneline

# Descarga y fusiona
git pull origin main

# O en una línea
git pull
```
