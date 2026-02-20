---
chunk_id: technique::web::lua-rce::reconnaissance::001
domain: web
chunk_type: technique
category: web-security
confidence: high
reuse_level: universal
tags: [lua, rce, reconnaissance, uid, permissions]
source_file: /home/ftpuser/uploads/WINGDATA/1 RCE lua.md
---

### ¿Cuál es el objetivo?

El objetivo principal es el **reconocimiento**. Antes de intentar borrar archivos o instalar malware, un atacante usa el comando `id` para saber:

1. Si la vulnerabilidad es real (si recibe respuesta, lo es).
    
2. Qué nivel de permisos tiene (**root** vs **usuario limitado**).
