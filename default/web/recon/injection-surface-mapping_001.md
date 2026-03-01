---
chunk_id: technique::web::recon::injection-surface-mapping::001
domain: web
chunk_type: technique
confidence: 5
reuse_level: 2
tags: [pentesting, hunting, attack-surface, burp-suite, injection, fuzzing, bug-bounty]
---

# Checklist Maestro de Puntos de Entrada para Inyeccion (V2)

Este checklist sirve como mapa tactico para la interceptacion de peticiones. Todo dato que viaje del cliente al servidor es hostil por definicion. Pruebalos en orden de prioridad durante la fase de descubrimiento.

## 1. Parametros de Entrada Directa (GET/POST)

Vectores clasicos que suelen mapear directamente a consultas de base de datos (`WHERE`, `ORDER`, `LIMIT`).

* **URL (GET)**: `id`, `page`, `product`, `user`, `order`, `post`, `article`, `cat`, `category`, `lang`, `langid`, `ref`, `search`, `q`, `query`, `item`, `tag`, `thread`.
* **Formularios (POST)**: `username`, `user`, `email`, `password`, `old_password`, `comment`, `message`, `name`, `title`, `body`, `date`, `amount`, `quantity`, `address`, `phone`.
* **Path Params**: `/user/1234/profile` -> El segmento `1234` suele ser un `id` en la query interna.

## 2. APIs y Estructuras Modernas

Formatos donde la inyeccion puede romper la logica del parser (JSON/XML/GraphQL).

* **REST / JSON**: Valores en el cuerpo: `{ "id": ..., "filter": "...", "limit": ... }`.
* **GraphQL**: Campos en `query` y `variables` utilizados por el resolver.
* **XML / SOAP**: Tags internos utilizados en conversiones o consultas.
* **Ajax / XHR**: Peticiones asincronas visibles en la consola que contienen parametros JSON/POST.

## 3. Cabeceras, Cookies y Metadatos

Entradas "invisibles" que el servidor suele procesar para analitica, sesiones o logs.

* **Cabeceras HTTP**: `Cookie`, `Authorization` (token), `Referer`, `X-Forwarded-For`, `User-Agent`, `Host`.
* **Cookies**: Valores como `sessionid`, `user` o `auth` que el servidor re-valida contra la DB.
* **Subida de Archivos**: Atributos como `filename` o metadatos (EXIF) que se consultan posteriormente.
* **Redirecciones**: Parametros `next`, `return`, `redirect`, `url`, `goto`.

## 4. Paneles Internos e Integraciones

Areas con menos auditoria de seguridad que suelen confiar en el input "interno".

* **Admin Panels**: Campos de busqueda avanzada, filtros manuales y acciones en lote (bulk actions).
* **Import/Export**: Procesamiento de archivos CSV/Excel que terminan escribiendose en la DB.
* **Consultas Externas**: Entradas de usuario (`username`) que disparan consultas adicionales a LDAP, OS o bases externas.

## 5. Oraculo de Respuesta: Que Observar

Monitoriza estas anomalias al inyectar (sin importar el payload):

| Indicador | Analisis Tecnico |
| :--- | :--- |
| **Cambio de Contenido** | Diferencias en el numero de filas o registros mostrados. |
| **Diferencia de Tiempo** | Respuestas significativamente lentas (Posible Blind por tiempo). |
| **Anomalia de Estado** | Cambios inesperados en codigos HTTP (ej. 500 Internal Error vs 200 OK). |
| **Revelacion de Estructura** | Stack traces, errores de sintaxis de DB o plantillas de error detalladas. |

## 6. Tips para Labs y HTB

* **No validacion**: Si acepta numeros, prueba operaciones (ej. `?page=2-1`).
* **Stored SQLi**: Inyecta en formularios de contacto o comentarios que persistan en el panel de admin.
* **Fuentes alternativas**: Revisa inputs `hidden`, metadatos HTML o datos en `localStorage` que la app reenvia.

> [!IMPORTANT]
> **Checklist de Burp/Reaper**: Intercepta, manda al Repeater y recorre sistematicamente cada parametro de esta lista. La persistencia es lo que encuentra la vulnerabilidad.
