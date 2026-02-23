# Pinecone CLI Essentials

The **Pinecone Assistant CLI** (`pa` command) is your gateway to manual Pinecone operations. This guide covers installation, configuration, and core commands.

## Installation & Configuration

### Check if Installed

```bash
which pa
pa --help
```

If installed, you'll see:
```
/usr/local/bin/pa
usage: pa [-h] [-a ASSISTANT] [-k TOP_K] [-m MACHINE] [-v] ...
```

### Environment Variables

The CLI requires Pinecone credentials. Verify these are set:

```bash
echo $PINECONE_API_KEY
echo $PINECONE_ENVIRONMENT
```

If empty, load from your env file:

```bash
source /root/.openskills/env/pinecone.env
echo $PINECONE_API_KEY  # Should show your key
```

### Test Connection

```bash
pa --help
```

If this works, Pinecone CLI is ready.

## Core Commands

### 1. List All Indices

```bash
pa list
```

**Output example:**
```
rag-canonical-v1-emb3large    3072d     114 vectors
my-test-index                  1536d      42 vectors
```

### 2. Describe an Index

Get detailed information about an index:

```bash
pa describe rag-canonical-v1-emb3large
```

**Output:**
```
Name:        rag-canonical-v1-emb3large
Status:      Ready
Dimension:   3072
Vectors:     114
Metric:      Cosine
Namespaces:  facts, gavel
```

### 3. Basic Query (Search)

Search for vectors similar to your query:

```bash
pa "LFI exploitation"
```

**This:**
1. Converts "LFI exploitation" to a 3072D embedding (using OpenAI)
2. Searches `rag-canonical-v1-emb3large` index
3. Returns top 5 most similar vectors

Add parameters:

```bash
# Return 10 results
pa "RCE techniques" -k 10

# Filter by machine (namespace)
pa "privesc" -m facts

# Verbose output (show full content)
pa "SQL injection" -v

# Custom assistant
pa -a "my-assistant" "query"
```

### 4. Delete a Vector

Remove a single vector by ID:

```bash
pa delete --id "chunk_facts_001"
```

### 5. Delete by File ID

If you uploaded a file, delete all vectors from it:

```bash
pa delete --file-id "file_12345"
```

### 6. Get Help

```bash
pa --help
pa -h
```

## Real-World Examples

### Example 1: Search FACTS Machine Chunks

```bash
pa "buffer overflow exploit" -m facts -k 5 -v
```

This searches only FACTS chunks and shows full content.

### Example 2: Search GAVEL Machine Chunks

```bash
pa "api endpoint parameter" -m gavel -k 10
```

### Example 3: Count Results

Search and count results:

```bash
pa "privilege escalation" -k 20 | wc -l
```

### Example 4: Export Results

```bash
pa "RCE" -k 10 -v > rce_results.txt
cat rce_results.txt
```

## Understanding the Index Structure

Your default index is `rag-canonical-v1-emb3large`:

- **Name**: `rag-canonical-v1-emb3large`
- **Dimension**: 3072 (OpenAI text-embedding-3-large)
- **Metric**: Cosine similarity
- **Total Vectors**: 114
- **Namespaces**: 
  - `facts` - 105 chunks from FACTS HTB machine
  - `gavel` - 9 chunks from GAVEL HTB machine

### Namespace-Based Organization

Vectors are organized by machine name. Query specific machines:

```bash
# All machines
pa "query"

# Only FACTS
pa "query" -m facts

# Only GAVEL
pa "query" -m gavel
```

## Troubleshooting CLI

### Command Not Found
```bash
# Install or locate it
which pa
# If not found, check installation
ls -la /usr/local/bin/pa
```

### API Key Issues
```bash
# Verify key is loaded
echo $PINECONE_API_KEY | head -c 10
# Should show first 10 chars of your API key
```

### Connection Timeout
```bash
# Test connectivity
ping api.pinecone.io

# Try with verbose output
pa --verbose "test query"
```

### Wrong Index
```bash
# List indices and verify the right one exists
pa list

# Explicitly target an index (if CLI supports it)
pa "query"  # Uses default index
```

---

**Next: Learn how to [embed chunks manually](embedding-chunks-manually.md) using the OpenAI API.**
