# RAG con Gemini Embeddings + Pinecone

Guía completa para configurar un sistema de consulta RAG usando Google Gemini Embeddings (3072 dimensiones) y Pinecone.

---

## Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Script Explicado](#script-explicado)
- [Uso](#uso)
- [Precios](#precios)
- [Troubleshooting](#troubleshooting)

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         FLUJO DE QUERY                          │
└─────────────────────────────────────────────────────────────────┘

    Usuario ingresa query
            │
            ▼
    ┌───────────────────┐
    │  Gemini API       │  ← Genera embedding (3072D)
    │  gemini-          │     - Costo: $0.15/1M tokens
    │  embedding-001    │     - Input: texto
    └─────────┬─────────┘     - Output: vector[3072]
              │
              ▼
    ┌───────────────────┐
    │  Pinecone Index   │  ← Búsqueda semántica
    │  rag-canonical-   │     - Dimensiones: 3072
    │  v1-emb3large     │     - Vectores: 147+
    └─────────┬─────────┘     - Namespace: __default__
              │
              ▼
    ┌───────────────────┐
    │  Metadata         │  ← Resultados
    │  - chunk_id       │     - Contenido embebido
    │  - domain         │     - Tags, confidence
    │  - content        │     - Score de similitud
    └───────────────────┘
```

### Componentes

| Componente | Propósito | Ubicación |
|------------|-----------|-----------|
| `gemini.env` | API key de Google | `/root/.openskills/env/` |
| `pinecone.env` | API key de Pinecone | `/root/.openskills/env/` |
| `query_gemini.py` | Script de consulta | `src/query_gemini.py` |
| `rag-gemini` | Comando global | `/usr/local/bin/rag-gemini` |

---

## Requisitos Previos

### API Keys Necesarias

1. **Google AI Studio** (Gemini)
   - Ir a: https://aistudio.google.com/apikey
   - Crear API key
   - Modelo: `gemini-embedding-001`

2. **Pinecone**
   - Ir a: https://app.pinecone.io/
   - Crear API key
   - Índice existente: `rag-canonical-v1-emb3large` (3072D)

### Sistema

```bash
# Python 3.11+
python3 --version

# Entorno virtual existente
/root/.openskills/venv/
```

---

## Instalación

### Paso 1: Instalar SDK de Google Genai

```bash
source /root/.openskills/venv/bin/activate
pip install google-genai
```

**Paquetes instalados:**
- `google-genai` - SDK oficial de Google AI
- `google-auth` - Autenticación
- `pydantic` - Validación de datos (v2)

### Paso 2: Verificar Instalación

```bash
python3 -c "from google import genai; print('✅ google-genai OK')"
python3 -c "from pinecone import Pinecone; print('✅ pinecone OK')"
```

---

## Configuración

### Paso 1: Crear archivo de environment para Gemini

```bash
# Crear directorio si no existe
mkdir -p /root/.openskills/env

# Crear archivo de configuración
cat > /root/.openskills/env/gemini.env << 'EOF'
GOOGLE_API_KEY=tu_api_key_aqui
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
GEMINI_EMBEDDING_DIM=3072
EOF
```

**Reemplazar `tu_api_key_aqui` con tu API key de Google AI Studio.**

### Paso 2: Verificar Pinecone Environment

```bash
# Verificar que existe
cat /root/.openskills/env/pinecone.env
```

Debe contener:
```
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX=rag-canonical-v1-emb3large
PINECONE_NAMESPACE=
```

### Paso 3: Proteger API Keys

Agregar al `.gitignore`:

```bash
# En /home/kali/Desktop/RAG/.gitignore
echo "gemini.env" >> .gitignore
```

---

## Script Explicado

### Ubicación

```
/home/kali/Desktop/RAG/src/query_gemini.py
```

### Código Completo con Explicaciones

```python
#!/usr/bin/env python3
"""
Query Pinecone usando Gemini Embeddings (3072 dimensiones).

FLUJO:
1. Cargar API keys desde archivos .env
2. Generar embedding con Gemini API
3. Consultar Pinecone con el vector
4. Formatear y mostrar resultados

MODELO: gemini-embedding-001
- Dimensiones: 3072 (compatible con OpenAI text-embedding-3-large)
- Precio: $0.15/1M tokens
- Input máximo: 2048 tokens

ÍNDICE COMPATIBLE: rag-canonical-v1-emb3large
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai
from google.genai import types

# ============================================================
# CONFIGURACIÓN DE PATHS
# ============================================================

GEMINI_ENV_PATH = "/root/.openskills/env/gemini.env"
PINECONE_ENV_PATH = "/root/.openskills/env/pinecone.env"

# Valores por defecto
DEFAULT_INDEX = "rag-canonical-v1-emb3large"
DEFAULT_NAMESPACE = ""  # Namespace vacío = __default__


# ============================================================
# CARGA DE VARIABLES DE ENTORNO
# ============================================================

def load_env():
    """
    Carga las variables de entorno desde los archivos .env
    
    Returns:
        tuple: (google_api_key, pinecone_api_key)
    
    Raises:
        ValueError: Si alguna API key no está configurada
    """
    # Cargar ambos archivos .env
    load_dotenv(GEMINI_ENV_PATH)
    load_dotenv(PINECONE_ENV_PATH)
    
    # Verificar Google API Key
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in gemini.env")
    
    # Verificar Pinecone API Key
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY not found in pinecone.env")
    
    return google_api_key, pinecone_api_key


# ============================================================
# GENERACIÓN DE EMBEDDINGS CON GEMINI
# ============================================================

def get_gemini_embedding(text: str, api_key: str) -> list:
    """
    Genera un embedding de 3072 dimensiones usando Gemini.
    
    Args:
        text: Texto a convertir en vector
        api_key: API key de Google AI Studio
    
    Returns:
        list: Vector de 3072 dimensiones
    
    Modelo: gemini-embedding-001
    - task_type="RETRIEVAL_QUERY": Optimizado para búsquedas
    - output_dimensionality=3072: Máxima resolución
    """
    client = genai.Client(api_key=api_key)
    
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",      # Optimizado para queries
            output_dimensionality=3072        # 3072 dimensiones
        )
    )
    
    return result.embeddings[0].values


# ============================================================
# CONSULTA A PINECONE
# ============================================================

def query_pinecone(embedding: list, index_name: str, namespace: str, top_k: int = 5):
    """
    Realiza una búsqueda vectorial en Pinecone.
    
    Args:
        embedding: Vector de consulta (3072D)
        index_name: Nombre del índice Pinecone
        namespace: Namespace dentro del índice
        top_k: Número de resultados a retornar
    
    Returns:
        dict: Resultados de Pinecone con matches y metadata
    
    Nota:
        - include_metadata=True: Retorna toda la metadata almacenada
        - La metadata incluye 'content' con el texto completo
    """
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    
    results = index.query(
        vector=embedding,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True    # Incluir metadata completa
    )
    return results


# ============================================================
# FORMATEO DE RESULTADOS
# ============================================================

def format_results(results) -> str:
    """
    Formatea los resultados para mostrar en terminal.
    
    Args:
        results: Resultados de Pinecone query
    
    Returns:
        str: Resultados formateados en Markdown
    
    Metadata disponible por resultado:
        - chunk_id: Identificador único
        - domain: Dominio de conocimiento
        - chunk_type: Tipo de contenido
        - tags: Etiquetas
        - content: Texto completo (← clave: no necesita archivos locales)
        - confidence: Nivel de confianza
    """
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"Found {len(results['matches'])} results")
    output.append(f"{'='*60}\n")
    
    for i, match in enumerate(results['matches'], 1):
        metadata = match.get('metadata', {})
        score = match.get('score', 0)
        
        # Header del resultado
        output.append(f"### Result {i} (Score: {score:.4f})")
        output.append(f"- **chunk_id**: {metadata.get('chunk_id', 'N/A')}")
        output.append(f"- **domain**: {metadata.get('domain', 'N/A')}")
        output.append(f"- **chunk_type**: {metadata.get('chunk_type', 'N/A')}")
        output.append(f"- **tags**: {metadata.get('tags', [])}")
        
        # Contenido embebido en metadata (no lee archivos locales)
        content = metadata.get('content', '')
        if content:
            preview = content[:800] + "..." if len(content) > 800 else content
            output.append(f"\n**Content:**\n{preview}\n")
        
        output.append("-" * 40)
    
    return "\n".join(output)


# ============================================================
# UTILIDADES
# ============================================================

def list_pinecone_indexes():
    """
    Lista todos los índices disponibles en Pinecone.
    Muestra dimensiones y cantidad de vectores.
    """
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indexes = pc.list_indexes()
    
    print("\n📋 Available Pinecone indexes:")
    for idx in indexes:
        index = pc.Index(idx.name)
        stats = index.describe_index_stats()
        print(f"  - {idx.name}: {stats.get('dimension', '?')}D, {stats.get('total_vector_count', 0)} vectors")
        
        # Mostrar namespaces
        namespaces = stats.get('namespaces', {})
        for ns, info in namespaces.items():
            ns_name = ns if ns else "__default__"
            print(f"      └─ {ns_name}: {info.get('vector_count', 0)} vectors")
    
    return indexes


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Query Pinecone with Gemini embeddings (3072D)"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--index", default=DEFAULT_INDEX, help="Pinecone index")
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE, help="Namespace")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument("--list-indexes", action="store_true", help="List indexes")
    
    args = parser.parse_args()
    
    # Cargar API keys
    google_api_key, pinecone_api_key = load_env()
    
    # Modo: listar índices
    if args.list_indexes:
        list_pinecone_indexes()
        return
    
    # Validar query
    if not args.query:
        parser.print_help()
        print("\n📝 Example: python3 query_gemini.py 'LFI exploitation techniques'")
        return
    
    # Verbose: mostrar configuración
    if args.verbose:
        print(f"\n🔍 Generating embedding with Gemini...")
    
    # Paso 1: Generar embedding
    embedding = get_gemini_embedding(args.query, google_api_key)
    
    if args.verbose:
        print(f"   Embedding: {len(embedding)} dimensions")
        print(f"   Index: {args.index}")
        print(f"   Namespace: {args.namespace or '__default__'}")
    
    # Paso 2: Query Pinecone
    print(f"\n🔎 Querying: \"{args.query}\"")
    results = query_pinecone(embedding, args.index, args.namespace, args.top_k)
    
    # Paso 3: Mostrar resultados
    print(format_results(results))


if __name__ == "__main__":
    main()
```

### Puntos Clave del Script

#### 1. Sin API Keys Hardcodeadas

```python
# ✅ CORRECTO: Cargar desde environment
google_api_key = os.getenv("GOOGLE_API_KEY")

# ❌ INCORRECTO: Hardcodeado
api_key = "AIzaSy..."  # NUNCA hacer esto
```

#### 2. Content embebido en Metadata

```python
# El contenido viene directo de Pinecone, no de archivos locales
content = metadata.get('content', '')
```

**Ventaja:** No depende de `chunk_registry.json` ni archivos locales.

#### 3. Task Type Optimizado

```python
config=types.EmbedContentConfig(
    task_type="RETRIEVAL_QUERY",  # Optimizado para búsquedas
    output_dimensionality=3072    # Máxima calidad
)
```

---

## Uso

### Comando Global

```bash
# Query básica
rag-gemini "tu búsqueda"

# Más resultados
rag-gemini "LFI exploitation" --top-k 10

# Modo verbose
rag-gemini "git commands" -v

# Listar índices
rag-gemini --list-indexes
```

### Uso Directo del Script

```bash
source /root/.openskills/venv/bin/activate
python3 /home/kali/Desktop/RAG/src/query_gemini.py "query"
```

### Ejemplo de Output

```
🔎 Querying: "git commands"

============================================================
Found 2 results
============================================================

### Result 1 (Score: 0.0353)
- **chunk_id**: cli::english::recovery::undo-commit::001
- **domain**: cli
- **chunk_type**: guide
- **tags**: ['git', 'revert', 'reset', 'undo-commit', 'english']

**Content:**
## Undo a Commit (Before Pushing)

```bash
# Option 1: Keep changes, undo commit only
git reset --soft HEAD~1

# Option 2: Discard everything (PERMANENT)
git reset --hard HEAD~1
```

----------------------------------------
```

---

## Precios

### Gemini Embeddings

| Métrica | Valor |
|---------|-------|
| Precio | $0.15 por 1M tokens |
| Query típica | ~10 tokens |
| 100,000 queries | ~$0.15 |

### Pinecone (Free Tier)

| Métrica | Límite |
|---------|--------|
| Queries/mes | 100,000 |
| Vectores | 100,000 |
| Almacenamiento | Ilimitado |

### Comparativa de Modelos

| Modelo | Precio/M tokens | Dimensiones |
|--------|-----------------|-------------|
| `gemini-embedding-001` | $0.15 | 3072 |
| `text-embedding-3-large` (OpenAI) | $0.13 | 3072 |
| `text-embedding-3-small` (OpenAI) | $0.02 | 1536 |

---

## Troubleshooting

### Error: "GOOGLE_API_KEY not found"

```bash
# Verificar archivo
cat /root/.openskills/env/gemini.env

# Verificar contenido
GOOGLE_API_KEY=AIzaSy...  # Debe tener valor real
```

### Error: "ModuleNotFoundError: No module named 'google'"

```bash
source /root/.openskills/venv/bin/activate
pip install google-genai
```

### Error: "Dimension mismatch"

El índice debe tener 3072 dimensiones:

```bash
rag-gemini --list-indexes

# Output esperado:
# rag-canonical-v1-emb3large: 3072D, 147 vectors
```

### Error: "Namespace not found"

```bash
# Verificar namespaces disponibles
rag-gemini --list-indexes

# Usar namespace correcto
rag-gemini "query" --namespace "__default__"
```

### Error: "Import 'google.genai' could not be resolved"

Esto es un error del LSP (Language Server Protocol), no afecta la ejecución. El script funciona correctamente.

---

## Archivos Creados

```
/root/.openskills/env/
└── gemini.env                    # API key de Google

/home/kali/Desktop/RAG/
├── src/
│   └── query_gemini.py          # Script principal
└── .gitignore                   # Actualizado con gemini.env

/usr/local/bin/
└── rag-gemini                   # Comando global
```

---

## Notas Importantes

1. **Sin Chunk Registry**: Este sistema no usa `chunk_registry.json`. El contenido viene embebido en la metadata de Pinecone.

2. **API Keys Protegidas**: Los archivos `.env` están en `.gitignore`. Nunca subir API keys a GitHub.

3. **Índice Compatible**: Solo funciona con índices de 3072 dimensiones (OpenAI text-embedding-3-large o Gemini embedding-001).

4. **Costos Mínimos**: Para uso personal, el costo es prácticamente gratuito ($0.15/1M tokens).

---

## Próximos Pasos

- [ ] Agregar más vectores al índice
- [ ] Crear índice alternativo con embeddings locales (gratis)
- [ ] Integrar con Telegram bot para queries remotas
- [ ] Agregar filtros por metadata (domain, tags, etc.)

---

**Creado:** 2026-02-22  
**Modelo:** gemini-embedding-001 (3072D)  
**Índice:** rag-canonical-v1-emb3large
