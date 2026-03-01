---
chunk_id: technique::web::url-encoding::double-encoding::001
domain: web
chunk_type: technique
---

**Un truco de atacante:** A veces se usan **ambos**. Primero codificas el código Lua en **Base64** para que el Firewall no reconozca la palabra `io.popen`, y luego metes ese bloque Base64 dentro de un **URL Encode** para enviarlo por la web.
