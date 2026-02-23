---
chunk_id: technique::linux::network::reset-network-services::001
domain: linux
chunk_type: technique
---

# Restart o reinicio de servicios de internet en entornos Linux/Kali

El error `Network is unreachable (code=101)` en OpenVPN indica que el sistema no posee una ruta válida para alcanzar la IP de destino. Este problema se soluciona diagnosticando la salida a internet y reiniciando el stack de red del sistema operativo.



## 1. Comandos de Diagnóstico Inicial
Antes de reiniciar, identifica el punto de fallo:

- **Verificar conectividad básica**: `ping -c 4 8.8.8.8`
- **Revisar interfaz e IP**: `ip addr` (Verifica que `eth0` o `wlan0` tengan una IP asignada).
- **Verificar Gateway (Puerta de enlace)**: `ip route` (Busca la línea que comienza con `default via...`).

## 2. Procedimiento de Reinicio (Reset)
Si la configuración parece correcta pero no hay tráfico, reinicia el gestor de red para forzar una nueva negociación de parámetros.

### Reinicio del Network Manager
Es el método más efectivo en Kali Linux para refrescar interfaces y rutas:
```bash
sudo systemctl restart NetworkManager

```

### Reinicio de Interfaz Específica

Si el problema persiste en una sola interfaz:

```bash
sudo ifconfig eth0 down && sudo ifconfig eth0 up

```

## 3. Resolución de Problemas de Ruta en VPN

Si el error ocurre específicamente al conectar OpenVPN, considera estos factores:

* **Bloqueos de Firewall**: Si el puerto (ej: 1337) está bloqueado, intenta cambiar el archivo `.ovpn` para usar el puerto `443 TCP`.
* **Rutas Persistentes**: A veces, una sesión de VPN anterior deja rutas "huérfanas". Reiniciar el servicio limpia la tabla de enrutamiento.
* **Configuración de VM**: En VirtualBox/VMware, asegúrate de que el adaptador esté en modo **Bridged** (Puente) o **NAT** con el cable conectado virtualmente.

> [!IMPORTANT]
> Si tras reiniciar el `NetworkManager` sigues sin tener una ruta por defecto (`default via`), es probable que el servidor DHCP de tu red no esté respondiendo o que necesites configurar una IP estática.

```

---
