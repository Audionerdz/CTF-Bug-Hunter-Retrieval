# Core Principles of Chunking

This is the definitive guide to chunking. If you follow these rules, your Atlas will retrieve the right information every time.

## What is a Chunk?

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

**The Golden Rule:** One chunk answers ONE question.

## What is a Namespace?

A namespace is a **semantic domain** -- a collection of related chunks. Think of it as a folder in your vector database.

Examples:

```
ctf           -- CTF-specific content
cve           -- CVE/vulnerability data
technique     -- Security techniques
tools         -- Security tools
payloads      -- Exploit payloads
```

When you query a namespace, you only search chunks in that group. This reduces noise and improves accuracy.

## Chunk Format

Every chunk is a markdown file with YAML frontmatter:

### Example 1: A General Guideline

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

### Example 2: A Reusable Technique

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

## Chunk ID Schema

Every chunk ID follows this format:

```
<origin>::<domain>::<subdomain>::<intent>::<nnn>
```

### Valid Origins

| Origin | Meaning |
|--------|---------|
| `concept` | Defines what something is |
| `technique` | How to do something |
| `exploit` | Weaponized technique |
| `procedure` | Step-by-step process |
| `finding` | Vulnerability discovered |
| `reference` | Commands, syntax, cheatsheet |
| `guideline` | Best practices |
| `tutorial` | Teaching content |
| `htb` | HTB machine-specific |

### Valid Domains

| Domain | Scope |
|--------|-------|
| `web` | Web application security |
| `linux` | Linux operating system |
| `windows` | Windows operating system |
| `python` | Python programming |
| `javascript` | JavaScript programming |
| `network` | Network security |
| `rag` | Atlass (meta) |

### Examples

```
concept::python::syntax::variables::001
technique::linux::privilege-escalation::suid-enumeration::001
htb::gavel::web::enumeration::git-exposure::001
exploit::web::sql-injection::union-based::001
```

**Never put** dates, languages, states (draft/final), IPs, or spaces in chunk IDs.

## Multi-Level Knowledge

The same topic can exist at three levels:

**Level 1: Universal Concept**

```yaml
chunk_id: concept::web::lfi::definition::001
reuse_level: universal
```
> "Local File Inclusion is a vulnerability allowing reading arbitrary files from the server filesystem via unsanitized user input."

**Level 2: Generic Technique**

```yaml
chunk_id: technique::web::lfi::file-download::001
reuse_level: scenario-specific
```
> "Files are downloaded using path traversal: ../../../etc/passwd. Null byte injection (%00) bypasses extensions."

**Level 3: Machine-Specific**

```yaml
chunk_id: htb::facts::web::exploit::lfi-download::001
reuse_level: machine-specific
```
> "Facts machine has LFI in /profile.php. Path traversal works with encoding: ..%2f..%2f..%2fetc%2fpasswd."

This is intelligent RAG. Same concept, multiple retrieval levels.

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| One chunk per file | Lacks granularity | One chunk per idea |
| Generic ID like chunk_001 | No semantic meaning | Use the schema |
| Mixing languages in IDs | Causes confusion | Language in metadata |
| Chunks that are too big | Noise in retrieval | Keep to 300-500 words |
| No namespace separation | Semantic pollution | Isolate by domain |

## Checklist

Before creating a chunk, verify:

- [ ] Does it answer **exactly one question**?
- [ ] Does it make sense **by itself**?
- [ ] Is the **chunk_id semantic** and follows the schema?
- [ ] Are all **metadata fields present**?
- [ ] Is the content **300-500 words**?
- [ ] Is the **reuse_level accurate**?

> **Writeups tell stories. Chunks build memory.**
