---
chunk_id: reference::linux::file-searching::find-by-type::001
domain: linux
chunk_type: reference
category: linux
confidence: high
reuse_level: universal
tags: [find, type, directory, file, linux, search]
source_file: /home/ftpuser/uploads/WINGDATA/Comandos para busquedas de Directorios o archivos sensibles.md
---

### 3. Buscar SOLO Directorios

Si sabes que lo que buscas es una carpeta (como la de Wing FTP), añade `-type d`:

```bash
find / -type d -name "Sessions" 2>/dev/null
```

### 4. Buscar SOLO Archivos

Si buscas un ejecutable o un script, añade `-type f`:

```bash
find / -type f -name "wftpserver" 2>/dev/null
```

### 6. Búsqueda por Insensibilidad a Mayúsculas

En sistemas donde no sabes si escribieron `Config` o `config`, usa `-iname`:

```bash
find / -iname "WINGFTP" 2>/dev/null
```

### Tabla comparativa para tu IA

|**Objetivo**|**Flag Clave**|**Ejemplo de uso**|
|---|---|---|
|**Cualquier cosa**|`-name`|`find / -name "passwords.txt"`|
|**Ignorar errores**|`2>/dev/null`|_Siempre añadir al final_|
|**Directorios**|`-type d`|`find / -type d -name "backup"`|
|**Archivos**|`-type f`|`find / -type f -name "id_rsa"`|
|**Mayús/Minús**|`-iname`|`find / -iname "Secret"`|
