---
chunk_id: procedure::web::web-enumeration::hosts-configuration::001
domain: web
chunk_type: procedure
category: web-security
confidence: high
reuse_level: universal
tags: [enumeration, hosts-file, dns-resolution, vhost, web-access]
source_file: /home/ftpuser/uploads/WINGDATA/Enumeracion WingData.md
---

**Paso 4: Actualizar /etc/hosts**

```bash
sed -i 's/.*wingdata.htb.*/10.129.1.206 wingdata.htb ftp.wingdata.htb/' /etc/hosts
```

**Paso 5: Explorar la interfaz Wing FTP**

```bash
curl -v http://ftp.wingdata.htb/loginok.html
```

**Output**: Página de login encontrada (200 OK)
