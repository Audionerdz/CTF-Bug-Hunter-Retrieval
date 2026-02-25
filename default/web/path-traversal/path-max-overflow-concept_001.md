---
chunk_id: concept::web::path-traversal::path-max-bypass::001
domain: web
chunk_type: concept
category: web-security
confidence: high
reuse_level: universal
tags: [path-traversal, path-max, overflow, bypass, symlink, realpath]
source_file: /home/ftpuser/uploads/WINGDATA/Exploit Data filter.md
---

### ¿Cómo funciona el bypass del `data_filter`?

El problema es un **desbordamiento lógico**. El filtro de Python confía en `os.path.realpath()` para saber dónde terminará un archivo.

1. Si la ruta es corta, `realpath` ve un symlink, lo sigue, y dice: _"Oye, esto va para `/etc/shadow`, ¡BLOQUEADO!"_.
    
2. Pero si inundamos la ruta con miles de caracteres hasta superar los **4096 bytes** (`PATH_MAX`), `realpath` se rinde y devuelve la ruta tal cual, sin resolver el symlink.
    
3. El filtro "data" ve esa ruta gigante, no detecta el salto al sistema raíz y da luz verde.
    
4. Cuando el sistema operativo hace la extracción real, **él sí sigue el symlink**, permitiendo el **Path Traversal**.
