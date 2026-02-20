# Vectorizer Modular - Archivos Individuales + Directorios

**File**: `/root/.openskills/vectorize_canonical_openai.py`  
**Version**: MODULAR (Feb 14, 2026)  
**Status**: ✅ Production Ready

---

## Overview

El vectorizer ahora es **totalmente modular** y soporta:
- ✅ Directorios completos
- ✅ Archivos individuales (.md)
- ✅ Detección automática

**Sin alterar** las 8 fases de procesamiento existentes.

---

## Usage

### 1. Vectorizar Archivo Individual

```bash
# Archivo suelto
python3 /root/.openskills/vectorize_canonical_openai.py /tmp/sql_injection.md

# Archivo relativo
python3 /root/.openskills/vectorize_canonical_openai.py ./mi_chunk.md

# Archivo en directorio actual
python3 /root/.openskills/vectorize_canonical_openai.py archivo.md
```

**Tiempo**: 2-3 segundos
**Output**: 1 vector + registry actualizado

### 2. Vectorizar Directorio Completo

```bash
# Ruta absoluta
python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/chunks/

# Ruta relativa
python3 /root/.openskills/vectorize_canonical_openai.py ./chunks/

# Nombre simple
python3 /root/.openskills/vectorize_canonical_openai.py cheatsheets
```

**Tiempo**: 15-25 segundos (para 20 archivos)
**Output**: N vectores + registry actualizado

### 3. Actualizar Chunk Existente

```bash
# Re-vectoriza un archivo existente (sobrescribe vector)
python3 /root/.openskills/vectorize_canonical_openai.py hotkeys_001.md
```

**Efecto**: Vector sobrescrito, registry sincronizado

---

## Detección Automática

El script detecta automáticamente el tipo de entrada:

| Input | Detecta | Ejemplo |
|-------|---------|---------|
| `archivo.md` | Archivo individual | `chunk.md` |
| `ruta/completa/` | Directorio | `/home/kali/chunks/` |
| `nombre-simple` | Directorio en base path | `cheatsheets` |
| `./archivo.md` | Archivo relativo | `./chunk.md` |

---

## Formato de Chunk Individual

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

**Requerido:**
- `chunk_id` - Identificador único (OBLIGATORIO)

**Opcional:**
- `domain`, `chunk_type`, `confidence`, `reuse_level`, `tags`

---

## Code Architecture (Modular)

### Función Principal: `get_chunk_files(path)`

```python
def get_chunk_files(path):
    """
    Detecta si es directorio o archivo y retorna lista.
    
    MODULAR:
    - Si es .md → get_chunk_files_from_file()
    - Si es directorio → get_chunk_files_from_directory()
    - Si es nombre → busca en /home/kali/Desktop/RAG/
    """
```

### Función para Archivos: `get_chunk_files_from_file(path)`

```python
def get_chunk_files_from_file(path):
    """
    Valida que el archivo:
    - Existe
    - Es un .md
    - Es un archivo (no directorio)
    
    Retorna: [path] (lista con 1 elemento)
    """
```

### Función para Directorios: `get_chunk_files_from_directory(path)`

```python
def get_chunk_files_from_directory(path):
    """
    Busca todos los .md recursivamente.
    Soporta rutas absolutas, relativas, y nombres simples.
    
    Retorna: [archivo1, archivo2, ...] (lista de rutas)
    """
```

---

## Flujo Completo

```
Tu archivo markdown
      ↓
Python detecta: ¿archivo o directorio?
      ↓ (NUEVO: soporta ambos)
get_chunk_files() 
├─ Si es .md → get_chunk_files_from_file()
├─ Si es carpeta → get_chunk_files_from_directory()
└─ Retorna: lista de archivos
      ↓
process_chunks() → 8 fases intactas
├─ Parsea YAML
├─ Valida metadata
├─ Genera embedding (3072D)
└─ Prepara vector
      ↓
upsert_vectors() → Pinecone
      ↓
generate_chunk_registry() → registry.json
      ↓
✅ Listo para Bot + Query Agent
```

---

## Casos Prácticos

### Caso A: Agregar 1 chunk nuevo

```bash
# Creaste: /tmp/sql_injection.md
cat /tmp/sql_injection.md
# ---
# chunk_id: technique::web::sql::injection::001
# domain: web
# chunk_type: technique
# tags: [sql]
# ---
# ### SQL Injection
# ...

# Vectorizalo
python3 /root/.openskills/vectorize_canonical_openai.py /tmp/sql_injection.md

# ✅ En 2-3 segundos
# ✅ Bot lo ve inmediatamente
# ✅ Registry actualizado
```

### Caso B: Agregar 10 chunks juntos

```bash
# Carpeta con 10 archivos
ls ~/nuevos_chunks/
# wifi.md, dns.md, dhcp.md, ... (10 archivos)

# Vectorizalos todos
python3 /root/.openskills/vectorize_canonical_openai.py ~/nuevos_chunks/

# ✅ En 15-25 segundos
# ✅ Los 10 en Pinecone
# ✅ Registry con los 10
```

### Caso C: Actualizar 1 chunk

```bash
# Editaste el archivo
nano hotkeys_001.md

# Re-vectorizalo
python3 /root/.openskills/vectorize_canonical_openai.py hotkeys_001.md

# ✅ Vector sobrescrito
# ✅ Registry sincronizado
```

---

## Registry Auto-Update

Cada vez que corres el vectorizer (archivo o directorio):

1. Lee todos los chunks procesados
2. Extrae `chunk_id` de cada uno
3. Mapea `chunk_id` → ruta del archivo
4. **Sobrescribe** `/home/kali/Desktop/RAG/chunk_registry.json`

**Resultado:**
```json
{
  "reference::linux::shortcuts::hotkeys::001": "/home/mi_archivo.md",
  "technique::web::sql::injection::001": "/tmp/sql_injection.md",
  ...
}
```

Bot y Query Agent leen este registry automáticamente.

---

## Performance

| Operación | Tiempo |
|-----------|--------|
| 1 archivo | 2-3 seg |
| 5 archivos | 5-8 seg |
| 20 archivos | 15-25 seg |
| Upsert Pinecone | ~1 seg |
| Registry update | ~0.5 seg |

---

## Checklist Antes de Vectorizar

- ✅ Archivo tiene extensión `.md`
- ✅ Tiene YAML frontmatter (`---` al inicio)
- ✅ Tiene `chunk_id` (OBLIGATORIO)
- ✅ Formato chunk_id: `namespace::domain::subdomain::intent::nnn`
- ✅ chunk_id es único (no duplicado)
- ✅ Archivo es válido (no corrupto)

---

## Integración Automática

Después de vectorizar:

✅ **Telegram Bot** - Automáticamente ve el nuevo chunk
✅ **Query Agent** - Puede buscar el nuevo chunk
✅ **Registry** - Se actualiza automáticamente
✅ **Local Files** - Bot lee desde filesystem

**No requiere reiniciar nada - todo automático!**

---

## Ventajas vs Antes

| Antes | Ahora |
|-------|-------|
| Solo directorios | Directorios + archivos individuales |
| Uno a la vez | 1 archivo o 100 archivos |
| Inflexible | Detección automática |
| 3 formas | 3 formas + auto-detect |
| Manual | Totalmente automático |

---

## Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `Archivo no encontrado` | Ruta incorrecta | Verifica ruta absoluta |
| `No es un archivo markdown` | Extensión no es .md | Cambia a `.md` |
| `Missing chunk_id` | Falta YAML | Agrega frontmatter |
| `No YAML frontmatter` | No comienza con `---` | Agrega `---` al inicio |
| `PINECONE_API_KEY not found` | Falta env file | Crea `/root/.openskills/env/pinecone.env` |

---

**Sistema modular, flexible y potente. Un script para todo.** 🚀
