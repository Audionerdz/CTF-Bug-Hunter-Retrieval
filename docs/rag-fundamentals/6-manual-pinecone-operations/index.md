# Manual Pinecone Operations

This section covers **pure operational workflows** for managing Pinecone indices without relying on automated scripts. You'll learn to:

- **Embed chunks manually** using OpenAI API
- **Upsert vectors** to specific indices
- **Query and search** your knowledge base
- **Delete vectors** by ID
- **Manage indices** (create, delete, describe)
- **Work with real RAG data** (FACTS, GAVEL)
- **Build indices from scratch**

## Why Manual Operations Matter

While scripts automate workflows, understanding manual operations allows you to:

1. **Debug issues** at each step
2. **Validate data** before upserting
3. **Maintain control** over your knowledge base
4. **Understand the RAG pipeline** completely
5. **Integrate with custom tools** and workflows

## Prerequisites

- **Pinecone CLI**: `pa` command installed and configured
- **API Keys**: Pinecone, OpenAI configured in environment
- **Python 3.9+**: For SDK examples
- **cURL or HTTP client**: For REST API examples

## Quick Command Reference

```bash
# Check Pinecone configuration
pa --help

# List indices
pa list

# Describe an index
pa describe <index-name>

# Query vectors
pa "your query"

# Delete vectors
pa delete --id <vector-id>
```

## Navigation

- **[Pinecone CLI Essentials](pinecone-cli-essentials.md)** - Install, configure, and master the `pa` command
- **[Embedding Chunks Manually](embedding-chunks-manually.md)** - Create embeddings using OpenAI API
- **[Upserting Vectors](upserting-vectors.md)** - Upload vectors to indices step-by-step
- **[Querying and Searching](querying-searching.md)** - Search your knowledge base manually
- **[Managing Vectors](managing-vectors.md)** - Delete, update, describe vectors
- **[Index Management](index-management-manual.md)** - Create, delete, and manage indices
- **[Real-World Examples](real-world-examples.md)** - FACTS, GAVEL, and custom workflows

## Your Current Setup

| Component | Value |
|-----------|-------|
| Default Index | `rag-canonical-v1-emb3large` |
| Embedding Model | `text-embedding-3-large` (3072D) |
| FACTS Machine | 105 chunks indexed |
| GAVEL Machine | 9 chunks indexed |
| Total Vectors | 114 active vectors |
| Namespace Support | Enabled (machine-based) |

---

**Start with [Pinecone CLI Essentials](pinecone-cli-essentials.md) to set up your environment.**
