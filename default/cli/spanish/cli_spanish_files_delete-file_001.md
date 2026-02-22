---
chunk_id: cli::spanish::files::delete-file::001
domain: cli
chunk_type: guide
category: file-operations
confidence: high
reuse_level: universal
tags: [git, delete, remove, file, spanish]
---

## Eliminar Archivos del Repositorio

```bash
# Eliminar un archivo y preparar la eliminación
git rm archivo.md

# Eliminar un directorio completo
git rm -r directorio/

# Confirmar la eliminación
git commit -m "docs: Eliminar archivo desactualizado"

# Subir cambios
git push origin main
```
