---
chunk_id: technique::web::fuzzing::ffuf::background-process-management::001
domain: web
chunk_type: technique
---

# Gestión de procesos de ffuf en segundo plano

En auditorías extensas, es necesario liberar la terminal para continuar trabajando mientras `ffuf` ejecuta escaneos pesados. Esto se logra mediante el control de procesos de Linux y la redirección de salidas para no perder los hallazgos.



## 1. Cómo correr ffuf en el Background
Para enviar `ffuf` al fondo desde el inicio, se utiliza el operador `&`. Es imperativo redirigir la salida a un archivo, de lo contrario, los resultados imprimirán "basura" en tu terminal activa.

### Comando recomendado:
```bash
ffuf -w wordlist.txt:FUZZ -u http://TARGET/FUZZ -o results.json > scan.log 2>&1 &

```

**Desglose de la sintaxis:**

* `> scan.log`: Guarda la salida estándar (lo que ves en pantalla).
* `2>&1`: Redirige los errores al mismo archivo de log.
* `&`: Envía el proceso al background inmediatamente.

### Alternativa: Pausar y enviar al fondo

Si ya iniciaste `ffuf` y te das cuenta de que tardará mucho:

1. Presiona `Ctrl + Z` (esto pausa el proceso y te da un ID de trabajo, ej: `[1]+ Stopped`).
2. Escribe `bg` y presiona Enter (esto reanuda el proceso pero en segundo plano).

## 2. Cómo ver el proceso activo

Si necesitas saber si `ffuf` sigue corriendo o cuántos recursos consume, puedes usar herramientas de monitoreo de procesos.

* **Listar procesos de ffuf**: `ps aux | grep ffuf`
* **Ver jerarquía de trabajos en la sesión actual**: `jobs -l`
* **Monitoreo dinámico**: `htop` (presiona `F4` y escribe "ffuf" para filtrar).

## 3. Cómo matar el proceso (Kill Workflow)

Si el escaneo está causando un DoS, detectaste un WAF o simplemente te equivocaste de wordlist, debes finalizar el proceso.

### Paso 1: Identificar el PID (Process ID)

Usa el comando `ps` para obtener el número de la segunda columna:

```bash
ps aux | grep ffuf
# Resultado: user  12345  0.5  0.2 ... ffuf -w ...

```

### Paso 2: Ejecutar el Kill

* **Muerte suave (recomendada)**: `kill 12345` (envía señal SIGTERM para que cierre archivos correctamente).
* **Muerte forzada**: `kill -9 12345` (si el proceso no responde).
* **Matar todos los ffuf**: `pkill ffuf` (útil si lanzaste varios por error).

## 4. Workflow de Reconexión (screen/tmux)

Para una gestión profesional, se recomienda usar multiplexores de terminal en lugar de `&`. Esto permite cerrar la terminal o la conexión SSH sin matar el proceso.

1. Iniciar sesión: `tmux new -s fuzzing`
2. Ejecutar ffuf: `ffuf -w ...`
3. Salir (Detach): `Ctrl + B` y luego `D`
4. Volver (Attach): `tmux attach -t fuzzing`

> [!IMPORTANT]
> Siempre usa el parámetro `-o` (output) al correr en background. Si el proceso termina o lo matas, el archivo JSON contendrá todos los resultados guardados hasta ese milisegundo.

```

---
