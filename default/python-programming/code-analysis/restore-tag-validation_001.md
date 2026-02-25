---
chunk_id: technique::python-programming::script-analysis::tag-validation::001
domain: python-programming
chunk_type: technique
category: python-programming
confidence: high
reuse_level: universal
tags: [python, validation, tag-validation, path-safety, input-sanitization]
source_file: /home/ftpuser/uploads/WINGDATA/restore_backup_clients.py.md
---

```python
    # L53-56: Fuerza a que el directorio de destino empiece por el prefijo "restore_".
    if not args.restore_dir.startswith("restore_"):
        print("[!] --restore-dir must start with 'restore_'", file=sys.stderr)
        sys.exit(1)

    # L58: Extrae el nombre del tag (lo que va después de los 8 caracteres de 'restore_').
    tag = args.restore_dir[8:]
    # L59-62: Si no hay nada después de 'restore_', el script se detiene.
    if not tag:
        print("[!] --restore-dir must include a non-empty tag...", file=sys.stderr)
        sys.exit(1)

    # L64-67: Valida que el tag no contenga caracteres maliciosos (path traversal básico).
    if not validate_restore_tag(tag):
        print("[!] Restore tag must be 1–24 characters long...", file=sys.stderr)
        sys.exit(1)

    # L69: Construye la ruta completa del directorio donde se hará la extracción.
    staging_dir = os.path.join(STAGING_BASE, args.restore_dir)
    print(f"[+] Backup: {args.backup}")
    print(f"[+] Staging directory: {staging_dir}")

    # L73: Crea el directorio de destino. 'exist_ok=True' evita errores si ya existe.
    os.makedirs(staging_dir, exist_ok=True)
```
