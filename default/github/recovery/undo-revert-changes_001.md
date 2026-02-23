---
chunk_id: github::recovery::undo-revert-changes::001
domain: github
chunk_type: technique
---

# Cómo Deshacer Cambios: Guía de Recuperación

## Tabla Rápida: ¿Qué Hiciste? ¿Cómo Deshaces?

```
┌─────────────────────────────────────┬──────────────────────────────┐
│ Situación                           │ Comando                      │
├─────────────────────────────────────┼──────────────────────────────┤
│ 1. Edité archivo (sin git add)      │ git restore archivo.md       │
│ 2. Preparé cambios (git add)        │ git reset archivo.md         │
│ 3. Hice commit local                │ git reset --soft HEAD~1      │
│ 4. Hice commit + quiero borrar      │ git reset --hard HEAD~1      │
│ 5. Empujé a GitHub                  │ git revert hash-commit       │
│ 6. Borrar múltiples commits         │ git reset --hard HEAD~5      │
│ 7. Ver cambios antes de deshacer    │ git diff / git diff --staged │
└─────────────────────────────────────┴──────────────────────────────┘
```

---

## Escenario 1: Edité un Archivo (Sin `git add`)

### La Situación:
```bash
# Estás en /home/kali/Desktop/RAG
cd /home/kali/Desktop/RAG

# Abriste archivo y lo editaste
nano docs/mi-guia.md

# Ahora te arrepientes
# Quieres volver a la versión original
```

### Ver Cambios Antes de Deshacer
```bash
# Ver qué cambió
git diff docs/mi-guia.md

# O ver TODOS los cambios
git diff
```

### Deshacer el Cambio
```bash
# Opción 1: Restaurar a la versión original (RECOMENDADO)
git restore docs/mi-guia.md

# Opción 2: Igual resultado, nombre antiguo
git checkout docs/mi-guia.md

# Verificar
git status
# El archivo debería estar limpio
```

### Ejemplo Completo
```bash
cd /home/kali/Desktop/RAG

# Edité por error
nano docs/vectorization-guide.md

# ¡Oops! Metí la pata
# Ver qué cambié
git diff docs/vectorization-guide.md

# Deshacer
git restore docs/vectorization-guide.md

# Listo, volvió a original
cat docs/vectorization-guide.md
```

---

## Escenario 2: Preparé Cambios con `git add` (Pero Aún No Commit)

### La Situación:
```bash
# Editaste archivos
nano archivo1.md
nano archivo2.md

# Los preparaste por error
git add archivo1.md
git add archivo2.md

# Ahora quieres deshacer
```

### Ver Qué Preparaste
```bash
# Ver archivos preparados
git status

# Ver cambios preparados en detalle
git diff --staged

# Ver cambios en un archivo específico
git diff --staged archivo1.md
```

### Deshacer el Staging (Dejar En Edición)
```bash
# Opción 1: Deshacer UN archivo
git reset archivo1.md

# Opción 2: Deshacer TODOS los preparados
git reset

# Verificar
git status
# Ahora dice "Changes not staged for commit"
```

### Deshacer Completamente (Archivo + Staging)
```bash
# Deshacer TODO: staging + cambios
git restore --staged --worktree archivo1.md

# O más simple:
git reset --hard HEAD -- archivo1.md
```

### Ejemplo Completo
```bash
cd /home/kali/Desktop/RAG

# Edité por error y preparé
nano docs/README.md
nano src/script.py
git add .

# ¡Oops! No quería preparar
# Ver qué preparé
git diff --staged

# Deshacer staging
git reset

# Archivos todavía editados, puedo seguir editando
git status
# "Changes not staged for commit"

# O si quiero deshacer COMPLETAMENTE
git restore docs/README.md
git restore src/script.py
```

---

## Escenario 3: Hice un Commit (Pero Aún No Empujé a GitHub)

### La Situación:
```bash
# Hiciste cambios y los confirmaste
git add .
git commit -m "feat: Agregar nueva guía"

# Ahora te arrepientes del commit
# Aún no hiciste push
```

### Ver el Commit
```bash
# Ver últimos commits
git log --oneline -5

# Ver detalles del último commit
git show HEAD

# Ver cambios del último commit
git diff HEAD~1..HEAD
```

### Opción A: Deshacer Commit PERO Mantén los Cambios

```bash
# Esto revierte el commit pero los archivos siguen editados
git reset --soft HEAD~1

# Ahora:
git status
# Dice: "Changes to be committed"
# Puedes editar más y hacer otro commit
```

### Opción B: Deshacer Commit Y Los Cambios (⚠️ PELIGRO)

```bash
# ¡ADVERTENCIA! Esto BORRA los cambios
git reset --hard HEAD~1

# Ahora todo vuelve a como estaba
git status
# "nothing to commit"
```

### Opción C: Mantén el Commit Pero Edita Algo

```bash
# Olvidaste algo en el commit
nano archivo.md  # Edita

# Agrega el cambio al commit anterior
git add archivo.md
git commit --amend -m "feat: Agregar nueva guía (con fix)"

# El commit anterior se reemplaza
git log --oneline -2
```

### Ejemplo Completo
```bash
cd /home/kali/Desktop/RAG

# Hiciste cambios y commit
nano docs/exploit-guide.md
git add docs/exploit-guide.md
git commit -m "docs: Add exploit guide"

# ¡Espera! Cometiste error de typo
# Ver qué hiciste
git log --oneline -2
git show HEAD

# Opción 1: Deshacer y mantener cambios
git reset --soft HEAD~1
# Edita el archivo
nano docs/exploit-guide.md
# Haz nuevo commit
git commit -m "docs: Add exploit guide (fixed)"

# Opción 2: Deshacer todo (¡CUIDADO!)
git reset --hard HEAD~1
# Todo vuelve a como era
```

---

## Escenario 4: Empujé a GitHub (¡La Peor!)

### La Situación:
```bash
# Hiciste commit + push
git commit -m "feat: Cambio"
git push origin main

# Ahora: "¡Oh no! ¡Eso no debería estar en GitHub!"
# ¡Pero ya está en el remoto!
```

### Ver el Commit
```bash
# Ver historial
git log --oneline -5

# Ver qué cambios tiene ese commit
git show hash-del-commit

# Ejemplo:
git show 7a3f9c2
```

### Opción A: Crear Un "Revert" Commit (RECOMENDADO)

```bash
# Esto crea un NUEVO commit que deshace el anterior
git revert 7a3f9c2

# Se abre editor para mensaje del revert
# (Mantén el mensaje por defecto o personaliza)

# Sube el revert commit
git push origin main

# Resultado:
# - El commit incorrecto sigue en el historial (para referencia)
# - El revert commit lo deshace
# - GitHub muestra ambos
```

### Opción B: Forzar Cambio (⚠️ PELIGRO - EQUIPO)

```bash
# ¡SOLO si trabajas solo! ¡NO en equipo!
# Esto borra el commit del historial completamente

git reset --hard HEAD~1
git push origin main --force

# ⚠️ ADVERTENCIA: Si otros tienen ese commit, ¡¡rompes todo!!
```

### Opción C: Si Subiste Secretos (¡CRÍTICO!)

```bash
# 1. INMEDIATAMENTE: Cambiar el secreto en el proveedor
#    (Revoca API keys, tokens, etc.)

# 2. HACER REPO PRIVADO
#    GitHub repo → Settings → Danger Zone → Make private

# 3. HACER REVERT COMMIT
git revert 7a3f9c2
git push origin main

# 4. VERIFICAR que el secreto no está
# (En GitHub, no debe ser visible)

# 5. DOCUMENTAR lo que pasó
```

### Ejemplo Completo
```bash
cd /home/kali/Desktop/RAG

# Hiciste cambios, commit y push
nano docs/guide.md
git add docs/guide.md
git commit -m "docs: Add guide"
git push origin main

# ¡¡Oops!! Tiene error

# Ver qué subiste
git log --oneline -3
git show HEAD

# Crear revert (lo CORRECTO)
git revert HEAD

# Se abre editor, guardar
# (Presiona Ctrl+O → Enter → Ctrl+X para nano)

# Push del revert
git push origin main

# Resultado: Dos commits en GitHub
# - Original: docs: Add guide
# - Revert: Revert "docs: Add guide"
# El cambio está deshecho
```

---

## Escenario 5: Quiero Borrar Múltiples Commits

### La Situación:
```bash
# Hiciste varios commits malos
git log --oneline
# 7a3f9c2 (malo)
# 8b4g5d3 (malo)
# 9c5h6e4 (malo)
# a1b2c3d (bueno - quiero volver aquí)

# Quiero volver a a1b2c3d y descartar los 3 commits
```

### Contar Cuántos Commits Deshacer
```bash
# Ver historial
git log --oneline -10

# Contar: Si están en las últimas 3 líneas
# Deshacer los últimos 3: HEAD~3

# Si quiero ver detalles
git show a1b2c3d  # El bueno
git show HEAD~3   # El mismo (HEAD~3 = a1b2c3d)
```

### Deshacer Múltiples Commits

```bash
# OPCIÓN A: Mantener cambios
git reset --soft HEAD~3
# Los 3 commits se deshacen pero archivos siguen editados
git status
# "Changes to be committed" (puedes re-hacer)

# OPCIÓN B: Descartar todo
git reset --hard HEAD~3
# Los 3 commits Y cambios se borran
# Vuelves al estado de a1b2c3d
```

### Ejemplo Completo
```bash
cd /home/kali/Desktop/RAG

# Ver historial
git log --oneline -5

# Hiciste 3 commits malos por error
git reset --hard HEAD~3

# Verificar
git log --oneline -5
# Los 3 malos desaparecieron

# Si trabajas en equipo (¡NO HAGAS!), mejor:
git revert HEAD~2   # El primero
git revert HEAD~1   # El segundo  
git revert HEAD     # El tercero
git push origin main
```

---

## Proyecto Nuevo: Casos Comunes

### Caso 1: Borraste Todo sin Querer

```bash
cd /home/kali/Desktop/mi-proyecto

# Edité archivos y ahora quiero volver
git restore .

# ¡Listo! Todo vuelve a original
```

### Caso 2: Hiciste Varios Commits Malos

```bash
cd /home/kali/Desktop/mi-proyecto

# Ver historial
git log --oneline

# Ver el bueno
git show hash-bueno

# Volver a ese commit
git reset --hard hash-bueno

# Verificar
git log --oneline
```

### Caso 3: Preparaste Por Error

```bash
cd /home/kali/Desktop/mi-proyecto

# Preparaste cambios malos
git status

# Deshacer staging
git reset

# Edita de nuevo si quieres
```

### Caso 4: Empujaste a GitHub (Proyecto Privado)

```bash
cd /home/kali/Desktop/mi-proyecto

# Empujaste cambios malos
git log --oneline -3

# Si es proyecto PRIVADO (seguro):
git reset --hard HEAD~1
git push origin main --force
# Solo TÚ accedes, está OK hacer force push

# Si es proyecto PÚBLICO (¡NO HAGAS!):
git revert HEAD
git push origin main
# Mejor para que otros no se confundan
```

---

## Resumen: Comandos Por Nivel de Arrepentimiento

### Nivel 1: "Edité pero no preparé"
```bash
git restore archivo.md
```

### Nivel 2: "Preparé con git add"
```bash
git reset archivo.md
```

### Nivel 3: "Hice commit local"
```bash
# Mantener cambios
git reset --soft HEAD~1

# Borrar cambios
git reset --hard HEAD~1
```

### Nivel 4: "Empujé a GitHub"
```bash
# Crear revert (RECOMENDADO)
git revert HEAD
git push origin main

# Force push (SOLO si proyecto privado y trabajas solo)
git reset --hard HEAD~1
git push origin main --force
```

### Nivel 5: "¡Subí secretos!"
```bash
# 1. Cambiar tokens inmediatamente
# 2. Hacer repo privado
# 3. git revert + push
# 4. Verificar que no aparecen
```

---

## Checklist: Antes de Deshacer Algo

```bash
✅ Ver qué va a pasar
   git diff                    # Cambios sin preparar
   git diff --staged           # Cambios preparados
   git show HEAD               # Último commit
   git log --oneline -5        # Últimos commits

✅ Verificar dónde estás
   git status
   git branch

✅ Hacer backup si es importante
   cp archivo.md archivo.md.bak

✅ Ejecutar el deshacer

✅ Verificar que funcionó
   git status
   git log --oneline -3
```

---

## Diferencias: RAG Repo vs Proyecto Nuevo

### En RAG Repo (Establecido)
```bash
# Es importante, cuidado con force push
# Mejor usar revert para cambios subidos

# Cambios sin preparar
git restore docs/archivo.md

# Cambios preparados
git reset docs/archivo.md

# Commits locales
git reset --soft HEAD~1  # Mantener cambios
git reset --hard HEAD~1  # Descartar

# Commits subidos
git revert HEAD
git push origin main

# ¡NUNCA hagas force push a main!
```

### En Proyecto Nuevo (Tuyo Solo)
```bash
# Es más flexible, puedes hacer fuerza
# Nadie más accede, es seguro

# Cambios sin preparar
git restore .

# Cambios preparados
git reset

# Commits locales
git reset --hard HEAD~1

# Commits subidos (en proyecto privado)
git reset --hard HEAD~1
git push origin main --force  # OK porque es tuyo

# Commits subidos (en proyecto público)
git revert HEAD
git push origin main
```

---

## Frases Útiles Para Recordar

> **"Antes de subir, puedes hacer lo que quieras"**
> 
> Editar, preparar, commit, incluso reset --hard

> **"Después de subir, mejor revert que reset"**
> 
> Porque preserva el historial y otros no se confunden

> **"Si subiste secretos, ¡ACCIÓN INMEDIATA!"**
>
> Cambiar tokens primero, después revert/reset

> **"git restore = volver a original"**
> 
> Sin preparar, sin commit

> **"git reset = deshacer preparar o commits"**
> 
> Con --soft (mantener) o --hard (borrar)

> **"git revert = crear nuevo commit que deshace"**
>
> Seguro, visible, para trabajar en equipo

---

## Ayuda Rápida

```bash
# "¿Qué cambié?"
git diff

# "¿Qué preparé?"
git diff --staged

# "¿Qué hice en el commit?"
git show HEAD

# "¿Qué commits tengo?"
git log --oneline -10

# "¿Dónde estoy?"
git status
git branch

# "Deshacer TODO"
git reset --hard HEAD
```
