---
chunk_id: github::workflow::before-changes::001
domain: github
chunk_type: technique
---

# Antes de Hacer Cambios: Qué Tengo que Hacer

## Paso 1: SIEMPRE Descargar Lo Último de GitHub

```bash
# Antes de empezar a trabajar, descarga cambios
git pull origin main

# Esto evita conflictos y asegura que tienes lo más reciente
```

## Paso 2: Verifica el Estado de Tu Repo

```bash
# Ver qué archivos tienes modificados
git status

# Ver detalles de los cambios
git diff
```

## Paso 3: Ahora Tienes OPCIONES Como Developer

### Opción 1: Trabajar en la Rama Principal (main) - SIMPLE

```bash
# Estás en main, haz cambios directamente
nano docs/mi-archivo.md

# Verifica cambios
git status
git diff

# Prepara cambios
git add .

# Commit
git commit -m "feat: Agregar nueva guía"

# Sube a GitHub
git push origin main
```

**Cuándo usar:** Cuando trabajas solo o cambios pequeños

---

### Opción 2: Crear una Rama Nueva - PROFESIONAL

```bash
# Crea una rama nueva para tu feature
git checkout -b feature/mi-nueva-guia

# Haz tus cambios
nano docs/mi-guia.md

# Prepara y commit
git add .
git commit -m "feat: Nueva guía de explotación"

# Sube la rama
git push origin feature/mi-nueva-guia

# Después crea un Pull Request en GitHub para revisar
# O fusiona manualmente:
# git checkout main
# git merge feature/mi-nueva-guia
# git push origin main
```

**Cuándo usar:** Cambios grandes, equipo de desarrolladores, quieres revisar antes

---

### Opción 3: Trabajar Localmente Primero - SEGURO

```bash
# Haz múltiples commits locales sin subir
git add archivo1.md
git commit -m "feat: Sección 1"

git add archivo2.md
git commit -m "feat: Sección 2"

git add archivo3.md
git commit -m "feat: Sección 3"

# Ve tu historial local
git log --oneline -5

# Cuando estés listo, sube todo junto
git push origin main
```

**Cuándo usar:** Quieres trabajar seguro sin afectar GitHub

---

## Checklist: Antes de Hacer Cambios

```bash
✅ Paso 1: Entrar a la carpeta correcta
   cd /home/kali/Desktop/RAG

✅ Paso 2: Descargar lo más reciente
   git pull origin main

✅ Paso 3: Verificar estado
   git status

✅ Paso 4: Ver cambios pendientes (si los hay)
   git diff

✅ Paso 5: AHORA SÍ hacer cambios
   nano docs/mi-archivo.md

✅ Paso 6: Preparar cambios
   git add .

✅ Paso 7: Confirmar con mensaje claro
   git commit -m "feat/fix/docs: Descripción"

✅ Paso 8: Subir a GitHub
   git push origin main

✅ Paso 9 (Opcional): Vectorizar contenido nuevo
   python3 src/vectorize_canonical_openai.py ./docs/
```

---

## Resumen Rápido: 3 Escenarios

### Escenario 1: Cambio Rápido
```bash
cd /home/kali/Desktop/RAG
git pull
nano archivo.md
git add .
git commit -m "fix: Corrección rápida"
git push origin main
```

### Escenario 2: Feature Nueva Completa
```bash
cd /home/kali/Desktop/RAG
git pull
git checkout -b feature/mi-feature
# ... haz cambios ...
git add .
git commit -m "feat: Nueva característica"
git push origin feature/mi-feature
# Crea Pull Request en GitHub
```

### Escenario 3: Múltiples Cambios Relacionados
```bash
cd /home/kali/Desktop/RAG
git pull
# Cambio 1
git add archivo1.md
git commit -m "docs: Parte 1"
# Cambio 2
git add archivo2.md
git commit -m "docs: Parte 2"
# Cambio 3
git add archivo3.md
git commit -m "docs: Parte 3"
# Sube todo
git push origin main
```

---

## Tips Como Developer

- 🔍 **Siempre hace `git pull` primero** - Evita conflictos
- 📝 **Mensajes de commit claros** - Usa `feat:`, `fix:`, `docs:`
- 🔀 **Usa ramas para cambios grandes** - No afecta main
- ✅ **Commit frecuente** - Cambios pequeños, fáciles de revertir
- 🚀 **Push cuando estés seguro** - Una vez pusheado es público
- 🧠 **Vectoriza después de cambios importantes** - Mantén la base de conocimiento actualizada
