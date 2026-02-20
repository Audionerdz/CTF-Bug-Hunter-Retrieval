# Query Agent Results

**Timestamp:** 2026-02-20 23:46:14

**Index:** `rag-canonical-v1-emb3large`

**Query:** `cómo vectorizar archivos`

**Results:** 5
---

### 1. cli::spanish::vectorization::single-file::001
- **Machine:** UNKNOWN
- **Phase:** unknown
- **Technique:** unknown
- **Score:** 0.475

```
---
chunk_id: cli::spanish::vectorization::single-file::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, file, single, spanish]
```

### 2. cli::spanish::vectorization::directory::001
- **Machine:** UNKNOWN
- **Phase:** unknown
- **Technique:** unknown
- **Score:** 0.460

```
---
chunk_id: cli::spanish::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directory, batch, spanish]
```

### 3. github::setup::remote-connection::001
- **Machine:** UNKNOWN
- **Phase:** unknown
- **Technique:** unknown
- **Score:** 0.434

```
# Cómo Conectarse a GitHub y Vectorizar

## Paso 1: Verificar tu Conexión Remota

~~~bash
# Ver la URL remota configurada
git remote -v

# Deberías ver algo como:
# origin  https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git (fetch)
# origin  https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git (push)
~~~

## Paso 2: Configurar GitHub por Primera Vez (Si es necesario)

~~~bash
# Añadir el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# O cambiar si ya existe
git remote set-url origin https://github.com/TU_USUARIO/TU_REPO.git

# Verificar que quedó bien
git remote -v
~~~

## Paso 3: Autenticación con GitHub

~~~bash
# Opción A: Con HTTPS (necesitas token personal)
git config --global user.email "tu@email.com"
git config --global user.name "Tu Nombre"

# Opción B: Con SSH (más seguro)
ssh -T git@github.com
# Si funciona, verás: Hi TU_USUARIO! You've successfully authenticated.
~~~

## Paso 4: Hacer Push a GitHub

~~~bash
# Después de hacer commits locales
git push origin main

# Primera vez con rama nueva
git push -u origin main

# Verificar que se subió
git log --oneline -3
~~~

## Paso 5: Vectorizar Contenido

~~~bash
# Vectorizar un archivo individual
vectorize /home/kali/Desktop/RAG/default/mi-guia.md

# Vectorizar un directorio completo
vectorize /home/kali/Desktop/RAG/default/

# Vectorizar el repositorio completo
vectorize /home/kali/Desktop/RAG/
~~~

## Paso 6: Consultar tu Base de Conocimiento Vectorizada

~~~bash
# Hacer una pregunta
query "tu pregunta aquí"

# Ejemplos:
query "how to connect to github"
query "cómo vectorizar archivos"
query "git push workflow"
~~~

## Ciclo Completo: Cambios → Commit → Push → Vectorizar

~~~bash
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
vectorize /home/kali/Desktop/RAG/default/nueva-guia.md

# 7. Probar la búsqueda semántica
query "tema de tu guía"
~~~
```

### 4. cli::english::vectorization::single-file::001
- **Machine:** UNKNOWN
- **Phase:** unknown
- **Technique:** unknown
- **Score:** 0.384

```
---
chunk_id: cli::english::vectorization::single-file::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, file, single, english]
```

### 5. cli::english::vectorization::directory::001
- **Machine:** UNKNOWN
- **Phase:** unknown
- **Technique:** unknown
- **Score:** 0.352

```
---
chunk_id: cli::english::vectorization::directory::001
domain: cli
chunk_type: guide
category: vectorization
confidence: high
reuse_level: universal
tags: [vectorization, directory, batch, english]
```
