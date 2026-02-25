---
chunk_id: concept::web::url-encoding::definition::001
domain: web
chunk_type: concept
category: web-security
confidence: high
reuse_level: universal
tags: [url-encoding, percent-encoding, http, ascii]
source_file: /home/ftpuser/uploads/WINGDATA/3 RCE lua.md
---

### Encoding Lua payloads tips 

¡Gran pregunta! Es muy común confundirlos, pero **no, no es Base64**. Lo que ves ahí es **URL Encoding** (también llamado _Percent-encoding_).

Aquí te explico la diferencia para que nunca los vuelvas a mezclar:

### 1. URL Encoding (Lo que pusiste en el ejemplo)

Se usa para que los caracteres "especiales" no rompan la estructura de una URL o de una petición HTTP.

- **Cómo funciona:** Sustituye caracteres no permitidos por un símbolo de porcentaje `%` seguido de dos números hexadecimales (su valor en la tabla ASCII).
    
- **Ejemplos en tu payload:**
    
    - `%20` = Espacio
        
    - `%22` = Comillas `"`
        
    - `%28` / `%29` = Paréntesis `(` y `)`
        
    - `%0A` = Salto de línea (Line Feed)
        
    - `%00` = Byte Nulo (`\0`)
