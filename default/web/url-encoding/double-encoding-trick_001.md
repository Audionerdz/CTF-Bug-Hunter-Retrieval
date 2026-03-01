---
chunk_id: technique::web::url-encoding::double-encoding::001
domain: web
chunk_type: technique
category: web-security
confidence: high
reuse_level: universal
tags: [url-encoding, base64, evasion, firewall-bypass, obfuscation]
source_file: /home/ftpuser/uploads/WINGDATA/3 RCE lua.md
---

**Un truco de atacante:** A veces se usan **ambos**. Primero codificas el código Lua en **Base64** para que el Firewall no reconozca la palabra `io.popen`, y luego metes ese bloque Base64 dentro de un **URL Encode** para enviarlo por la web.
