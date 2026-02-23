---
chunk_id: github::recovery::undo-local-commit::001
domain: github
chunk_type: technique
---

# Deshacer: Hice un Commit (Pero No Empujé)

## La Situación
```bash
git add .
git commit -m "feat: Cambio"
# ¡Ahora me arrepiento!
# (Aún no hiciste push)
```

## Opción A: Mantén los Cambios
```bash
git reset --soft HEAD~1
# El commit se borra
# Los archivos siguen editados
# Puedes re-hacer el commit
```

## Opción B: Borra Todo (⚠️)
```bash
git reset --hard HEAD~1
# Todo se borra, vuelve a como estaba
```

## Verificar
```bash
git log --oneline -3
# El commit debería desaparecer
```

## Ejemplo RAG
```bash
cd /home/kali/Desktop/RAG
git commit -m "docs: Add guide"
# ¡Espera! Tiene error

# Opción A: Mantener y re-hacer
git reset --soft HEAD~1
nano docs/guide.md  # Edita
git commit -m "docs: Add guide (fixed)"

# Opción B: Descartar todo
git reset --hard HEAD~1
```

## Ejemplo Proyecto Nuevo
```bash
cd /home/kali/Desktop/mi-proyecto
git commit -m "feat: Core"
# No lo quería aquí
git reset --hard HEAD~1
# ✅ Volvió
```
