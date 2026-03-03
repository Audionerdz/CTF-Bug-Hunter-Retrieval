# Chunk Fields Explained

Every chunk has metadata in its YAML frontmatter. These fields make your chunks searchable, filterable, and maintainable.

## The 6 Mandatory Fields

### 1. chunk_id (String)

Unique semantic identifier for the chunk.

**Format:** `<origin>::<domain>::<subdomain>::<intent>::<nnn>`

```yaml
chunk_id: technique::web::sql-injection::union-based::001
```

Rules:

- Must be globally unique
- Must follow the schema exactly
- Used for version control and updates
- Enables prefix-based search filtering

### 2. domain (String)

Primary knowledge domain.

```yaml
domain: web          # Web application security
domain: linux        # Operating system concepts
domain: python       # Programming language
domain: rag          # Meta-knowledge about RAG itself
domanin: langchain   # LangChain notes.
```

Valid values: `web`, `linux`, `windows`, `langchain`, `python`, `javascript`, `infrastructure`, `cryptography`, `network`, `rag`

### 3. chunk_type (String)

Categorizes the knowledge type.

| Type | Meaning | Example |
|------|---------|---------|
| `concept` | Defines what something is | "What is SQL injection?" |
| `technique` | How to do something | "How to perform UNION-based SQLi" |
| `exploit` | Weaponized attack | "Exploit code for RCE" |
| `procedure` | Step-by-step process | "Steps to root a system" |
| `finding` | Discovered vulnerability | "Gavel has .git exposure" |
| `reference` | Cheatsheet, syntax, commands | "Linux privesc cheatsheet" |
| `guideline` | Best practices | "How to design good chunks" |
| `tutorial` | Teaching content | "YouTube tutorial on Python async" |
| `vulnerability` | Security weakness description | ".git folder risks" |

### 4. confidence (String)

How verified the information is.

| Value | Meaning |
|-------|---------|
| `verified` | Tested and confirmed correct |
| `high` | Very reliable, authoritative source |
| `medium` | Reliable but not independently verified |
| `low` | Possibly correct, needs verification |
| `unverified` | Needs testing before use |

```yaml
confidence: verified      # Linux command tested on 5 distros
confidence: high          # From CVE database
confidence: medium        # From a tutorial, not independently tested
```

### 5. reuse_level (String)

How broadly the chunk can be applied.

| Value | Scope | Example |
|-------|-------|---------|
| `universal` | Anywhere, no context needed | "What is SQL injection?" |
| `scenario-specific` | Similar scenarios | "UNION-based SQL injection technique" |
| `machine-specific` | One specific target | "Gavel HTB .git exposure" |
| `context-dependent` | Requires prior knowledge | "Advanced LFI chains with wrapper abuse" |

### 6. tags (Array)

Searchable keywords. Use 3-5 tags per chunk.

```yaml
# Good tags (specific)
tags:
  - sql-injection
  - union-based
  - database-enumeration
  - web-application

# Bad tags (too vague)
tags:
  - stuff
  - important
  - web
```

Rules:

- Use lowercase with hyphens
- Make tags specific to content
- Include both broad and specific terms

## Optional But Recommended

```yaml
source: "OWASP Testing Guide"        # Where info came from
creator: "SecurityTutor (YouTube)"    # Who created/verified it
updated: "2026-02-12"                 # Last verified date
language: "en"                        # Content language
related_chunks:                       # Links to related chunks
  - concept::web::sql-injection::definition::001
  - technique::web::sql-injection::time-based::001
```

## Complete Example

```yaml
---
chunk_id: technique::web::lfi::null-byte-bypass::001
domain: web
chunk_type: technique
confidence: high
reuse_level: scenario-specific
tags:
  - lfi
  - null-byte
  - bypass
  - web-exploitation
source: "HackTricks LFI Guide"
creator: "Security Researcher"
updated: "2026-02-10"
language: "en"
related_chunks:
  - concept::web::lfi::definition::001
  - technique::web::lfi::path-traversal::001
---

# Null Byte Bypass for LFI

In PHP versions < 5.3.4, null bytes (%00) can terminate string processing.
If a script appends .php to user input, you can bypass it:

Request: /profile.php?file=../../../../etc/passwd%00
Server processes: ../../../../etc/passwd\0.php
Null byte terminates string, loads passwd file instead.

Modern PHP (5.3.4+) removed this vulnerability.
On legacy systems, this is critical.
```

## Validation Checklist

Before publishing a chunk:

- [ ] `chunk_id` follows schema exactly
- [ ] `domain` is from the valid list
- [ ] `chunk_type` matches content type
- [ ] `confidence` reflects actual verification
- [ ] `reuse_level` is accurate
- [ ] `tags` are specific and relevant (3-5 tags)
- [ ] Optional fields filled when applicable
- [ ] No sensitive information in metadata
