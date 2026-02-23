---
chunk_id: github::workflow::branches-rag-new-project::001
domain: github
chunk_type: technique
---

# Cómo Usar Ramas con RAG y Proyecto Nuevo

## Escenario 1: Trabajar con Ramas en RAG Repo

### Workflow Típico: Agregar Nueva Guía en RAG

```bash
# 1. Asegúrate estar en la carpeta correcta
cd /home/kali/Desktop/RAG

# 2. Descargas lo último de main
git pull origin main

# 3. Creas rama para tu nueva guía
git checkout -b feature/sql-injection-guide

# 4. Haces cambios en la rama
nano docs/sql-injection.md

# 5. Verificas cambios
git status
git diff

# 6. Commit en la rama
git add docs/sql-injection.md
git commit -m "feat: Add SQL injection exploitation guide"

# 7. Subes rama a GitHub
git push origin feature/sql-injection-guide

# 8. En GitHub, haces Pull Request o fusionas manualmente:
git checkout main
git merge feature/sql-injection-guide
git push origin main

# 9. Vectoriza el nuevo contenido
python3 src/vectorize_canonical_openai.py ./docs/sql-injection.md

# 10. Borra rama local (opcional)
git branch -d feature/sql-injection-guide
```

### Beneficios en RAG

- **main siempre estable** - La rama principal funciona perfectamente
- **Experimenta sin riesgo** - Creas feature branches para probar
- **Vectorización segura** - Vectorizas solo cuando estés seguro
- **Historial limpio** - Cada rama representa un cambio lógico
- **Fácil deshacer** - Si algo falla, boras la rama

### Ramas Típicas en RAG

```bash
# Nuevas guías
feature/xss-attacks-guide
feature/injection-payloads
feature/privilege-escalation

# Mejoras
feature/improve-documentation
feature/add-examples

# Correcciones
hotfix/fix-typo-in-readme
bugfix/wrong-code-example

# Refactoring
refactor/reorganize-docs
```

---

## Escenario 2: Trabajar con Ramas en Proyecto Nuevo

### Workflow Típico: Nuevo Proyecto desde Cero

```bash
# 1. Crear carpeta desde Desktop
cd /home/kali/Desktop
mkdir mi-proyecto
cd mi-proyecto

# 2. Inicializar git
git init

# 3. Crear rama develop (opcional pero bueno)
git checkout -b develop

# 4. Crear estructura inicial
mkdir -p src docs tests
echo "# Mi Proyecto" > README.md
echo "*.pyc" > .gitignore

# 5. Primer commit en develop
git add .
git commit -m "Initial commit: Create project structure"

# 6. Crear rama de feature
git checkout -b feature/core-functionality

# 7. Haces cambios
echo "def hello():" > src/main.py

# 8. Commit
git add .
git commit -m "feat: Add core functionality"

# 9. Vuelves a develop y fusionas
git checkout develop
git merge feature/core-functionality

# 10. Conectas con GitHub
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mi-proyecto.git
git push -u origin develop
git push -u origin main

# 11. Crear más features
git checkout -b feature/documentation
# ... haces cambios ...
git add .
git commit -m "docs: Add initial documentation"
git checkout develop
git merge feature/documentation
git push origin develop
```

### Estructura de Ramas en Proyecto Nuevo

```
main (Rama de producción - solo cambios probados)
 ↓
develop (Rama de desarrollo - integración)
 ↓
feature/feature-1 (Tu trabajo)
feature/feature-2 (Otro desarrollo)
hotfix/bug-fix (Para errores urgentes)
```

---

## Comparación: RAG vs Proyecto Nuevo

### RAG Repo - Estructura Simple

```bash
# RAG es un repo establecido
# Generalmente trabajas directamente en main o creas features

Opción A: Cambio pequeño → directo a main
cd /home/kali/Desktop/RAG
git pull
git add .
git commit -m "docs: pequeño cambio"
git push

Opción B: Cambio grande → feature branch
git checkout -b feature/major-update
# ... trabajo ...
git push origin feature/major-update
# Fusionar cuando esté lista
```

### Proyecto Nuevo - Estructura Profesional

```bash
# Proyecto nuevo aprovecha ramas para estructura

main          ← Código en "producción"
develop       ← Integración de features
feature/*     ← Tu trabajo actual
hotfix/*      ← Arreglos urgentes

Flujo:
feature → develop → main (cuando esté listo para release)
```

---

## Caso Práctico: RAG con Ramas

### Quiero agregar una nueva guía sin afectar RAG

```bash
# 1. Entrar a RAG
cd /home/kali/Desktop/RAG
git pull

# 2. Crear rama
git checkout -b feature/buffer-overflow-guide

# 3. Crear guía
mkdir -p docs/exploitation
cat > docs/exploitation/buffer-overflow.md << 'DOC'
# Buffer Overflow Exploitation

## Conceptos...
DOC

# 4. Commit
git add docs/exploitation/buffer-overflow.md
git commit -m "feat: Add buffer overflow guide with examples"

# 5. Subir rama
git push origin feature/buffer-overflow-guide

# 6. Cuando estés seguro, fusionar
git checkout main
git pull origin main
git merge feature/buffer-overflow-guide
git push origin main

# 7. Vectorizar la guía
python3 src/vectorize_canonical_openai.py ./docs/exploitation/buffer-overflow.md

# 8. Borrar rama
git branch -d feature/buffer-overflow-guide
git push origin --delete feature/buffer-overflow-guide
```

---

## Caso Práctico: Proyecto Nuevo con Ramas

### Crear proyecto con estructura profesional

```bash
# 1. Crear desde Desktop
cd /home/kali/Desktop
mkdir mi-framework
cd mi-framework

# 2. Init y crear develop
git init
git checkout -b develop

# 3. Estructura base
mkdir -p src tests docs
echo "# Mi Framework" > README.md

# 4. Primer commit
git add .
git commit -m "Initial commit"

# 5. Crear features en paralelo
git checkout -b feature/core-module
echo "class Framework:" > src/core.py
git add .
git commit -m "feat: Add core module"
git push origin feature/core-module

# 6. Otra feature
git checkout develop
git checkout -b feature/utilities
echo "def helper():" > src/utils.py
git add .
git commit -m "feat: Add utility functions"
git push origin feature/utilities

# 7. Fusionar todo a develop
git checkout develop
git merge feature/core-module
git merge feature/utilities
git push origin develop

# 8. Conectar GitHub
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mi-framework.git
git push -u origin develop
git push -u origin main
```

---

## Resumen: Ramas en RAG vs Nuevo Proyecto

### En RAG
- ✅ Main es estable
- ✅ Creas features para cambios grandes
- ✅ Vectorizas en main
- ✅ Cambios pequeños pueden ir directo a main

### En Proyecto Nuevo
- ✅ main = Release oficial
- ✅ develop = Integración
- ✅ features = Tu trabajo
- ✅ Todo pasa por develop antes de main

---

## Pro Tips

```bash
# Ver rama actual
git branch

# Crear rama y cambiar en uno
git checkout -b feature/nombre

# Borrar rama local
git branch -d nombre

# Borrar rama en GitHub
git push origin --delete nombre

# Fusionar sin crear commit
git merge --squash feature/nombre

# Ver commits no mergeados
git log main..feature/nombre
```
