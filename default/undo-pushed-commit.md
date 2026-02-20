---
chunk_id: github::recovery::undo-pushed::001
domain: github
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, undo, revert, pushed-commit, github, after-push]
source_file: undo-pushed-commit.md
---

# Deshacer: Empujé a GitHub

## La Situación
```bash
git commit -m "feat: Cambio"
git push origin main
# ¡¡Oh no!! ¡¡Eso no debería estar!!
```

## El Comando (RECOMENDADO)
```bash
git revert HEAD
# Crea un NUEVO commit que deshace
git push origin main
```

## Resultado
```
GitHub muestra:
- Commit original (para referencia)
- Revert commit (que lo deshace)
```

## Ejemplo RAG
```bash
cd /home/kali/Desktop/RAG
git commit -m "docs: Add guide"
git push origin main
# ¡¡Tiene error!!

# Crear revert
git revert HEAD
# Se abre editor, guardar (Enter)
git push origin main
# ✅ Deshecho en GitHub
```

## Ejemplo Proyecto Nuevo
```bash
cd /home/kali/Desktop/mi-proyecto
git push origin main
# ¡Metí la pata!

git revert HEAD
git push origin main
# ✅ Deshecho
```

## ⚠️ Si es Proyecto Privado (Solo Tú)
```bash
# Puedes hacer force push (¡NO en público!)
git reset --hard HEAD~1
git push origin main --force
```

