---
chunk_id: technique::web::path-traversal::path-max-phase5-6::001
domain: web
chunk_type: technique
category: web-security
confidence: high
reuse_level: universal
tags: [path-traversal, persistence, ssh, authorized-keys, backdoor]
source_file: /home/ftpuser/uploads/WINGDATA/Exploit Data filter.md
---

### Fase 5 y 6: El "Backdoor" Permanente (Persistencia)

Esta es la parte más agresiva del exploit. No solo quieres leer un archivo, quieres **quedarte con la llave de la casa**.

- **`escape_ssh`**: Apunta a la carpeta oculta de configuración de llaves de seguridad del administrador (`/root/.ssh`).
    
- **`authorized_keys`**: El script toma tu llave pública de `exploit_key.pub` y la escribe dentro del servidor.
    
- **Resultado**: La próxima vez que quieras entrar al servidor, no necesitarás contraseña. Solo escribes `ssh root@wingdata.htb` y el servidor te dejará pasar porque "reconoce" tu llave como autorizada.

### 💡 Nota Crítica

> **Punto Crítico**: El exploit depende totalmente de que el script de restauración se ejecute como **root** (o con `sudo`), lo cual es común en scripts de mantenimiento de servidores. Si el script se ejecutara como un usuario normal, fallaría al intentar escribir en `/root`.
