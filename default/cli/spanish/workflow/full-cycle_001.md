---
chunk_id: cli::spanish::workflow::full-cycle::001
domain: cli
chunk_type: technique
---

## Ciclo Completo: Cambios → Commit → Push

```bash
# 1. Inicia el día descargando lo último
git pull

# 2. Haz cambios en tus archivos
nano docs/mi-guia.md

# 3. Verifica qué cambió
git status

# 4. Prepara todos los cambios
git add .

# 5. Confirma con mensaje descriptivo
git commit -m "feat: Agregar nueva guía de explotación"

# 6. Sube a GitHub
git push origin main

# 7. Verifica que se subió
git log --oneline -3
```
