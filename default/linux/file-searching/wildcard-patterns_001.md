---
chunk_id: reference::linux::file-searching::wildcard-patterns::001
domain: linux
chunk_type: reference
category: linux
confidence: high
reuse_level: universal
tags: [wildcards, find, pattern, search, linux]
source_file: /home/ftpuser/uploads/WINGDATA/Comandos para busquedas de Directorios o archivos sensibles.md
---

### 2. Cómo se usan (Ejemplos prácticos)

#### A. Al final: `palabra*`

Busca todo lo que **empiece** por esa palabra.

```bash
find / -name "backup*" 2>/dev/null

```

*Encontrará: `backup.tar`, `backup_2024.sql`, `backups_clientes/`.*

#### B. Al principio: `*.extensión`

Busca todo lo que **termine** con esa extensión. Es el más usado para encontrar configuraciones.

```bash
find /etc -name "*.conf" 2>/dev/null

```

*Encontrará: `nginx.conf`, `apache2.conf`, `resolv.conf`.*

#### C. En ambos lados (Contiene): `*palabra*`

Busca cualquier archivo que **tenga esa palabra en alguna parte** del nombre.

```bash
find / -name "*user*" 2>/dev/null

```

*Encontrará: `user.txt`, `authorized_users`, `new_user_config.lua`.*

```

---

