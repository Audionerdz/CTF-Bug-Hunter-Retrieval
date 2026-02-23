---
chunk_id: technique::linux::security::ssh-forensics-management::001
domain: linux
chunk_type: technique
---

# Forense de SSH y Gestión de Sesiones

Esta guía proporciona comandos esenciales para detectar intrusiones, analizar intentos de fuerza bruta y gestionar sesiones sospechosas en servidores Linux.



## 1. Detección de Actividad Inmediata
Identifica quién está en el sistema y qué procesos están ejecutando en tiempo real.

```bash
w                # Usuarios logueados y actividad de procesos
who              # Lista simplificada de conexiones actuales
last -n 20       # Historial de los últimos 20 inicios de sesión exitosos
lastb -n 20      # Historial de los últimos 20 intentos fallidos (Bad logins)

```

## 2. Análisis Profundo de Logs (Auditoría)

Extracción de inteligencia de los archivos de autenticación para identificar patrones de ataque.

```bash
# Ver intentos fallidos (ajustar ruta según distribución)
tail -50 /var/log/auth.log || tail -50 /var/log/secure

# Extraer IPs con más intentos fallidos (Fuerza Bruta)
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr | head

# IPs con más ruido total (Fallidos + Usuarios Inválidos)
grep -E "(Failed|Invalid)" /var/log/auth.log | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq -c | sort -nr | head

```

## 3. Monitoreo de Conexiones y Procesos

Verifica el estado de las conexiones TCP y los procesos del demonio `sshd`.

```bash
ss -tnp | grep :22   # Conexiones activas al puerto 22 con sus PIDs
ps aux | grep sshd   # Lista procesos del servidor SSH

```

## 4. Contención y Gestión de Sesiones

Procedimientos para expulsar atacantes o limpiar sesiones colgadas.

```bash
# Matar sesión por terminal (TTY)
pkill -9 -t pts/0

# Expulsar todas las conexiones de una IP específica
ss -tnp | grep "IP_SOSPECHOSA" | grep -oP 'pid=\K[0-9]+' | xargs kill -9

# Reiniciar servicio para purgar conexiones zombie
systemctl restart ssh

```

## 5. Verificación de Defensas (Firewall/Fail2Ban)

Comprobar si las herramientas de baneo automático están funcionando correctamente.

```bash
fail2ban-client status sshd   # Ver IPs actualmente baneadas por fail2ban
iptables -L -n | grep 22      # Listar reglas de firewall para el puerto 22
ufw status                    # Estado de Uncomplicated Firewall

```

## Resumen Forense Rápido (One-liner)

Ejecuta este comando para obtener una foto instantánea del estado de seguridad de SSH:

```bash
echo "=== Usuarios activos ===" && w && echo -e "\n=== Conexiones SSH ===" && ss -tnp | grep :22 && echo -e "\n=== Top IPs atacantes ===" && grep -E "(Failed|Invalid)" /var/log/auth.log 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq -c | sort -nr | head -5

```

> [!TIP]
> Si detectas una IP atacante persistente que Fail2Ban no ha bloqueado, puedes banearla manualmente con: `iptables -A INPUT -s IP_ATACANTE -j DROP`.

```

---
