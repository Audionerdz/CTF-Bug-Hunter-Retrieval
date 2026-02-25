---
chunk_id: technique::python-programming::script-analysis::argument-parsing::001
domain: python-programming
chunk_type: technique
---

```python
def main():
    # L22-26: Inicializa argparse con descripción y ejemplos para el usuario.
    parser = argparse.ArgumentParser(
        description="Restore client configuration from a validated backup tarball.",
        epilog="Example: sudo %(prog)s -b backup_1001.tar -r restore_john"
    )
    # L27-32: Define el argumento obligatorio -b para el archivo backup.
    parser.add_argument("-b", "--backup", required=True, help="Ruta relativa del backup")
    # L33-38: Define el argumento obligatorio -r para el nombre del directorio destino.
    parser.add_argument("-r", "--restore-dir", required=True, help="Nombre del directorio de staging")

    args = parser.parse_args() # L40: Procesa los argumentos introducidos por el usuario.

    # L42-45: Valida el nombre del archivo backup usando la función Regex definida arriba.
    if not validate_backup_name(args.backup):
        print("[!] Invalid backup name...", file=sys.stderr)
        sys.exit(1)

    # L47: Une la base del directorio con el nombre del archivo proporcionado.
    backup_path = os.path.join(BACKUP_BASE_DIR, args.backup)
    # L48-51: Verifica físicamente si el archivo existe en el sistema de archivos.
    if not os.path.isfile(backup_path):
        print(f"[!] Backup file not found: {backup_path}", file=sys.stderr)
        sys.exit(1)
```
