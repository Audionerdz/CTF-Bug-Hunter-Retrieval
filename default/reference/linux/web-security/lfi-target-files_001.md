---
chunk_id: reference::linux::web-security::lfi-target-files::001
domain: reference
chunk_type: technique
---

# Diccionario de archivos críticos para explotación de LFI en Linux

Una vez confirmada la vulnerabilidad de Local File Inclusion (LFI), el objetivo es extraer información sensible o preparar el camino hacia una Ejecución Remota de Comandos (RCE). A continuación se listan los archivos objetivos categorizados por su utilidad.

## 1. Identificación de Usuarios y Credenciales
* **/etc/passwd**: Lista de usuarios del sistema. Crucial para identificar nombres de usuario válidos para ataques de fuerza bruta o SSH.
* **/etc/shadow**: Contiene los hashes de las contraseñas (requiere privilegios elevados para ser leído).

## 2. Archivos de Configuración Web y Entorno
Contienen frecuentemente credenciales de bases de datos, llaves de API y configuraciones de seguridad.
* `/var/www/html/config.php`: Archivo de configuración estándar en PHP.
* `/var/www/html/.env`: Archivo de variables de entorno (común en frameworks modernos).
* `/var/www/html/wp-config.php`: Configuración de sitios WordPress.

## 3. Configuración del Servidor y Lenguaje
Útiles para entender límites de subida de archivos y wrappers permitidos.
* `/etc/php.ini` o `/etc/php/[VERSION]/apache2/php.ini`: Configuración global de PHP.

## 4. Archivos de Log (Vectores para RCE)
El acceso a logs permite realizar **Log Poisoning** inyectando código PHP en campos como el `User-Agent`.
* **Apache:** `/var/log/apache2/access.log`, `/var/log/apache2/error.log`
* **Nginx:** `/var/log/nginx/access.log`, `/var/log/nginx/error.log`

## 5. Gestión de Sesiones
Si se conoce el ID de sesión del usuario (`PHPSESSID`), se puede intentar leer o manipular los datos de sesión.
* `/var/lib/php/sessions/sess_[ID_DE_SESION]`

## 6. Archivos Especiales del Sistema (/proc)
Permiten obtener información sobre el proceso actual y variables de entorno del servidor.
* **/proc/self/environ**: Lista las variables de entorno del proceso web (potencial para RCE si se puede manipular una variable).
* **/proc/self/fd/[ID]**: File descriptors; permiten acceder a archivos abiertos por el proceso (útil si los logs estándar están protegidos).

> **TIP:** Si no encuentras los archivos en las rutas por defecto, utiliza el fuzzing de rutas para identificar directorios de instalación personalizados.
