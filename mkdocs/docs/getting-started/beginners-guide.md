# Beginner's Guide: Using a Python Framework

If you've only ever used Python by running individual scripts like `python3 my_script.py`, this page is for you. A framework works differently -- you open a Python **interactive session** and talk to it like a conversation.

## The Old Way: Running Scripts

You're probably used to this:

```bash
python3 query_fast.py "LFI exploitation"
python3 vectorize_canonical_openai.py /path/to/chunks
python3 gemini_rag.py
```

Each script is independent. You run it, it does one thing, it exits. If you want to do something else, you run a different script.

## The New Way: Interactive Framework

With the RAG framework, you open **one Python session** and do everything from there:

```bash
python3
```

Your terminal changes from `$` to `>>>`. This means Python is listening. Now type:

```python
from atlas_engine import Atlas
atlas = Atlas()
```

You'll see:

```
Atlas Engine v2.0
  Index: rag-canonical-v1-emb3large:__default__
  Chunks: 158
  Root: /home/kali/Desktop/RAG
```

That `r` object is your **entire framework**. Think of it as a remote control with all the buttons.

## Your First Commands

Now that `r` is ready, try these one at a time:

### Search your knowledge base

```python
atlas.query("LFI exploitation, top_k=2")
```

```python
atlas.query("Ffuf cheatsheet") # Default 5
```

## Common query flags

```
 atlas.query(
      "search text",
      top_k=5,           # Número de resultados
      machine="facts",   # Filtrar por máquina
      domain="web",      # Filtrar por dominio
      max_chars=1000,    # Limitar caracteres del contenido
      namespace="cve",   # Namespace específico
      show=True          # Mostrar en terminal
  )
```


This searches your Pinecone index and shows results right in the terminal. No script needed.

### Search with filters

```python
atlas.query("privilege escalation", top_k=10, machine="facts")
```

### Get a specific chunk

```python
r.fetch("technique::web::lfi::path-traversal::001")
```

### See index statistics

```python
r.stats()
```

### Ask a question (AI-powered answer)

```python
response, sources = atlas.ask("How does SQL injection work?")
print(response)
```

### See all available commands

```python
r.help()
```

## How It Feels

Think of the `>>>` prompt as a **chat with your framework**:

```
You:       atlas.query("RCE")
Framework: [shows 5 results with scores, content, metadata]

You:       atlas.query("RCE", top_k=10, namespace="cve")
Framework: [shows 10 results from the CVE namespace]

You:       atlas.ask("What is SUID?")
Framework: [returns AI-generated answer with cited sources]

You:       r.chunk("/home/kali/reports/scan.pdf")
Framework: [splits the PDF into chunks, saves them]

You:       atlas.vectorize("/home/kali/Desktop/RAG/chunks")
Framework: [embeds and uploads all chunks to Pinecone]
```

You stay in the same session. Everything shares the same connection to Pinecone, the same registry, the same configuration. No re-initialization between commands.

## The `r` Object Explained

When you type `atlas = Atlas()`, you create an object that contains:

| What | How to Access | Description |
|------|---------------|-------------|
| Query Engine | `atlas.query()` | Search Pinecone |
| Chunker | `r.chunk()` | Split PDFs/text into pieces |
| Vectorizer | `atlas.vectorize()` | Embed and upload to Pinecone |
| Chat | `atlas.chat()` / `atlas.ask()` | Talk to an LLM with your data |
| Telegram | `atlas.send()` | Send results to Telegram |
| Registry | `r.chunks()` | See all tracked chunks |

All of these are connected. The query engine knows about your registry. The vectorizer registers new chunks automatically. Everything stays in sync.

## Namespace Support

You can target specific namespaces (think of them as folders in your vector database):

```python
# At creation time (affects everything)
r = RAG(namespace="cve")

# Per command (one-off override)
atlas.query("buffer overflow", namespace="ctf")
atlas.ask("What is XSS?", namespace="technique")
atlas.vectorize("/path/to/chunks", namespace="tools")
```

## Adding Metadata to Plain Markdown

If you have `.md` files without YAML frontmatter, you can inject metadata at vectorize time:

```python
# Add domain and tags to plain markdown files
atlas.vectorize("notes.md", domain="web", tags=["exploit", "lfi"])

# Add arbitrary metadata fields
atlas.vectorize("/chunks/", domain="cve", metadata={"confidence": "high", "source": "NIST"})
```

From the CLI:

```bash
vectorize notes.md --domain web --tags exploit,lfi
```

Files that already have frontmatter keep their existing fields -- only missing fields get filled in.

## Exiting

When you're done, type:

```python
exit()
```

Or press `Ctrl+D`.

## Quick Recipe: Common Workflows

### "I have a PDF and want to search it"

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.ingest("/home/kali/reports/nmap_scan.pdf")
atlas.query("open ports")
```

### "I want to search and send results to Telegram"

```python
from atlas_engine import Atlas
atlas = Atlas()
results = atlas.query("RCE techniques")
atlas.send(results)
```

### "I want to chat with my knowledge base"

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.chat()          # Gemini (default)
atlas.chat("gpt")     # GPT-4o-mini
atlas.chat("ollama")   # Ollama local
```

### "I just want a quick answer"

```python
from atlas_engine import Atlas
atlas = Atlas()
answer, sources = atlas.ask("How do I enumerate SUID binaries?")
print(answer)
```

## Still Prefer Scripts?

The CLI aliases still work. You don't have to use the interactive mode:

```bash
query "LFI exploitation"
query "RCE" --namespace cve
vectorize /path/to/chunks --namespace ctf
GeminiRag
pa "search text"
```

Both approaches hit the same framework underneath. Use whatever feels natural.
