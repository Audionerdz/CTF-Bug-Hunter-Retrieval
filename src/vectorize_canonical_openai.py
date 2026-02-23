#!/usr/bin/env python3
"""
OFFICIAL VECTORIZER (FULL FRONTMATTER + BODY):
Canonical Schema → 3072D OpenAI → rag-canonical-v1-emb3large

Este script procesa chunks (directorios O archivos individuales),
valida su metadata canónica, genera embeddings de 3072 dimensiones
usando OpenAI text-embedding-3-large, y los sube al índice Pinecone
'rag-canonical-v1-emb3large' en el root namespace (__default__).

VERSIÓN MODULAR - Soporta:
1. Directorio: python3 vectorize_canonical_openai.py /ruta/directorio
2. Archivo: python3 vectorize_canonical_openai.py /ruta/archivo.md
3. Nombre simple: python3 vectorize_canonical_openai.py cheatsheets

Uso:
  python3 vectorize_canonical_openai.py <path_o_archivo>
Ejemplos:
  python3 vectorize_canonical_openai.py /root/chunks/
  python3 vectorize_canonical_openai.py /root/mi_chunk.md
  python3 vectorize_canonical_openai.py cheatsheets
"""

import os
import sys
import yaml
import glob
import warnings
from pathlib import Path
from pinecone import Pinecone
from openai import OpenAI

# Evita warnings innecesarios
warnings.filterwarnings("ignore")

# ============================================================================
# FASE 1 — CARGA DE CREDENCIALES
# ============================================================================


def load_api_keys():
    """Carga Pinecone y OpenAI API keys desde archivos de entorno"""
    with open("/root/.openskills/env/pinecone.env") as f:
        pinecone_key = None
        for line in f:
            if "PINECONE_API_KEY=" in line:
                pinecone_key = line.split("=")[1].strip()
                break

    with open("/root/.openskills/env/openai.env") as f:
        openai_key = None
        for line in f:
            if "OPENAI_API_KEY=" in line:
                openai_key = line.split("=")[1].strip()
                break

    if not pinecone_key or not openai_key:
        print("❌ ERROR: API keys no encontradas en /root/.openskills/env/")
        sys.exit(1)

    return pinecone_key, openai_key


# ============================================================================
# FASE 2A — DESCUBRIMIENTO DE CHUNKS (DIRECTORIO)
# ============================================================================


def get_chunk_files_from_directory(path):
    """
    Busca todos los archivos *.md recursivamente en un directorio.
    Soporta rutas absolutas, relativas, o solo nombres.
    """
    # Si es una ruta absoluta o relativa, úsala directamente
    if os.path.isabs(path) or path.startswith("./"):
        chunks_dir = path
    else:
        # Si es solo un nombre, busca en /home/kali/Desktop/RAG/
        chunks_dir = f"/home/kali/Desktop/RAG/{path}"

    if not os.path.exists(chunks_dir):
        print(f"❌ ERROR: Directorio no encontrado: {chunks_dir}")
        return None

    if not os.path.isdir(chunks_dir):
        print(f"❌ ERROR: No es un directorio: {chunks_dir}")
        return None

    chunk_files = sorted(glob.glob(f"{chunks_dir}/**/*.md", recursive=True))

    if not chunk_files:
        print(f"❌ ERROR: No se encontraron archivos .md en {chunks_dir}")
        return None

    return chunk_files


# ============================================================================
# FASE 2B — SOPORTE PARA ARCHIVO INDIVIDUAL
# ============================================================================


def get_chunk_files_from_file(path):
    """
    Valida que el archivo existe y es un .md.
    Retorna lista con solo ese archivo.
    """
    # Expandir ruta si es relativa
    if os.path.isabs(path):
        file_path = path
    else:
        file_path = os.path.abspath(path)

    if not os.path.exists(file_path):
        print(f"❌ ERROR: Archivo no encontrado: {file_path}")
        return None

    if not file_path.endswith(".md"):
        print(f"❌ ERROR: No es un archivo markdown (.md): {file_path}")
        return None

    if not os.path.isfile(file_path):
        print(f"❌ ERROR: No es un archivo: {file_path}")
        return None

    return [file_path]


# ============================================================================
# FASE 2C — DETECTOR: ¿DIRECTORIO O ARCHIVO?
# ============================================================================


def get_chunk_files(path):
    """
    Detecta si es directorio o archivo y retorna lista de chunks.

    MODULAR:
    - Si es directorio → get_chunk_files_from_directory()
    - Si es archivo .md → get_chunk_files_from_file()
    - Si es solo nombre → busca en /home/kali/Desktop/RAG/
    """
    # Caso 1: Archivo individual (ruta con .md)
    if path.endswith(".md"):
        print(f"📄 Detectado: Archivo individual")
        return get_chunk_files_from_file(path)

    # Caso 2: Directorio
    if os.path.isdir(path):
        print(f"📁 Detectado: Directorio")
        return get_chunk_files_from_directory(path)

    # Caso 3: Ruta absoluta que no existe (error)
    if os.path.isabs(path):
        print(f"❌ ERROR: Ruta no encontrada: {path}")
        return None

    # Caso 4: Solo nombre - intenta buscar en /home/kali/Desktop/RAG/
    test_path = f"/home/kali/Desktop/RAG/{path}"
    if os.path.isdir(test_path):
        print(f"📁 Detectado: Directorio (base path)")
        return get_chunk_files_from_directory(path)

    # Caso 5: Intenta como archivo
    test_file = os.path.abspath(path)
    if os.path.isfile(test_file) and test_file.endswith(".md"):
        print(f"📄 Detectado: Archivo individual")
        return get_chunk_files_from_file(path)

    print(f"❌ ERROR: No se puede determinar si es directorio o archivo: {path}")
    return None


# ============================================================================
# FASE 3 — VALIDACIÓN DE METADATA
# ============================================================================


def validate_metadata(metadata):
    """Comprueba que el chunk tenga al menos chunk_id"""
    if "chunk_id" not in metadata:
        return False, "Missing chunk_id"
    return True, "Valid"


# ============================================================================
# FASE 4 — GENERACIÓN DE EMBEDDINGS
# ============================================================================


def generate_embedding(client, text):
    """Genera un embedding de 3072 dimensiones usando OpenAI text-embedding-3-large"""
    response = client.embeddings.create(
        model="text-embedding-3-large", input=text, dimensions=3072
    )
    return response.data[0].embedding


# ============================================================================
# FASE 5 — PROCESAMIENTO DE CHUNKS
# ============================================================================


def generate_chunk_registry(chunk_files):
    """
    Generar chunk_registry.json que mapea chunk_ids a rutas de archivos
    Este registry es necesario para que el query agent lea archivos localmente
    """
    import re

    registry = {}

    for chunk_file in chunk_files:
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extraer chunk_id del frontmatter
            match = re.search(r"chunk_id:\s*(.+?)\n", content)
            if match:
                chunk_id = match.group(1).strip()
                registry[chunk_id] = str(chunk_file)
        except Exception as e:
            print(f"⚠️  Error leyendo {chunk_file}: {e}")
            continue

    return registry


def save_chunk_registry(registry, registry_path):
    """Guardar registry como JSON (simple append)"""
    import json
    from pathlib import Path

    # Crear directorio si no existe
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    # Cargar registry existente si existe
    existing_registry = {}
    if registry_path.exists():
        try:
            with open(registry_path, "r") as f:
                existing_registry = json.load(f)
        except Exception as e:
            print(f"⚠️  No se pudo leer registry existente: {e}")

    # Simple append: mezclar nuevos con existentes
    merged_registry = {**existing_registry, **registry}

    # Guardar registry (sorted para consistencia)
    with open(registry_path, "w") as f:
        json.dump(dict(sorted(merged_registry.items())), f, indent=2)

    new_count = len(registry)
    total = len(merged_registry)
    print(f"✅ Registry append: +{new_count} chunks → {total} total")


def process_chunks(machine_name, chunk_files, pinecone_key, openai_key):
    """
    Itera sobre cada chunk:
      - Lee el archivo
      - Parsea YAML frontmatter
      - Valida metadata
      - Genera embedding incluyendo todo el frontmatter + body
      - Prepara vector para upsert
    """
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")
    client = OpenAI(api_key=openai_key)

    vectors_to_upsert = []
    success_count = 0
    error_count = 0

    print(f"\n📁 Procesando {len(chunk_files)} chunks\n")

    for chunk_file in chunk_files:
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Verifica YAML frontmatter
            if not content.startswith("---"):
                print(f"⚠️  {Path(chunk_file).name}: No YAML frontmatter (skipped)")
                error_count += 1
                continue

            # Parsear YAML
            parts = content.split("---", 2)
            metadata_str = parts[1]
            body = parts[2] if len(parts) > 2 else ""

            metadata = yaml.safe_load(metadata_str)

            # Validar metadata
            is_valid, msg = validate_metadata(metadata)
            if not is_valid:
                print(f"❌ {metadata.get('chunk_id', 'UNKNOWN')}: {msg}")
                error_count += 1
                continue

            # 🔹 Convertir todo el frontmatter a texto
            metadata_text = " ".join(f"{k}: {v}" for k, v in metadata.items())
            text_to_embed = f"{metadata_text} {body.strip()}"

            # Generar embedding
            embedding = generate_embedding(client, text_to_embed)

            # Preparar vector para Pinecone (incluir content completo)
            vectors_to_upsert.append(
                {
                    "id": metadata["chunk_id"],
                    "values": embedding,
                    "metadata": {
                        **metadata,
                        "content": body.strip(),  # Incluir contenido completo
                        "content_length": len(body.strip()),
                    },
                }
            )

            print(f"✅ {metadata['chunk_id']} (3072D)")
            success_count += 1

        except Exception as e:
            print(f"❌ {Path(chunk_file).name}: {str(e)}")
            error_count += 1
            continue

    return vectors_to_upsert, success_count, error_count


# ============================================================================
# FASE 6 — UPSERT EN PINECONE (root namespace)
# ============================================================================


def upsert_vectors(vectors, pinecone_key):
    """Sube los vectores a Pinecone en el root namespace (__default__) en batches"""
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")

    print(f"\n📤 Subiendo {len(vectors)} vectores a rag-canonical-v1-emb3large\n")

    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        # CRÍTICO: No usar namespace=, todo va a __default__
        idx.upsert(vectors=batch)
        print(f"  ✅ Batch {i // batch_size + 1} ({len(batch)} vectores)")


# ============================================================================
# FASE 7 — VERIFICACIÓN DEL ÍNDICE
# ============================================================================


def verify_index(pinecone_key, machine_name):
    """
    Verifica que los vectores se hayan indexado correctamente
    """
    pc = Pinecone(api_key=pinecone_key)
    idx = pc.Index("rag-canonical-v1-emb3large")

    stats = idx.describe_index_stats()
    print(f"\n📊 Estadísticas del índice:")
    print(f"  Total vectores: {stats['total_vector_count']}")
    print(f"  Namespaces: {list(stats['namespaces'].keys())}")


# ============================================================================
# FASE 8 — MAIN
# ============================================================================


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 vectorize_canonical_openai.py <path>")
        print("\nModos soportados:")
        print(
            "  1. Directorio:      python3 vectorize_canonical_openai.py /home/kali/chunks/"
        )
        print(
            "  2. Archivo:         python3 vectorize_canonical_openai.py /home/kali/mi_chunk.md"
        )
        print("  3. Nombre simple:   python3 vectorize_canonical_openai.py cheatsheets")
        print("\nEjemplos:")
        print("  python3 vectorize_canonical_openai.py /root/chunks/")
        print("  python3 vectorize_canonical_openai.py ./mi_chunk.md")
        print("  python3 vectorize_canonical_openai.py cheatsheets")
        sys.exit(1)

    input_path = sys.argv[1]

    print(f"\n{'=' * 70}")
    print(f"🧠 VECTORIZER MODULAR - OpenAI 3072D")
    print(f"{'=' * 70}")
    print(f"Path: {input_path}")
    print(f"Index: rag-canonical-v1-emb3large")
    print(f"Model: text-embedding-3-large (3072D)")

    # Cargar keys
    pinecone_key, openai_key = load_api_keys()

    # Buscar chunks (MODULAR - directorio O archivo)
    chunk_files = get_chunk_files(input_path)
    if not chunk_files:
        sys.exit(1)

    print(f"📦 Encontrados: {len(chunk_files)} archivo(s)")

    # Procesar chunks
    vectors, success, errors = process_chunks(
        input_path, chunk_files, pinecone_key, openai_key
    )

    if not vectors:
        print(f"\n❌ No se generaron vectores (errores: {errors})")
        sys.exit(1)

    # Subir vectores
    upsert_vectors(vectors, pinecone_key)

    # Verificar índice
    verify_index(pinecone_key, input_path)

    # Generar chunk registry (necesario para query agent)
    print(f"\n📝 Generando chunk registry para query agent...")
    registry = generate_chunk_registry(chunk_files)
    registry_path = Path("/home/kali/Desktop/RAG/chunk_registry.json")
    save_chunk_registry(registry, registry_path)

    print(f"\n✅ Vectorización completa!")
    print(f"   Success: {success}")
    print(f"   Errors: {errors}")
    print(f"   Total: {len(vectors)} vectores")
    print(f"   Registry: {registry_path}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
