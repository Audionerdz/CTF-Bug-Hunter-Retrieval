---
chunk_id: technique::web::path-traversal::path-max-phase2::001
domain: web
chunk_type: technique
---

### Fase 2: El Túnel de Escape

Una vez que sabemos que el guardia (el filtro) está "mareado" por el laberinto del paso anterior, creamos un enlace simbólico (`SYMTYPE`).

- **`linkname = "../" * len(steps)`**: Este es el comando para "subir" niveles. Básicamente dice: _"Sal de todas estas carpetas y vuelve a la raíz del disco duro (`/`)"_. Como está al final del laberinto gigante, el filtro no lo ve venir.
