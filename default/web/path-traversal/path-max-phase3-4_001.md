---
chunk_id: technique::web::path-traversal::path-max-phase3-4::001
domain: web
chunk_type: technique
---

### Fase 3 y 4: Acceso a Datos Sensibles

Aquí es donde empezamos a tocar archivos que normalmente están prohibidos.

- **`escape_root`**: Crea un acceso directo que apunta directamente a la carpeta personal del administrador (`/root`).
    
- **`rootflag_link`**: Crea un enlace duro (`LNKTYPE`) hacia el archivo `root.txt`. Esto te permitiría leer la "bandera" o el secreto del servidor solo con extraer el backup.
