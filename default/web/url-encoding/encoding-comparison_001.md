---
chunk_id: reference::web::url-encoding::encoding-comparison::001
domain: web
chunk_type: reference
category: web-security
confidence: high
reuse_level: universal
tags: [url-encoding, base64, comparison, encoding-methods]
source_file: /home/ftpuser/uploads/WINGDATA/3 RCE lua.md
---

### Diferencias Clave

|**Característica**|**URL Encoding**|**Base64**|
|---|---|---|
|**Símbolo clave**|El porcentaje `%`|El igual `==` al final|
|**Propósito**|Compatibilidad con protocolos web (HTTP/URLs).|Transporte de datos binarios como texto plano.|
|**Legibilidad**|Se puede medio leer el original.|Es ilegible a simple vista.|

---

**Un truco de atacante:** A veces se usan **ambos**. Primero codificas el código Lua en **Base64** para que el Firewall no reconozca la palabra `io.popen`, y luego metes ese bloque Base64 dentro de un **URL Encode** para enviarlo por la web.
