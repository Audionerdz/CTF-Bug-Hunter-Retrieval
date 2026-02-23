---
chunk_id: github::setup::create-new-repo::001
domain: github
chunk_type: technique
---

# Cómo Crear un Repositorio Nuevo desde /home/kali/Desktop

## Paso 1: Crear la Carpeta del Nuevo Repo

```bash
# Desde /home/kali/Desktop crea tu carpeta
cd /home/kali/Desktop

# Crea la carpeta de tu nuevo proyecto
mkdir mi-nuevo-repo

# Entra a la carpeta
cd mi-nuevo-repo

# Verifica que estás dentro
pwd
# Deberías ver: /home/kali/Desktop/mi-nuevo-repo
```

## Paso 2: Inicializar Git Localmente

```bash
# Dentro de tu carpeta, inicializa git
git init

# Configura tu usuario (si no está configurado globalmente)
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Verifica que git está inicializado
git status
# Deberías ver: "On branch master" o "On branch main"
```

## Paso 3: Crear Archivos Iniciales (Opcional pero Recomendado)

```bash
# Crea un README
echo "# Mi Nuevo Repo" > README.md

# Crea un .gitignore para excluir archivos
cat > .gitignore << 'IGNORE'
*.pyc
__pycache__/
.env
*.log
node_modules/
IGNORE

# Crea una estructura básica
mkdir -p src docs default
echo "# Documentación" > docs/README.md
echo "# Código fuente" > src/README.md
```

## Paso 4: Hacer el Primer Commit

```bash
# Ve qué cambios tienes
git status

# Prepara todos los archivos
git add .

# Haz el primer commit
git commit -m "Initial commit: Create project structure"

# Verifica el commit
git log --oneline
```

## Paso 5: Crear el Repositorio en GitHub

1. Abre GitHub: https://github.com/new
2. Nombre del repo: `mi-nuevo-repo`
3. Descripción (opcional): "Descripción de mi proyecto"
4. Elige: **Public** (si quieres que sea público) o **Private** (si es privado)
5. **NO marques** "Initialize this repository with a README" (ya lo tienes)
6. Click en **"Create repository"**

## Paso 6: Conectar Tu Repo Local con GitHub

```bash
# GitHub te dirá exactamente esto. Cópialo y pégalo:

# Renombra la rama a main (GitHub usa main por defecto)
git branch -M main

# Añade el remoto de GitHub
git remote add origin https://github.com/TU_USUARIO/mi-nuevo-repo.git

# Verifica que se conectó
git remote -v
# Deberías ver:
# origin  https://github.com/TU_USUARIO/mi-nuevo-repo.git (fetch)
# origin  https://github.com/TU_USUARIO/mi-nuevo-repo.git (push)
```

## Paso 7: Subir Tu Repo a GitHub

```bash
# Sube los cambios locales a GitHub
git push -u origin main

# Si pide credenciales, usa tu token personal de GitHub
# (no la contraseña)
```

## Paso 8: Verificar en GitHub

- Abre https://github.com/TU_USUARIO/mi-nuevo-repo
- Deberías ver tus archivos subidos (README.md, .gitignore, etc.)

---

## Resumen Rápido: Crear Repo Nuevo en 10 Comandos

```bash
# 1. Desde Desktop crea carpeta
cd /home/kali/Desktop
mkdir mi-nuevo-repo
cd mi-nuevo-repo

# 2. Inicializa git
git init

# 3. Crea archivo inicial
echo "# Mi Nuevo Repo" > README.md

# 4. Prepara y confirma
git add .
git commit -m "Initial commit"

# 5. Añade el remoto de GitHub
git remote add origin https://github.com/TU_USUARIO/mi-nuevo-repo.git

# 6. Renombra rama a main
git branch -M main

# 7. Sube a GitHub
git push -u origin main
```

---

## Estructura Recomendada para Nuevo Repo

```bash
/home/kali/Desktop/mi-nuevo-repo/
├── README.md              ← Descripción del proyecto
├── .gitignore             ← Archivos a ignorar
├── LICENSE                ← Licencia (MIT, Apache, etc.)
├── src/                   ← Tu código
│   └── main.py
├── docs/                  ← Documentación
│   ├── README.md
│   └── guides/
├── default/               ← Chunks para vectorizar
│   ├── chunk-1.md
│   └── chunk-2.md
├── config/                ← Configuración
│   └── requirements.txt
└── .git/                  ← Repositorio Git (automático)
```

---

## Diferencia: RAG Repo vs Nuevo Repo

### RAG Repo (Ya Existe)
```bash
cd /home/kali/Desktop/RAG
git pull                    # Descarga cambios
git add .
git commit -m "cambios"
git push origin main        # Sube
```

### Nuevo Repo (Desde Cero)
```bash
cd /home/kali/Desktop
mkdir nuevo-proyecto
cd nuevo-proyecto
git init                    # Inicializa
git add .
git commit -m "Initial"
git remote add origin ...   # Conecta con GitHub
git push -u origin main     # Sube por primera vez
```

---

## Tips Para Nuevo Repo

- 📝 **Crea un README bueno** - Es lo primero que ven
- 🚫 **Configura .gitignore** - No subas archivos innecesarios
- 📄 **Agrega LICENSE** - Define términos de uso
- 🔑 **Nunca subas secretos** - API keys, tokens, contraseñas NO
- 📦 **Estructura clara** - src/, docs/, config/, etc.
- 🎯 **Primer commit significativo** - "Initial commit" está bien
