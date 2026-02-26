---
chunk_id: technique::web::recon::injection-surface-mapping::sqli::001
domain: web
tags:
- pentesting
- hunting
- attack-surface
- burp-suite
- injection
- fuzzing
- bug-bounty
- sqli
- sql-injection
- injection-map
- injection-surface
chunk_type: technique
confidence: 5
reuse_level: 2
---

# Checklist Maestro de Puntos de Entrada para Inyeccion (V2 + SQLi)

Checklist tactico para mapear entradas de inyeccion y priorizar pruebas en descubrimiento.

## 1. Parametros de Entrada Directa (GET/POST)

* **URL (GET)**: `id`, `page`, `product`, `user`, `order`, `post`, `article`, `cat`, `category`, `lang`, `langid`, `ref`, `search`, `q`, `query`, `item`, `tag`, `thread`.
* **Formularios (POST)**: `username`, `user`, `email`, `password`, `old_password`, `comment`, `message`, `name`, `title`, `body`, `date`, `amount`, `quantity`, `address`, `phone`.
* **Path Params**: `/user/1234/profile` -> El segmento `1234` suele ser un `id` en la query interna.

## 2. APIs y Estructuras Modernas

* **REST / JSON**: `{ "id": ..., "filter": "...", "limit": ... }`.
* **GraphQL**: Campos en `query` y `variables`.
* **XML / SOAP**: Tags usados en conversiones o consultas.
* **Ajax / XHR**: Peticiones asincronas con parametros JSON/POST.

## 3. Cabeceras, Cookies y Metadatos

* **Cabeceras HTTP**: `Cookie`, `Authorization`, `Referer`, `X-Forwarded-For`, `User-Agent`, `Host`.
* **Cookies**: `sessionid`, `user`, `auth`.
* **Subida de Archivos**: `filename` y metadatos (EXIF).
* **Redirecciones**: `next`, `return`, `redirect`, `url`, `goto`.

## 4. Paneles Internos e Integraciones

* **Admin Panels**: filtros avanzados, busquedas, bulk actions.
* **Import/Export**: CSV/Excel que terminan en DB.
* **Consultas Externas**: entradas que disparan LDAP/OS/DB externas.

## 5. Oraculo de Respuesta

| Indicador | Analisis Tecnico |
| :--- | :--- |
| **Cambio de Contenido** | Diferencias en filas/records. |
| **Diferencia de Tiempo** | Respuestas lentas (Blind por tiempo). |
| **Anomalia de Estado** | Cambios de HTTP (500 vs 200). |
| **Revelacion de Estructura** | Stack traces, errores SQL. |

## 6. Mapa SQLi (puntos de inyeccion)

* **Filtros y orden**: `sort`, `order`, `orderby`, `dir`.
* **Paginacion**: `page`, `offset`, `limit`, `per_page`.
* **Busqueda**: `search`, `q`, `query`, `term`.
* **Identificadores**: `id`, `uid`, `item`, `product`, `post`, `user`.
* **Campos de login**: `username`, `email`, `password`.
* **Parametros ocultos**: inputs `hidden`, `csrf`, `token` que se reusan en query.

## 7. Tips rapidos SQLi

* Probar operaciones numericas simples: `?id=2-1`.
* Revisar paneles admin y reportes con filtros.
* Si hay logs o reportes, intentar stored SQLi via comentarios o contacto.

> [!IMPORTANT]
> Intercepta y recorre cada parametro con Repeater. Persistencia > payloads.
