---
chunk_id: procedure::web::web-enumeration::application-research::001
domain: procedure
chunk_type: technique
---

### 1.3 - Wing FTP Research

**Investigación**: ¿Qué versión de Wing FTP está corriendo?

```bash
curl -s http://ftp.wingdata.htb/ | grep -i version

# También revisar headers
curl -v http://ftp.wingdata.htb/ 2>&1 | grep -i "server\|x-"
```

**Análisis manual**: Wing FTP Server puede ser vulnerable a CVE-2025-47812 (NULL byte injection en login).

**Vectores conocidos para Wing FTP**:

- CVE-2025-47812: NULL byte injection en parámetro `username` durante login

- Permite ejecutar código Lua en el contexto del servidor FTP
