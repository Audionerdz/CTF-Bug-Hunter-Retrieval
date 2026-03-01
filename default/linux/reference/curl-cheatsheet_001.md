---
chunk_id: reference::linux::commands::curl-cheatsheet::001
domain: linux
chunk_type: reference
confidence: 5
reuse_level: 1
tags: [curl, cli, http-requests, file-transfer, networking, cheatsheet]
---

# Referencia de comandos curl para transferencia de datos e interacción web

`curl` es una herramienta de línea de comandos para transferir datos con sintaxis de URL. Es esencial para interactuar con APIs, descargar archivos y realizar tareas de depuración de red.



## 1. Operaciones de Descarga y Gestión de Archivos

- **Descarga Básica (stdout)**: `curl [URL]`
- **Guardar en archivo**: `curl -o nombre_archivo.html [URL]`
- **Guardar con nombre original**: `curl -O [URL]`
- **Descargar múltiples archivos**: `curl -O [URL1] -O [URL2]`
- **Resumir descarga interrumpida**: `curl -C - -O [URL]`
- **Limitar velocidad de descarga**: `curl --limit-rate 100K -O [URL]`
- **Mostrar barra de progreso**: `curl -# -O [URL]`

## 2. Interacción con Métodos HTTP y APIs

Para interactuar con servicios web y APIs RESTful, se utilizan modificadores de método y envío de datos.

- **Petición POST (Formulario)**: `curl -X POST -d "user=val&pass=val" [URL]`
- **Petición POST (JSON)**: `curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' [URL]`
- **Petición PUT**: `curl -X PUT -d '{"id": 1}' -H "Content-Type: application/json" [URL]`
- **Petición HEAD (Solo cabeceras)**: `curl -I [URL]`



## 3. Cabeceras, Cookies y Autenticación

- **Añadir Header personalizado**: `curl -H "Authorization: Bearer TOKEN" [URL]`
- **Autenticación básica**: `curl -u usuario:password [URL]`
- **Guardar Cookies**: `curl -c cookies.txt [URL]`
- **Usar Cookies guardadas**: `curl -b cookies.txt [URL]`
- **Seguir redirecciones (3xx)**: `curl -L [URL]`

## 4. Configuración de Red y Depuración

- **Modo Verbose (Detallado)**: `curl -v [URL]`. Muestra todo el flujo de la petición y respuesta.
- **Ignorar verificación SSL**: `curl -k [URL]` (Útil para certificados auto-firmados).
- **Usar Proxy**: `curl -x proxy.dominio.com:8080 [URL]`
- **Tiempo máximo de petición**: `curl --max-time 10 [URL]`

> [!TIP]
> Combina `-s` (Silent) con `-D -` para obtener solo las cabeceras de respuesta en la salida estándar sin el cuerpo de la página: `curl -s -D - [URL] -o /dev/null`.
