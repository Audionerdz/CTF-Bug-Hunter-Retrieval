# Vectorizer - Plain Markdown Support (No Frontmatter)

## Overview

The Vectorizer now supports **both**:
1. Markdown **with frontmatter** (YAML metadata)
2. Markdown **without frontmatter** (plain text)

Previously, only markdown with frontmatter was accepted. Now you can vectorize plain `.md` files and set/edit their metadata directly in the Pinecone console.

## How It Works

### Markdown WITH Frontmatter (Original)
```markdown
---
chunk_id: technique::rce::php::001
domain: web
chunk_type: technique
technique: RCE
---

# PHP RCE via eval()

Description...
```

**Metadata source:** YAML frontmatter  
**Workflow:** Parse → Validate → Embed → Upsert → Register

---

### Markdown WITHOUT Frontmatter (New)
```markdown
# My Security Research

This is a markdown file with useful information about...
No YAML needed.
```

**Metadata source:** Auto-generated, then editable in Pinecone  
**Workflow:** 
1. Parse (auto-generates `chunk_id` from filename)
2. Validate (detects plain markdown, sets `requires_metadata_edit: true`)
3. Embed (uses auto-generated `chunk_id`)
4. Upsert (saves to Pinecone WITH placeholder metadata)
5. **Edit in Pinecone console** (optional: refine metadata via web UI)

---

## Usage

### Simple: Vectorize Plain Markdown
```python
from rag import RAG

r = RAG()

# Just vectorize - metadata will be auto-generated
result = r.vectorize("/path/to/plain_file.md")
# Output: chunk_id = "chunk::plain_file"
```

### Granular: Control Each Phase
```python
# 1. Discover
files = r.vectorizer.discover("/path/to/md_files/")

# 2. Parse (handles both WITH & WITHOUT frontmatter)
parsed = r.vectorizer.parse(files)

# 3. Validate (auto-generates chunk_id if missing)
validated = r.vectorizer.validate(parsed, strict=False)
# strict=False (default): Accept plain markdown, auto-generate metadata
# strict=True: Reject plain markdown, require chunk_id in frontmatter

# 4. Embed
embedded = r.vectorizer.embed(validated)

# 5. Upsert
upserted = r.vectorizer.upsert(embedded)

# 6. Register
r.vectorizer.register(files)
```

---

## Auto-Generated Metadata

When a plain markdown file is vectorized:

```json
{
  "chunk_id": "chunk::my_file",
  "source": "/path/to/my_file.md",
  "chunk_type": "plain-markdown",
  "requires_metadata_edit": true,
  "content": "... full text ...",
  "content_length": 1234
}
```

The `requires_metadata_edit: true` flag indicates this vector was auto-generated and could be refined manually.

---

## Editing Metadata in Pinecone

Once vectorized, you can edit metadata **directly in Pinecone console**:

1. Go to your Pinecone index web UI
2. Find the vector by `chunk_id` (e.g., `chunk::my_file`)
3. Edit metadata fields:
   - `domain`: cyber, web, linux, etc.
   - `chunk_type`: technique, cve, tutorial, etc.
   - `technique`: RCE, LFI, SQLi, etc.
   - `machine`: gavel, facts, etc.
   - Add custom fields as needed

4. Save changes - the updated metadata will be used in future queries

---

## Mixed Workflows

You can vectorize a **mix** of files:

```python
# Directory with both types
# ├── with_frontmatter.md    (---YAML---)
# ├── plain_file1.md         (plain text)
# └── plain_file2.md         (plain text)

r.vectorize("/path/to/mixed/")

# Output:
# Discovered: 3 file(s)
# Parsed: 3 chunk(s)
# Validated: 3 valid (2 plain markdown), 0 invalid
# 
# ⚠️  2 plain markdown file(s) detected!
# These will be vectorized WITH auto-generated metadata.
#
# Embedding 3 chunks...
#   [1/3] technique::rce::php::001 (unknown)
#   [2/3] chunk::plain_file1 (plain-markdown)
#   [3/3] chunk::plain_file2 (plain-markdown)
```

---

## Recommendations

### ✅ Use WITH Frontmatter When:
- You have structured metadata ready
- Building a consistent knowledge base
- Batch processing documents

### ✅ Use WITHOUT Frontmatter When:
- Quick prototyping
- Don't want to edit YAML
- Plan to refine metadata in Pinecone UI
- One-off documents

---

## Technical Details

### Phase 2: Parse
- **WITH frontmatter:** Split `---YAML---` + body
- **WITHOUT frontmatter:** Treat entire file as body, auto-generate minimal metadata

### Phase 3: Validate
- **strict=False (default):** Accept both types, auto-generate `chunk_id` if missing
- **strict=True:** Reject plain markdown, require explicit `chunk_id`

### Phase 4: Embed
- Works with both: metadata + body → embedding

### Phase 5: Upsert
- Saves all metadata to Pinecone, editable via web console

---

## Example: Create & Vectorize Plain Markdown

```bash
# Create a plain .md file (no frontmatter needed)
cat > /tmp/rce_techniques.md << 'EOF'
# RCE via Command Injection

Command injection occurs when user input is passed unsanitized to shell commands.

## PHP Example

```php
system($_GET['cmd']);  // VULNERABLE
```

## Prevention

- Use escapeshellarg()
- Use parameterized APIs
- Input validation
EOF

# Vectorize it
python3 << 'PYTHON'
import sys
sys.path.insert(0, '/home/kali/Desktop/RAG')
from rag import RAG

r = RAG()
result = r.vectorize("/tmp/rce_techniques.md")
print(f"\nVectorized: {result['upserted']} vector(s)")
print("Auto-generated chunk_id: chunk::rce_techniques")
print("Edit metadata in Pinecone console if needed")
PYTHON
```

---

## FAQ

**Q: Will plain markdown break my queries?**  
A: No. Plain markdown vectors work exactly like frontmatter vectors. Only metadata availability differs.

**Q: How do I add domain/technique tags to plain markdown?**  
A: Either:
1. Add YAML frontmatter before vectorizing
2. Vectorize as-is, then edit metadata in Pinecone console

**Q: Can I vectorize a directory mix of both?**  
A: Yes! The Vectorizer detects and handles both automatically.

**Q: Is the auto-generated metadata enough for queries?**  
A: The content embedding works perfectly. But for **filtering** by domain/technique/machine, you should refine the metadata.

---

## Summary

Plain markdown support makes the Vectorizer more flexible:
- **Lower friction:** No YAML required
- **Editability:** Refine metadata in Pinecone UI
- **Compatibility:** Works alongside frontmatter markdown
- **Control:** Choose your workflow per file
