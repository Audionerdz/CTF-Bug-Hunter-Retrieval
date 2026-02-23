---
chunk_id: technique::web::lua-rce::reconnaissance::001
domain: web
chunk_type: technique
---

### ¿Cuál es el objetivo?

El objetivo principal es el **reconocimiento**. Antes de intentar borrar archivos o instalar malware, un atacante usa el comando `id` para saber:

1. Si la vulnerabilidad es real (si recibe respuesta, lo es).
    
2. Qué nivel de permisos tiene (**root** vs **usuario limitado**).
