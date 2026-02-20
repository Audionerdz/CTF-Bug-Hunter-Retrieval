---
chunk_id: cli::spanish-guide::setup::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, setup, spanish, cheatsheet, beginners]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Setup Absoluto para Principiantes

## Primera Configuración (Copia y Pega)

```bash
# 1. Navega a tu repositorio
cd /home/kali/Desktop/RAG

# 2. Verifica que git esté inicializado (debe estar ✅)
git status

# 3. Configura git (primera vez - usa tu información)
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# 4. Verifica tu configuración
git config --list

# 5. Instala dependencias de Python
python3 -m pip install -r config/requirements.txt
```

## Verifica que Estés Listo

```bash
# Debe mostrar: On branch main, nothing to commit
git status

# Debe mostrar tus commits
git log --oneline -5
```

---
chunk_id: cli::spanish-guide::git-basics::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, basics, spanish, states, workflow]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Conceptos Básicos de Git (Rastrear Cambios)

## Entendiendo los Estados de Git

```
DIRECTORIO DE TRABAJO → ÁREA DE STAGING → REPOSITORIO LOCAL → GITHUB
      (archivos)          (git add)        (git commit)      (git push)
```

## Verifica Qué Cambió

```bash
# Ve todos los archivos modificados
git status

# Ve cambios detallados en archivos
git diff

# Ve cambios que ya preparaste
git diff --staged

# Ve cambios en UN archivo específico
git diff nombre-archivo.md
```

## Prepara Archivos para Commit

```bash
# Prepara UN archivo
git add nombre-archivo.md

# Prepara TODOS los archivos modificados
git add .

# Prepara todos EXCEPTO uno
git add . && git reset nombre-archivo.md

# Desprepara un archivo (saca del staging)
git reset nombre-archivo.md

# Verifica qué preparaste
git status
```

---
chunk_id: cli::spanish-guide::commit-messages::001
domain: cli
chunk_type: guide
category: git-and-cli
confidence: high
reuse_level: universal
tags: [cli, git, commits, messages, spanish]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Confirmar (Guarda Localmente)

## Commit simple
```bash
git commit -m "Corregí typo en README"
```

## Mejor commit (con detalles)
```bash
git commit -m "fix: Actualizar instrucciones del vectorizer para Python 3.10
- Agregué pasos de activación de entorno virtual
- Aclaré instalación de dependencias
- Agregué sección de troubleshooting"
```

## Prepara y confirma todo de una vez
```bash
git add . && git commit -m "feat: Agregar nueva guía CTF para inyección SQL"
```

## Verifica tus commits
```bash
git log --oneline -10
```

### Formato de Mensaje de Commit (Consejos Pro)

- **Fix**: Para correcciones
- **Feat**: Nueva característica agregada
- **Docs**: Actualizaciones de documentación
- **Refactor**: Reestructuración de código
- **Test**: Adición de pruebas

---
chunk_id: cli::spanish-guide::undo-mistakes::001
domain: cli
chunk_type: guide
category: git-recovery
confidence: high
reuse_level: universal
tags: [cli, git, undo, revert, recovery, spanish]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Revertir y Corregir Errores

## "Oops, No Quería Hacer Eso" - Guía de Recuperación

### Edité un Archivo pero No Lo Preparé

```bash
# Ve qué cambió
git status
git diff nombre-archivo.md

# Opción A: Mantén cambios pero desprepara
git reset nombre-archivo.md

# Opción B: Descarta cambios completamente (⚠️ PERMANENTE)
git restore nombre-archivo.md
# O
git checkout nombre-archivo.md
```

### Preparé Archivos pero Quiero Despreperarlos

```bash
# Desprepara UN archivo
git reset nombre-archivo.md

# Desprepara TODOS los archivos
git reset

# Verifica
git status
```

### Confirmé pero Quiero Deshacer (Antes de Subir)

```bash
# Mantén cambios, deshaz commit
git reset --soft HEAD~1
# Ahora puedes re-preparar y re-confirmar de otra forma

# Deshaz commit Y descarta cambios (⚠️ PERMANENTE)
git reset --hard HEAD~1
```

---
chunk_id: cli::spanish-guide::vectorization::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, spanish, guide, cli, workflow]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Flujo de Vectorización

## ¿Qué es la Vectorización?

Convertir tus archivos markdown en **chunks buscables** para consultarlos después:

```
Archivo Markdown → Dividir en Chunks → Convertir a Vectores → Guardar en Pinecone
```

## Vectorizar un Archivo Único

```bash
# Desde raíz del repo
cd /home/kali/Desktop/RAG

# Vectoriza UN archivo markdown
python3 src/vectorize_canonical_openai.py \
  ./docs/mi-guia.md

# Verifica que funcionó
echo "¡Vectorización completa! Consultalo después con:"
echo "python3 src/query_canonical_openai.py 'término de búsqueda'"
```

## Vectorizar un Directorio Completo

```bash
# Vectoriza TODOS los archivos en docs/
python3 src/vectorize_canonical_openai.py \
  ./docs/

# Vectoriza el repo completo
python3 src/vectorize_canonical_openai.py \
  .
```

## Vectorizar Archivos Nuevos (Después de Agregarlos a Git)

**Flujo de trabajo recomendado:**

```bash
# 1. Agrega nueva guía
nano docs/nueva-guia.md

# 2. Agrégalo a git
git add docs/nueva-guia.md

# 3. Confirma
git commit -m "docs: Agregar nueva guía de explotación"

# 4. Vectoriza el archivo
python3 src/vectorize_canonical_openai.py ./docs/nueva-guia.md

# 5. Sube a GitHub
git push origin main

# 6. Ahora consulta
python3 src/query_canonical_openai.py "tema de la guía"
```

---
chunk_id: cli::spanish-guide::push-pull::001
domain: cli
chunk_type: guide
category: git-remote
confidence: high
reuse_level: universal
tags: [git, push, pull, github, remote, spanish]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Subir a GitHub (Repositorio Remoto)

## Flujo de Trabajo Empujar-Tirar

### Sube tus Cambios a GitHub

```bash
# Después de confirmar localmente, sube a rama main
git push origin main

# Verifica que funcionó
git status
# Debe mostrar: "Your branch is up to date with 'origin/main'"
```

### Descarga Cambios desde GitHub (Si Otros lo Modificaron)

```bash
# Obtén lo último de GitHub
git fetch origin

# Ve qué cambió
git log HEAD..origin/main --oneline

# Descarga (descarga y fusiona)
git pull origin main

# O más rápido en una línea
git pull
```

## Flujo Completo "Una Persona"

```bash
# 1. Inicia tu día - obtén lo último
git pull

# 2. Haz cambios
# ... edita archivos ...

# 3. Verifica qué cambió
git status

# 4. Prepara todos los cambios
git add .

# 5. Confirma con mensaje
git commit -m "feat: Agregar nueva guía de explotación"

# 6. Sube a GitHub
git push

# 7. Verifica
git log --oneline -3
```

---
chunk_id: cli::spanish-guide::quick-reference::001
domain: cli
chunk_type: reference
category: git-and-cli
confidence: high
reuse_level: universal
tags: [quick-reference, commands, spanish, cheatsheet]
source_file: GUIA_CLI_CHEATSHEET.md
---

# Tarjeta de Referencia Rápida

| Tarea | Comando |
|------|---------|
| **Ver Estado** | `git status` |
| **Ver Cambios** | `git diff` |
| **Preparar Todo** | `git add .` |
| **Confirmar** | `git commit -m "msg"` |
| **Subir** | `git push origin main` |
| **Descargar** | `git pull origin main` |
| **Ver Historial** | `git log --oneline -10` |
| **Deshacer Último Commit** | `git reset --soft HEAD~1` |
| **Descartar Cambios** | `git restore .` |
| **Vectorizar Archivo** | `python3 src/vectorize_canonical_openai.py ./docs/archivo.md` |
| **Vectorizar Directorio** | `python3 src/vectorize_canonical_openai.py ./docs/` |
| **Consultar KB** | `python3 src/query_canonical_openai.py "búsqueda"` |
| **Copiar Directorio** | `cp -r origen/ destino/` |
| **Eliminar Archivo** | `git rm archivo.md` |
| **Revertir Commit** | `git revert hash-commit` |

