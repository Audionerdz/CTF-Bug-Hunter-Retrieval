# Core Principles: The Master Guide to Chunking

This is the **definitive guide**. If you follow this, you'll never doubt how to chunk again.

## 🧠 Fundamental Concepts (Critical Foundation)

### What is a CHUNK?

A chunk is:
- The **smallest unit of knowledge**
- That **stands alone and makes sense**
- Answers **exactly one question**
- Is **reusable**

A chunk is NOT:
- A chapter
- A writeup
- A chronological story
- A general reference

**The Golden Rule:** A chunk answers ONE question.

### What is a NAMESPACE?

A namespace is:
- A **semantic domain** (collection of related chunks)
- A **filter before embeddings**
- A **grouping for context**

Examples:
```
htb-machines
chunking-guides
rag-architecture
programming-python
life-notes
web-security
```

### What is a MANIFEST?

A manifest is:
- An **index of files**
- A **record of ingestion**
- A **control table**

NOT:
- Knowledge
- Content
- Something Telegram queries

## 📊 Correct Architecture

```
rag/
├── htb-machines/
│   ├── manifest.json
│   ├── gavel/
│   │   ├── enum/
│   │   │   ├── git_exposure.md
│   │   │   ├── nmap_ports.md
│   │   ├── exploit/
│   │   │   ├── runkit_rce.md
│
├── chunking-guides/
│   ├── manifest.json
│   ├── principles/
│   │   ├── single_intent.md
│   │   ├── chunk_size.md
│
├── rag-architecture/
│   ├── manifest.json
│   ├── namespaces.md
│   ├── manifests.md
```

Clean, scalable, auditable.

## 📄 Real Chunk Format

### Example 1: General Guide (Meta)

```yaml
---
chunk_id: guide::rag::chunking::single-intent::001
domain: rag
chunk_type: guideline
confidence: verified
reuse_level: universal
tags:
  - chunking
  - rag
  - memory
---

A chunk must answer exactly one question.
If it answers multiple questions, divide it.
Smaller chunks improve recall and reduce noise.
```

### Example 2: Reusable Technique

```yaml
---
chunk_id: technique::web::git-exposure::overview::001
domain: web
chunk_type: vulnerability
confidence: high
reuse_level: scenario-specific
tags:
  - git
  - source-code
  - exposure
---

An accessible .git folder allows extraction of complete source code.
This exposes authentication logic, business rules, and secrets.
Common discovery methods: direct browsing, directory traversal, misconfiguration.
```

### Example 3: Machine-Specific Finding

```yaml
---
chunk_id: htb::gavel::web::enum::git-exposure::001
domain: web
chunk_type: finding
confidence: verified
reuse_level: machine-specific
tags:
  - htb
  - gavel
  - git
---

The directory http://gavel.htb/.git/ was publicly accessible.
git-dumper was used to extract the complete repository.
Repository contained hardcoded API keys in config.php.
```

## 🆔 Chunk ID Schema (Fixed Format)

**MANDATORY FORMAT:**

```
<origin>::<domain>::<subdomain>::<intent>::<nnn>
```

### Valid Origins

```
concept      - Defines what something is
technique    - How to do something
exploit      - Weaponized technique
procedure    - Step-by-step process
finding      - Vulnerability discovered
reference    - Commands, syntax, cheatsheet
guideline    - Best practices
tutorial     - Teaching content
htb          - HTB machine-specific
```

### Valid Domains

```
web          - Web application security
linux        - Linux operating system
windows      - Windows operating system
python       - Python programming
javascript   - JavaScript programming
infrastructure - DevOps, cloud, networking
cryptography - Cryptographic concepts
network      - Network security
rag          - RAG systems (meta)
```

### Examples of Valid IDs

```
concept::python::syntax::variables::001
technique::linux::privilege-escalation::suid-enumeration::001
htb::gavel::web::enumeration::git-exposure::001
exploit::web::sql-injection::union-based::001
guideline::rag::chunking::single-intent::001
reference::linux::commands::privilege-escalation::001
tutorial::youtube::python::virtualenv-setup::001
```

❌ **NEVER:**
- Put dates in IDs
- Put languages
- Put states (draft/final)
- Put IPs
- Use spaces

## 📋 Metadata Fields (6 Mandatory)

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `chunk_id` | string | Unique identifier | `technique::web::lfi::file-download::001` |
| `domain` | string | Primary domain | `web`, `linux`, `rag` |
| `chunk_type` | string | Type of content | `concept`, `technique`, `exploit` |
| `confidence` | string | Verification level | `verified`, `high`, `medium` |
| `reuse_level` | string | Reusability scope | `universal`, `scenario-specific`, `machine-specific` |
| `tags` | array | Search keywords | `[chunking, rag, memory]` |

**Optional but recommended:**
```yaml
source: "PDF, YouTube, documentation"
creator: "Author name"
updated: "2026-02-12"
language: "en"
```

## ✅ One Manifest Per Namespace

### Example: chunking-guides/manifest.json

```json
{
  "namespace": "chunking-guides",
  "index": "openskills-rag",
  "description": "Guides and principles for chunking and RAG design",
  "last_updated": "2026-02-09",
  "chunks": [
    {
      "chunk_id": "guide::rag::chunking::single-intent::001",
      "file": "principles/single_intent.md",
      "hash": "sha256:abc123",
      "indexed": true
    },
    {
      "chunk_id": "guide::rag::chunking::chunk-size::001",
      "file": "principles/chunk_size.md",
      "hash": "sha256:def456",
      "indexed": true
    }
  ]
}
```

## 🚀 Multi-Level Example: LFI (Reusable + Specific)

Same topic, three levels of memory:

**Level 1: Universal Concept**
```yaml
chunk_id: concept::web::lfi::definition::001
chunk_type: definition
reuse_level: universal
```
"Local File Inclusion is a vulnerability allowing reading arbitrary files from the server filesystem via unsanitized user input in file inclusion functions."

**Level 2: Generic Technique**
```yaml
chunk_id: technique::web::lfi::file-download::001
chunk_type: technique
reuse_level: scenario-specific
```
"Files are downloaded using path traversal: ../../../etc/passwd. Null byte injection (%00) bypasses extensions. Wrappers like php:// enable code execution."

**Level 3: Machine-Specific**
```yaml
chunk_id: htb::facts::web::exploit::lfi-download::001
chunk_type: exploit
reuse_level: machine-specific
```
"Facts machine has LFI in /profile.php. Path traversal works with encoding: ..%2f..%2f..%2fetc%2fpasswd. Downloaded /etc/passwd to enumerate users."

**This is intelligent RAG.** Same concept, multiple retrieval levels.

## ❌ Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| One chunk per file | Lacks granularity | One chunk per idea |
| Generic ID like chunk_001 | No semantic meaning | Use the schema |
| Mixing languages in IDs | Causes confusion | Language in metadata |
| No manifest | Can't track state | Create per-namespace |
| Chunks that are too big | Noise in retrieval | Keep to 300-500 words |
| No namespace separation | Semantic pollution | Isolate by domain |

## 🎯 Final Checklist

Before creating a chunk, verify:

- [ ] Does it answer **exactly one question**?
- [ ] Does it make sense **by itself**?
- [ ] Is the **chunk_id semantic** and follows the schema?
- [ ] Is the **namespace correct**?
- [ ] Are all 6 **metadata fields present**?
- [ ] Is the content **300-500 words**?
- [ ] Is the **reuse_level accurate**?

If yes to all → You're ready.

## 🧠 Golden Phrase (Memorize This)

> **Writeups tell stories.  
> Chunks build memory.  
> The manifest maintains order.**

---

**Next:** Learn [Chunk ID Examples and Schema](chunk-id-examples.md)
