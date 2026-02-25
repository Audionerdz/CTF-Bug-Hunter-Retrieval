---
chunk_id: technique::linux::git::ignore-default-workflow::001
domain: linux
chunk_type: technique
---

# Gestión de flujos de trabajo con directorios ignorados en Git

El archivo `.gitignore` mantiene `default/*` ignorado. Esto garantiza que tu trabajo local nunca se suba automáticamente, permitiendo publicaciones selectivas mediante el uso de fuerza.



### 1. Flujo de Trabajo en Directorio Protegido
Trabajas normalmente dentro de la carpeta sin que Git rastree los cambios:

```bash
# Trabajas normalmente en default/
mkdir default/mi-proyecto
echo "contenido" > default/mi-proyecto/chunk.md

# Git ignora todo lo que agregues en default/
git status
# No aparece nada de default/

```

### 2. Publicación Selectiva

Para subir un archivo específico que está siendo ignorado, se utiliza el flag `-f` (force):

```bash
# Solo si quieres pushear algo específico:
git add -f default/mi-proyecto/chunk.md
git commit -m "feat: add my chunk"
git push

```

### 3. Recuperar Estado Minimal

Si deseas limpiar el directorio y volver al estado original del repositorio:

```bash
# Si quieres volver al estado minimal del repo:
git checkout main -- default/

```

---
