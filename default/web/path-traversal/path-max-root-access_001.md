---
chunk_id: technique::web::path-traversal::path-max-phase3-4::001
domain: web
chunk_type: technique
category: web-security
confidence: high
reuse_level: universal
tags: [path-traversal, root-access, file-reading, hardlink, symlink]
source_file: /home/ftpuser/uploads/WINGDATA/Exploit Data filter.md
---

### Fase 3 y 4: Acceso a Datos Sensibles

Aquí es donde empezamos a tocar archivos que normalmente están prohibidos.

- **`escape_root`**: Crea un acceso directo que apunta directamente a la carpeta personal del administrador (`/root`).
    
- **`rootflag_link`**: Crea un enlace duro (`LNKTYPE`) hacia el archivo `root.txt`. Esto te permitiría leer la "bandera" o el secreto del servidor solo con extraer el backup.
