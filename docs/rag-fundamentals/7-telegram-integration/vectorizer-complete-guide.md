# Vectorizer Script Complete Guide (OpenAI 3072D)

## Overview

The vectorizer script is the **core engine** that transforms your markdown chunks into searchable vectors in Pinecone. It's the first step in the RAG pipeline that makes your knowledge base available through Telegram Bot and Query Agent.

```
Your Chunks (.md files)
        ↓
  Vectorizer Script
  (vectorize_canonical_openai.py)
        ↓
  OpenAI text-embedding-3-large (3072D)
        ↓
  Pinecone Index (rag-canonical-v1-emb3large)
        ↓
  chunk_registry.json (for local file mapping)
        ↓
  Telegram Bot + Query Agent (ready to search)
```

---

## What the Script Does

### Input
- **Chunk files** (`.md` with YAML frontmatter)
- **Any directory path** (absolute, relative, or just name)

### Process
1. Load API keys (Pinecone + OpenAI)
2. Find all `.md` files recursively
3. Parse YAML frontmatter from each chunk
4. Validate metadata (minimum: `chunk_id`)
5. Generate 3072D embeddings (OpenAI text-embedding-3-large)
6. Upload vectors to Pinecone index
7. Auto-generate `chunk_registry.json` mapping chunk_id → file paths

### Output
- **Pinecone**: 15 vectors (example) with full content in metadata
- **Local**: `chunk_registry.json` for Telegram Bot and Query Agent to read files locally

---

## Script Architecture - 8 Phases

### Phase 1: Load API Keys

```python
def load_api_keys():
    """
    Carga Pinecone y OpenAI API keys desde archivos de entorno
    
    Flujo:
    1. Lee /root/.openskills/env/pinecone.env
    2. Busca línea que contiene "PINECONE_API_KEY="
    3. Extrae el valor después del "="
    4. Repite para OpenAI en openai.env
    5. Valida que ambas claves existan
    """
    with open("/root/.openskills/env/pinecone.env") as f:
        # Abre archivo de configuración
        pinecone_key = None
        for line in f:
            # Itera cada línea del archivo
            if "PINECONE_API_KEY=" in line:
                # Busca la línea que contiene la clave
                pinecone_key = line.split("=")[1].strip()
                # Divide por "=" y toma la parte derecha
                # .strip() elimina espacios en blanco
                break
                # Detiene la búsqueda

    with open("/root/.openskills/env/openai.env") as f:
        # Repite para OpenAI
        openai_key = None
        for line in f:
            if "OPENAI_API_KEY=" in line:
                openai_key = line.split("=")[1].strip()
                break

    # Validación: si faltan claves, sale del programa
    if not pinecone_key or not openai_key:
        print("❌ ERROR: API keys no encontradas")
        sys.exit(1)
        # sys.exit(1) = salida de error

    return pinecone_key, openai_key
    # Retorna un tuple con ambas claves
```

**Why this matters**: API keys are stored separately for security. This function reads them at runtime instead of hardcoding them.

---

### Phase 2: Discover Chunk Files

```python
def get_chunk_files(path):
    """
    Busca todos los archivos *.md recursivamente en cualquier ruta
    
    Soporta:
    - Rutas absolutas: /home/kali/Desktop/RAG/cheatsheets
    - Rutas relativas: ./chunks
    - Solo nombres: cheatsheets (busca en /home/kali/Desktop/RAG/)
    """
    # Determina si la ruta es absoluta o relativa
    if os.path.isabs(path) or path.startswith("./"):
        # Si es absoluta (emppieza con /) o relativa (./)
        chunks_dir = path
        # Úsala directamente
    else:
        # Si es solo un nombre (ej: "cheatsheets")
        chunks_dir = f"/home/kali/Desktop/RAG/{path}"
        # Asume que está en el directorio base

    # Verifica que el directorio existe
    if not os.path.exists(chunks_dir):
        print(f"❌ ERROR: Directorio no encontrado: {chunks_dir}")
        sys.exit(1)

    # glob.glob() busca archivos que coinciden con un patrón
    chunk_files = sorted(
        glob.glob(f"{chunks_dir}/**/*.md", recursive=True)
        # **/*.md = busca cualquier .md en cualquier subdirectorio
        # recursive=True = busca en subdirectorios
    )

    # Valida que encontró archivos
    if not chunk_files:
        print(f"❌ ERROR: No se encontraron archivos .md")
        sys.exit(1)

    return chunk_files
    # Retorna lista de rutas (sorted = ordenadas alfabéticamente)
```

**Flexibility**: This is why the script works with ANY directory - it doesn't enforce a specific structure.

---

### Phase 3: Validate Metadata

```python
def validate_metadata(metadata):
    """
    Comprueba que el chunk tenga al menos 'chunk_id'
    
    El chunk_id es OBLIGATORIO porque:
    - Es el identificador único del vector en Pinecone
    - Se usa como clave en chunk_registry.json
    - El Telegram bot lo usa para leer archivos locales
    """
    if "chunk_id" not in metadata:
        # Si no existe la clave 'chunk_id'
        return False, "Missing chunk_id"
        # Retorna (falso, mensaje de error)

    return True, "Valid"
    # Retorna (verdadero, mensaje de éxito)
```

**Critical Field**: `chunk_id` is the only required field. Everything else is optional metadata.

---

### Phase 4: Generate Embeddings

```python
def generate_embedding(client, text):
    """
    Genera un embedding de 3072 dimensiones 
    usando OpenAI text-embedding-3-large
    
    Embedding = representación numérica del texto
    3072D = 3072 números que representan el significado
    
    Ejemplo:
    Texto: "chmod u+x script.sh"
    ↓
    Embedding: [0.234, -0.891, 0.123, ..., 0.456] (3072 números)
    """
    response = client.embeddings.create(
        # Llama a la API de OpenAI
        model="text-embedding-3-large",
        # Modelo más avanzado de OpenAI para RAG
        # Otros modelos:
        #   - text-embedding-3-small (1536D, más rápido, menos preciso)
        #   - text-embedding-ada-002 (legacy)
        input=text,
        # El texto a convertir en embedding
        dimensions=3072
        # Dimensión exacta = 3072 (máximo para este modelo)
    )
    return response.data[0].embedding
    # Extrae el vector del response y lo retorna
```

**Why 3072D?**: This is the highest quality embedding OpenAI offers. It's best for semantic search and RAG systems.

---

### Phase 5: Process Chunks

```python
def process_chunks(machine_name, chunk_files, pinecone_key, openai_key):
    """
    Itera sobre cada chunk:
    1. Lee el archivo
    2. Parsea YAML frontmatter
    3. Valida metadata
    4. Genera embedding (frontmatter + body)
    5. Prepara vector para upsert a Pinecone
    """
    # Inicializa cliente de Pinecone
    pc = Pinecone(api_key=pinecone_key)
    # Conexión a Pinecone
    idx = pc.Index("rag-canonical-v1-emb3large")
    # Conecta al índice específico (no crea, debe existir)
    
    # Inicializa cliente de OpenAI
    client = OpenAI(api_key=openai_key)
    # Para generar embeddings

    vectors_to_upsert = []
    # Lista que acumulará todos los vectores
    success_count = 0
    error_count = 0

    print(f"\n📁 Procesando {len(chunk_files)} chunks\n")

    for chunk_file in chunk_files:
        # Itera cada archivo .md
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                # Abre el archivo en modo lectura
                # encoding="utf-8" = soporte para caracteres especiales
                content = f.read()
                # Lee TODO el contenido del archivo

            # VALIDACIÓN 1: Verifica que tenga frontmatter YAML
            if not content.startswith("---"):
                # Debe empezar con --- (marcador YAML)
                print(f"⚠️  {Path(chunk_file).name}: No YAML frontmatter")
                error_count += 1
                continue
                # Salta a la siguiente iteración

            # PARSEO: Extrae frontmatter y body
            parts = content.split("---", 2)
            # Divide el contenido por "---" en máximo 3 partes
            # Parte 0: vacía (antes del primer ---)
            # Parte 1: YAML frontmatter
            # Parte 2: body (contenido)
            
            metadata_str = parts[1]
            # El YAML crudo (como texto)
            body = parts[2] if len(parts) > 2 else ""
            # El contenido después del frontmatter
            # Si no hay body, asigna string vacío

            metadata = yaml.safe_load(metadata_str)
            # Convierte el YAML a diccionario Python
            # Ejemplo:
            #   YAML: chunk_id: reference::linux::chmod::001
            #   Python: {"chunk_id": "reference::linux::chmod::001"}

            # VALIDACIÓN 2: Verifica que tenga chunk_id
            is_valid, msg = validate_metadata(metadata)
            if not is_valid:
                print(f"❌ {metadata.get('chunk_id', 'UNKNOWN')}: {msg}")
                error_count += 1
                continue

            # GENERACIÓN DE EMBEDDING
            # 🔹 Convertir todo el frontmatter a texto
            metadata_text = " ".join(f"{k}: {v}" for k, v in metadata.items())
            # Crea string con todos los campos de metadata
            # Ejemplo: "chunk_id: reference::linux... domain: linux..."
            
            text_to_embed = f"{metadata_text} {body.strip()}"
            # Combina metadata + body para el embedding
            # Esto permite buscar por metadata Y contenido simultáneamente
            # .strip() = elimina espacios en blanco al inicio/fin

            # Generar embedding (3072D)
            embedding = generate_embedding(client, text_to_embed)
            # Llama a OpenAI para generar el vector

            # PREPARACIÓN DEL VECTOR para Pinecone
            vectors_to_upsert.append({
                "id": metadata["chunk_id"],
                # ID único = el chunk_id
                "values": embedding,
                # El vector (3072 números)
                "metadata": {
                    **metadata,
                    # ** = "unpacking" (copia todos los campos de metadata)
                    "content": body.strip(),
                    # Almacena el contenido completo en metadata
                    # IMPORTANTE: Sin truncamiento
                    "content_length": len(body.strip()),
                    # Longitud para estadísticas
                },
            })
            # Este diccionario se enviará a Pinecone

            print(f"✅ {metadata['chunk_id']} (3072D)")
            success_count += 1

        except Exception as e:
            # Captura cualquier error
            print(f"❌ {Path(chunk_file).name}: {str(e)}")
            error_count += 1
            continue

    return vectors_to_upsert, success_count, error_count
    # Retorna: lista de vectores, contador de éxitos, contador de errores
```

**Key Innovation**: Including entire frontmatter in the embedding allows semantic search across metadata AND content simultaneously.

---

### Phase 6: Upsert to Pinecone

```python
def upsert_vectors(vectors, pinecone_key):
    """
    Sube los vectores a Pinecone en el namespace root (__default__)
    
    Upsert = Update (si existe) + Insert (si es nuevo)
    """
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")

    print(f"\n📤 Subiendo {len(vectors)} vectores\n")

    batch_size = 100
    # Procesa en lotes de 100 vectores (límite de Pinecone)
    
    for i in range(0, len(vectors), batch_size):
        # range(0, 300, 100) = [0, 100, 200]
        # i = posición de inicio de cada lote
        
        batch = vectors[i : i + batch_size]
        # Extrae 100 vectores (desde posición i hasta i+100)
        # Esto es slicing de listas en Python

        # CRÍTICO: No usar namespace=, todo va a __default__
        idx.upsert(vectors=batch)
        # Sube el lote a Pinecone
        # __default__ = namespace root (no especificado = default)

        print(f"  ✅ Batch {i // batch_size + 1} ({len(batch)} vectores)")
        # i // 100 + 1 = número del lote (división entera)
        # Ejemplo: i=100 → 100//100+1 = 2 (lote número 2)
```

**Why batches?**: Pinecone has limits on request size. Batching ensures reliability and optimal performance.

---

### Phase 7: Verify Index

```python
def verify_index(pinecone_key, machine_name):
    """
    Verifica que los vectores se hayan indexado correctamente
    y muestra estadísticas
    """
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")

    stats = idx.describe_index_stats()
    # Obtiene estadísticas del índice
    
    print(f"\n📊 Estadísticas del índice:")
    print(f"  Total vectores: {stats['total_vector_count']}")
    # Todos los vectores en el índice
    print(f"  Namespaces: {list(stats['namespaces'].keys())}")
    # Namespaces activos (__default__ siempre existe)

    # Verificación opcional por IDs
    all_ids = []
    for id_batch in idx.list():
        # idx.list() retorna batches de IDs
        all_ids.extend(id_batch)
        # extend() agrega todos los IDs a la lista

    machine_vectors = [id for id in all_ids if f"::{machine_name}::" in id]
    # List comprehension: filtro de IDs que contienen el nombre de máquina
    # Ejemplo: si machine_name="facts", filtra los que tengan "::facts::"
    
    print(f"  Vectores indexados: {len(machine_vectors)}")
```

**Verification**: This confirms the vectors were successfully uploaded before moving to the next phase.

---

### Phase 8A: Generate Chunk Registry

```python
def generate_chunk_registry(chunk_files):
    """
    Generar chunk_registry.json que mapea chunk_ids a rutas de archivos
    
    Este registry es CRÍTICO porque:
    1. Telegram Bot lo usa para leer archivos locales (no solo metadata)
    2. Query Agent lo usa para obtener contenido completo
    3. Fallback chain: intenta local file primero, luego metadata
    
    Ejemplo de output:
    {
      "reference::linux::permissions::chmod-user::001": 
        "/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md",
      "reference::linux::permissions::chmod-group::001":
        "/root/.openskills/CHEATSHEETS CHUNKS/chmod-group_001.md"
    }
    """
    import re
    # Para buscar patrones con expresiones regulares

    registry = {}
    # Diccionario vacío para almacenar mapping

    for chunk_file in chunk_files:
        # Itera cada archivo
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Buscar chunk_id en el frontmatter
            match = re.search(r"chunk_id:\s*(.+?)\n", content)
            # r"..." = raw string (no procesa escapes)
            # chunk_id: = busca esta literal
            # \s* = cualquier cantidad de espacios
            # (.+?) = captura 1+ caracteres (no greedy)
            # \n = hasta el salto de línea
            
            if match:
                # Si encontró el patrón
                chunk_id = match.group(1).strip()
                # group(1) = lo capturado dentro de ()
                # .strip() = elimina espacios
                
                registry[chunk_id] = str(chunk_file)
                # Mapea chunk_id → ruta del archivo
        
        except Exception as e:
            # Si hay error leyendo el archivo
            print(f"⚠️  Error leyendo {chunk_file}: {e}")
            continue
            # Continúa con el siguiente archivo

    return registry
    # Retorna el diccionario mapeado


def save_chunk_registry(registry, registry_path):
    """
    Guardar registry como JSON
    
    El JSON es un formato estándar que puede leer:
    - Telegram Bot (Python)
    - Query Agent (Python)
    - Cualquier otra herramienta
    """
    import json
    from pathlib import Path

    # Crear directorio si no existe
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    # .parent = directorio padre
    # parents=True = crea directorios intermedios si faltan
    # exist_ok=True = no falla si ya existe

    with open(registry_path, "w") as f:
        # Abre archivo en modo escritura
        json.dump(registry, f, indent=2)
        # dump = escribe el diccionario como JSON
        # indent=2 = formatea con 2 espacios (legible)

    print(f"✅ Chunk registry guardado: {registry_path}")
    print(f"   Total chunks mapeados: {len(registry)}")
```

**Why This Matters**: This registry file is what makes the Telegram Bot able to read files locally instead of relying only on Pinecone metadata.

---

### Phase 8B: Main Execution

```python
def main():
    """
    Orquesta todas las fases del pipeline
    """
    
    # VALIDACIÓN: Verifica que el usuario pasó un argumento
    if len(sys.argv) < 2:
        # sys.argv[0] = nombre del script
        # sys.argv[1] = primer argumento del usuario
        # Si no hay argumento → len(sys.argv) = 1 (solo el script)
        
        print("Uso: python3 vectorize_canonical_openai.py <path>")
        print("Ejemplos:")
        print("  python3 vectorize_canonical_openai.py cheatsheets")
        print("  python3 vectorize_canonical_openai.py /home/kali/mi_carpeta/")
        print("  python3 vectorize_canonical_openai.py ./chunks")
        sys.exit(1)

    input_path = sys.argv[1]
    # Extrae el primer argumento (la ruta)

    # HEADER: Información visual
    print(f"\n{'=' * 70}")
    print(f"🧠 VECTORIZER (OpenAI text-embedding-3-large 3072D)")
    print(f"{'=' * 70}")
    print(f"Path: {input_path}")
    print(f"Index: rag-canonical-v1-emb3large")
    print(f"Model: text-embedding-3-large (3072D)")

    # FASE 1: Cargar credenciales
    pinecone_key, openai_key = load_api_keys()
    # Retorna tuple (pinecone_key, openai_key)

    # FASE 2: Buscar chunks
    chunk_files = get_chunk_files(input_path)
    # Retorna lista de rutas

    # FASE 5: Procesar chunks
    vectors, success, errors = process_chunks(
        input_path, chunk_files, pinecone_key, openai_key
    )
    # Retorna (lista de vectores, contador de éxitos, contador de errores)

    # VALIDACIÓN: Verifica que se generaron vectores
    if not vectors:
        print(f"\n❌ No se generaron vectores (errores: {errors})")
        sys.exit(1)

    # FASE 6: Subir vectores a Pinecone
    upsert_vectors(vectors, pinecone_key)

    # FASE 7: Verificar que se indexaron correctamente
    verify_index(pinecone_key, input_path)

    # FASE 8A: Generar chunk registry para Query Agent
    print(f"\n📝 Generando chunk registry...")
    registry = generate_chunk_registry(chunk_files)
    # Crea el diccionario mapping
    
    registry_path = Path("/home/kali/Desktop/RAG/chunk_registry.json")
    # Define dónde guardar el archivo
    
    save_chunk_registry(registry, registry_path)
    # Guarda el JSON

    # RESUMEN FINAL
    print(f"\n✅ ¡Vectorización completa!")
    print(f"   Success: {success}")
    print(f"   Errors: {errors}")
    print(f"   Total: {len(vectors)} vectores")
    print(f"   Registry: {registry_path}")


# ENTRY POINT: Punto de entrada del programa
if __name__ == "__main__":
    # Se ejecuta solo si el script es ejecutado directamente
    # (no si es importado como módulo)
    main()
```

---

## Usage Guide

### Basic Usage

```bash
# Opción 1: Solo el nombre (busca en /home/kali/Desktop/RAG/)
python3 /root/.openskills/vectorize_canonical_openai.py cheatsheets

# Opción 2: Ruta absoluta
python3 /root/.openskills/vectorize_canonical_openai.py /home/kali/Desktop/RAG/cheatsheets

# Opción 3: Ruta relativa
cd /home/kali && python3 /root/.openskills/vectorize_canonical_openai.py ./Desktop/RAG/cheatsheets

# Opción 4: Punto actual
python3 /root/.openskills/vectorize_canonical_openai.py ./chunks
```

### What Happens Step by Step

```
1. Script carga tus API keys
   └─ Busca en /root/.openskills/env/pinecone.env
   └─ Busca en /root/.openskills/env/openai.env

2. Descubre todos los .md en la carpeta
   └─ glob busca recursivamente
   └─ Encuentra 15 archivos (ejemplo)

3. Para cada archivo:
   └─ Lee el contenido
   └─ Parsea YAML frontmatter
   └─ Valida que tenga chunk_id
   └─ Genera embedding 3072D con OpenAI
   └─ Prepara vector para Pinecone

4. Sube vectores en lotes de 100
   └─ Batch 1: 100 vectores
   └─ Batch 2: 15 vectores (resto)

5. Verifica que se indexaron
   └─ Muestra estadísticas del índice

6. Genera chunk_registry.json
   └─ Mapea chunk_id → rutas de archivos
   └─ Guardado en /home/kali/Desktop/RAG/

7. Listo para usar con Telegram Bot y Query Agent
```

### Expected Output

```
======================================================================
🧠 VECTORIZER (OpenAI text-embedding-3-large 3072D)
======================================================================
Path: /root/.openskills/CHEATSHEETS CHUNKS/
Index: rag-canonical-v1-emb3large
Model: text-embedding-3-large (3072D)

📁 Procesando 15 chunks

✅ reference::linux::permissions::chmod-user::001 (3072D)
✅ reference::linux::permissions::chmod-group::001 (3072D)
... (13 más)

📤 Subiendo 15 vectores

  ✅ Batch 1 (15 vectores)

📊 Estadísticas del índice:
  Total vectores: 15
  Namespaces: ['__default__']
  Vectores indexados: 15

📝 Generando chunk registry...
✅ Chunk registry guardado: /home/kali/Desktop/RAG/chunk_registry.json
   Total chunks mapeados: 15

✅ ¡Vectorización completa!
   Success: 15
   Errors: 0
   Total: 15 vectores
   Registry: /home/kali/Desktop/RAG/chunk_registry.json
```

---

## chunk_registry.json Format

### What It Is

A JSON file that maps `chunk_id` → file paths. Essential for local file reading.

### Example Structure

```json
{
  "reference::linux::permissions::chmod-user::001": "/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md",
  "reference::linux::permissions::chmod-group::001": "/root/.openskills/CHEATSHEETS CHUNKS/chmod-group_001.md",
  "reference::linux::permissions::chmod-symbolic::001": "/root/.openskills/CHEATSHEETS CHUNKS/chmod-symbolic_001.md",
  "technique::linux::compression::001": "/root/.openskills/CHEATSHEETS CHUNKS/compression_001.md"
}
```

### How It's Used

```
Query comes in from Telegram
        ↓
Telegram Bot searches Pinecone
        ↓
Gets back chunk_id (e.g., "reference::linux::permissions::chmod-user::001")
        ↓
Looks up in chunk_registry.json
        ↓
Finds file path: "/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md"
        ↓
Reads file locally (gets COMPLETE content)
        ↓
Sends to Telegram (full content, not truncated)
```

---

## Integration with Telegram Bot

The vectorizer output feeds into three components:

### 1. **Telegram Bot** (`telegram_bot.py`)
- Reads `chunk_registry.json` at startup
- When query arrives:
  1. Generate embedding with OpenAI (same model: 3072D)
  2. Search Pinecone with that embedding
  3. Get back chunk_id from results
  4. Look up chunk_id in registry
  5. Read file locally
  6. Send complete content to Telegram

### 2. **Query Agent** (`query-agent-hybrid.py`)
- Reads registry to find local files
- Generates markdown reports with full content
- Optionally sends to Telegram

### 3. **Pinecone Index** (`rag-canonical-v1-emb3large`)
- Stores vectors (3072D)
- Stores metadata (including full content)
- Fallback if local file doesn't exist

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No markdown files found" | Wrong directory | Check path exists and has `.md` files |
| "Missing chunk_id" | Chunk lacks `chunk_id` field in YAML | Add `chunk_id: reference::...::001` to frontmatter |
| "PINECONE_API_KEY not found" | Missing env file | Create `/root/.openskills/env/pinecone.env` |
| "OPENAI_API_KEY not found" | Missing env file | Create `/root/.openskills/env/openai.env` |
| Registry not updated | Permissions issue | Check write access to `/home/kali/Desktop/RAG/` |
| Vectors not searchable | Index doesn't exist | Create index `rag-canonical-v1-emb3large` in Pinecone |

---

## Next Steps

1. **Prepare chunks** with YAML frontmatter (minimum: `chunk_id`)
2. **Run vectorizer**: `python3 /root/.openskills/vectorize_canonical_openai.py <path>`
3. **Verify output**: Check `chunk_registry.json` was created
4. **Start Telegram Bot**: Bot automatically reads the registry
5. **Query via Telegram**: `/q <your_query>`

---

## Key Takeaways

✅ **Script is flexible**: Works with any directory structure  
✅ **Embedding includes metadata + body**: Better semantic search  
✅ **Registry is auto-generated**: No manual step needed  
✅ **OpenAI 3072D**: Highest quality embeddings available  
✅ **Complete content stored**: In Pinecone metadata + local files  
✅ **Telegram bot ready**: After vectorization, bot can search immediately
