---
chunk_id: cli::spanish::github::pull::001
domain: cli
chunk_type: technique
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
