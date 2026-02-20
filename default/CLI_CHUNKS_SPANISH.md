---
chunk_id: cli::spanish::setup::configure-git::001
domain: cli
chunk_type: guide
category: git-setup
confidence: high
reuse_level: universal
tags: [setup, git, configuration, spanish]
---

## Configurar Git por Primera Vez

```bash
# Configura tu nombre de usuario
git config user.name "Tu Nombre"

# Configura tu email
git config user.email "tu@email.com"

# Verifica la configuración
git config --list
```

---
chunk_id: cli::spanish::git-basics::check-status::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, status, check, spanish]
---

## Verificar Estado de Git

```bash
# Ver estado general
git status

# Ver cambios detallados
git diff

# Ver cambios preparados
git diff --staged

# Ver cambios en un archivo específico
git diff archivo.md
```

---
chunk_id: cli::spanish::git-basics::staging::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, staging, add, spanish]
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

---
chunk_id: cli::spanish::git-basics::commit::001
domain: cli
chunk_type: guide
category: git-operations
confidence: high
reuse_level: universal
tags: [git, commit, message, spanish]
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

---
chunk_id: cli::spanish::recovery::undo-before-stage::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, undo, recovery, spanish]
---

## Deshacer Cambios Sin Preparar

```bash
# Ver qué cambió
git status
git diff archivo.md

# Opción 1: Restaurar archivo original
git restore archivo.md

# Opción 2: Usar checkout
git checkout archivo.md

# Descartar TODOS los cambios
git restore .
```

---
chunk_id: cli::spanish::recovery::undo-staged::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, unstage, reset, spanish]
---

## Deshacer Staging (Cambios Preparados)

```bash
# Deshacer staging de un archivo
git reset archivo.md

# Deshacer staging de TODOS
git reset

# Verificar estado
git status
```

---
chunk_id: cli::spanish::recovery::undo-commit::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, reset, undo-commit, spanish]
---

## Deshacer un Commit (Antes de Subir)

```bash
# Opción 1: Mantén cambios, solo deshaz el commit
git reset --soft HEAD~1

# Opción 2: Descarta todo (PERMANENTE)
git reset --hard HEAD~1

# Verifica el historial
git log --oneline -5
```

---
chunk_id: cli::spanish::recovery::revert-pushed::001
domain: cli
chunk_type: guide
category: recovery
confidence: high
reuse_level: universal
tags: [git, revert, pushed, github, spanish]
---

## Deshacer Cambios Ya Subidos a GitHub

```bash
# Ve el commit que quieres deshacer
git log --oneline -5

# Crea un nuevo commit que lo revierte
git revert hash-del-commit

# Sube el revert
git push origin main
```

---
chunk_id: cli::spanish::files::copy-directory::001
domain: cli
chunk_type: guide
category: file-operations
confidence: high
reuse_level: universal
tags: [files, directory, copy, spanish]
---

## Copiar Directorios al Repositorio

```bash
# Copiar un directorio completo
cp -r /ruta/origen /home/kali/Desktop/RAG/destino

# Copiar archivos de un directorio
cp -r /ruta/origen/* /home/kali/Desktop/RAG/destino/

# Crear directorio en el repo
mkdir -p /home/kali/Desktop/RAG/nuevo-directorio
```

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

---
chunk_id: cli::spanish::github::push::001
domain: cli
chunk_type: guide
category: github
confidence: high
reuse_level: universal
tags: [git, push, github, upload, spanish]
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

---
chunk_id: cli::spanish::github::pull::001
domain: cli
chunk_type: guide
category: github
confidence: high
reuse_level: universal
tags: [git, pull, fetch, download, spanish]
---

## Descargar Cambios desde GitHub

```bash
# Obtén lo último sin fusionar
git fetch origin

# Ve qué cambió
git log HEAD..origin/main --oneline

# Descarga y fusiona
git pull origin main

# O en una línea
git pull
```

---
chunk_id: cli::spanish::vectorization::single-file::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, file, single, spanish]
---

## Vectorizar un Archivo Individual

```bash
# Desde la raíz del repositorio
cd /home/kali/Desktop/RAG

# Vectoriza UN archivo
python3 src/vectorize_canonical_openai.py ./docs/mi-guia.md

# Ver resultado
echo "Vectorización completa!"
```

---
chunk_id: cli::spanish::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directory, batch, spanish]
---

## Vectorizar un Directorio Completo

```bash
# Vectoriza todos los archivos en docs/
python3 src/vectorize_canonical_openai.py ./docs/

# Vectoriza el repositorio completo
python3 src/vectorize_canonical_openai.py .

# Resultado mostrará chunks creados
```

---
chunk_id: cli::spanish::query::how-to-query::001
domain: cli
chunk_type: guide
category: search
confidence: high
reuse_level: universal
tags: [query, search, semantic, spanish]
---

## Cómo Consultar tu Base de Conocimiento

```bash
# Pregunta en español
python3 src/query_canonical_openai.py "cómo revertir un commit"

# Pregunta en inglés
python3 src/query_canonical_openai.py "how to push to github"

# Consulta general
python3 src/query_canonical_openai.py "git workflow"
```

---
chunk_id: cli::spanish::workflow::full-cycle::001
domain: cli
chunk_type: guide
category: workflow
confidence: high
reuse_level: universal
tags: [workflow, cycle, complete, spanish]
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

---
chunk_id: cli::spanish::tips::commit-messages::001
domain: cli
chunk_type: guide
category: best-practices
confidence: high
reuse_level: universal
tags: [tips, commit, message, best-practice, spanish]
---

## Consejo: Mensajes de Commit Efectivos

```bash
# Malo - no descriptivo
git commit -m "update"

# Bueno - claro y específico
git commit -m "fix: Corregir typo en README.md"

# Mejor - con contexto
git commit -m "feat: Agregar guía SQL injection con 5 payloads

- Incluye técnicas de bypass
- Ejemplos de laboratorio real
- Sección de remediation"
```

---
chunk_id: cli::spanish::tips::commit-often::001
domain: cli
chunk_type: guide
category: best-practices
confidence: high
reuse_level: universal
tags: [tips, workflow, commit-frequency, spanish]
---

## Consejo: Confirma Frecuentemente

```bash
# Confirma cambios pequeños regularmente
git add seccion-1.md
git commit -m "docs: Completar sección 1"

git add seccion-2.md
git commit -m "docs: Completar sección 2"

# Sube todos al final
git push origin main

# Verifica historial
git log --oneline -5
```

---
chunk_id: cli::spanish::reference::quick-commands::001
domain: cli
chunk_type: reference
category: quick-ref
confidence: high
reuse_level: universal
tags: [reference, quick, commands, spanish]
---

## Referencia Rápida de Comandos Principales

```bash
# Verificar estado
git status

# Ver cambios
git diff

# Preparar todo
git add .

# Confirmar
git commit -m "mensaje"

# Subir
git push origin main

# Descargar
git pull origin main

# Ver historial
git log --oneline -10

# Deshacer cambios
git restore .

# Revertir commit
git revert hash-del-commit
```

