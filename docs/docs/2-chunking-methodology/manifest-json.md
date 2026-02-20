# Manifest JSON Guide

The manifest is NOT content. It's metadata ABOUT your metadata - the index of what you have.

## What is a Manifest?

Think of it like a **library catalog**, not the books themselves.

| Item | Analogy |
|------|---------|
| Books (Content) | Your chunks (markdown files) |
| Catalog (Metadata) | The manifest.json |
| Catalog Entry | Information about one book |

Without a catalog, a library is just a room of books.

## Why Manifests Matter

In a RAG system:

✅ **Tells agentswhat chunks exist**  
✅ **Tracks ingestion state** (indexed or pending)  
✅ **Enables change detection** (via hash)  
✅ **Prevents duplicate indexing**  
✅ **Synchronizes filesystem with vector DB**  

Without manifest:
- You'd re-read all files constantly (slow)
- You'd miss version updates
- You'd duplicate chunks in Pinecone
- You'd lose track of what's indexed

## Manifest Structure

```json
{
  "namespace": "string",
  "index": "string",
  "description": "string",
  "last_updated": "ISO 8601 date",
  "chunks": [
    {
      "chunk_id": "string",
      "file": "relative/path/to/chunk.md",
      "hash": "sha256:...",
      "indexed": boolean,
      "vector_id": "optional pinecone vector id"
    }
  ]
}
```

## Real Example: chunking-guides/manifest.json

```json
{
  "namespace": "chunking-guides",
  "index": "openskills-rag",
  "description": "Guides and principles for chunking and RAG design",
  "version": "1.0",
  "last_updated": "2026-02-12T10:30:00Z",
  "chunk_count": 12,
  "indexed_count": 12,
  "chunks": [
    {
      "chunk_id": "guide::rag::chunking::single-intent::001",
      "file": "principles/single_intent.md",
      "hash": "sha256:abc123def456789",
      "indexed": true,
      "vector_id": "vec-001-abc123",
      "size_bytes": 1254,
      "embedding_model": "text-embedding-3-large"
    },
    {
      "chunk_id": "guide::rag::chunking::chunk-size::001",
      "file": "principles/chunk_size.md",
      "hash": "sha256:def456ghi789jkl",
      "indexed": true,
      "vector_id": "vec-002-def456",
      "size_bytes": 1842,
      "embedding_model": "text-embedding-3-large"
    },
    {
      "chunk_id": "guide::rag::chunking::namespace-design::001",
      "file": "principles/namespace_design.md",
      "hash": "sha256:ghi789jkl012mno",
      "indexed": false,
      "vector_id": null,
      "size_bytes": 2156,
      "embedding_model": null
    }
  ]
}
```

## Real Example: htb-machines/manifest.json

```json
{
  "namespace": "htb-machines",
  "index": "openskills-rag",
  "description": "HTB machine-specific vulnerability findings and exploitation techniques",
  "version": "1.0",
  "last_updated": "2026-02-11T14:22:00Z",
  "chunk_count": 48,
  "indexed_count": 42,
  "machines": {
    "gavel": {
      "status": "completed",
      "difficulty": "medium",
      "chunks": 12
    },
    "facts": {
      "status": "in-progress",
      "difficulty": "hard",
      "chunks": 8
    }
  },
  "chunks": [
    {
      "chunk_id": "htb::gavel::web::enum::nmap-scan::001",
      "file": "gavel/enumeration/nmap_scan.md",
      "hash": "sha256:111aaa222bbb",
      "indexed": true,
      "machine": "gavel",
      "phase": "enumeration"
    },
    {
      "chunk_id": "htb::gavel::web::enum::git-exposure::001",
      "file": "gavel/enumeration/git_exposure.md",
      "hash": "sha256:222bbb333ccc",
      "indexed": true,
      "machine": "gavel",
      "phase": "enumeration"
    },
    {
      "chunk_id": "htb::gavel::web::exploit::runkit-rce::001",
      "file": "gavel/exploitation/runkit_rce.md",
      "hash": "sha256:333ccc444ddd",
      "indexed": true,
      "machine": "gavel",
      "phase": "exploitation"
    },
    {
      "chunk_id": "htb::facts::web::exploit::lfi-chain::001",
      "file": "facts/exploitation/lfi_chain.md",
      "hash": "sha256:444ddd555eee",
      "indexed": false,
      "machine": "facts",
      "phase": "exploitation"
    }
  ]
}
```

## Field Explanations

### namespace (Required)
```json
"namespace": "chunking-guides"
```
The semantic domain this manifest covers. Must match directory name.

### index (Required)
```json
"index": "openskills-rag"
```
The Pinecone index name where chunks are vectorized. Used for synchronization.

### description (Required)
```json
"description": "Guides and principles for chunking and RAG design"
```
Human-readable description of what's in this namespace.

### version (Recommended)
```json
"version": "1.0"
```
Version of the manifest schema itself (not content).

### last_updated (Recommended)
```json
"last_updated": "2026-02-12T10:30:00Z"
```
ISO 8601 timestamp. Used to detect staleness.

### chunk_count (Recommended)
```json
"chunk_count": 12
```
Total number of chunks in this namespace.

### indexed_count (Recommended)
```json
"indexed_count": 12
```
How many chunks are currently vectorized in Pinecone.

### chunks (Required)
```json
"chunks": [...]
```
Array of chunk metadata objects.

### Per-Chunk Fields

#### chunk_id (Required)
```json
"chunk_id": "guide::rag::chunking::single-intent::001"
```
Matches the ID in the chunk's YAML front matter.

#### file (Required)
```json
"file": "principles/single_intent.md"
```
Relative path from namespace root. Used to retrieve content.

#### hash (Required)
```json
"hash": "sha256:abc123def456789"
```
SHA256 of file contents. Used to detect changes:
- If hash matches → file unchanged, skip re-embedding
- If hash differs → file changed, needs re-embedding

#### indexed (Required)
```json
"indexed": true
```
Boolean indicating if chunk is in Pinecone:
- `true` → Already vectorized
- `false` → Pending vectorization

#### vector_id (Optional)
```json
"vector_id": "vec-001-abc123"
```
Pinecone's internal vector ID. Optional, helps with deletion/updates.

#### size_bytes (Optional)
```json
"size_bytes": 1254
```
File size. Used for monitoring and quotas.

#### embedding_model (Optional)
```json
"embedding_model": "text-embedding-3-large"
```
Which embedding model was used. Important if you change models.

## Manifest Operations

### Creating a Manifest

```json
{
  "namespace": "my-namespace",
  "index": "rag-canonical-v1-emb3large",
  "description": "My custom knowledge base",
  "version": "1.0",
  "last_updated": "2026-02-12T00:00:00Z",
  "chunk_count": 0,
  "indexed_count": 0,
  "chunks": []
}
```

Start empty, then add chunks as you create them.

### Adding a Chunk

When you create `principles/single_intent.md`:

```json
{
  "chunk_id": "guide::rag::chunking::single-intent::001",
  "file": "principles/single_intent.md",
  "hash": "sha256:compute_sha256_of_file",
  "indexed": false,
  "vector_id": null,
  "size_bytes": 1254,
  "embedding_model": null
}
```

Add to `chunks` array.

### Updating After Vectorization

Once you embed in Pinecone:

```json
{
  "chunk_id": "guide::rag::chunking::single-intent::001",
  "file": "principles/single_intent.md",
  "hash": "sha256:compute_sha256_of_file",
  "indexed": true,
  "vector_id": "vec-001-abc123",
  "size_bytes": 1254,
  "embedding_model": "text-embedding-3-large"
}
```

Change `indexed: true` and populate `vector_id`.

### Detecting Changes

When you edit a chunk:

1. New hash: `sha256:xyz789` (different from manifest's `sha256:abc123`)
2. Agent detects mismatch
3. Sets `indexed: false`
4. Re-embeds the chunk
5. Updates hash and vector_id

## One Manifest Per Namespace

❌ **Don't do this:**
```
/root/.openskills/rag/
└── manifest.json (global)
```

✅ **Do this instead:**
```
/root/.openskills/rag/
├── chunking-guides/
│   └── manifest.json
├── htb-machines/
│   └── manifest.json
├── web-security/
│   └── manifest.json
```

Reasons:
- Each namespace can scale independently
- Easier to manage permissions
- Clearer responsibility boundaries
- Better for distributed teams

## Manifest Validation Checklist

- [ ] `namespace` matches directory name
- [ ] `index` is correct Pinecone index
- [ ] `description` is clear
- [ ] All chunks have `chunk_id` and `file`
- [ ] All `file` paths are relative
- [ ] `hash` values are SHA256
- [ ] `indexed` status is accurate
- [ ] `chunk_count` matches array length
- [ ] `indexed_count` is accurate count
- [ ] `last_updated` is recent

## Integration with Pinecone

The manifest is the **bridge** between:
- **Filesystem** (source of truth)
- **Vector Database** (indexed data)

```
Filesystem Changes → Manifest Change Detection → Pinecone Update
```

When an agent runs:
1. Reads manifest for last sync state
2. Checks for hash mismatches
3. Adds new chunks (indexed: false)
4. Removes deleted chunks
5. Updates Pinecone with changes
6. Updates manifest with new hashes and vector IDs

---

**Next:** Move to [Part 3: Pinecone Complete Guide](../3-pinecone-guide/quick-start.md)
