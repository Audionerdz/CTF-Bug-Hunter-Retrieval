---
chunk_id: github::setup::remote-connection::001
domain: github
chunk_type: guide
category: setup
confidence: high
reuse_level: universal
tags: [github, git, remote, connection, setup, authentication]
source_file: github-connection-setup.md
---

# Cómo Conectarse a GitHub y Vectorizar

## Paso 1: Verificar tu Conexión Remota

```bash
# Ver la URL remota configurada
git remote -v

# Deberías ver algo como:
# origin  https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git (fetch)
# origin  https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git (push)
```

## Paso 2: Configurar GitHub por Primera Vez (Si es necesario)

```bash
# Añadir el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# O cambiar si ya existe
git remote set-url origin https://github.com/TU_USUARIO/TU_REPO.git

# Verificar que quedó bien
git remote -v
```

## Paso 3: Autenticación con GitHub

```bash
# Opción A: Con HTTPS (necesitas token personal)
git config --global user.email "tu@email.com"
git config --global user.name "Tu Nombre"

# Opción B: Con SSH (más seguro)
ssh -T git@github.com
# Si funciona, verás: Hi TU_USUARIO! You've successfully authenticated.
```

## Paso 4: Hacer Push a GitHub

```bash
# Después de hacer commits locales
git push origin main

# Primera vez con rama nueva
git push -u origin main

# Verificar que se subió
git log --oneline -3
```

## Paso 5: Vectorizar Contenido

```bash
# Vectorizar un archivo individual
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/mi-guia.md

# Vectorizar un directorio completo
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/

# Vectorizar el repositorio completo
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/
```

## Paso 6: Consultar tu Base de Conocimiento Vectorizada

```bash
# Hacer una pregunta
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "tu pregunta aquí"

# Ejemplos:
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "how to connect to github"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "cómo vectorizar archivos"
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "git push workflow"
```

## Ciclo Completo: Cambios → Commit → Push → Vectorizar

```bash
# 1. Hacer cambios en archivos
nano /home/kali/Desktop/RAG/default/nueva-guia.md

# 2. Ver qué cambió
cd /home/kali/Desktop/RAG
git status

# 3. Preparar los cambios
git add .

# 4. Confirmar con mensaje
git commit -m "docs: Agregar nueva guía"

# 5. Subir a GitHub
git push origin main

# 6. Vectorizar el nuevo contenido
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/vectorize_canonical_openai.py /home/kali/Desktop/RAG/default/nueva-guia.md

# 7. Probar la búsqueda semántica
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/query_canonical_openai.py "tema de tu guía"
```

