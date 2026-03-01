# Chunk Templates - RAG Graph Naming Convention

## Naming Pattern

```
{domain}/{chunk_type}/{category}/{subcategory}/{name}_{sequence}.md
```

### Components

- **domain**: `rag`, `langchain`, `python`, `web`, `linux`, `windows`, `networking`, `crypto`, `reverse`
- **chunk_type**: `technique`, `exploit`, `procedure`, `guideline`, `reference`, `concept`
- **category**: Descriptive grouping
- **subcategory**: Specific area
- **name**: Descriptive identifier (kebab-case)
- **sequence**: `001`, `002`, etc.

---

## Template 1: RAG Domain

### RAG Query Technique

**File**: `rag/technique/query/basic-syntax/query-with-keywords_001.md`

```yaml
---
chunk_id: technique::rag::query::basic-syntax::query-with-keywords::001
domain: rag
chunk_type: technique
confidence: high
reuse_level: universal
source: documentation
creator: RAG-Team
tags:
  - query-syntax
  - keywords
  - searching
---

# Query with Keywords - Basic Syntax

## Overview
Explains how to search chunks using keyword-based queries.

## Basic Syntax
```
query: "keyword1 keyword2"
```

## Examples
- Query: "LFI exploitation"
- Query: "Python virtual environment"

## Best Practices
- Use multiple keywords for better precision
- Combine related terms
- Review documentation before querying
```

### RAG Vectorization Procedure

**File**: `rag/procedure/vectorization/chunking/chunk-and-vectorize_001.md`

```yaml
---
chunk_id: procedure::rag::vectorization::chunking::chunk-and-vectorize::001
domain: rag
chunk_type: procedure
confidence: high
reuse_level: universal
source: documentation
creator: RAG-Team
tags:
  - vectorization
  - chunking
  - pinecone
---

# Chunk and Vectorize Documents

## Step 1: Prepare Documents
- Organize PDFs or markdown files
- Ensure YAML frontmatter is correct
- Validate metadata

## Step 2: Run Chunker
```bash
python src/vectorize.py --input docs/ --domain web
```

## Step 3: Verify Vectors
```bash
python src/check_vectors.py
```

## Step 4: Query
```bash
python src/query.py "search term"
```
```

---

## Template 2: LangChain Domain

### LangChain Concept

**File**: `langchain/concept/chains/retrieval-chain/rag-chain_001.md`

```yaml
---
chunk_id: concept::langchain::chains::retrieval-chain::rag-chain::001
domain: langchain
chunk_type: concept
confidence: high
reuse_level: universal
source: documentation
creator: RAG-Team
tags:
  - chains
  - retrieval
  - langchain
---

# RAG Chain in LangChain

## Definition
A retrieval-augmented generation chain that retrieves relevant context before generating responses.

## Components
1. **Retriever**: Fetches relevant documents
2. **Prompt**: Provides context and instructions
3. **LLM**: Generates response
4. **Output Parser**: Formats result

## Architecture
```
User Query → Retriever → LLM → Response
```

## Code Example
```python
from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
```
```

### LangChain Technique

**File**: `langchain/technique/chains/custom-chain/building-custom-chain_001.md`

```yaml
---
chunk_id: technique::langchain::chains::custom-chain::building-custom-chain::001
domain: langchain
chunk_type: technique
confidence: high
reuse_level: universal
source: documentation
creator: RAG-Team
tags:
  - custom-chains
  - langchain
  - advanced
---

# Building Custom Chains

## Overview
How to create custom LangChain chains for specific use cases.

## Basic Structure
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = "Answer: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)
```

## Advanced Patterns
- Sequential chains (SequentialChain)
- Conditional routing (RouterChain)
- Multi-step processing (MapReduceChain)
```

---

## Template 3: Web Security Domain

### Web Technique

**File**: `web/technique/lfi/path-traversal/filter-bypass_001.md`

```yaml
---
chunk_id: technique::web::lfi::path-traversal::filter-bypass::001
domain: web
chunk_type: technique
confidence: high
reuse_level: universal
source: hackthebox
creator: Security-Researcher
tags:
  - lfi
  - path-traversal
  - filter-bypass
htb_machine: Machines with LFI
---

# Filter Bypass - Path Traversal

## Overview
Techniques to bypass file filters and access restricted files.

## Common Bypasses
- Double encoding: `%252e%252e/`
- Null byte: `file.php%00`
- Case variation: `FiLe.PhP`
- Alternative encodings: `..%2f`

## Example
```
GET /?file=....//....//etc/passwd
```

## Detection
- Monitor for encoded payloads
- Log path traversal attempts
```

### Web Exploit

**File**: `web/exploit/lfi/cve-2025-xxxx/exploitation-script_001.md`

```yaml
---
chunk_id: exploit::web::lfi::cve-2025-xxxx::exploitation-script::001
domain: web
chunk_type: exploit
confidence: high
reuse_level: universal
source: github-poc
creator: Security-Researcher
cve_ids:
  - CVE-2025-XXXX
tags:
  - lfi
  - automation
  - python-script
htb_machine: TargetMachine
---

# LFI Exploitation Script

## Code
```python
import requests

url = "http://target.com/?file="
files = ["/etc/passwd", "/etc/shadow", "/var/www/config.php"]

for file in files:
    payload = f"....//....//....{file}"
    response = requests.get(url + payload)
    print(f"{file}: {response.status_code}")
```

## Usage
```bash
python exploit.py
```

## Mitigation
- Input validation
- Whitelist allowed files
- Use safe APIs
```

### Web Procedure

**File**: `web/procedure/enumeration/manual-testing/burp-proxy-setup_001.md`

```yaml
---
chunk_id: procedure::web::enumeration::manual-testing::burp-proxy-setup::001
domain: web
chunk_type: procedure
confidence: high
reuse_level: universal
source: documentation
creator: Security-Researcher
tags:
  - enumeration
  - burp-suite
  - manual-testing
---

# Setting Up Burp Proxy

## Step 1: Start Burp Suite
```bash
burpsuite &
```

## Step 2: Configure Browser
- Set proxy to localhost:8080
- Accept Burp certificate

## Step 3: Capture Traffic
- Enable Intercept
- Browse target application
- Analyze requests/responses

## Step 4: Scan
- Send to Scanner
- Configure scan settings
- Review results
```

### Web Guideline

**File**: `web/guideline/injection/sql-injection/prevention-best-practices_001.md`

```yaml
---
chunk_id: guideline::web::injection::sql-injection::prevention-best-practices::001
domain: web
chunk_type: guideline
confidence: high
reuse_level: universal
source: owasp
creator: Security-Team
tags:
  - prevention
  - sql-injection
  - best-practices
---

# SQL Injection Prevention

## Best Practices

### 1. Parameterized Queries
```python
# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Bad
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### 2. Input Validation
- Whitelist allowed characters
- Validate data types
- Limit string length

### 3. Least Privilege
- Use minimal database permissions
- Separate read/write accounts
- Restrict admin access

### 4. Error Handling
- Don't expose database errors
- Log security events
- Alert on suspicious patterns
```

---

## Template 4: Python Domain

### Python Concept

**File**: `python/concept/virtual-environments/venv/python-isolation_001.md`

```yaml
---
chunk_id: concept::python::virtual-environments::venv::python-isolation::001
domain: python
chunk_type: concept
confidence: high
reuse_level: universal
source: documentation
creator: Python-Team
tags:
  - virtual-environments
  - isolation
  - best-practices
---

# Python Virtual Environments

## What is venv?
Virtual environments create isolated Python installations.

## Benefits
- Project dependency isolation
- Version control for packages
- Clean development setup
- Avoid system conflicts

## Structure
```
project/
├── venv/               # Isolated Python
│   ├── bin/            # Python executable
│   ├── lib/            # Packages
│   └── pyvenv.cfg      # Config
└── requirements.txt    # Dependencies
```
```

### Python Technique

**File**: `python/technique/debugging/error-handling/exception-handling_001.md`

```yaml
---
chunk_id: technique::python::debugging::error-handling::exception-handling::001
domain: python
chunk_type: technique
confidence: high
reuse_level: universal
source: documentation
creator: Python-Team
tags:
  - error-handling
  - exceptions
  - debugging
---

# Python Exception Handling

## Basic Syntax
```python
try:
    risky_code()
except SpecificError as e:
    handle_error(e)
finally:
    cleanup()
```

## Custom Exceptions
```python
class CustomError(Exception):
    pass

raise CustomError("Error message")
```

## Best Practices
- Catch specific exceptions
- Log all errors
- Provide meaningful messages
- Clean up resources
```

---

## Template 5: Linux Domain

### Linux Technique

**File**: `linux/technique/privilege-escalation/sudo/sudo-misconfiguration_001.md`

```yaml
---
chunk_id: technique::linux::privilege-escalation::sudo::sudo-misconfiguration::001
domain: linux
chunk_type: technique
confidence: high
reuse_level: universal
source: hackthebox
creator: Linux-Security
tags:
  - privilege-escalation
  - sudo
  - misconfiguration
---

# Sudo Misconfiguration Exploitation

## NOPASSWD Sudo
```bash
# Check sudoers
sudo -l

# If NOPASSWD:
sudo /bin/bash
```

## Wildcards in Sudoers
```bash
# If: /usr/bin/python* NOPASSWD
sudo /usr/bin/python3.9 -c "import os; os.system('/bin/bash')"
```

## LD_PRELOAD
```bash
# If: env_keep += LD_PRELOAD
# Create malicious library
gcc -shared -fPIC preload.c -o preload.so
sudo LD_PRELOAD=/tmp/preload.so /restricted/binary
```
```

---

## Naming Consistency Rules

### Do's ✅
- Use kebab-case for file names
- Use consistent domain names
- Include sequence numbers
- Use descriptive names
- Keep related chunks in same category

### Don'ts ❌
- Mix case styles (don't: MyFile_001)
- Use spaces in names
- Skip sequence numbers
- Use generic names (don't: "info_001")
- Scatter related chunks

---

## File Organization Example

```
default/
├── rag/
│   ├── technique/
│   │   └── query/basic-syntax/query-with-keywords_001.md
│   ├── procedure/
│   │   └── vectorization/chunking/chunk-and-vectorize_001.md
│   └── guideline/
│       └── best-practices/query-optimization_001.md
│
├── langchain/
│   ├── concept/
│   │   └── chains/retrieval-chain/rag-chain_001.md
│   ├── technique/
│   │   └── chains/custom-chain/building-custom-chain_001.md
│   └── reference/
│       └── api/langchain-core_001.md
│
├── web/
│   ├── technique/
│   │   └── lfi/path-traversal/filter-bypass_001.md
│   ├── exploit/
│   │   └── lfi/cve-2025-xxxx/exploitation-script_001.md
│   ├── procedure/
│   │   └── enumeration/manual-testing/burp-proxy-setup_001.md
│   └── guideline/
│       └── injection/sql-injection/prevention-best-practices_001.md
│
├── python/
│   ├── concept/
│   │   └── virtual-environments/venv/python-isolation_001.md
│   └── technique/
│       └── debugging/error-handling/exception-handling_001.md
│
└── linux/
    └── technique/
        └── privilege-escalation/sudo/sudo-misconfiguration_001.md
```

---

## Chunk ID Format Reference

```
{chunk_type}::{domain}::{category}::{subcategory}::{name}::{sequence}
```

### Examples
```
technique::rag::query::basic-syntax::query-with-keywords::001
concept::langchain::chains::retrieval-chain::rag-chain::001
exploit::web::lfi::cve-2025-xxxx::exploitation-script::001
procedure::web::enumeration::manual-testing::burp-proxy-setup::001
guideline::web::injection::sql-injection::prevention-best-practices::001
technique::python::debugging::error-handling::exception-handling::001
technique::linux::privilege-escalation::sudo::sudo-misconfiguration::001
```

---

## How RAG-Graph Tracking Works

1. **Chunk Created** → Gets `chunk_id` with consistent naming
2. **Metadata Extracted** → YAML frontmatter parsed
3. **Node Created** → Added to graph with full metadata
4. **Domain Mapped** → Connected to knowledge domain node
5. **Relationships** → Semantic edges created automatically

Your consistent naming ensures:
- Easy tracking in graphs
- Automatic categorization
- Relationship discovery
- Version control clarity
