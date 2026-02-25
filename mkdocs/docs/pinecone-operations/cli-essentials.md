# Pinecone CLI Essentials

The **Pinecone Assistant CLI** (`pa` command) lets you interact with your Pinecone vector database directly from the terminal.

## Check if Installed

```bash
which pa
pa --help
```

If installed, you'll see:

```
/usr/local/bin/pa
usage: pa [-h] [-a ASSISTANT] [-k TOP_K] [-m MACHINE] [-v] ...
```

## Environment Setup

The CLI needs your Pinecone credentials:

```bash
# Check if keys are loaded
echo $PINECONE_API_KEY

# If empty, load from env file
source /home/kali/Desktop/RAG/.env/pinecone.env
```

## Core Commands

### Search (Most Common)

```bash
# Basic search (top 5 results)
pa "LFI exploitation"

# More results
pa "RCE techniques" -k 10

# Filter by machine
pa "privesc" -m facts

# Verbose output (show full content)
pa "SQL injection" -v

# Combine flags
pa "buffer overflow" -m facts -k 5 -v
```

### List All Indices

```bash
pa list
```

Output:

```
rag-canonical-v1-emb3large    3072d     158 vectors
```

### Describe an Index

```bash
pa describe rag-canonical-v1-emb3large
```

Output:

```
Name:        rag-canonical-v1-emb3large
Status:      Ready
Dimension:   3072
Vectors:     158
Metric:      Cosine
Namespaces:  facts, gavel
```

### Delete a Vector

```bash
# Delete by ID
pa delete --id "chunk_facts_001"

# Delete by file ID
pa delete --file-id "file_12345"
```

### Help

```bash
pa --help
pa -h
```

## Flags Reference

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--help` | `-h` | Show help | -- |
| `-k` | -- | Number of results | 5 |
| `-m` | -- | Filter by machine/namespace | All |
| `-v` | -- | Verbose output (full content) | Off |
| `-a` | -- | Custom assistant name | Default |

## Real-World Examples

### Search only FACTS machine chunks

```bash
pa "buffer overflow exploit" -m facts -k 5 -v
```

### Search GAVEL machine chunks

```bash
pa "api endpoint parameter" -m gavel -k 10
```

### Export results to a file

```bash
pa "RCE" -k 10 -v > rce_results.txt
```

### Count matches

```bash
pa "privilege escalation" -k 20 | wc -l
```

## Understanding the Index

Your default index `rag-canonical-v1-emb3large`:

- **Dimension:** 3072 (OpenAI text-embedding-3-large)
- **Metric:** Cosine similarity
- **Namespaces:** Vectors are organized by machine or category

### Namespace-Based Queries

```bash
# All namespaces
pa "query"

# Only FACTS namespace
pa "query" -m facts

# Only GAVEL namespace
pa "query" -m gavel
```

## Troubleshooting

### "Command not found"

```bash
which pa
ls -la /usr/local/bin/pa
```

### API key issues

```bash
echo $PINECONE_API_KEY | head -c 10
# Should show first 10 chars
```

### Connection timeout

```bash
ping api.pinecone.io
pa --verbose "test query"
```
