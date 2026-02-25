---
chunk_id: github::concepts::branches-explained::001
domain: github
chunk_type: technique
---

# Cómo Funcionan las Ramas (Explicación Simple)

## ¿Qué es una Rama? Analogía Simple

Imagina que tu proyecto es un árbol:
- **El tronco principal = main branch** (la versión "oficial" y estable)
- **Las ramas = feature branches** (donde experimentas sin afectar el tronco)

```
                    feature/nueva-guia
                    /
                   /
main  ----●----●----●----●----●
               \
                \
              hotfix/bug-fix
```

## Las 2 Ramas Principales

### Rama main (Producción)
```bash
# Esta es tu rama principal, la "oficial"
# Aquí está el código estable y funcionando
# NO experimentes directamente aquí si es importante
```

### Feature Branch (Experimentación)
```bash
# Creas una rama nueva para un cambio
# Trabajas sin afectar main
# Cuando termines, fusionas a main
```

## Ventajas de Usar Ramas

1. **Seguridad** - No rompes main mientras trabajas
2. **Orden** - Cada rama para un propósito específico
3. **Revisión** - Puedes revisar cambios antes de fusionar
4. **Paralelo** - Múltiples desarrolladores trabajan sin conflicto

## Analogía con la Vida Real

```
Sin ramas (PELIGRO):
Tu código en vivo en sitio web
↓
Haces cambios directamente
↓
Si algo falla, todo se cae

Con ramas (SEGURO):
Código en vivo en rama main
↓
Creas rama feature/cambios
↓
Trabajas sin afectar sitio en vivo
↓
Cuando estés seguro, fusionas a main
↓
Ahora tu cambio es "en vivo"
```

## Comandos Básicos de Ramas

### Ver tus ramas
```bash
# Ver ramas locales
git branch

# Ver ramas locales + remotas
git branch -a

# Ejemplo de salida:
#   main
# * feature/mi-cambio
#   remotes/origin/main
```

### Crear una rama nueva
```bash
# Opción 1: Crear y cambiar en un comando
git checkout -b feature/mi-nueva-rama

# Opción 2: Crear sin cambiar
git branch feature/mi-nueva-rama

# Luego cambiar
git checkout feature/mi-nueva-rama
```

### Cambiar entre ramas
```bash
# Cambiar a main
git checkout main

# Cambiar a otra rama
git checkout feature/mi-cambio

# Versión moderna (igual resultado)
git switch main
git switch feature/mi-cambio
```

### Fusionar una rama a main
```bash
# 1. Cambiate a main
git checkout main

# 2. Fusiona la rama
git merge feature/mi-cambio

# 3. Si quieres, borra la rama (opcional)
git branch -d feature/mi-cambio
```

### Subir rama a GitHub
```bash
# Sube la rama a GitHub
git push origin feature/mi-cambio

# La próxima vez
git push

# O crea Pull Request en GitHub para revisar
```

## Ciclo Típico con Ramas

```bash
# 1. Estás en main
git checkout main

# 2. Descargas lo último
git pull origin main

# 3. Creas rama nueva
git checkout -b feature/nueva-funcionalidad

# 4. Haces cambios
nano docs/archivo.md

# 5. Commitseas cambios
git add .
git commit -m "feat: Agregar funcionalidad"

# 6. Subes rama a GitHub
git push origin feature/nueva-funcionalidad

# 7. En GitHub, creas Pull Request
# (o fusionas manualmente)

# 8. De vuelta en terminal
git checkout main
git merge feature/nueva-funcionalidad
git push origin main

# 9. Boras rama local (opcional)
git branch -d feature/nueva-funcionalidad
```

## Nombres de Ramas: Convención

```bash
# Buenos nombres (descriptivos):
feature/nueva-guia
feature/sql-injection-guide
hotfix/corregir-typo
bugfix/error-vectorizacion
docs/actualizar-readme
refactor/mejorar-estructur

# Malos nombres (no describen nada):
rama1
cambios
test
prueba
asdadasd
```

## Resumen Rápido

| Comando | Qué hace |
|---------|----------|
| `git branch` | Ver ramas |
| `git checkout -b nombre` | Crear rama y cambiar |
| `git checkout main` | Cambiar a main |
| `git merge nombre` | Fusionar rama a main |
| `git push origin nombre` | Subir rama a GitHub |
| `git branch -d nombre` | Borrar rama |
