---
chunk_id: concept::linux::buffer-overflow::path-max::001
domain: linux
chunk_type: concept
category: linux
confidence: high
reuse_level: universal
tags: [path-max, linux, limits, buffer-overflow, system-constant]
source_file: /home/ftpuser/uploads/WINGDATA/PATH MAX.md
---

### ¿Qué es `PATH_MAX`?

Es un **límite de velocidad para el tamaño de las rutas**. Es una constante en el sistema (normalmente **4096 caracteres**) que le dice al sistema operativo: _"Oye, ninguna ruta de archivo (ej. `/home/user/archivo.txt`) puede ser más larga que esto"_. Si intentas crear algo que mida 4097, el sistema simplemente te da un error y se detiene.

```

---

### Notas para tu RAG de Binbash:

Este concepto es el **pilar fundamental** que explica por qué funcionó el exploit que analizamos antes.

* **Dato Técnico:** El valor de `PATH_MAX` se define en el archivo de cabecera de C `limits.h`.
* **Importancia en Pentesting:** Cuando un programa como el script de backups intenta validar una ruta que excede este límite, muchas funciones de seguridad fallan silenciosamente, permitiendo el bypass de filtros.

