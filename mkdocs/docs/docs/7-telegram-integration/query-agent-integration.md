# Query Agent Integration - Hybrid Search Mode

**File**: `/root/.opencode/skills/query-agent/executables/query-agent-hybrid.py`  
**Lines**: 369  
**Purpose**: Manual RAG queries with local file reading + markdown reporting + optional Telegram sending

---

## Overview

The Query Agent is an **alternative to the Telegram Bot** for users who prefer:
- Manual/scheduled searches
- Detailed markdown reports
- Saving results to files
- Custom formatting
- Sending results to Telegram programmatically

```
Query Agent Flow:
User runs command
        ↓
Parse arguments (query, top_k, machine filter)
        ↓
Initialize HybridQueryAgent
        ├─ Load API keys
        ├─ Connect to Pinecone
        ├─ Load chunk_registry.json
        ↓
Generate 3072D embedding (OpenAI)
        ↓
Search Pinecone with embedding
        ↓
For each result:
  ├─ Look up chunk_id in registry
  ├─ Read file locally
  ├─ Extract body (remove YAML)
  ├─ Include COMPLETE content
        ↓
Format as Markdown (with full content)
        ↓
Save to file
        ↓
Optionally send to Telegram
        ↓
Display summary in terminal
```

---

## Usage

### Basic Query
```bash
python3 /root/.opencode/skills/query-agent/executables/query-agent-hybrid.py "chmod permissions"
```

Output:
- Markdown file saved: `query_results_chmod_permissions_20260214_120530.md`
- Content includes COMPLETE chunks (not truncated)
- Sends to Telegram by default

### Advanced Options

```bash
# Specify top_k (number of results)
python3 query-agent-hybrid.py "LFI exploitation" --top-k 10

# Filter by machine
python3 query-agent-hybrid.py "RCE techniques" --machine facts

# Both options
python3 query-agent-hybrid.py "privesc" --top-k 15 --machine gavel

# Save only (no Telegram sending)
python3 query-agent-hybrid.py "web enum" --no-telegram
```

### Output Examples

#### Markdown Report
```markdown
# Query Agent - Resultados de Busqueda Completa

**Timestamp:** 2026-02-14 12:05:30
**Index:** `rag-canonical-v1-emb3large`
**Modelo:** `text-embedding-3-large` (3072D)
**Consulta:** `chmod permissions`
**Resultados:** 5

---

## Resultados Relevantes

### 1. reference::linux::permissions::chmod-user::001
- **Maquina:** FACTS
- **Fase:** enumeration
- **Tecnica:** permissions
- **Dominio:** linux
- **Score:** 0.874
- **Archivo:** `/root/.openskills/CHEATSHEETS CHUNKS/chmod-user_001.md`
- **Tamano:** 428 caracteres

**Contenido Completo:**
```
### **Permisos archivos al dueño (u)**

Dar solo lectura:  
`chmod u+r archivo`

Dar solo escritura:  
`chmod u+w archivo`

Dar solo ejecución:  
`chmod u+x archivo`
...
```

### 2. reference::linux::permissions::chmod-group::001
...

---
```

---

## Code Architecture (369 lines)

### Class: `HybridQueryAgent`

```python
class HybridQueryAgent:
    """
    Agente híbrido que:
    1. Busca en Pinecone (embedding similarity)
    2. Lee archivos locales (complete content)
    3. Genera reportes markdown
    4. Opcionalmente envía a Telegram
    """
    
    def __init__(self):
        """
        Inicializa:
        - Conexión a Pinecone
        - Cliente OpenAI
        - Carga chunk_registry.json
        """
        
    def get_embedding(self, text):
        """
        Genera 3072D embedding con OpenAI
        - Mismo modelo que vectorizer
        - Mismo modelo que telegram bot
        """
        
    def extract_body(self, content):
        """
        Extrae body del chunk (sin YAML frontmatter)
        - Busca "---" al inicio
        - Divide en 3 partes
        - Retorna parte 2 (body)
        """
        
    def read_chunk_locally(self, chunk_id):
        """
        Lee chunk completo desde filesystem
        - Busca chunk_id en registry
        - Abre archivo en ruta mapeada
        - Extrae body
        - Retorna contenido COMPLETO (no truncado)
        """
        
    def query(self, user_query, top_k=5, machine_filter=None):
        """
        Ejecuta búsqueda RAG completa:
        1. Genera embedding (3072D)
        2. Busca en Pinecone
        3. Lee archivos locales
        4. Retorna resultados con contenido completo
        """
        
    def format_response(self, results, query=None, machine_filter=None):
        """
        Formatea resultados como markdown profesional
        - Header con metadata
        - Cada resultado con campos estructurados
        - Contenido COMPLETO en bloque de código
        """
        
    def save_markdown(self, content, query):
        """
        Guarda markdown a archivo con timestamp
        - Nombre: query_results_<query>_<timestamp>.md
        - Ubicación: /home/kali/Desktop/RAG/
        - Encoding: UTF-8
        """
        
    def send_to_telegram(self, markdown_path):
        """
        Envía markdown a Telegram usando telegram_sender.py
        - Valida que archivo existe
        - Ejecuta subprocess con telegram_sender.py
        - Captura output/errores
        """
```

---

## Comparison: Bot vs Query Agent

| Feature | Telegram Bot | Query Agent |
|---------|-------------|------------|
| **Trigger** | Message in Telegram | Manual command |
| **Online** | 24/7 polling | Run-on-demand |
| **Response** | Immediate (bot) | Saved to file + optional Telegram |
| **Formatting** | Multiple Telegram messages | Single markdown file |
| **Persistence** | No saved history | Files saved with timestamp |
| **Customization** | Limited (CLI commands) | Full Python script (can modify) |
| **Use Case** | Quick queries on mobile | Detailed reports, batch searches, automation |

---

## When to Use Each

### Use Telegram Bot (`/q <query>`)
- ✅ Quick query while on the go
- ✅ Mobile device (phone)
- ✅ Real-time collaboration
- ✅ Interactive exploration

### Use Query Agent
- ✅ Save detailed reports
- ✅ Schedule regular searches
- ✅ Batch multiple queries
- ✅ Generate markdown for documentation
- ✅ Custom post-processing
- ✅ Integrate with other tools

---

## Integration Points

### 1. With Pinecone
```python
# Both bot and agent use same:
# - Index: rag-canonical-v1-emb3large
# - Model: text-embedding-3-large (3072D)
# - Namespace: __default__
```

### 2. With chunk_registry.json
```python
# Both read same registry file:
# /home/kali/Desktop/RAG/chunk_registry.json
# Enables local file reading
```

### 3. With Telegram
```python
# Agent can optionally send results:
subprocess.run([
    venv_python,
    telegram_script,
    "--file",
    str(markdown_path)
])
# Uses same telegram_sender.py as other tools
```

### 4. With OpenAI
```python
# Same embedding model as vectorizer + bot:
# text-embedding-3-large
# dimensions=3072
```

---

## Example Workflows

### Workflow 1: Daily Security Report
```bash
#!/bin/bash
# Run every morning at 8am
python3 query-agent-hybrid.py "latest exploits" --top-k 10
python3 query-agent-hybrid.py "CVE updates" --top-k 10
python3 query-agent-hybrid.py "OWASP top 10" --top-k 5
# All saved as .md files with timestamp
```

### Workflow 2: CTF Preparation
```bash
#!/bin/bash
# Generate cheatsheet for upcoming CTF
python3 query-agent-hybrid.py "web exploitation" --top-k 20 --machine facts
python3 query-agent-hybrid.py "Linux privesc" --top-k 15 --machine facts
python3 query-agent-hybrid.py "network enumeration" --top-k 10
# Combine all markdown files into one document
```

### Workflow 3: Share Results with Team
```bash
#!/bin/bash
# Search and send to team Telegram
python3 query-agent-hybrid.py "RCE techniques" --top-k 15
# Markdown file created
# Automatically sent to Telegram group
# Team can review complete content
```

### Workflow 4: Documentation Generation
```bash
#!/bin/bash
# Generate knowledge base
python3 query-agent-hybrid.py "API security" --top-k 25 --no-telegram
# Save to file
# Convert markdown to PDF
# Upload to wiki
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `chunk_registry.json` not found | Registry not generated | Run vectorizer script first |
| `PINECONE_API_KEY not found` | Missing env file | Create `/root/.openskills/env/pinecone.env` |
| `OPENAI_API_KEY not found` | Missing env file | Create `/root/.openskills/env/openai.env` |
| File not found in registry lookup | Chunk_id doesn't exist | Check that chunk was vectorized |
| Telegram sending fails | Credentials or network issue | Check telegram.env, verify internet |

---

## Advanced Usage

### Modify for Custom Formatting
```python
def format_response(self, results):
    # Change markdown format
    # Add custom fields
    # Filter results
    # Add calculations
```

### Chain Multiple Queries
```python
queries = [
    ("LFI exploitation", 10, "facts"),
    ("RCE payloads", 10, "facts"),
    ("web shells", 5, "gavel"),
]

for query, top_k, machine in queries:
    results = agent.query(query, top_k, machine)
    md = agent.format_response(results, query, machine)
    agent.save_markdown(md, query)
```

### Process Results Programmatically
```python
agent = HybridQueryAgent()
results = agent.query("docker escape")

for result in results:
    chunk_id = result["chunk_id"]
    machine = result["machine"]
    score = result["score"]
    content = result["content_full"]
    
    # Do something with the content
    if score > 0.8:
        print(f"High relevance: {chunk_id}")
```

---

## Best Practices

1. **Always specify --machine if needed** - Reduces noise in results
2. **Use appropriate top_k** - 5-10 for quick lookup, 15-20 for reports
3. **Save markdown files** - They're permanent records of searches
4. **Review before sharing** - Edit markdown before sending to team
5. **Combine with Telegram** - Use agent for detailed reports, bot for quick access
6. **Schedule regular runs** - Build knowledge base incrementally

---

## Next Steps

1. Try basic query: `query-agent-hybrid.py "your_topic"`
2. Check generated markdown file
3. Explore options: `--top-k`, `--machine`, `--no-telegram`
4. Automate with cron/scheduler
5. Integrate with your workflow

---

**The Query Agent: powerful, flexible, scriptable.**
