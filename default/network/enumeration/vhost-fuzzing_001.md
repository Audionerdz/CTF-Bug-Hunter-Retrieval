---
chunk_id: technique::network::enumeration::vhost-fuzzing::001
domain: network
chunk_type: technique
---

# Detección de Virtual Hosts mediante Fuzzing del Header Host

El VHost Fuzzing es una técnica de reconocimiento que permite descubrir subdominios alojados en un mismo servidor (misma IP) que no poseen registros DNS públicos. A diferencia de la enumeración DNS tradicional, esta técnica manipula directamente la capa de aplicación HTTP.

## 1. VHosts vs. Subdominios
- **Subdominios:** Requieren un registro en servidores DNS públicos para ser resueltos por el navegador.
- **Virtual Hosts (VHosts):** Son configuraciones en el servidor web que permiten servir múltiples dominios desde una única dirección IP. Se diferencian exclusivamente mediante el valor del campo `Host` en el encabezado (header) de la petición HTTP.

## 2. Técnica de Fuzzing con ffuf
Cuando un subdominio no tiene DNS público, el fuzzing se realiza inyectando el diccionario en el header `Host` mientras se mantiene fija la URL del servidor objetivo.

```bash
# Comando para VHost Fuzzing
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ \
-u http://academy.htb:44231/ \
-H 'Host: FUZZ.academy.htb'
```

**Parámetros críticos:**
* `-u`: La URL/IP del servidor donde sospechamos que residen los VHosts.
* `-H 'Host: FUZZ.dominio.com'`: Inyecta cada palabra del wordlist en el encabezado de host.

## 3. Identificación de Resultados Positivos

En el VHost Fuzzing, el código de estado (ej: 200 OK) no suele ser suficiente para confirmar un hallazgo, ya que muchos servidores devuelven la página por defecto para cualquier host inexistente.

**Indicadores de éxito:**
* **Diferencia de Tamaño (Size):** Un VHost válido devolverá un tamaño de respuesta distinto al de la página genérica/default.
* **Filtrado:** Se recomienda identificar el tamaño de la respuesta genérica y filtrarlo en ffuf usando `-fs [size]` para dejar visibles solo los VHosts reales.

> **NOTE:** Esta técnica es vital en entornos de auditoría interna o CTFs donde los servicios no están expuestos en DNS reales pero sí están configurados en el servidor web (ej: `admin.target.htb`, `dev.target.htb`).
