---
chunk_id: cli::spanish::github::push::001
domain: cli
chunk_type: technique
---

## Subir Cambios a GitHub

```bash
# Después de confirmar, sube a main
git push origin main

# Sube y verifica
git push origin main && git status

# Si la rama no existe aún
git push -u origin main
```
