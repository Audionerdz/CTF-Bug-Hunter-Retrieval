---
chunk_id: exploit::python-programming::tarfile::vulnerable-code::001
domain: python-programming
chunk_type: exploit
category: python-programming
confidence: high
reuse_level: universal
tags: [python, tarfile, vulnerability, filter=data, path-traversal]
source_file: /home/ftpuser/uploads/WINGDATA/CVE-2025-4517 PrivEsc Python.md
---

## 4. ¿Cómo se ve el código "malo"?

Si ves algo así en tu programa, tienes un problema:

```python
import tarfile

# El empleado abre la caja "maliciosa.tar"
with tarfile.open("maliciosa.tar", "r") as tar:
    # El error es poner filter="data"
    # Esto le da permiso de escribir fuera de la carpeta si el archivo lo pide
    tar.extractall(path="./mi_carpeta", filter="data") 
```
