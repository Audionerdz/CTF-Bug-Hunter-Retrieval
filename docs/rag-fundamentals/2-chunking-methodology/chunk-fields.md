# Chunk Fields Explained

Understanding metadata fields is critical for building searchable, maintainable RAG systems.

## The 6 Mandatory Fields

Every chunk MUST have these fields in its YAML front matter:

### 1. chunk_id (String)

**Purpose:** Unique semantic identifier  
**Format:** `<origin>::<domain>::<subdomain>::<intent>::<nnn>`  
**Example:** `technique::web::sql-injection::union-based::001`

**Rules:**
- Must be globally unique
- Must follow the schema exactly
- Used for version control and updates
- Enables prefix-based search filtering

### 2. domain (String)

**Purpose:** Primary knowledge domain  
**Valid Values:** `web`, `linux`, `windows`, `python`, `javascript`, `infrastructure`, `cryptography`, `network`, `rag`

**Why it matters:**
- Enables domain-specific filtering
- Helps with namespace organization
- Allows cross-domain searches

**Examples:**
```yaml
domain: web          # Web application security
domain: linux        # Operating system concepts
domain: python       # Programming language
domain: rag          # Meta-knowledge about RAG itself
```

### 3. chunk_type (String)

**Purpose:** Categorizes the knowledge type  
**Valid Values:**

| Type | Meaning | Example |
|------|---------|---------|
| `concept` | Defines what something is | "What is SQL injection?" |
| `technique` | How to do something | "How to perform UNION-based SQLi" |
| `exploit` | Weaponized attack | "Exploit code for RCE" |
| `procedure` | Step-by-step process | "Steps to root a system" |
| `finding` | Discovered vulnerability | "Gavel has .git exposure" |
| `reference` | Cheatsheet, syntax, commands | "Linux privilege escalation cheatsheet" |
| `guideline` | Best practices, advice | "How to design good chunks" |
| `tutorial` | Teaching content | "YouTube tutorial on Python async" |
| `vulnerability` | Security weakness description | ".git folder risks" |

**When to use what:**
- Use **concept** for definitions and theory
- Use **technique** for methodologies
- Use **exploit** for weaponized versions
- Use **guideline** for meta/process advice
- Use **finding** for specific discoveries

### 4. confidence (String)

**Purpose:** Indicates verification level  
**Valid Values:** `verified`, `high`, `medium`, `low`, `unverified`

**What it means:**
- `verified` - Tested and confirmed correct
- `high` - Very reliable based on authoritative sources
- `medium` - Reliable but not independently verified
- `low` - Possibly correct but needs verification
- `unverified` - Needs testing before use

**Real examples:**
```yaml
confidence: verified      # Linux command tested on 5 distros
confidence: high          # Information from CVE database
confidence: medium        # From tutorial without independent test
confidence: low           # Theory that might need adjustment
```

### 5. reuse_level (String)

**Purpose:** Indicates scope of reusability  
**Valid Values:** `universal`, `scenario-specific`, `machine-specific`, `context-dependent`

**What each means:**

#### universal
- Applicable anywhere
- No context needed
- Examples: "What is SQL injection?", "Python list syntax"
- Used in: Any project, any domain, any machine

#### scenario-specific
- Applicable to similar scenarios
- Medium context needed
- Examples: "UNION-based SQL injection technique", "SUID enumeration"
- Used in: Multiple similar targets or problems

#### machine-specific
- Only for specific target
- High context needed
- Examples: "Gavel HTB machine .git exposure", "Facts machine sudo misconfiguration"
- Used in: Single machine or very specific scenario

#### context-dependent
- Applicable only with specific knowledge
- Requires prior understanding
- Examples: "Advanced LFI chains with wrapper abuse"
- Used in: Follow-up knowledge after prerequisites

**Choosing correctly:**
```yaml
chunk_id: concept::web::sql-injection::definition::001
reuse_level: universal  # Can use anywhere

chunk_id: technique::web::sql-injection::union-based::001
reuse_level: scenario-specific  # Many web apps, not all

chunk_id: htb::gavel::web::enum::git-exposure::001
reuse_level: machine-specific  # Only for Gavel machine
```

### 6. tags (Array)

**Purpose:** Searchable keywords  
**Format:** YAML array of strings  

**Examples:**
```yaml
tags:
  - sql-injection
  - database
  - web-security

tags:
  - linux
  - privilege-escalation
  - suid
  - security

tags:
  - python
  - async
  - concurrency
  - programming
```

**Rules:**
- Use lowercase with hyphens
- 3-5 tags per chunk (optimal)
- Make tags specific to content
- Include both broad and specific terms
- Enables keyword-based search before vector search

**Bad tags:**
```yaml
tags:
  - stuff
  - important
  - web
  - thing
```

**Good tags:**
```yaml
tags:
  - sql-injection
  - union-based
  - database-enumeration
  - web-application
```

## Optional But Recommended Fields

### source (String)

Where the information came from:
```yaml
source: "OWASP Testing Guide"
source: "CVE-2024-1234"
source: "YouTube tutorial"
source: "GitHub repository"
```

### creator (String)

Who created or verified the chunk:
```yaml
creator: "SecurityTutor (YouTube)"
creator: "ChatGPT + manual verification"
creator: "HTB official walkthrough"
```

### updated (Date)

When the chunk was last verified/updated:
```yaml
updated: "2026-02-12"
updated: "2026-01-15"
```

### language (String)

Language of the content:
```yaml
language: "en"
language: "es"
language: "fr"
```

### related_chunks (Array)

Links to related chunks:
```yaml
related_chunks:
  - concept::web::sql-injection::definition::001
  - technique::web::sql-injection::time-based::001
  - exploit::web::sql-injection::database-dump::001
```

## Complete Example with All Fields

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
Null byte terminates string, loads passwd file instead of .php file.

Modern PHP (5.3.4+) removed this vulnerability.
On legacy systems, this is critical.
```

## Field Validation Checklist

Before publishing a chunk:

- [ ] `chunk_id` follows schema exactly
- [ ] `domain` is from valid list
- [ ] `chunk_type` matches content type
- [ ] `confidence` reflects actual verification
- [ ] `reuse_level` is accurate
- [ ] `tags` are specific and relevant
- [ ] At least 3-5 tags present
- [ ] Optional fields filled when applicable
- [ ] No sensitive information in metadata

## Metadata Inheritance

When chunks are related, metadata can be inherited:

```yaml
Parent (Universal):
chunk_id: concept::web::sql-injection::definition::001
reuse_level: universal

Child (Specific):
chunk_id: technique::web::sql-injection::union-based::001
reuse_level: scenario-specific
related_chunks:
  - concept::web::sql-injection::definition::001

Grandchild (Machine-specific):
chunk_id: htb::facts::web::exploit::lfi-download::001
reuse_level: machine-specific
related_chunks:
  - concept::web::sql-injection::definition::001
  - technique::web::sql-injection::union-based::001
```

---

**Next:** Learn [Manifest JSON Guide](manifest-json.md)
