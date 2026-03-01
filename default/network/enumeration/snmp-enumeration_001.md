---
chunk_id: technique::network::exploitation::snmp-enumeration::001
domain: network
chunk_type: technique
confidence: 5
reuse_level: 2
tags: [snmp, enumeracion, public, enumeration, mib-2, reconnaissance, post-mortem, information-gathering]
---

# Metodología Maestra de Enumeración SNMP: El Valor de lo Simple

SNMP (Simple Network Management Protocol) es a menudo pasado por alto o sobrecomplicado. Esta guía establece el flujo de trabajo táctico basado en la explotación exitosa de configuraciones inseguras por defecto (v1/v2c) y la interpretación de la jerarquía OID para la extracción de secretos.



## 1. La Llave: Fuerza Bruta de Comunidad
Antes de intentar ataques complejos en v3, se debe agotar la fase de descubrimiento de comunidades en v1/v2c. El acceso de lectura suele estar protegido por strings predecibles.

* **Herramienta**: `onesixtyone` (Eficiencia por paralelismo).
* **Comando Táctico**:
    ```bash
    onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt <TARGET_IP>
    ```
* **Intención**: Si responde a `public`, el vector de ataque se desplaza de "intrusión" a "exfiltración de datos de gestión".

## 2. Ejecución: El "Walk" Inicial
Una vez confirmada la comunidad (ej. `public`), el primer paso operativo es volcar el contenido completo del agente para su análisis posterior.

* **Comando Táctico**:
    ```bash
    # Volcado completo usando v2c y comunidad public
    snmpwalk -v 2c -c public <TARGET_IP>
    ```
* **Nota**: Si el output es masivo, redirige a un archivo (`> snmp_dump.txt`) para realizar búsquedas (`grep`) de strings sensibles como "pass", "key", o "admin".



## 3. El OID Crítico: `.1.3.6.1.2.1.1.1.0` (sysDescr)
Al realizar el `snmpwalk`, la primera línea de respuesta suele ser la más valiosa. El OID `.1.3.6.1.2.1.1.1.0` corresponde a **sysDescr**.

### Anatomía del OID de Sistema
La ruta `.1.3.6.1.2.1.1` (ISO.Org.DoD.Internet.Mgmt.MIB-2.System) es el estándar universal para describir el dispositivo.
* **sysDescr (.1.0)**: Puede contener versiones de OS, hardware y, crucialmente, **notas del administrador**.
* **Lección Operativa**: Si el entorno no tiene MIBs instaladas, verás números. Memorizar esta secuencia permite identificar el "banner" del sistema instantáneamente.



## 4. Hoja de Ruta de Exfiltración (Post-Exploitation)
Una vez obtenido el acceso de lectura, no te detengas en la descripción. Busca "joyas" en estos OIDs específicos de la MIB-2:

| OID / Nombre | Función Táctica | Valor para el Atacante |
| :--- | :--- | :--- |
| **sysName** (.1.1.5.0) | Nombre del Host | Identificación de rol (ej: DB-PROD). |
| **hrSWRunName** (...25.4.2.1.2) | Procesos | Enumeración de software instalado. |
| **hrSWRunParameters** (...25.4.2.1.4) | **Argumentos** | **Passwords en línea de comandos.** |
| **ipNetToMediaPhysAddress** (...4.22.1.2) | Tabla ARP | Mapeo de la red interna (Pivoting). |
| **tcpConnRemAddress** (...6.13.1.2) | Netstat | Conexiones activas y comunicaciones. |

## 5. Análisis de Fallo (Debriefing)
* **Error cometido**: Foco excesivo en SNMPv3 y escaneos agresivos que causaron bloqueo.
* **Corrección**: Volver a `v2c -c public`.
* **Resultado**: La contraseña de acceso estaba en la descripción del sistema (`sysDescr`), visible desde el primer segundo del "walk".

> [!TIP]
> **Regla de Oro SNMP**: Siempre asume que el administrador fue perezoso. Empieza con `public` en `v2c`, realiza un `walk` completo y analiza las primeras 10 líneas con especial atención a campos de "contacto" o "descripción".
