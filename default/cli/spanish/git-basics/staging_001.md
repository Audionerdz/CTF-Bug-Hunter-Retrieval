---
chunk_id: cli::spanish::git-basics::staging::001
domain: cli
chunk_type: technique
---

## Preparar Archivos (Staging)

```bash
# Preparar un archivo específico
git add archivo.md

# Preparar todos los cambios
git add .

# Preparar todos EXCEPTO uno
git add . && git reset archivo-excluir.md

# Deshacer staging de un archivo
git reset archivo.md

# Deshacer staging de todos
git reset
```
