# PDF Chunker

The PDF Chunker splits PDFs (and other documents) into RAG-ready markdown chunks with YAML frontmatter. It uses LangChain's `RecursiveCharacterTextSplitter` to create semantically meaningful splits.

## Supported Formats

| Format | Extension |
|--------|-----------|
| PDF | `.pdf` |
| Plain Text | `.txt` |
| Markdown | `.md` |
| HTML | `.html` |
| CSV | `.csv` |

## Quick Start

### From Python (Recommended)

```python
from atlas_engine import Atlas
atlas = Atlas()

# Chunk a single PDF
r.chunk("/home/kali/reports/nmap_scan.pdf")

# Chunk all files in a directory
r.chunk("/home/kali/reports/")

# Chunk and vectorize in one shot
atlas.ingest("/home/kali/reports/nmap_scan.pdf")
```

### From the Terminal

```bash
vectorize /home/kali/Desktop/RAG/chunks
```

## Parameters

### r.chunk() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | string | Required | File or directory path |
| `output_dir` | string | `RAG/chunks/` | Where to save output chunks |
| `domain` | string | `"document"` | Metadata domain field |
| `tags` | list | None | Optional tags for all chunks |
| `chunk_size` | int | 2800 | Max characters per chunk (~700 tokens) |
| `chunk_overlap` | int | 320 | Overlap between chunks (~80 tokens) |

### atlas.ingest() Parameters

Same as `r.chunk()` plus:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `namespace` | string | Instance default | Pinecone namespace to vectorize into |

## Examples

### Single PDF

```python
r.chunk("/home/kali/reports/scan_results.pdf")
```

Output:

```
============================================================
CHUNKER - RecursiveCharacterTextSplitter
============================================================
Path: /home/kali/reports/scan_results.pdf
Chunk size: 2800 chars
Overlap: 320 chars

Discovered: 1 file(s)
  loaded: scan_results.pdf (12 pages/sections)
Total loaded: 12 documents from 1 files
Split: 12 docs -> 28 chunks (size=2800, overlap=320)
Saved: 28 chunks to /home/kali/Desktop/RAG/chunks

Done: 1 files -> 12 docs -> 28 chunks
```

### Directory of PDFs

```python
r.chunk("/home/kali/reports/")
```

This recursively finds all supported files in the directory and chunks them all.

### With Domain Tag

```python
r.chunk("/home/kali/cve_reports/", domain="cve", tags=["vulnerability", "2026"])
```

Every chunk gets the `domain: cve` metadata and the specified tags.

### Custom Chunk Size

```python
# Smaller chunks (more precise retrieval)
r.chunk("/path/to/file.pdf", chunk_size=1500, chunk_overlap=150)

# Larger chunks (more context per chunk)
r.chunk("/path/to/file.pdf", chunk_size=4000, chunk_overlap=500)
```

### Custom Output Directory

```python
r.chunk("/path/to/file.pdf", output_dir="/home/kali/my_chunks")
```

### Full Pipeline: PDF to Pinecone

```python
# One command: chunk + vectorize
atlas.ingest("/home/kali/reports/scan.pdf")

# With options
atlas.ingest("/home/kali/reports/", domain="cve", namespace="cve")

# With all options
atlas.ingest(
    "/home/kali/reports/pentest.pdf",
    domain="web",
    tags=["pentest", "2026"],
    chunk_size=2000,
    chunk_overlap=200,
    namespace="ctf"
)
```

## Granular Pipeline

For more control, use the chunker directly:

```python
from atlas_engine import Atlas
atlas = Atlas()

# Step 1: Find files
files = r.chunker.discover("/home/kali/reports/")
# Returns: ['/home/kali/reports/scan.pdf', '/home/kali/reports/notes.txt']

# Step 2: Load documents
docs = r.chunker.load(files)
# Returns: list of LangChain Document objects

# Step 3: Split into chunks
chunks = r.chunker.split(docs, chunk_size=2000)
# Returns: list of Chunk dataclass objects

# Step 4: Save as markdown with frontmatter
saved = r.chunker.save(chunks, domain="web", tags=["pentest"])
# Returns: list of saved file paths
```

## What the Output Looks Like

Each chunk is saved as a `.md` file with YAML frontmatter:

```yaml
---
chunk_id: chunk::scan-results::001
chunk_type: pdf-chunk
domain: document
source: /home/kali/reports/scan_results.pdf
page: 1
chunk_index: 0
total_chunks: 28
created: 2026-02-25
---

Nmap scan report for 10.10.11.25
Host is up (0.045s latency).
Not shown: 998 closed tcp ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1
80/tcp open  http    Apache httpd 2.4.52
```

## Default Settings

| Setting | Value | Explanation |
|---------|-------|-------------|
| Chunk size | 2800 chars | ~700 tokens at 4 chars/token |
| Overlap | 320 chars | ~80 tokens, 10-15% of chunk size |
| Splitter | RecursiveCharacterTextSplitter | Splits on paragraphs, then sentences, then words |
| Output dir | `RAG/chunks/` | Default save location |

The `RecursiveCharacterTextSplitter` tries to split on natural boundaries:

1. Double newlines (`\n\n`) -- paragraph breaks
2. Single newlines (`\n`) -- line breaks
3. Periods (`. `) -- sentence breaks
4. Spaces (` `) -- word breaks
5. Empty string (`""`) -- character level (last resort)

## Injecting Metadata at Vectorize Time

After chunking, when you vectorize the output, you can inject metadata into the chunks -- even if they don't have YAML frontmatter:

### From Python

```python
# Chunk a PDF (generates .md files with basic frontmatter)
r.chunk("/path/to/report.pdf")

# Vectorize with extra metadata injected
atlas.vectorize("/home/kali/Desktop/RAG/chunks", domain="web", tags=["pentest", "2026"])

# Or with arbitrary metadata fields
atlas.vectorize("/home/kali/Desktop/RAG/chunks",
    domain="cve",
    tags=["vulnerability"],
    metadata={"confidence": "high", "source": "NIST"}
)
```

### From the CLI

```bash
vectorize /home/kali/Desktop/RAG/chunks --domain web --tags pentest,2026
vectorize notes.md --domain cve --tags exploit,lfi --namespace cve
```

### How It Works

- For **plain markdown** (no frontmatter): `domain`, `tags`, and any `metadata` fields are added to the auto-generated metadata
- For **files with frontmatter**: only missing fields get filled in -- existing fields are never overwritten
- Tags are merged: if the chunk already has `["web"]` and you inject `["exploit"]`, it gets `["web", "exploit"]`

## Tips

- **For dense technical PDFs** (CVEs, nmap scans): Use default settings (2800/320)
- **For long narrative reports**: Consider larger chunks (4000/500)
- **For code-heavy content**: Consider smaller chunks (1500/150)
- **Always review a few output chunks** to make sure the splits make sense
- **Use `atlas.ingest()`** when you want the fastest path from PDF to searchable Pinecone index
- **Use `--domain` and `--tags`** on vectorize to add metadata to plain markdown without editing files
