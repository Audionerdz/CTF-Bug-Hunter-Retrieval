---
chunk_id: github::security::privacy-setup::001
domain: github
chunk_type: guide
category: security
confidence: high
reuse_level: universal
tags: [github, privacy, security, settings, public-private, permissions, access-control]
source_file: github-privacy-security-setup.md
---

# Privacidad y Seguridad en GitHub: Guía Completa

## Conceptos Básicos

### Repositorio Público (Public)
```
- Visible para todo el mundo
- Cualquiera puede verlo
- Solo TÚ puedes editar
- Gratis
- Ideal para: proyectos open-source, portfolios
```

### Repositorio Privado (Private)
```
- Solo visible para ti y personas que invites
- Nadie más lo ve
- Invitados pueden tener permisos de lectura/escritura
- Gratis en GitHub
- Ideal para: proyectos personales, secretos, trabajo
```

---

## Crear Repositorio con Privacidad Desde el Inicio

### Opción 1: Desde GitHub.com

1. **Ir a https://github.com/new**

2. **Llenar formulario:**
   - Repository name: `mi-proyecto`
   - Description: (opcional) "Descripción"
   - **Escoge: Public o Private**
   - Initialize with: (sin marcar)

3. **Click "Create repository"**

### Opción 2: Desde Terminal (Recomendado)

```bash
# 1. Crear carpeta
cd /home/kali/Desktop
mkdir mi-proyecto
cd mi-proyecto

# 2. Inicializar git
git init

# 3. Crear archivo
echo "# Mi Proyecto" > README.md

# 4. Commit
git add .
git commit -m "Initial commit"

# 5. Ir a GitHub y crear repo PRIVATE manualmente

# 6. Conectar desde terminal
git branch -M main
git remote add origin https://github.com/TU_USUARIO/mi-proyecto.git
git push -u origin main
```

---

## Cambiar Privacidad de Repositorio Existente

### De Público a Privado

1. Ir a tu repo en GitHub
2. Click **Settings** (esquina superior derecha)
3. Bajar a **"Danger Zone"**
4. Click **"Change repository visibility"**
5. Seleccionar **"Make private"**
6. Confirmar escribiendo nombre del repo
7. Click **"I understand, change repository visibility"**

### De Privado a Público

1. Ir a tu repo en GitHub
2. Click **Settings**
3. Bajar a **"Danger Zone"**
4. Click **"Change repository visibility"**
5. Seleccionar **"Make public"**
6. Confirmar
7. Click **"I understand, change repository visibility"**

⚠️ **ADVERTENCIA**: Al hacerlo público, TODO lo que esté en el repo será visible

---

## Gestionar Acceso (Invitar Colaboradores)

### Agregar Colaborador a Repositorio Privado

1. En tu repo → Click **Settings**
2. En menú izquierdo → **"Collaborators"**
3. Click **"Add people"**
4. Buscar por username: `audionerdz`
5. Seleccionar nivel de acceso:
   - **Pull**: Solo lectura (ver código)
   - **Triage**: Lectura + gestión de issues
   - **Push**: Lectura + escritura
   - **Maintain**: Acceso total (casi admin)
   - **Admin**: Control total

6. Click **"Add audionerdz to this repository"**

### Remover Colaborador

1. Settings → Collaborators
2. Buscar el usuario
3. Click el ícono de basura (🗑️)
4. Confirmar "Remove"

---

## Secretos y API Keys: NUNCA Subir

### ❌ NUNCA hagas esto:

```bash
# Malo - API keys en el código
export OPENAI_API_KEY="sk-12345abcde"
export PINECONE_API_KEY="abc123def"

# Malo - Contraseñas en archivos
password = "mySecurePassword123"
token = "github_pat_11A2B3C4D"
```

### ✅ SIEMPRE haz esto:

```bash
# 1. Crear archivo .env (NO subir a git)
echo "OPENAI_API_KEY=sk-12345abcde" > .env
echo "PINECONE_API_KEY=abc123def" >> .env

# 2. Agregar a .gitignore
echo ".env" >> .gitignore

# 3. En tu código, leer desde .env
# En Python:
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# En Bash:
source .env
echo $OPENAI_API_KEY
```

### Si Accidentalmente Subiste Secretos

⚠️ **ACCIÓN INMEDIATA**:

```bash
# 1. Genera un token nuevo en tu API provider
# 2. El token viejo está comprometido, revocarlo

# 3. Opción A: Borrar archivo del historio (complejo)
# 4. Opción B: Hacer repo privado + cambiar todos los tokens
# 5. Opción C: Usar git-secrets para prevenir

# Instalar git-secrets
brew install git-secrets  # macOS
apt-get install git-secrets  # Linux

# Configurar
git secrets --install
git secrets --register-aws
```

---

## Configuración de Privacidad Recomendada

### Para Proyecto Personal (Privado)

```bash
# 1. Crear como PRIVATE
# 2. Solo tú tienes acceso
# 3. .gitignore incluye: .env, .secrets, *.key, *.pem
# 4. Archivo .env NO está en git
# 5. Cambiar tokens si expusiste alguno
```

### Para Proyecto Open-Source (Público)

```bash
# 1. Crear como PUBLIC
# 2. .gitignore COMPLETO (node_modules, .env, etc)
# 3. README.md con instrucciones
# 4. LICENSE file (MIT es buena opción)
# 5. Sin API keys, contraseñas, o secretos NUNCA
# 6. Documentación clara
# 7. CONTRIBUTING.md si quieres colaboradores
```

### Para Equipo (Privado con Colaboradores)

```bash
# 1. Crear como PRIVATE
# 2. Invitar colaboradores con permisos "Push"
# 3. Configurar branch protection (opcional):
#    - Require reviews before merge
#    - Require status checks
# 4. .env con valores de desarrollo (ejemplo)
# 5. Documentación clara
```

---

## Archivo .gitignore: La Mejor Defensa

### .gitignore Para RAG Repo

```bash
cat > /home/kali/Desktop/RAG/.gitignore << 'IGNORE'
# Secrets y configuración
.env
.env.local
.env.*.local
*.key
*.pem
secrets.json
credentials.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Sistema
.DS_Store
*.tmp
IGNORE

cat /home/kali/Desktop/RAG/.gitignore
```

### .gitignore Para Proyecto Nuevo

```bash
cat > /home/kali/Desktop/mi-proyecto/.gitignore << 'IGNORE'
# Secretos
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
config/secrets.yaml

# Python
__pycache__/
*.py[cod]
.Python
venv/
env/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log
yarn-error.log

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Logs
*.log
logs/

# Datos
*.db
*.sqlite
*.tmp
IGNORE

cat /home/kali/Desktop/mi-proyecto/.gitignore
```

---

## Checklist de Privacidad y Seguridad

### ✅ Crear Repositorio Seguro

```bash
✅ Decidir: ¿Público o Privado?
✅ Crear repo en GitHub
✅ Clonar y configurar .gitignore
✅ Agregar .env.example (SIN valores reales)
✅ Documentar cómo configurar .env
✅ Commit inicial
✅ Verificar: git status muestra .env como ignorado
✅ Push a GitHub
✅ Verificar en GitHub que .env NO aparece
```

### ✅ Antes de Cada Push

```bash
✅ git status → ¿Aparece .env o secretos?
✅ NO debe haber archivos sensibles
✅ git diff → Revisar cambios
✅ Verificar que solo cambias lo que quisiste
```

### ✅ Para Repos Públicos

```bash
✅ README.md con instrucciones
✅ LICENSE file
✅ .gitignore hermético
✅ Sin API keys, tokens, contraseñas
✅ Sin data sensible
✅ Sin dependencias innecesarias
```

### ✅ Para Repos Privados

```bash
✅ Solo TÚ puedes acceder
✅ .env configurado localmente
✅ Collaboradores invitados si necesario
✅ Permisos ajustados
✅ Cambios de token si fue expuesto
```

---

## Casos Reales

### RAG Repo (Público)

```bash
# Tu RAG es público porque es educational
# NUNCA incluyas:
❌ OPENAI_API_KEY
❌ PINECONE_API_KEY
❌ TELEGRAM_BOT_TOKEN
❌ Archivos .env

# Sí incluye:
✅ .env.example (template sin valores)
✅ Instrucciones: "Copiar .env.example a .env y completar"
✅ README con setup
```

### Proyecto Nuevo (Privado)

```bash
# Tu proyecto nuevo es privado
# Puedes tener .env.example CON valores de desarrollo
# Pero NUNCA valores de producción

# Ejemplos seguros:
OPENAI_API_KEY=test-key-for-development
DATABASE_URL=sqlite:///dev.db
DEBUG=true

# NUNCA production keys:
OPENAI_API_KEY=sk-PRODUCCION-REAL-KEY
DATABASE_URL=postgresql://prod-database
```

---

## Comandos Útiles para Verificar

```bash
# Ver qué archivos van a git
git ls-files

# Ver archivos ignorados
git status --ignored

# Verificar que .env no está
git status | grep .env
# Debería estar vacío

# Ver .gitignore
cat .gitignore

# Simular qué se subiría
git diff --cached --name-only
```

---

## Resumen Rápido

| Escenario | Privacidad | .gitignore | API Keys | Colaboradores |
|-----------|-----------|-----------|----------|---------------|
| **RAG Repo** | Public | Hermético | En .env.example | Ninguno |
| **Proyecto Personal** | Private | Hermético | En .env (no subido) | Ninguno |
| **Proyecto en Equipo** | Private | Hermético | En .env.example | Invitados con permisos |
| **Open-Source** | Public | Muy hermético | NUNCA | Community |

