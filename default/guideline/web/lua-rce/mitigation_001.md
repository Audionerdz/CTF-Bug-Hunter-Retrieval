---
chunk_id: guideline::web::lua-rce::mitigation::001
domain: guideline
chunk_type: technique
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
