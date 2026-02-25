---
chunk_id: cli::spanish::troubleshooting::merge-conflict::001
domain: cli
chunk_type: guide
category: troubleshooting
confidence: high
reuse_level: universal
tags: [troubleshooting, merge, conflict, spanish]
---

## Solución: Conflicto de Fusión

```bash
# Cuando falla git pull
git pull origin main

# Abre el archivo conflictivo
nano archivo-conflictivo.md

# Busca estos marcadores:
# <<<<<<< HEAD (tus cambios)
# ======= (divisor)
# >>>>>>> origin/main (sus cambios)

# Edita para mantener lo correcto, elimina marcadores

# Prepara y confirma
git add archivo-conflictivo.md
git commit -m "fix: Resolver conflicto de fusión"

# Sube
git push origin main
```
