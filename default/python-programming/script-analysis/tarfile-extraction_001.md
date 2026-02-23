---
chunk_id: technique::python-programming::script-analysis::tarfile-extraction::001
domain: python-programming
chunk_type: technique
---

```python
    try:
        # L76: Abre el archivo .tar en modo lectura.
        with tarfile.open(backup_path, "r") as tar:
            # L77: Extrae el contenido. 'filter="data"' previene ataques de Path Traversal (Python 3.12+).
            tar.extractall(path=staging_dir, filter="data")
        print(f"[+] Extraction completed in {staging_dir}")
    except (tarfile.TarError, OSError, Exception) as e:
        # L79-82: Captura cualquier error durante la extracción (permisos, archivos corruptos, etc).
        print(f"[!] Error during extraction: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main() # L85-86: Punto de entrada estándar de Python.
```
