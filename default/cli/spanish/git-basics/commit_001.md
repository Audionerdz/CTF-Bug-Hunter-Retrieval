---
chunk_id: cli::spanish::git-basics::commit::001
domain: cli
chunk_type: technique
---

## Hacer un Commit (Guardar Cambios)

```bash
# Commit simple
git commit -m "Corrección en README"

# Commit con descripción detallada
git commit -m "fix: Actualizar instrucciones

- Agregué paso de activación del venv
- Aclaré instalación de dependencias
- Agregué sección de troubleshooting"

# Ver historial de commits
git log --oneline -10
```
