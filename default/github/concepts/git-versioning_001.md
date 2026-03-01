---
chunk_id: github::concepts::git-versioning::001
domain: github
chunk_type: technique
---

# Versionado en Git: Guía Completa

## ¿Qué es Versionado?

Es marcar puntos específicos en tu proyecto con un número de versión (v1.0.0, v2.1.3, etc.).

```
Tu proyecto evoluciona:
v1.0.0 → v1.1.0 → v1.2.0 → v2.0.0
(release) (feature) (fix)   (major change)
```

## Versionado Semántico (Semantic Versioning)

La mayoría de proyectos usa: **MAJOR.MINOR.PATCH**

```
v2.1.3
│ │ └─ PATCH (2.1.2 → 2.1.3) - Correcciones de bugs
│ └─── MINOR (2.0.0 → 2.1.0) - Nuevas características
└───── MAJOR (1.0.0 → 2.0.0) - Cambios incompatibles

Ejemplos:
v1.0.0 - Primera versión estable
v1.1.0 - Agregaste features pero compatible
v1.1.1 - Corregiste un bug
v2.0.0 - Cambios grandes, puede romper compatibilidad
```

## Crear una Versión (Tag)

### Opción 1: Tag Simple (Lightweight)

```bash
# Crear tag en commit actual
git tag v1.0.0

# Subir tag a GitHub
git push origin v1.0.0

# Ver tags
git tag
# Resultado:
# v1.0.0
# v1.0.1
```

### Opción 2: Tag Anotado (Recomendado)

```bash
# Crear tag con descripción
git tag -a v1.0.0 -m "Primera versión estable del proyecto"

# Ver información del tag
git show v1.0.0

# Subir tag
git push origin v1.0.0
```

## Flujo de Versionado Completo

### Escenario: Lanzar una Nueva Versión

```bash
# 1. Estar en main y actualizado
cd /home/kali/Desktop/tu-proyecto
git checkout main
git pull origin main

# 2. Hacer commits con cambios
git add .
git commit -m "feat: Agregar nueva característica"

# 3. Decidir qué versión va
# Ejemplo: Era v1.0.0, agregaste feature → v1.1.0

# 4. Crear tag
git tag -a v1.1.0 -m "Release v1.1.0: Agregar nueva característica"

# 5. Subir cambios + tag a GitHub
git push origin main
git push origin v1.1.0

# 6. En GitHub aparecerá como "Release"
```

## Workflow Recomendado: Release Branch

### Crear rama de release

```bash
# 1. De develop, crear rama release
git checkout develop
git checkout -b release/v1.1.0

# 2. Arreglar bugs menores de versión
# ... cambios ...
git add .
git commit -m "fix: Arreglar bug en v1.1.0"

# 3. Crear tag
git tag -a v1.1.0 -m "Release v1.1.0: Description"

# 4. Fusionar a main
git checkout main
git merge release/v1.1.0

# 5. Fusionar de vuelta a develop
git checkout develop
git merge release/v1.1.0

# 6. Subir todo
git push origin main
git push origin develop
git push origin v1.1.0

# 7. Borrar rama de release
git branch -d release/v1.1.0
```

## Casos de Uso: Cuándo Versionar

### v1.0.0 - Primera Versión Estable
```bash
# Tu proyecto está listo para uso público
git tag -a v1.0.0 -m "Primera versión estable"
git push origin v1.0.0
```

### v1.1.0 - Agregaste Características
```bash
# Hiciste feature/nueva-funcionalidad
# Fue a develop → main
# Ahora estás listo para release

git tag -a v1.1.0 -m "Release: Agregar soporte para X"
git push origin v1.1.0
```

### v1.1.1 - Corregiste Un Bug
```bash
# Encontraste un bug en v1.1.0
# Lo arreglaste rápido

git tag -a v1.1.1 -m "Hotfix: Corregir error de parsing"
git push origin v1.1.1
```

### v2.0.0 - Cambios Grandes
```bash
# Refactorizaste todo, API cambió
# NO es compatible con v1.x

git tag -a v2.0.0 -m "Major release: Rewrite core engine"
git push origin v2.0.0
```

## Ver Historial de Versiones

```bash
# Ver todos los tags
git tag

# Ver tags con información
git tag -l -n

# Ver commits para cada tag
git log --oneline --graph --decorate --all

# Buscar commits de una versión
git log v1.0.0..v1.1.0 --oneline
# Muestra commits entre v1.0.0 y v1.1.0
```

## Crear Releases en GitHub

### Desde Terminal

```bash
# Crear tag
git tag -a v1.0.0 -m "Description"

# Subir
git push origin v1.0.0

# GitHub detecta el tag automáticamente
# Aparecerá como "Release" en pestaña Releases
```

### Desde GitHub Web

1. Ir a tu repo → **Releases**
2. Click **"Create a new release"**
3. Escoge o crea un tag: `v1.0.0`
4. Título: "Version 1.0.0"
5. Descripción: cambios importantes
6. Click **"Publish release"**

## Descargar Versión Específica

### Alguien quiere tu versión v1.0.0

```bash
# Opción 1: Clonar rama específica
git clone --branch v1.0.0 https://github.com/usuario/proyecto.git

# Opción 2: Descargar ZIP desde GitHub Releases
# En GitHub → Releases → v1.0.0 → Download ZIP
```

## Navegar a Versiones Anteriores

```bash
# Ver qué versiones tienes
git tag

# Ir a v1.0.0 (solo lectura)
git checkout v1.0.0
# Ahora ves el código de esa versión

# Crear rama desde tag (para trabajar)
git checkout -b hotfix/v1.0.0-fix v1.0.0

# Volver a main
git checkout main
```

## Casos Reales: RAG y Proyecto Nuevo

### RAG Repo (Versionado Simple)

```bash
# Tu RAG original
git tag -a v1.0.0 -m "Initial CTF RAG system"
git push origin v1.0.0

# Agregaste 50 guías nuevas
git tag -a v1.1.0 -m "Add 50 exploitation guides"
git push origin v1.1.0

# Mejoraste vectorización
git tag -a v1.2.0 -m "Improve vectorization performance"
git push origin v1.2.0
```

### Proyecto Nuevo (Versionado Profesional)

```bash
# Proyecto inicial
git tag -a v0.1.0 -m "Initial alpha"
git push origin v0.1.0

# Primeras features
git tag -a v0.2.0 -m "Add core modules"
git push origin v0.2.0

# Release candidato
git tag -a v1.0.0-rc1 -m "Release candidate 1"
git push origin v1.0.0-rc1

# Versión estable
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0

# Nuevas features
git tag -a v1.1.0 -m "Add new features"
git push origin v1.1.0

# Fix urgente
git tag -a v1.1.1 -m "Security patch"
git push origin v1.1.1
```

## Convenciones de Nombres

```bash
# Buenas versiones:
v1.0.0       ← Estándar
v1.0.0-beta  ← Versión beta
v1.0.0-rc1   ← Release candidate
v2.0.0       ← Major release
v1.1.0       ← Minor release
v1.0.1       ← Patch

# Evita:
version1
1.0
release
latest
v1.0.0.0    ← Demasiados números
```

## Resumen: Comandos Clave

```bash
# Crear tag
git tag -a v1.0.0 -m "Description"

# Ver tags
git tag

# Subir tag a GitHub
git push origin v1.0.0

# Subir todos los tags
git push origin --tags

# Borrar tag local
git tag -d v1.0.0

# Borrar tag en GitHub
git push origin --delete v1.0.0

# Ir a versión específica
git checkout v1.0.0

# Ver cambios entre versiones
git log v1.0.0..v1.1.0
```

## Checklist: Primera Versión

```bash
✅ Commit último cambio
✅ Verificar que main está limpia (git status)
✅ Crear tag: git tag -a v1.0.0 -m "First release"
✅ Subir código: git push origin main
✅ Subir tag: git push origin v1.0.0
✅ Verificar en GitHub → Releases
✅ Ver changelog (git log v1.0.0 --oneline)
```
