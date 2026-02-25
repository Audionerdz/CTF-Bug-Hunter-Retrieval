---
chunk_id: technique::network::ntlm::hash-cracking::001
domain: network
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [netntlmv1, hashcat, eaphammer, evil-twin, security]
---

# 🔨 Guía de Cracking NetNTLMv1 (Hashcat)

Esta técnica describe el proceso de formateo y ruptura de hashes NetNTLMv1 capturados mediante ataques de Evil Twin. Para que la herramienta Hashcat procese el hash correctamente (Modo 5500), los datos deben seguir una estructura específica.

## 1. Preparación y Limpieza de Datos
Los datos capturados originalmente por herramientas como Eaphammer contienen separadores de dos puntos (`:`) que deben ser eliminados de los campos hexadecimales antes de construir la cadena final.

**Valores de ejemplo:**
- **Usuario:** `r4ulcl`
- **Challenge:** `8a:21:38:ee:3f:f4:31:12` → **Limpio:** `8a2138ee3ff43112`
- **Response:** `2dd7f48a8344...` (Eliminar todos los `:`)

## 2. Construcción del Hash para Hashcat
El archivo `hash.txt` debe contener una sola línea con el formato `Usuario::::Respuesta:Challenge`. Los cuatro puntos y coma (`::::`) actúan como marcadores de posición necesarios para el Modo 5500.

**Línea exacta para el archivo:**
`r4ulcl::::2dd7f48a8344bad778365b62b922ea69ff2e292069b6bc95:8a2138ee3ff43112`

## 3. Comando de Ejecución
Se utiliza el modo de ataque 5500 (NetNTLMv1 / NetNTLMv1+ESS) junto con un diccionario de contraseñas.

```bash
# Comando estándar para cracking
hashcat -m 5500 hash.txt /usr/share/wordlists/rockyou.txt

```

**Resultado esperado:**
Si la contraseña es débil (ej. `laboratory`), Hashcat la mostrará al finalizar el proceso.

```

