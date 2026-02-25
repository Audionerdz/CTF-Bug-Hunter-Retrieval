---
chunk_id: guideline::web::lua-rce::mitigation::001
domain: web
chunk_type: guideline
category: web-security
confidence: high
reuse_level: universal
tags: [lua, rce, mitigation, sandbox, protection, blacklist]
source_file: /home/ftpuser/uploads/WINGDATA/2 RCE lua.md
---

### Cómo protegerse (El "Derrumbamiento" de la librería)

La forma más efectiva de evitar esto en Lua es **eliminar** las funciones peligrosas antes de ejecutar cualquier código del usuario. Un desarrollador seguro haría algo como esto en el backend:

```lua
-- Lista negra: eliminamos el acceso al sistema operativo
os.execute = nil
os.exit = nil
io.popen = nil
io.open = nil
-- Ahora, aunque el payload entre, la función 'io.popen' será 'nil' (nula)
```
