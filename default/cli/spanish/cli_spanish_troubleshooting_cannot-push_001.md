---
chunk_id: cli::spanish::troubleshooting::cannot-push::001
domain: cli
chunk_type: guide
category: troubleshooting
confidence: high
reuse_level: universal
tags: [troubleshooting, push, error, spanish]
---

## Solución: No Puedo Subir a GitHub

```bash
# Verifica la conexión remota
git remote -v

# Intenta descargar primero
git pull origin main

# Luego intenta subir
git push origin main

# Si sigue fallando, verifica la rama
git branch -v
```
