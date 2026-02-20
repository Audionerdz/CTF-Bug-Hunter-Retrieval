# Vectorizer Modular - Directorio OR Archivo Individual

## ¿Qué Cambió?

El script `vectorize_canonical_openai.py` ahora es **totalmente modular**:
- ✅ Soporta directorios completos
- ✅ Soporta archivos individuales (.md)
- ✅ Soporta nombres simples (búsqueda automática)
- ✅ Mantiene todas las funcionalidades anteriores
- ✅ Genera registry actualizado automáticamente

---

## Uso

### 1️⃣ Vectorizar un Directorio Completo

```bash
# Opción A: Ruta absoluta
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/chunks/

# Opción B: Ruta relativa
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py ./chunks/

# Opción C: Solo nombre (busca en /home/kali/Desktop/RAG/)
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py cheatsheets
```

**Output:**
```
======================================================================
🧠 VECTORIZER MODULAR - OpenAI 3072D
======================================================================
Path: /home/kali/chunks/
Index: rag-canonical-v1-emb3large
Model: text-embedding-3-large (3072D)

📁 Detectado: Directorio
📦 Encontrados: 5 archivo(s)

📁 Procesando 5 chunks

✅ reference::linux::permissions::chmod-user::001 (3072D)
✅ reference::linux::permissions::chmod-group::001 (3072D)
✅ technique::linux::compression::001 (3072D)
✅ reference::web::pentest::ctf-workflow::001 (3072D)
✅ reference::linux::shortcuts::hotkeys::001 (3072D)

📤 Subiendo 5 vectores a rag-canonical-v1-emb3large

  ✅ Batch 1 (5 vectores)

📊 Estadísticas del índice:
  Total vectores: 20
  Namespaces: ['__default__']

📝 Generando chunk registry para query agent...
✅ Chunk registry guardado: /home/kali/Desktop/RAG/chunk_registry.json
   Total chunks mapeados: 20

✅ Vectorización completa!
   Success: 5
   Errors: 0
   Total: 5 vectores
   Registry: /home/kali/Desktop/RAG/chunk_registry.json
```

---

### 2️⃣ Vectorizar UN Archivo Individual

```bash
# Opción A: Ruta absoluta
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/mi_chunk.md

# Opción B: Ruta relativa
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py ./mi_chunk.md

# Opción C: Archivo en directorio actual
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py chunk.md
```

**Output:**
```
======================================================================
🧠 VECTORIZER MODULAR - OpenAI 3072D
======================================================================
Path: /home/kali/mi_chunk.md
Index: rag-canonical-v1-emb3large
Model: text-embedding-3-large (3072D)

📄 Detectado: Archivo individual
📦 Encontrados: 1 archivo(s)

📁 Procesando 1 chunks

✅ reference::linux::shortcuts::hotkeys::001 (3072D)

📤 Subiendo 1 vectores a rag-canonical-v1-emb3large

  ✅ Batch 1 (1 vectores)

📊 Estadísticas del índice:
  Total vectores: 21
  Namespaces: ['__default__']

📝 Generando chunk registry para query agent...
✅ Chunk registry guardado: /home/kali/Desktop/RAG/chunk_registry.json
   Total chunks mapeados: 21

✅ Vectorización completa!
   Success: 1
   Errors: 0
   Total: 1 vectores
   Registry: /home/kali/Desktop/RAG/chunk_registry.json
```

---

## 📋 Formato de Chunk Individual

Tu archivo `.md` debe tener YAML frontmatter:

```yaml
---
chunk_id: reference::linux::shortcuts::hotkeys::001
domain: linux
chunk_type: reference
confidence: verified
reuse_level: universal
tags:
  - linux
  - hotkeys
---

### Contenido del Chunk

Tu contenido aquí...
```

**Campos Requeridos:**
- `chunk_id` - Identificador único (OBLIGATORIO)

**Campos Opcionales:**
- `domain` - Dominio
- `chunk_type` - Tipo (reference, technique, etc)
- `confidence` - Confianza (high, medium, low)
- `reuse_level` - Reutilizabilidad
- `tags` - Lista de etiquetas

---

## 🔄 Flujo Completo

### Caso 1: Tienes un archivo suelto

```bash
# 1. Tu archivo: /home/mi_nuevo_chunk.md
cat /home/mi_nuevo_chunk.md
# ---
# chunk_id: technique::linux::network::ifconfig::001
# domain: linux
# chunk_type: technique
# tags:
#   - networking
#   - ifconfig
# ---
# 
# ### ifconfig - Configuración de Red
# ...

# 2. Vectoriza SOLO ese archivo
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/mi_nuevo_chunk.md

# 3. Automáticamente:
#    - Genera embedding (3072D)
#    - Sube a Pinecone
#    - Actualiza chunk_registry.json
#    - Bot y Query Agent lo ven inmediatamente
```

### Caso 2: Tienes 5 archivos nuevos en una carpeta

```bash
# 1. Tu carpeta con archivos
ls /home/kali/nuevos_chunks/
# wifi.md, dns.md, dhcp.md, subnet.md, gateway.md

# 2. Vectoriza TODO el directorio
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/nuevos_chunks/

# 3. Automáticamente:
#    - Procesa los 5 archivos
#    - Genera 5 embeddings
#    - Sube todos a Pinecone
#    - Actualiza registry con los 5

# 4. Telegram Bot y Query Agent ven los 5 nuevos inmediatamente
```

### Caso 3: Carpeta existente en /home/kali/Desktop/RAG/

```bash
# Si tu carpeta está aquí:
/home/kali/Desktop/RAG/network-stuff/

# Puedes hacer:
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py network-stuff

# O:
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/Desktop/RAG/network-stuff
```

---

## 🎯 Detección Automática

El script detecta automáticamente:

| Input | Detecta Como | Ejemplo |
|-------|--------------|---------|
| `/ruta/archivo.md` | Archivo individual | `/home/kali/chunk.md` |
| `/ruta/carpeta/` | Directorio | `/home/kali/chunks/` |
| `nombre-simple` | Directorio en base path | `cheatsheets` → `/home/kali/Desktop/RAG/cheatsheets` |
| `./archivo.md` | Archivo relativo | `./mi_chunk.md` |
| `./carpeta/` | Directorio relativo | `./chunks/` |

---

## ✅ Checklist para Archivo Individual

Antes de vectorizar un archivo `.md`:

- ✅ Tiene YAML frontmatter (entre `---`)
- ✅ Tiene `chunk_id` (OBLIGATORIO)
- ✅ Tiene extensión `.md`
- ✅ El `chunk_id` es único (no duplicado)
- ✅ Formato: `namespace::domain::subdomain::intent::nnn`
  - Ejemplo: `reference::linux::shortcuts::hotkeys::001`

---

## 🔄 Registry Se Actualiza Automáticamente

Cada vez que corres el vectorizer (directorio o archivo):

1. Lee todos los chunks procesados
2. Extrae `chunk_id` de cada uno
3. Mapea `chunk_id` → ruta del archivo
4. Sobrescribe `/home/kali/Desktop/RAG/chunk_registry.json`

**Resultado:**
```json
{
  "reference::linux::shortcuts::hotkeys::001": "/home/mi_nuevo_chunk.md",
  "technique::linux::network::ifconfig::001": "/home/kali/nuevos_chunks/wifi.md",
  ...
}
```

---

## 🚀 Ejemplos Prácticos

### Ejemplo 1: Agregar UN chunk nuevo

```bash
# Creaste un archivo
echo '---
chunk_id: technique::web::sql::injection::001
domain: web
chunk_type: technique
tags:
  - sql
  - injection
---

### SQL Injection

Técnicas para explotar vulnerabilidades SQL...
' > /tmp/sql_injection.md

# Vectorizalo
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py /tmp/sql_injection.md

# ✅ Listo para usar en Telegram Bot y Query Agent
```

### Ejemplo 2: Vectorizar carpeta completa

```bash
# Creaste una carpeta con 10 archivos
mkdir ~/hacking-techniques
# (copias 10 archivos .md con YAML frontmatter)

# Vectoriza todo
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py ~/hacking-techniques

# ✅ Los 10 archivos listos en Pinecone + Registry actualizado
```

### Ejemplo 3: Actualizar UN chunk existente

```bash
# El archivo ya existe pero lo editaste
nano /root/.openskills/CHEATSHEETS\ CHUNKS/hotkeys_001.md

# Vectoriza de nuevo (sobrescribe el vector anterior)
/root/.openskills/venv/bin/python3 /root/.openskills/vectorize_canonical_openai.py "/root/.openskills/CHEATSHEETS CHUNKS/hotkeys_001.md"

# ✅ Vector actualizado en Pinecone, registry sincronizado
```

---

## ⚡ Velocidad

| Operación | Tiempo |
|-----------|--------|
| 1 archivo | ~2-3 segundos |
| 5 archivos | ~5-8 segundos |
| 20 archivos | ~15-25 segundos |
| Upsert a Pinecone | ~1 segundo |
| Actualizar registry | ~0.5 segundos |

---

## ❌ Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `No es un archivo markdown` | Archivo no es `.md` | Asegúrate extensión es `.md` |
| `Archivo no encontrado` | Ruta incorrecta | Verifica ruta absoluta o relativa |
| `Missing chunk_id` | Falta YAML frontmatter | Agrega `---` y `chunk_id:` |
| `No YAML frontmatter` | Archivo no comienza con `---` | Agrega YAML frontmatter al inicio |
| `PINECONE_API_KEY not found` | Falta env file | Crea `/root/.openskills/env/pinecone.env` |

---

## 🔗 Integración Automática

Después de vectorizar (archivo o directorio):

✅ **Telegram Bot** - Automáticamente ve el nuevo chunk
✅ **Query Agent** - Puede buscar el nuevo chunk
✅ **Registry** - Se actualiza automáticamente
✅ **Local Files** - Bot lee el archivo directamente

**No requiere reiniciar bot ni nada - todo automático!**

---

**Script MODULAR lista. Soporta todo: directorios, archivos individuales, nombres simples. ¡Una sola herramienta para todo!**
