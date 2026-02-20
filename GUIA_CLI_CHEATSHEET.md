---
title: "Guía CLI: Sistema de Recuperación CTF Bug Hunter"
desc: "Guía completa de comandos CLI para trabajar con repositorio CTF Bug Hunter - Git, vectorización, directorios y operaciones de archivo"
author: "CTF Community"
created: 2026-02-20
updated: 2026-02-20
tags: ["cli", "git", "vectorización", "guía", "cheatsheet", "español"]
namespace: "guia-cli-comandos-es"
---

# Guía CLI: Sistema de Recuperación CTF Bug Hunter

> **Modo Cheatcode Activado** 🔥 - Todo lo que necesitas para trabajar con el repo. Sin rodeos, directo al grano.

---

## Tabla de Contenidos

1. [Setup Absoluto para Principiantes](#setup-absoluto-para-principiantes)
2. [Conceptos Básicos de Git (Rastrear Cambios)](#conceptos-básicos-de-git-rastrear-cambios)
3. [Hacer Cambios (Editar y Confirmar)](#hacer-cambios-editar-y-confirmar)
4. [Revertir y Corregir Errores](#revertir-y-corregir-errores)
5. [Operaciones con Directorios y Archivos](#operaciones-con-directorios-y-archivos)
6. [Subir a GitHub (Repositorio Remoto)](#subir-a-github-repositorio-remoto)
7. [Flujo de Vectorización](#flujo-de-vectorización)
8. [Referencia Rápida de Scripts](#referencia-rápida-de-scripts)

---

## Setup Absoluto para Principiantes

### Primera Configuración (Copia y Pega)

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

### Verifica que Estés Listo

```bash
# Debe mostrar: On branch main, nothing to commit
git status

# Debe mostrar tus commits
git log --oneline -5
```

---

## Conceptos Básicos de Git (Rastrear Cambios)

### Entendiendo los Estados de Git

```
DIRECTORIO DE TRABAJO → ÁREA DE STAGING → REPOSITORIO LOCAL → GITHUB
      (archivos)          (git add)        (git commit)      (git push)
```

### Verifica Qué Cambió

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

### Prepara Archivos para Commit

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

### Confirma (Guarda Localmente)

```bash
# Commit simple
git commit -m "Corregí typo en README"

# Mejor commit (con detalles)
git commit -m "fix: Actualizar instrucciones del vectorizer para Python 3.10
- Agregué pasos de activación de entorno virtual
- Aclaré instalación de dependencias
- Agregué sección de troubleshooting"

# Prepara y confirma todo de una vez
git add . && git commit -m "feat: Agregar nueva guía CTF para inyección SQL"

# Verifica tus commits
git log --oneline -10
```

### Formato de Mensaje de Commit (Consejos Pro)

```
Fix: Descripción breve (para correcciones)
Feat: Nueva característica agregada
Docs: Actualizaciones de documentación
Refactor: Reestructuración de código
Test: Adición de pruebas
```

---

## Hacer Cambios (Editar y Confirmar)

### Flujo de Trabajo: Cambio → Preparar → Confirmar → Subir

#### Ejemplo 1: Editar un Archivo Markdown

```bash
# 1. Abre y edita el archivo
nano docs/guias/mi-guia.md
# (O usa tu editor: vim, code, gedit, etc.)

# 2. Verifica qué cambió
git diff docs/guias/mi-guia.md

# 3. Prepáralo
git add docs/guias/mi-guia.md

# 4. Confirma
git commit -m "docs: Mejorar guía de inyección SQL con ejemplos"

# 5. Sube a GitHub
git push origin main
```

#### Ejemplo 2: Agregar un Archivo Nuevo

```bash
# 1. Crea el archivo
echo "# Mi Nueva Guía" > docs/guias/nueva-guia.md

# 2. Añade contenido (usa tu editor)
nano docs/guias/nueva-guia.md

# 3. Prepáralo
git add docs/guias/nueva-guia.md

# 4. Confirma
git commit -m "docs: Agregar guía para técnicas de enumeración de APIs"

# 5. Sube
git push origin main
```

#### Ejemplo 3: Agregar Múltiples Archivos a la Vez

```bash
# 1. Crea varios archivos
echo "Contenido 1" > docs/api-1.md
echo "Contenido 2" > docs/api-2.md
echo "Contenido 3" > docs/api-3.md

# 2. Prepara todos
git add .

# 3. Confirma juntos
git commit -m "docs: Agregar documentación de enumeración de APIs (3 nuevas guías)"

# 4. Sube
git push origin main
```

### Verifica Tu Progreso

```bash
# Ve commits locales no subidos aún
git log origin/main..HEAD --oneline

# Ve commits en GitHub no descargados
git log HEAD..origin/main --oneline

# Ve historial completo
git log --graph --oneline --all
```

---

## Revertir y Corregir Errores

### "Oops, No Quería Hacer Eso" - Guía de Recuperación

#### Edité un Archivo pero No Lo Preparé

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

#### Preparé Archivos pero Quiero Despreperarlos

```bash
# Desprepara UN archivo
git reset nombre-archivo.md

# Desprepara TODOS los archivos
git reset

# Verifica
git status
```

#### Confirmé pero Quiero Deshacer (Antes de Subir)

```bash
# Mantén cambios, deshaz commit
git reset --soft HEAD~1
# Ahora puedes re-preparar y re-confirmar de otra forma

# Deshaz commit Y descarta cambios (⚠️ PERMANENTE)
git reset --hard HEAD~1
```

#### Subí a GitHub y Necesito Deshacer (⚠️ PELIGRO)

```bash
# Ve el commit que quieres deshacer
git log --oneline -5

# Crea un NUEVO commit que lo revierte
git revert hash-commit-aqui
# Esto crea un nuevo commit que deshace los cambios

# Sube el revert
git push origin main
```

#### Confirmé con Mensaje Incorrecto

```bash
# Corrige SOLO el último mensaje de commit (antes de subir)
git commit --amend -m "Mensaje corregido aquí"

# Sube el commit corregido
git push origin main
```

#### "Opción Nuclear" - Descarta Todo

```bash
# Descarta TODOS los cambios y vuelve al último commit
git reset --hard HEAD

# Vuelve al último estado subido
git reset --hard origin/main
```

---

## Operaciones con Directorios y Archivos

### Trabajar con Múltiples Archivos

#### Subir un Directorio Completo

```bash
# Copia un directorio al repo
cp -r /ruta/a/mis/apuntes-ctf /home/kali/Desktop/RAG/docs/

# O créalo en el repo
mkdir -p /home/kali/Desktop/RAG/docs/mis-apuntes-ctf

# Prepara todo en ese directorio
git add docs/mis-apuntes-ctf/

# Confirma
git commit -m "docs: Agregar apuntes CTF para OWASP Top 10"

# Sube
git push origin main
```

#### Subir Archivos al Directorio `default/`

El directorio `default/` es para chunks de CTF de ejemplo:

```bash
# Copia chunks CTF a default/
cp -r /ruta/a/ctf-chunks/* /home/kali/Desktop/RAG/default/

# Prepáralo en git
git add default/

# Confirma
git commit -m "docs: Agregar chunks CTF de ejemplo para máquinas X e Y"

# Sube
git push origin main
```

#### Subir Archivos a `src/` (Scripts de Python)

Solo scripts de Python van aquí:

```bash
# Copia nuevo script de Python
cp /ruta/a/mi-script.py /home/kali/Desktop/RAG/src/

# Prepáralo
git add src/mi-script.py

# Confirma
git commit -m "feat: Agregar nuevo script para fuzzing automatizado"

# Actualiza SCRIPTS_INDEX.md para documentarlo
nano SCRIPTS_INDEX.md

# Re-prepara y confirma
git add SCRIPTS_INDEX.md
git commit -m "docs: Documentar nuevo script de fuzzing"

# Sube ambos
git push origin main
```

#### Subir Archivos a `scripts/` (Scripts Bash)

Solo wrappers CLI Bash van aquí:

```bash
# Copia script bash
cp /ruta/a/mi-script.sh /home/kali/Desktop/RAG/scripts/

# Hazlo ejecutable
chmod +x /home/kali/Desktop/RAG/scripts/mi-script.sh

# Prepáralo
git add scripts/mi-script.sh

# Confirma
git commit -m "feat: Agregar wrapper bash para nueva herramienta de fuzzing"

# Actualiza documentación
nano SCRIPTS_INDEX.md

# Confirma actualización de docs
git add SCRIPTS_INDEX.md
git commit -m "docs: Documentar nuevo wrapper bash"

# Sube
git push origin main
```

#### Subir Archivos a `docs/` (Guías Markdown)

Las guías van en subdirectorios organizados:

```bash
# Navega a docs
cd /home/kali/Desktop/RAG/docs

# Crea una nueva guía
nano docs/mi-nueva-guia-ctf.md

# O copia guías existentes
cp /ruta/a/mi-guia.md docs/

# Desde la raíz del repo, prepáralo
git add docs/

# Confirma
git commit -m "docs: Agregar guía para explotación de [tema]"

# Sube
git push origin main
```

### Lista Todo lo que Tienes

```bash
# Ve todos los archivos en el repo
ls -la

# Ve estructura
tree -L 2

# Ve solo archivos modificados
git status

# Cuenta archivos
find . -type f | wc -l

# Ve tamaño del repo
du -sh .
```

### Eliminar Archivos (Si es Necesario)

```bash
# Elimina un archivo y prepara la eliminación
git rm nombre-archivo.md

# Elimina un directorio
git rm -r nombre-directorio/

# Confirma la eliminación
git commit -m "docs: Eliminar guía desactualizada"

# Sube
git push origin main
```

---

## Subir a GitHub (Repositorio Remoto)

### Flujo de Trabajo Empujar-Tirar

#### Sube tus Cambios a GitHub

```bash
# Después de confirmar localmente, sube a rama main
git push origin main

# Verifica que funcionó
git status
# Debe mostrar: "Your branch is up to date with 'origin/main'"
```

#### Descarga Cambios desde GitHub (Si Otros lo Modificaron)

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

#### Maneja Conflictos (Dos Personas Editaron el Mismo Archivo)

```bash
# Intenta descargar
git pull origin main

# Si hay conflicto:
# 1. Abre el archivo conflictivo
nano archivo-conflictivo.md

# 2. Busca estos marcadores:
# <<<<<<< HEAD (tus cambios)
# ======= (divisor)
# >>>>>>> origin/main (sus cambios)

# 3. Edita para mantener lo que quieres, elimina marcadores de conflicto

# 4. Prepara y confirma
git add archivo-conflictivo.md
git commit -m "fix: Resolver conflicto de fusión en [archivo]"

# 5. Sube
git push origin main
```

### Flujo Completo "Una Persona"

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

## Flujo de Vectorización

### ¿Qué es la Vectorización?

Convertir tus archivos markdown en **chunks buscables** para consultarlos después:

```
Archivo Markdown → Dividir en Chunks → Convertir a Vectores → Guardar en Pinecone
```

### Vectorizar un Archivo Único

```bash
# Desde raíz del repo
cd /home/kali/Desktop/RAG

# Vectoriza UN archivo markdown
python3 src/vectorize_canonical_openai.py \
  --file docs/mi-guia.md \
  --namespace guias-ctf

# Verifica que funcionó
echo "¡Vectorización completa! Consultalo después con:"
echo "python3 src/query_canonical_openai.py 'término de búsqueda'"
```

### Vectorizar un Directorio Completo

```bash
# Vectoriza TODOS los archivos en docs/
python3 src/vectorize_canonical_openai.py \
  --directory docs/ \
  --namespace guias-ctf

# Vectoriza el repo completo
python3 src/vectorize_canonical_openai.py \
  --directory . \
  --namespace ctf-todo

# Salida de progreso:
# Processing: docs/guias/inyeccion-sql.md ... ✓
# Processing: docs/guias/ataques-xss.md ... ✓
# Created 45 chunks | Stored in Pinecone
```

### Vectorizar Archivos Nuevos (Después de Agregarlos a Git)

**Flujo de trabajo recomendado:**

```bash
# 1. Agrega nueva guía
nano docs/nueva-guia.md

# 2. Agrégalo a git
git add docs/nueva-guia.md

# 3. Confirma
git commit -m "docs: Agregar nueva guía de explotación"

# 4. Vectoriza el archivo
python3 src/vectorize_canonical_openai.py \
  --file docs/nueva-guia.md \
  --namespace guias-ctf

# 5. Sube a GitHub
git push origin main

# 6. Ahora consulta
python3 src/query_canonical_openai.py "tema de la guía"
```

### Vectorizar la Guía CLI (¡ESTE ARCHIVO!)

```bash
# Vectoriza esta guía
python3 src/vectorize_canonical_openai.py \
  --file GUIA_CLI_CHEATSHEET.md \
  --namespace guia-comandos-cli

# Prueba una consulta
python3 src/query_canonical_openai.py "cómo revertir un commit"

# ¡Debe retornar secciones relevantes de esta guía!
```

### Vectorizar Todo de Una Vez

```bash
# De una vez: confirma + vectoriza + sube
git add .
git commit -m "docs: Actualización mayor de documentación"
python3 src/vectorize_canonical_openai.py --directory . --namespace todo
git push origin main
```

### Vectorizar Múltiples Directorios en Lote

```bash
# Script para vectorizar múltiples partes por separado

# Vectoriza guías
python3 src/vectorize_canonical_openai.py \
  --directory docs/ \
  --namespace guias

# Vectoriza documentación del vectorizer
python3 src/vectorize_canonical_openai.py \
  --directory docs-vectorizer/ \
  --namespace guias-vectorizer

# Vectoriza chunks de ejemplo
python3 src/vectorize_canonical_openai.py \
  --directory default/ \
  --namespace chunks-ejemplo

# Vectoriza guía CLI
python3 src/vectorize_canonical_openai.py \
  --file GUIA_CLI_CHEATSHEET.md \
  --namespace guia-cli
```

---

## Referencia Rápida de Scripts

### Comandos Más Usados

```bash
# Verifica estado de git
git status

# Ve qué cambió
git diff

# Prepara todos los cambios
git add .

# Confirma
git commit -m "msg"

# Sube a GitHub
git push

# Descarga lo último
git pull

# Ve historial
git log --oneline -10

# Vectoriza archivos
python3 src/vectorize_canonical_openai.py --directory docs/ --namespace guias

# Consulta la base de conocimiento
python3 src/query_canonical_openai.py "tu pregunta"

# Envía a Telegram
python3 src/rag_to_telegram.py "tu consulta"
```

### Cheatsheet de Operaciones de Archivos

```bash
# Crear directorio
mkdir -p ruta/a/nuevo/dir

# Copiar archivo
cp origen.md destino.md

# Copiar directorio
cp -r origen/ destino/

# Mover/renombrar
mv nombre-viejo.md nombre-nuevo.md

# Listar archivos
ls -la

# Ver árbol de directorios
tree -L 3

# Eliminar archivo
rm archivo.md

# Eliminar directorio
rm -r directorio/

# Buscar archivos
find . -name "*.md"

# Contar archivos
find . -name "*.md" | wc -l
```

### Atajos Mágicos de Git

Crea en `~/.bashrc` o `~/.zshrc`:

```bash
# Agrega a tu archivo de configuración de shell
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline -10'
alias gd='git diff'
alias gca='git add . && git commit -m'
alias gcap='git add . && git commit -m "$1" && git push'

# Luego usa:
# gs (en lugar de git status)
# gc "mi mensaje" (en lugar de git commit -m)
# gcap "mi mensaje" (¡prepara, confirma y sube en uno!)
```

---

## Escenarios Comunes y Soluciones

### Escenario 1: "Hice Cambios, Quiero Guardarlos"

```bash
git add .
git commit -m "feat: Describir tus cambios"
git push origin main
```

### Escenario 2: "Hice Cambios, Quiero Descartarlos"

```bash
git restore .
# O
git reset --hard HEAD
```

### Escenario 3: "Confirmé Localmente pero Olvidé Subir"

```bash
git log origin/main..HEAD --oneline  # Ve commits no subidos
git push origin main                 # Súbelos
```

### Escenario 4: "Quiero Vectorizar Mi Nueva Guía"

```bash
git add docs/mi-nueva-guia.md
git commit -m "docs: Agregar nueva guía"
python3 src/vectorize_canonical_openai.py --file docs/mi-nueva-guia.md --namespace guias
git push origin main
```

### Escenario 5: "Quiero Consultar Mis Guías Vectorizadas"

```bash
python3 src/query_canonical_openai.py "¿Qué es inyección SQL?"
# ¡Obtiene todas las secciones relevantes de tus guías vectorizadas!
```

### Escenario 6: "Quiero Agregar Chunks CTF a default/"

```bash
cp -r ~/mis-chunks-ctf/* /home/kali/Desktop/RAG/default/
git add default/
git commit -m "docs: Agregar chunks CTF para máquinas X, Y, Z"
python3 src/vectorize_canonical_openai.py --directory default/ --namespace chunks-ctf
git push origin main
```

### Escenario 7: "Subí Algo Incorrecto, Necesito Deshacer"

```bash
git log --oneline -3              # Encuentra el commit incorrecto
git revert hash-commit-incorrecto  # Crea un commit de deshacer
git push origin main               # Sube el deshacer
```

---

## Ambiente y Dependencias

### Verifica Setup de Python

```bash
# Verifica que Python 3 esté instalado
python3 --version

# Verifica paquetes requeridos
python3 -c "import openai, pinecone; print('✓ Dependencias OK')"

# Instala requisitos
python3 -m pip install -r config/requirements.txt

# Verifica venv (si lo usas)
which python3
```

### Verifica Setup de API Keys

```bash
# API de Pinecone
echo $PINECONE_API_KEY

# API de OpenAI
echo $OPENAI_API_KEY

# Si está vacío, configúralo:
export PINECONE_API_KEY="tu-clave"
export OPENAI_API_KEY="tu-clave"

# O usa archivos .env (recomendado):
# Crea config/.env con tus claves
```

### Verifica Configuración de Git

```bash
# Ve tu configuración
git config --list

# Configura info de usuario
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Hazlo global (todos los repos)
git config --global user.name "Tu Nombre"
```

---

## Troubleshooting

### "Git dice que tengo cambios sin confirmar"

```bash
# Ve qué cambió
git status

# Revisa los cambios
git diff

# Prepáralo
git add .

# Confirma
git commit -m "mensaje"
```

### "No puedo subir a GitHub"

```bash
# Verifica conexión
git remote -v

# Intenta descargar primero
git pull origin main

# Luego sube
git push origin main
```

### "Script de Python no se encuentra"

```bash
# Asegúrate estar en raíz del repo
pwd
# Debe ser /home/kali/Desktop/RAG

# Verifica que el archivo exista
ls src/vectorize_canonical_openai.py

# Ejecuta con ruta completa
python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py --help
```

### "La vectorización falla"

```bash
# Verifica API keys
echo $OPENAI_API_KEY
echo $PINECONE_API_KEY

# Verifica dependencias
python3 -m pip list | grep -E "openai|pinecone"

# Verifica formato del archivo
file docs/mi-guia.md  # Debe ser "ASCII text"

# Intenta modo verbose
python3 src/vectorize_canonical_openai.py \
  --file docs/mi-guia.md \
  --namespace test \
  --verbose
```

---

## Consejos Pro

### Consejo 1: Confirma Frecuentemente, Sube Cuando Estés Listo

```bash
# Confirma localmente múltiples veces
git commit -m "Trabajo en progreso"
git commit -m "Agregué sección A"
git commit -m "Corregí bugs en sección B"

# Sube una vez cuando todo esté bien
git push origin main
```

### Consejo 2: Usa Mensajes de Commit Descriptivos

```bash
# Malo
git commit -m "update"

# Bueno
git commit -m "feat: Agregar guía de explotación de inyección SQL con payloads y técnicas de bypass"
```

### Consejo 3: Vectoriza Después de Cada Actualización Mayor

```bash
# ¿Nueva guía? ¡Vectorízala!
# ¿Guía antigua actualizada? ¡Re-vectoriza!
# ¿Ejemplos agregados? ¡Vectoriza de nuevo!

# Consulta para verificar
python3 src/query_canonical_openai.py "tu tema"
```

### Consejo 4: Usa Aliases para Acelerar

```bash
alias vc='python3 src/vectorize_canonical_openai.py'
alias qc='python3 src/query_canonical_openai.py'

# Luego:
vc --directory docs/ --namespace guias
qc "término de búsqueda"
```

### Consejo 5: Siempre Descarga Antes de Trabajar

```bash
# Inicio de sesión
git pull origin main

# Trabajo
# ... edita archivos ...

# Final de sesión
git push origin main
```

---

## Tarjeta de Referencia Rápida

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
| **Vectorizar Archivo** | `python3 src/vectorize_canonical_openai.py --file docs/archivo.md --namespace ns` |
| **Vectorizar Directorio** | `python3 src/vectorize_canonical_openai.py --directory docs/ --namespace ns` |
| **Consultar KB** | `python3 src/query_canonical_openai.py "búsqueda"` |
| **Copiar Directorio** | `cp -r origen/ destino/` |
| **Eliminar Archivo** | `git rm archivo.md` |
| **Revertir Commit** | `git revert hash-commit` |

---

## Lista de Verificación Final Antes de Usar el Repositorio

```bash
# ✓ Instalé dependencias
python3 -m pip install -r config/requirements.txt

# ✓ Git configurado
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# ✓ Puedo ver estado
git status

# ✓ Puedo ver historial
git log --oneline -5

# ✓ Tengo API keys
echo $OPENAI_API_KEY
echo $PINECONE_API_KEY

# ✓ Puedo ejecutar vectorizer
python3 src/vectorize_canonical_openai.py --help

# ✓ Puedo hacer consultas
python3 src/query_canonical_openai.py --help

# ¡ESTÁS LISTO PARA EMPEZAR! 🚀
```

---

**Última Actualización**: Febrero 2026  
**Repositorio**: https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval  
**Estado**: Listo para Producción

