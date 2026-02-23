---
chunk_id: procedure::web::web-enumeration::hosts-configuration::001
domain: procedure
chunk_type: technique
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
