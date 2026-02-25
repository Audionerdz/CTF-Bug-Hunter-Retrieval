---
chunk_id: procedure::web::lua-detection::fingerprinting::001
domain: procedure
chunk_type: technique
---

Detectar que un servidor está utilizando **Lua** en el backend no siempre es obvio, porque a diferencia de PHP (`.php`) o ASP.NET (`.aspx`), Lua suele estar integrado "bajo el capó" en servicios como servidores web (Nginx con OpenResty) o servidores FTP/Gaming.

Aquí tienes las claves para detectar el uso de Lua y evaluar si es vulnerable:

### 1. ¿Cómo se detecta el uso de Lua?

- **Cabeceras HTTP (Fingerprinting):**
    
    Si el servidor responde con la cabecera `Server: OpenResty`, es una señal clara. OpenResty es una versión de **Nginx** que utiliza Lua para manejar peticiones.
    
- **Mensajes de Error:**
    
    Si envías un carácter especial (como una comilla simple `'`, un corchete `[` o un null byte `%00`) y el servidor devuelve un error de sintaxis que menciona palabras como `nil`, `stack traceback` o `.lua`, has confirmado la tecnología.
    
- **Servicios Específicos:**
    
    Ciertos servicios son "famosos" por usar Lua. Si ves **Wing FTP Server**, **Tarantool**, o sistemas de scripting en juegos como **Roblox** o **FiveM**, sabes que Lua está corriendo ahí.
