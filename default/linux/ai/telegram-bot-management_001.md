---
chunk_id: technique::linux::ai::telegram-bot-management::001
domain: linux
chunk_type: technique
confidence: 5
reuse_level: 1
tags: [telegram-bot, python, rag, automation, maintenance, logs]
---

# Operación y Gestión del Bot de Telegram (RAG Engine)

Guía operativa para el control del bot de Telegram integrado con el motor RAG. Incluye comandos de ciclo de vida, monitoreo de salud y resolución de fallos.



## 1. Comandos de Control de Ciclo de Vida
Interfaz rápida para el manejo del proceso en segundo plano.

| Acción | Comando |
| :--- | :--- |
| **Iniciar** | `telegram-bot-start` |
| **Parar** | `telegram-bot-stop` |
| **Reiniciar** | `telegram-bot-stop && telegram-bot-start` |
| **Ver Estado** | `ps aux | grep telegram_bot` |
| **Logs (Live)** | `telegram-bot-logs` |

## 2. Ubicaciones Críticas del Sistema
Rutas fundamentales para la configuración y auditoría del servicio.

* **Script Principal**: `/home/kali/Desktop/RAG/src/telegram_bot.py`
* **Archivo de Logs**: `/home/kali/Desktop/RAG/telegram_bot.log`
* **Variables de Entorno**: `/root/.openskills/env/telegram.env`
* **Registro de Chunks**: `/home/kali/Desktop/RAG/chunk_registry.json`



## 3. Comandos Disponibles en Telegram
El bot responde a la siguiente gramática de comandos:

- `/query <TEXTO>`: Realiza una búsqueda semántica en la base de datos de vectores.
- `/stats`: Muestra estadísticas del índice y del sistema.
- `/start` / `/help`: Información de inicio y lista de comandos.

## 4. Troubleshooting y Recuperación
Si el bot no responde o presenta errores de conexión:

**A. Reinicio Forzado (One-liner):**
```bash
pkill -f telegram_bot.py ; sleep 2 ; cd /home/kali/Desktop/RAG && nohup /root/.openskills/venv/bin/python3 src/telegram_bot.py > telegram_bot.log 2>&1 &

```

**B. Verificación de Conectividad:**
Revisa los logs buscando `HTTP Request: POST https://api.telegram.org/`. Si hay errores 401, verifica el token en `telegram.env`.

**C. Mantenimiento de Logs:**
Para evitar saturación de disco, vacía el log sin detener el proceso:

```bash
> /home/kali/Desktop/RAG/telegram_bot.log

```

> [!IMPORTANT]
> El bot requiere que los índices de Pinecone ("rag-canonical-v1-emb3large") y las APIs de OpenAI/Gemini estén activos. Verifica los archivos `.env` en `/root/.openskills/env/` antes de reportar fallos en el script.

```

---

