#!/usr/bin/env python3
"""
SYNC REGISTRY: Sincroniza chunk_registry.json con archivos reales en el filesystem.

Propósito: Evitar que el registry quede desincronizado con los archivos.
Usa esto después de vectorizar para asegurar consistencia.

Uso:
    python3 sync_registry.py                    # Sincroniza toda la carpeta default/
    python3 sync_registry.py /path/to/dir      # Sincroniza un directorio específico
"""

import json
import re
from pathlib import Path
import sys

RAG_ROOT = Path("/home/kali/Desktop/RAG")
REGISTRY_FILE = RAG_ROOT / "chunk_registry.json"
DEFAULT_DIR = RAG_ROOT / "default"


def extract_chunk_id(file_path):
    """Extrae chunk_id del frontmatter YAML del archivo"""
    try:
        # Intentar UTF-8, luego latin-1 como fallback
        for encoding in ["utf-8", "latin-1", "iso-8859-1"]:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return None

        # Buscar chunk_id en el frontmatter
        match = re.search(r"chunk_id:\s*(.+?)(?:\n|$)", content)
        if match:
            return match.group(1).strip()
    except Exception as e:
        pass  # Silencio los errores

    return None


def build_registry_from_filesystem(target_dir=None):
    """Construye registry completo desde los archivos .md del filesystem"""
    if target_dir is None:
        target_dir = DEFAULT_DIR
    else:
        target_dir = Path(target_dir)

    if not target_dir.exists():
        print(f"❌ Directorio no encontrado: {target_dir}")
        return {}

    registry = {}

    # Buscar todos los .md files
    for md_file in sorted(target_dir.rglob("*.md")):
        chunk_id = extract_chunk_id(md_file)

        if chunk_id:
            registry[chunk_id] = str(md_file)
        else:
            print(f"⚠️  {md_file.name}: No chunk_id found (skipped)")

    return registry


def validate_registry(registry):
    """Verifica que todos los archivos en el registry existen"""
    valid = {}
    missing = []

    for chunk_id, file_path in registry.items():
        if Path(file_path).exists():
            valid[chunk_id] = file_path
        else:
            missing.append((chunk_id, file_path))

    return valid, missing


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None

    print("🔄 Sincronizando chunk_registry.json...")

    # Construir registry desde filesystem
    new_registry = build_registry_from_filesystem(target_dir)

    if not new_registry:
        print("❌ No se encontraron chunks válidos")
        return

    # Validar que todos los archivos existan
    valid, missing = validate_registry(new_registry)

    if missing:
        print(
            f"\n⚠️  {len(missing)} chunks no encontrados en filesystem (removidos del registry):"
        )
        for chunk_id, path in missing[:5]:
            print(f"   - {chunk_id}")
        if len(missing) > 5:
            print(f"   ... y {len(missing) - 5} más")

    # Guardar registry limpio y sincronizado
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(valid, f, indent=2)

    print(f"\n✅ Registry sincronizado:")
    print(f"   📁 Total chunks: {len(valid)}")
    print(f"   📄 Archivo: {REGISTRY_FILE}")


if __name__ == "__main__":
    main()
