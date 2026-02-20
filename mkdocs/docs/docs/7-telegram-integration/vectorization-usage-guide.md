# Instrucciones de Vectorización - RAG Completo

## 🎯 Estado Actual (Feb 14, 2026)

**✅ Sistema completamente funcional y probado:**
- 15 chunks vectorizados y almacenados en Pinecone
- Bot de Telegram corriendo con embeddings OpenAI 3072D
- Query agent híbrido buscando en Pinecone + leyendo archivos locales
- Registry automático mapeando chunk_id → rutas de archivos

---

## 📍 Scripts Disponibles

Hay **3 formas** de vectorizar tus chunks:

### Opción 1: Script Official (OpenAI 3072D - RECOMENDADO) ⭐
```
/root/.openskills/vectorize_canonical_openai.py
```
- **Usa OpenAI text-embedding-3-large (3072D)** ← Modelo más avanzado de OpenAI
- Acepta CUALQUIER ruta de directorio (absoluta, relativa, flexible)
- No requiere estructura específica de directorios
- Busca recursivamente todos los `.md`
- Flexible con el schema de metadatos (solo requiere `chunk_id`)
- **Auto-genera `chunk_registry.json`** después de vectorizar
- **Subida a `rag-canonical-v1-emb3large`** (índice universal de calidad superior)
- **MEJOR OPCIÓN - CALIDAD SUPERIOR** ✅
- Integrado con Telegram Bot y Query Agent

### Opción 2: Script Simple (SentenceTransformers - GRATIS)
```
/root/.opencode/skills/vectorizer/executables/vectorize_simple.py
```
- Usa modelo local (sin costo de API)
- Acepta CUALQUIER ruta de directorio
- No requiere estructura específica
- **Subida a `rag-universal-3072`**
- Buena relación costo-beneficio

### Opción 3: Script Universal (Legacy)
```
/root/.opencode/skills/vectorizer/executables/vectorize_universal.py
```
- Requiere directorios en `/home/kali/Desktop/RAG/`
- Soporta múltiples directorios simultáneamente

## 🗂️ Estructura de Directorios Requerida

El script espera que todos tus directorios estén ubicados en:

```
/home/kali/Desktop/RAG/
```

### Estructura recomendada:

```
/home/kali/Desktop/RAG/
├── cheatsheets/
│   ├── linux/
│   │   ├── admin/
│   │   │   └── env-config_001.md
│   │   ├── commands/
│   │   │   └── essential-linux-commands_001.md
│   │   ├── permissions/
│   │   │   ├── chmod-user_001.md
│   │   │   └── chmod-group_001.md
│   │   ├── shell/
│   │   │   └── tty-upgrade_001.md
│   │   └── text-processing/
│   │       └── awk-basics_001.md
│   └── web-security/
│       ├── pentest/
│       │   └── ctf-workflow_001.md
│       └── git-leak/
│           └── source-analysis_001.md
├── GAVEL/
│   └── (tus chunks aquí)
└── FACTS_CHUNKS/
    └── (tus chunks aquí)
```

## 📝 Nomenclatura de Archivos Chunk

### Formato de nombre:
```
<intent>_<numero>.md
```

### Ejemplos válidos:
- `tty-upgrade_001.md`
- `chmod-user_001.md`
- `awk-basics_001.md`
- `env-config_001.md`
- `ctf-workflow_001.md`
- `source-analysis_001.md`

### Números:
- Usa tres dígitos: `_001`, `_002`, `_003`, etc.
- El número es incremental para múltiples versiones del mismo intent

## 📋 Estructura de Contenido del Chunk (YAML Frontmatter)

Cada archivo `.md` debe tener frontmatter YAML al inicio:

```yaml
---
chunk_id: reference::linux::permissions::chmod-user::001
domain: linux
subdomain: permissions
chunk_type: reference
category: linux
confidence: high
reuse_level: high
tags:
  - chmod
  - permissions
  - file-modes
  - user-ownership
---

# Contenido del chunk aquí
(150-250 palabras aprox.)
```

### Campos requeridos:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `chunk_id` | Identificador único | `reference::linux::permissions::chmod-user::001` |
| `domain` | Dominio principal | `linux`, `web-security` |
| `subdomain` | Subdominio específico | `permissions`, `shell`, `pentest` |
| `chunk_type` | Tipo de contenido | `reference`, `technique`, `procedure`, `guideline` |
| `category` | Categoría general | `linux`, `web-security` |
| `confidence` | Confiabilidad del contenido | `high`, `medium`, `low` |
| `reuse_level` | Reutilizabilidad | `high`, `medium`, `low` |
| `tags` | Lista de etiquetas | `[chmod, permissions, file-modes]` |

## 🔄 Cómo Ejecutar los Scripts

### OPCIÓN 1: Script Official OpenAI (RECOMENDADO) ⭐

#### Sintaxis:
```bash
python3 /root/.openskills/vectorize_canonical_openai.py <ruta_a_directorio>
```

#### Ejemplos:

**Vectorizar chunks en directorio actual:**
```bash
python3 /root/.openskills/vectorize_canonical_openai.py cheatsheets
```

**Vectorizar chunks con ruta absoluta:**
```bash
python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/Desktop/RAG/cheatsheets
```

**Vectorizar chunks con ruta relativa:**
```bash
python3 /root/.openskills/vectorize_canonical_openai.py ./mis_chunks
```

**Ventajas:**
- ✅ Usa OpenAI (3072D - calidad superior)
- ✅ No requiere estructura específica
- ✅ Acepta cualquier ruta absoluta o relativa
- ✅ Flexible con metadatos (solo requiere chunk_id)
- ✅ Busca automáticamente todos los `.md` recursivamente

---

### OPCIÓN 2: Script Simple (Gratis - Sin costo de API)

#### Sintaxis:
```bash
python3 /root/.opencode/skills/vectorizer/executables/vectorize_simple.py <ruta_a_directorio>
```

#### Ejemplos:

**Vectorizar chunks:**
```bash
python3 /root/.opencode/skills/vectorizer/executables/vectorize_simple.py /home/kali/Desktop/RAG/cheatsheets
```

**Ventajas:**
- ✅ No requiere API key de OpenAI
- ✅ Rápido y sin costo
- ✅ Acepta cualquier ruta

---

### OPCIÓN 3: Script Universal (Legacy)

#### Sintaxis:
```bash
python3 /root/.opencode/skills/vectorizer/executables/vectorize_universal.py <directorio_1> [<directorio_2> ...]
```

#### Ejemplos:

**Vectorizar solo cheatsheets:**
```bash
python3 /root/.opencode/skills/vectorizer/executables/vectorize_universal.py cheatsheets
```

**Vectorizar múltiples directorios:**
```bash
python3 /root/.opencode/skills/vectorizer/executables/vectorize_universal.py cheatsheets GAVEL FACTS_CHUNKS
```

## ✅ Ejemplo Completo de un Chunk

### Archivo: `/home/kali/Desktop/RAG/cheatsheets/linux/permissions/chmod-user_001.md`

```yaml
---
chunk_id: reference::linux::permissions::chmod-user::001
domain: linux
subdomain: permissions
chunk_type: reference
category: linux
confidence: high
reuse_level: high
tags:
  - chmod
  - permissions
  - user-ownership
---

# chmod - Permisos de Usuario

El comando `chmod` modifica los permisos de archivos. Para cambiar permisos de usuario (propietario), usa:

```bash
chmod u+x archivo.txt    # Agregar permiso de ejecución al usuario
chmod u-w archivo.txt    # Quitar permiso de escritura al usuario
chmod u=rwx archivo.txt  # Establecer permisos exactos: lectura, escritura, ejecución
```

Los permisos disponibles son:
- `r` (read - lectura): permite leer el archivo
- `w` (write - escritura): permite modificar el archivo
- `x` (execute - ejecución): permite ejecutar el archivo

Ejemplos prácticos:
- `chmod u+x script.sh` - Hacer un script ejecutable
- `chmod u-w config.txt` - Proteger un archivo contra escritura accidental
```

## 🎯 Cosas Importantes

1. **Ubicación base**: Todos los directorios DEBEN estar en `/home/kali/Desktop/RAG/`
2. **Nombres de archivos**: Usa guiones (`-`) en los nombres, no espacios
3. **Formato YAML**: El frontmatter DEBE estar entre `---` y `---`
4. **chunk_id único**: Cada chunk debe tener un `chunk_id` único
5. **Estructura de directorios**: Es importante que respetes `categoria/dominio/subdominio/`

## 🔍 Cómo Funciona el Script (Optimizado Feb 2026)

### Embedding (Vectorización):
- **Genera embeddings de 3072 dimensiones** usando **OpenAI text-embedding-3-large**
- Combina YAML frontmatter + contenido del chunk para mejor semántica
- Permite búsqueda simultánea por metadatos (tags, domain, subdomain) Y contenido
- Es el modelo más avanzado y preciso de OpenAI para RAG

### Lo que se guarda en Pinecone:

```
Vector ID: chunk_id (ej: reference::linux::permissions::chmod-user::001)
├── Embedding (3072 dimensiones - OpenAI)
└── Metadata:
    ├── Frontmatter completo (chunk_id, domain, subdomain, chunk_type, etc.)
    ├── content: TODO el contenido del chunk (sin truncamiento, COMPLETO)
    ├── content_length: Longitud total del contenido
    └── (se lee de archivo local si es posible, fallback a metadata)
```

### Auto-generación de Registry:

Después de vectorizar, el script **automáticamente genera `chunk_registry.json`**:

```json
{
  "reference::linux::permissions::chmod-user::001": "/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md",
  "reference::linux::permissions::chmod-group::001": "/root/.openskills/CHEATSHEETS CHUNKS/chmod-group_001.md",
  "..." : "..."
}
```

Este archivo es **crítico** para:
- **Telegram Bot**: Lee archivos locales completos en lugar de confiar solo en metadata
- **Query Agent**: Localiza y lee contenido completo del filesystem
- **Fallback chain**: Si el archivo local existe, úsalo; si no, fallback a metadata.content

## 📊 Salida Esperada del Script (OpenAI)

Cuando ejecutes el script, verás algo como:

```
🔑 Using Pinecone API key from /root/.openskills/env/pinecone.env
🔑 Using OpenAI API key from /root/.openskills/env/openai.env

✅ Index exists: rag-canonical-v1-emb3large (3072D, cosine)
🧠 Using embedding model: text-embedding-3-large (3072D)

🚀 Processing /root/.openskills/CHEATSHEETS\ CHUNKS/

📂 Found 15 markdown files

Processing chunks:
  ✅ reference::linux::permissions::chmod-user::001 (428 chars)
  ✅ reference::linux::permissions::chmod-group::001 (405 chars)
  ✅ technique::linux::compression::001 (613 chars)
  ✅ reference::web::pentest::ctf-workflow::001 (1617 chars)
  ... (12 más)

🔄 Upserting 15 vectors to rag-canonical-v1-emb3large/default...
  ✅ Batch 1: 15 vectors uploaded (3072D)

✅ Vectorization Complete!

📊 Index Statistics:
   Total vectors: 15
   Dimension: 3072
   Metric: cosine
   Namespace: __default__

📝 Auto-generating chunk_registry.json...
✅ Registry created: /home/kali/Desktop/RAG/chunk_registry.json
   Mapped 15 chunk_id → file paths
```

---

## 🔌 Integración Completa

### 1. Telegram Bot
```bash
# Bot en ejecución
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py

# Comando para consultar:
/q <tu_query> [top_k]
```
- ✅ Genera embeddings con OpenAI text-embedding-3-large 3072D
- ✅ Busca en Pinecone
- ✅ Lee archivos locales via chunk_registry.json
- ✅ Envia contenido COMPLETO (sin truncar)
- ✅ Fallback: Si archivo no existe, usa metadata.content

### 2. Query Agent Híbrido
```bash
python3 /root/.opencode/skills/query-agent/executables/query-agent-hybrid.py "tu_query" [--top-k 5]
```
- ✅ Busca en Pinecone + lee localmente
- ✅ Genera markdown con contenido COMPLETO
- ✅ Opcionalmente envía a Telegram

### 3. Registry Automático
- ✅ **Se genera automáticamente** después de cada vectorización
- ✅ Mapea chunk_id → rutas de archivos locales
- ✅ Requerido para lectura local en Bot y Query Agent
- ✅ Ubicación: `/home/kali/Desktop/RAG/chunk_registry.json`

## ❌ Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `No markdown files found` | No hay archivos `.md` en el directorio | Verifica que los chunks están en la ruta correcta |
| `Skipped: No YAML frontmatter` | Falta el YAML frontmatter en el archivo | Agrega `---` al inicio y fin del frontmatter (mínimo: `chunk_id:`) |
| `Directory not found: /home/kali/Desktop/RAG/cheatsheets` | El directorio no existe en esa ubicación | Verifica la ruta absoluta del directorio |
| `PINECONE_API_KEY not found` | Falta la variable de entorno | Configura `/root/.openskills/env/pinecone.env` |
| `OPENAI_API_KEY not found` | Falta OpenAI API key | Configura `/root/.openskills/env/openai.env` |
| `"Content not available" en Telegram` | Bot usando proceso viejo sin fixes | Mata bot: `killall python3` y reinicia: `/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py` |
| `chunk_registry.json no actualizado` | Registry no se auto-generó | Verifica permisos de escritura en `/home/kali/Desktop/RAG/` |

---

## 🔧 Troubleshooting - Bot de Telegram

### Si recibas "Content not available":

**Causa más probable:** Bot corre con proceso viejo (anterior a los fixes)

**Solución:**
```bash
# 1. Mata todos los procesos Python
killall python3

# 2. Verifica que el bot está muerto
ps aux | grep telegram_bot | grep -v grep  # No debe mostrar nada

# 3. Reinicia con la versión nueva
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py &

# 4. Verifica que cargó el registry
tail -f /home/kali/Desktop/RAG/telegram_bot.log | grep "chunks in registry"
```

Deberías ver: `RAG Engine initialized: 15 chunks in registry`

---

## 📈 Checklist de Implementación

- ✅ Script vectorizer acepta cualquier ruta (absoluta o relativa)
- ✅ Script auto-genera chunk_registry.json después de vectorizar
- ✅ Telegram bot corre con Python correcto (`/root/.openskills/venv/bin/python3`)
- ✅ Bot carga registry al iniciar
- ✅ Bot lee archivos locales via registry (fallback a metadata)
- ✅ Bot no trunca contenido (envía en múltiples mensajes si es necesario)
- ✅ Modelo embedding: OpenAI text-embedding-3-large (3072D)
- ✅ Índice: rag-canonical-v1-emb3large
- ✅ Namespace: __default__
- ✅ Query agent integrado con registry

## 🚀 Forma Más Fácil de Empezar (RÁPIDO) ⭐

Si solo quieres empezar sin complicaciones:

```bash
# 1. Crea un directorio donde quieras
mkdir /home/kali/mis_chunks

# 2. Copia tus archivos .md ahí (con YAML frontmatter - mínimo chunk_id)
cp tus_archivos.md /home/kali/mis_chunks/

# 3. Vectoriza con OpenAI (mejor calidad):
python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/mis_chunks

# ¡Listo! Tus chunks están en Pinecone con embeddings de calidad superior
```

**Eso es todo. No necesitas estructura de directorios complicada.**

---

## 🚀 Resumen Rápido - Feb 2026

### Para empezar AHORA (RECOMENDADO - OpenAI 3072D):
```bash
# 1. Crea un directorio con tus chunks
mkdir /ruta/mis_chunks

# 2. Copia tus .md con YAML frontmatter (mínimo: chunk_id)
cp tus_archivos.md /ruta/mis_chunks/

# 3. Vectoriza con OpenAI (mejor calidad)
python3 /root/.openskills/vectorize_canonical_openai.py /ruta/mis_chunks

# 4. ✅ Script auto-genera chunk_registry.json
# ✅ 15 chunks vectorizados y listos
# ✅ Bot de Telegram + Query Agent automáticamente disponibles
```

### Sin costo de API (alternativa):
```bash
# Mismo proceso pero con embeddings locales (SentenceTransformers)
python3 /root/.opencode/skills/vectorizer/executables/vectorize_simple.py /ruta/mis_chunks
```

### Para estructura muy organizada (opcional):
```bash
# Dentro de /home/kali/Desktop/RAG/:
/home/kali/Desktop/RAG/
├── cheatsheets/
│   └── linux/permissions/chmod-user_001.md
├── GAVEL/
└── FACTS_CHUNKS/

# Luego vectoriza cualquier directorio:
python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/Desktop/RAG/cheatsheets
```

---

## 📚 Archivos de Configuración Necesarios

Asegúrate de que existan:

```
/root/.openskills/env/
├── pinecone.env         # PINECONE_API_KEY=...
├── openai.env           # OPENAI_API_KEY=...
└── telegram.env         # TELEGRAM_BOT_TOKEN=... y TELEGRAM_CHAT_ID=...
```

---

## 🎯 Próximas Acciones

1. **Crea nuevos chunks** con formato YAML frontmatter
2. **Vectoriza con:** `python3 /root/.openskills/vectorize_canonical_openai.py <tu_ruta>`
3. **Consulta por Telegram:** `/q <tu_query>`
4. **O usa Query Agent:** `query-agent-hybrid.py "tu_query"`

El flujo completo está automatizado. Solo necesitas chunks con estructura correcta.
