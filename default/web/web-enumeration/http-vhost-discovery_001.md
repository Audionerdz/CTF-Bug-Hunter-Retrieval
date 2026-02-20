---
chunk_id: procedure::web::web-enumeration::vhost-discovery::001
domain: web
chunk_type: procedure
category: web-security
confidence: high
reuse_level: universal
tags: [enumeration, virtual-hosts, http-headers, vhost-fuzzing, web-application]
source_file: /home/ftpuser/uploads/WINGDATA/Enumeracion WingData.md
---

### 1.2 - Web Enumeration

**Paso 1: Acceder a la web por IP**

```bash
curl -v http://10.129.1.206/
```

**Output**: Redirige a `http://wingdata.htb/loginok.html` con error 301.

**Lección aprendida**: La aplicación usa Virtual Hosts. Necesitamos resolver `wingdata.htb`.

**Paso 2: Agregar a /etc/hosts**

```bash
echo "10.129.1.206 wingdata.htb" >> /etc/hosts
```

**Paso 3: Identificar Virtual Hosts**

La aplicación redirige a `wingdata.htb`, pero intentar acceder a `/loginok.html` da 404. El wing FTP web interface podría estar en otro vhost.

```bash
# Fuzzing de subdomains
for sub in ftp wftp wing webftp files sftp admin portal; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -H "Host: $sub.wingdata.htb" "http://10.129.1.206/loginok.html")
  echo "$sub.wingdata.htb -> $code"
done
```

**Output esperado**:

```
ftp.wingdata.htb -> 200          ← AQUÍ ESTÁ!
wftp.wingdata.htb -> 301
wing.wingdata.htb -> 301
```

**Hallazgo**: Wing FTP web interface está en `ftp.wingdata.htb`
