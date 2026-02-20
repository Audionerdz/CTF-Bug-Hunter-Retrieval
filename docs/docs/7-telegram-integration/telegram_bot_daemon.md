# Telegram Bot Daemon - 24/7 Online Pattern

**File**: `/home/kali/Desktop/RAG/telegram_bot.py`  
**Lines**: 686  
**Purpose**: Bot RAG completamente funcional que busca en Pinecone + lee archivos locales
**Status**: ✅ Running with OpenAI 3072D embeddings + chunk_registry.json integration

---

## System Architecture (Feb 2026 Update)

El bot ahora funciona con un sistema completo de 4 componentes:

```
┌─────────────────────────────────────────────────────────┐
│           Telegram Bot System (Feb 2026)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. VECTORIZER (vectorize_canonical_openai.py)         │
│     └─ Genera embeddings 3072D (OpenAI)                │
│     └─ Sube a Pinecone: rag-canonical-v1-emb3large    │
│     └─ Auto-genera: chunk_registry.json                │
│        │                                                │
│  2. chunk_registry.json (LOCAL MAPPING)                │
│     └─ Maps: chunk_id → /ruta/archivo.md              │
│     └─ Ubicación: /home/kali/Desktop/RAG/             │
│     └─ Leído por Bot y Query Agent                    │
│        │                                                │
│  3. TELEGRAM BOT (telegram_bot.py)                      │
│     └─ Corre 24/7 en polling loop                     │
│     └─ Genera embeddings (OpenAI 3072D)               │
│     └─ Busca en Pinecone                              │
│     └─ Lee archivos locales via registry              │
│     └─ Envía contenido COMPLETO a Telegram            │
│        │                                                │
│  4. QUERY AGENT (query-agent-hybrid.py)               │
│     └─ Búsqueda manual + reporte markdown             │
│     └─ Puede enviar resultados a Telegram             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Startup Flow

Cuando arrancas el bot, ocurre esto:

```bash
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py
```

### Step 1: Load API Keys
```python
def load_api_keys():
    # Lee /root/.openskills/env/telegram.env
    # Lee /root/.openskills/env/pinecone.env  
    # Lee /root/.openskills/env/openai.env
    # Retorna: (telegram_token, chat_id, pinecone_key, openai_key)
```

### Step 2: Initialize RAG Engine
```python
rag_engine = RAGQueryEngine(pinecone_key, openai_key)
# En __init__:
#   1. Conecta a Pinecone (rag-canonical-v1-emb3large)
#   2. Carga chunk_registry.json
#   3. Imprime: "RAG Engine initialized: 15 chunks in registry"
```

**Output esperado:**
```
RAG Engine initialized: 15 chunks in registry
```

Este mensaje confirma que:
- ✅ Pinecone conectado
- ✅ Registry cargado (mapeando chunk_ids → archivos)
- ✅ Ready para búsquedas

### Step 3: Register Handlers

```python
app.add_handler(CommandHandler("q", query_command))
app.add_handler(CommandHandler("qf", query_facts_command))
app.add_handler(CommandHandler("qg", query_gavel_command))
app.add_handler(CommandHandler("qz", query_zip_command))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
```

Esto registra qué función ejecutar para cada comando.

---

## El Patrón: Polling Loop

Tu bot está **online 24/7** porque usa un **polling loop infinito**:

```python
# ════════════════════════════════════════════════════════════════════════════
# PATRÓN CLAVE: Application + run_polling()
# ════════════════════════════════════════════════════════════════════════════

from telegram.ext import Application

def main():
    # 1. Load API keys
    keys = load_api_keys()
    
    # 2. Create application (initializa bot connection)
    app = Application.builder().token(keys["telegram_token"]).build()
    
    # 3. Register command/message handlers
    app.add_handler(CommandHandler("start", start))          # /start command
    app.add_handler(CommandHandler("q", query_command))      # /q command
    app.add_handler(MessageHandler(filters.TEXT, handle))    # Any text message
    
    # 4. START POLLING LOOP (CORRE FOREVER)
    # ════════════════════════════════════════════════════════════════════════
    # Este es el secreto - el loop que mantiene el bot online
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    # ════════════════════════════════════════════════════════════════════════
    # Esta línea NUNCA retorna (a menos que Ctrl+C)
    # El bot:
    # 1. Conecta a Telegram API
    # 2. Pregunta constantemente: "¿hay mensajes nuevos?"
    # 3. Cuando hay, ejecuta los handlers registrados
    # 4. Responde al usuario
    # 5. Vuelve a 2) en loop infinito

if __name__ == "__main__":
    main()
```

## Query Flow (When User Sends `/q chmod permissions`)

Aquí es donde ocurre la magia - integración de 4 componentes:

```
1. USER SENDS MESSAGE
   └─ "/q chmod permissions" en Telegram

2. POLLING LOOP DETECTS IT
   └─ app.run_polling() recibe el mensaje

3. COMMAND HANDLER TRIGGERED
   └─ CommandHandler("q", query_command) → query_command()
   └─ context.args = ["chmod", "permissions"]

4. PARSE QUERY & TOP_K
   └─ parse_query_and_topk(["chmod", "permissions"]) 
   └─ query_text = "chmod permissions"
   └─ top_k = 5 (default)

5. GENERATE EMBEDDING (OpenAI 3072D)
   └─ client.embeddings.create(
       model="text-embedding-3-large",
       input="chmod permissions",
       dimensions=3072
   )
   └─ Retorna: [0.234, -0.891, ..., 0.456] (3072 números)

6. SEARCH PINECONE
   └─ idx.query(
       vector=embedding,
       top_k=5,
       include_metadata=True
   )
   └─ Retorna: 5 matches con metadata + chunk_id

7. READ LOCAL FILES (CRITICAL STEP)
   └─ FOR EACH match:
      a) Get chunk_id from metadata
      b) Look up in chunk_registry.json
      c) Get file path (e.g., "/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md")
      d) Read file locally
      e) Extract body (remove YAML frontmatter)
      f) Return complete content (NO TRUNCATION)

8. FALLBACK CHAIN (if local file fails)
   └─ If not found locally:
      content = metadata.get("content", "")
      └─ Uses Pinecone metadata as fallback

9. FORMAT RESPONSE
   └─ For each result:
      - chunk_id
      - machine (FACTS, GAVEL, etc)
      - score (relevance 0-1)
      - phase, technique
      - COMPLETE content

10. SEND TO TELEGRAM
    └─ If message > 4096 chars:
       └─ Split into multiple messages
       └─ Each message sent separately
    └─ NO TRUNCATION
    └─ User receives FULL content

11. BACK TO POLLING
    └─ Handler finishes
    └─ Bot goes back to listening
    └─ Espera next message
```

### Key Points

✅ **Complete integration**: Embedding → Pinecone → Registry → Local files  
✅ **3072D embeddings**: OpenAI text-embedding-3-large (highest quality)  
✅ **Local file priority**: Reads from disk first (better than metadata alone)  
✅ **No truncation**: Sends full content even if > 4096 chars (splits across messages)  
✅ **Graceful fallback**: If local file missing, uses metadata.content from Pinecone  

---

## Cómo Funciona el Polling

```
┌─────────────────────────────────────────────────────────┐
│                    POLLING LOOP (Infinito)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Iteración N:                                           │
│  ├─ Conecta a Telegram API                             │
│  ├─ Pregunta: "¿mensajes nuevos?"                      │
│  ├─ Si hay: ejecuta handler correspondiente            │
│  ├─ → Esto ejecuta la secuencia de 11 pasos arriba ←   │
│  └─ Espera < 1 segundo                                 │
│                                                         │
│  Iteración N+1:                                         │
│  ├─ Pregunta: "¿mensajes nuevos?"                      │
│  ├─ (usuario envía: "/q RCE techniques")              │
│  ├─ Ejecuta: query_command() → 11 pasos                │
│  ├─ Responde con resultados RAG                        │
│  └─ Espera < 1 segundo                                 │
│                                                         │
│  Iteración N+2: (continúa forever...)                  │
│  ...                                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
     ↑ Esto corre mientras el proceso esté activo
```
┌─────────────────────────────────────────────────────────────┐
│                    POLLING LOOP (Infinito)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Iteración 1:                                               │
│  ├─ Conecta a Telegram API                                 │
│  ├─ Pregunta: "¿mensajes nuevos?"                          │
│  ├─ Si hay: ejecuta handler correspondiente                │
│  └─ Espera 1 segundo                                       │
│                                                             │
│  Iteración 2:                                               │
│  ├─ Pregunta: "¿mensajes nuevos?"                          │
│  ├─ (usuario envía: "/q LFI")                              │
│  ├─ Ejecuta: query_command()                               │
│  ├─ Responde con resultados RAG                            │
│  └─ Espera 1 segundo                                       │
│                                                             │
│  Iteración 3: (continúa forever...)                        │
│  ...                                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
     ↑ Esto corre mientras el proceso esté activo
```

## Logs - Dos Niveles

### Nivel 1: Logging del Bot

```python
# El script incluye logging built-in
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Se usa para registrar eventos
logger.info("Mensaje recibido")
logger.error("Error en query")
```

**Sale por stdout:**
```bash
2026-02-13 10:30:45,123 - __main__ - INFO - Mensaje recibido
2026-02-13 10:30:46,456 - __main__ - INFO - Query procesada
```

### Nivel 2: Capturar Logs en Archivo

Para guardar logs 24/7, necesitas redirigir stdout:

```bash
# Opción A: Redirección simple
nohup python3 telegram_bot.py > /tmp/bot.log 2>&1 &

# Opción B: Con rotación de logs
python3 telegram_bot.py >> /var/log/telegram_bot/$(date +%Y%m%d).log 2>&1 &

# Opción C: systemd service (mejor)
# /etc/systemd/system/telegram-bot.service
[Unit]
Description=RAG Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/kali/Desktop/RAG
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## Cómo Está Arrancado Ahora (Feb 2026)

Bot se arranca con:
```bash
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py &
```

Para verificar:

```bash
# ¿Está corriendo?
ps aux | grep telegram_bot | grep -v grep
# Output: root  PID  0.0  0.4  449924  102888 ?  SNl  FEB14  0:36 /root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py

# ¿Qué versión está corriendo?
head -1 /home/kali/Desktop/RAG/telegram_bot.py
# Output: #!/usr/bin/env python3

# Ver logs
tail -f /home/kali/Desktop/RAG/telegram_bot.log
# Output: 2026-02-14 00:52:49,145 - __main__ - INFO - RAG Engine initialized: 15 chunks in registry

# Buscar errores
grep ERROR /home/kali/Desktop/RAG/telegram_bot.log

# Ver si está procesando queries
grep "Query error" /home/kali/Desktop/RAG/telegram_bot.log
```

### If Bot Shows "Content not available" Problem

**Causa**: Bot corre con versión vieja antes del fix

**Solución**:
```bash
# 1. Mata el proceso viejo
killall python3
sleep 1

# 2. Verifica que está muerto
ps aux | grep telegram_bot | grep -v grep
# (should return nothing)

# 3. Reinicia con versión nueva
/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/telegram_bot.py > /home/kali/Desktop/RAG/telegram_bot.log 2>&1 &

# 4. Verifica que cargó el registry
sleep 2 && tail -5 /home/kali/Desktop/RAG/telegram_bot.log
# Debe mostrar: "RAG Engine initialized: 15 chunks in registry"
```

## Patrón Resumido (Complete Feb 2026)

```
TELEGRAM_BOT_PATTERN:

1. Load credentials (API keys)
   - telegram.env
   - pinecone.env
   - openai.env
   ↓
2. Initialize RAG Engine
   - Conecta a Pinecone (rag-canonical-v1-emb3large)
   - Carga chunk_registry.json (15 chunks mapped)
   - Print: "RAG Engine initialized: 15 chunks in registry"
   ↓
3. Create Application object (Telegram bot)
   ↓
4. Register command handlers
   - /q (query all)
   - /qf (query FACTS)
   - /qg (query GAVEL)
   - /qz (query as ZIP)
   - /status, /help, etc
   ↓
5. START POLLING LOOP (app.run_polling())
   ↓
6. LOOP INFINITO (for each message):
   a) Detect message from user
   b) Identify command or text
   c) Parse query + top_k parameters
   d) Generate embedding (OpenAI 3072D)
   e) Query Pinecone with embedding
   f) For each result:
      - Get chunk_id
      - Look up in chunk_registry.json
      - Read file locally
      - Extract content (remove frontmatter)
      - Fallback to metadata.content if needed
   g) Format response
   h) Send to Telegram (multiple messages if > 4096 chars)
   i) Return to polling
   ↓
7. (Solo termina con Ctrl+C o crash)
```

### What Makes This Work (Feb 2026)

| Component | Purpose | Status |
|-----------|---------|--------|
| Vectorizer | Generate 3072D embeddings & upload to Pinecone | ✅ Working |
| chunk_registry.json | Map chunk_id → local file paths | ✅ Auto-generated |
| Telegram Bot | Polling + query handling | ✅ 24/7 online |
| RAG Engine | Coordinate Pinecone + local file reads | ✅ Integrated |
| OpenAI 3072D | Highest quality embeddings | ✅ Active |
| Fallback chain | Local file → metadata.content | ✅ Implemented |

## Comandos Disponibles

```bash
/start              # Inicializar
/help               # Mostrar ayuda
/status             # Estadísticas del índice
/q <query> [top_k]  # Query RAG (todos)
/qf <query> [top_k] # Query RAG (FACTS)
/qg <query> [top_k] # Query RAG (GAVEL)
/qz <query> [top_k] # Query RAG (ZIP output)

# Texto plano también funciona como query
"LFI exploitation"  # Busca automáticamente
```

## Diferencia: STT vs Bot

| Aspecto | STT (stt) | Bot (telegram_bot.py) |
|---------|-----------|----------------------|
| **Tipo** | CLI wrapper | Daemon/Service |
| **Ejecución** | Run & exit | Run forever |
| **Logs** | Ninguno | Built-in logger |
| **Triggers** | Llamadas manuales | Mensajes de Telegram |
| **Online** | No | Sí, 24/7 |
| **Patrón** | Script simple | Polling loop |

---

**El bot usa python-telegram-bot Application + run_polling() para estar siempre escuchando**
