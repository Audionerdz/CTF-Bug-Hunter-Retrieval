---
chunk_id: technique::network::enumeration::parameter-fuzzing-get::001
domain: network
chunk_type: technique
---

# Enumeración de parámetros GET mediante Fuzzing con ffuf

El Parameter Fuzzing se utiliza para descubrir nombres de variables ocultas en el lado del servidor (backend) que no son visibles en el cliente. Esta técnica es fundamental cuando una página devuelve mensajes de acceso denegado que sugieren la necesidad de un token, ID o llave secreta.

## 1. Conceptos Fundamentales
A diferencia del fuzzing de directorios, aquí el objetivo es identificar la clave (`key`) del par `clave=valor` en la URL.

- **Parámetro (Clave):** El nombre que el backend espera (Ej: `id`, `user`, `token`).
- **Valor:** El dato asignado al parámetro. Durante el descubrimiento de parámetros, se usa un valor estático o "dummy" (Ej: `test`, `1`, `key`).

## 2. Metodología de Ejecución
Para que el servidor procese la petición, se debe enviar el formato completo `?PARAMETRO=VALOR`. Si se envía solo el parámetro sin el signo `=`, el backend podría ignorar la entrada.

### Comando de Descubrimiento
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ \
-u "http://admin.academy.htb:PORT/admin/admin.php?FUZZ=test" \
-fs [size_a_filtrar]
```
