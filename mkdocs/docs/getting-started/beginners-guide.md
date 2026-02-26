# Beginner's Guide: Atlas Engine

Atlas Engine is meant to be used from a single interactive Python session.

## Start a session

```bash
python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()
```

## Core commands (minimal)

```python
atlas.query("LFI", top_k=3)
atlas.ask("What is LFI?")
atlas.chat()
atlas.chat(backend="gpt")
atlas.fetch("technique::web::lfi::path-traversal::001")
atlas.delete("chunk_id::here")
atlas.vectorize("/path/to/chunk.md")
atlas.stats()
atlas.help()
```

Notes:
- `atlas.chat()` is interactive; use `atlas.ask()` for a single answer.
- If you do not pass `namespace`, Atlas uses the default namespace automatically.

## Vectorize without frontmatter (manual metadata)

```python
atlas.vectorize(
    "/path/to/notes.md",
    domain="web",
    tags=["pentesting", "injection"],
    metadata={"confidence": 5, "reuse_level": 2}
)
```

## Vectorize from text (one shot)

```python
from atlas_engine import Atlas
atlas = Atlas()

atlas.vectorize_text(
    """
# Checklist Maestro de Puntos de Entrada para Inyección (V2)

Este checklist sirve como mapa táctico para la interceptación de peticiones. Todo dato que viaje del cliente al servidor es hostil por definición. Pruébalos en orden de prioridad durante la fase de descubrimiento.

## 1. Parámetros de Entrada Directa (GET/POST)
Vectores clásicos que suelen mapear directamente a consultas de base de datos (`WHERE`, `ORDER`, `LIMIT`).

* **URL (GET)**: `id`, `page`, `product`, `user`, `order`, `post`, `article`, `cat`, `category`, `lang`, `langid`, `ref`, `search`, `q`, `query`, `item`, `tag`, `thread`.
* **Formularios (POST)**: `username`, `user`, `email`, `password`, `old_password`, `comment`, `message`, `name`, `title`, `body`, `date`, `amount`, `quantity`, `address`, `phone`.
* **Path Params**: `/user/1234/profile` -> El segmento `1234` suele ser un `id` en la query interna.

## 2. APIs y Estructuras Modernas
Formatos donde la inyección puede romper la lógica del parser (JSON/XML/GraphQL).

* **REST / JSON**: Valores en el cuerpo: `{ "id": ..., "filter": "...", "limit": ... }`.
* **GraphQL**: Campos en `query` y `variables` utilizados por el resolver.
* **XML / SOAP**: Tags internos utilizados en conversiones o consultas.
* **Ajax / XHR**: Peticiones asíncronas visibles en la consola que contienen parámetros JSON/POST.

## 3. Cabeceras, Cookies y Metadatos
Entradas "invisibles" que el servidor suele procesar para analítica, sesiones o logs.

* **Cabeceras HTTP**: `Cookie`, `Authorization` (token), `Referer`, `X-Forwarded-For`, `User-Agent`, `Host`.
* **Cookies**: Valores como `sessionid`, `user` o `auth` que el servidor re-valida contra la DB.
* **Subida de Archivos**: Atributos como `filename` o metadatos (EXIF) que se consultan posteriormente.
* **Redirecciones**: Parámetros `next`, `return`, `redirect`, `url`, `goto`.

## 4. Paneles Internos e Integraciones
Áreas con menos auditoría de seguridad que suelen confiar en el input "interno".

* **Admin Panels**: Campos de búsqueda avanzada, filtros manuales y acciones en lote (bulk actions).
* **Import/Export**: Procesamiento de archivos CSV/Excel que terminan escribiéndose en la DB.
* **Consultas Externas**: Entradas de usuario (`username`) que disparan consultas adicionales a LDAP, OS o bases externas.

## 5. Oráculo de Respuesta: Qué Observar
Monitoriza estas anomalías al inyectar (sin importar el payload):

| Indicador | Análisis Técnico |
| :--- | :--- |
| **Cambio de Contenido** | Diferencias en el número de filas o registros mostrados. |
| **Diferencia de Tiempo** | Respuestas significativamente lentas (Posible Blind por tiempo). |
| **Anomalía de Estado** | Cambios inesperados en códigos HTTP (ej. 500 Internal Error vs 200 OK). |
| **Revelación de Estructura** | Stack traces, errores de sintaxis de DB o plantillas de error detalladas. |

## 6. Tips para Labs y HTB
* **No validación**: Si acepta números, prueba operaciones (ej. `?page=2-1`).
* **Stored SQLi**: Inyecta en formularios de contacto o comentarios que persistan en el panel de admin.
* **Fuentes alternativas**: Revisa inputs `hidden`, metadatos HTML o datos en `localStorage` que la app reenvía.

> [!IMPORTANT]
> **Checklist de Burp/Reaper**: Intercepta, manda al Repeater y recorre sistemáticamente cada parámetro de esta lista. La persistencia es lo que encuentra la vulnerabilidad.
""",
    chunk_id="technique::web::recon::injection-surface-mapping::001",
    path="default/web/recon/injection-surface-mapping_001.md",
    domain="web",
    tags=["pentesting", "hunting", "attack-surface", "burp-suite", "injection", "fuzzing", "bug-bounty"],
    metadata={"chunk_type": "technique", "confidence": 5, "reuse_level": 2},
)
```

## Exit

```python
exit()
```
