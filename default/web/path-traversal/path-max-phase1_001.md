---
chunk_id: technique::web::path-traversal::path-max-phase1::001
domain: web
chunk_type: technique
---

## 🛠 Análisis del Exploit (CVE-2025-4517)

### Fase 1: El Laberinto Infinito (PATH_MAX Overflow)

El objetivo aquí es crear una ruta de carpetas tan absurdamente larga que supere el límite de Linux (**4096 caracteres**).

- **`comp` y `steps`**: Crea 16 niveles de profundidad. En cada nivel pone una carpeta con un nombre de 247 letras.
    
- **El truco**: Al final, la ruta "real" que Python intenta validar es gigantesca. Cuando la función de seguridad (`realpath()`) intenta recorrerla para ver si hay peligro, se encuentra con que el camino es más largo que su "regla de medir" y **deja de comprobar los enlaces simbólicos**.
