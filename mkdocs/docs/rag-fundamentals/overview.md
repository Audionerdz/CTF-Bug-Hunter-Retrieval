# System Overview

A high-level view of how the Atlas Engine fits together and how information flows through it.

## The Three Pillars

```
+------------------------+
|  Semantic Chunking     |  <-- How to break down knowledge
+------------------------+
|  Vector Database       |  <-- How to store and search
+------------------------+
|  RAG Architecture      |  <-- How to integrate everything
+------------------------+
```

### Pillar 1: Semantic Chunking

**What:** Breaking documents into meaningful, atomic units.
**Why:** Enables precise retrieval and reduces noise.

Instead of one massive document, you get focused chunks:

```
Document: "Complete guide to Linux Privilege Escalation"

Chunks:
  technique::linux::privilege-escalation::suid-enumeration::001
  technique::linux::privilege-escalation::capability-abuse::001
  concept::linux::privilege-escalation::definition::001
```

### Pillar 2: Vector Database

**What:** Storing chunk embeddings in Pinecone for semantic search.
**Why:** Enables fast, relevant retrieval at scale.

```
Query: "How to find SUID binaries?"
    |
    v
Search vector database
    |
    v
Returns: [suid-enumeration::001, suid-exploitation::001]
    |
    v
Retrieve actual content from filesystem
    |
    v
Use in generation
```

### Pillar 3: RAG Architecture

**What:** The framework that ties chunking, search, and generation together.
**Why:** One object (`atlas = Atlas()`) gives you access to everything.

## Information Flow

```
+-----------------+
|   Raw Docs      |  (PDF, text, markdown)
+--------+--------+
         |
         v  r.chunk()
+-----------------+
| Semantic Chunks |  (300-500 word units with YAML frontmatter)
+--------+--------+
         |
         v  atlas.vectorize()
+-----------------+
| Vector Embeddings|  (3072-dimensional vectors via OpenAI)
+--------+--------+
         |
         v  (stored in Pinecone)
+-----------------+
| Pinecone Index  |  (fast semantic search with metadata filters)
+--------+--------+
         |
         v  atlas.query() / atlas.ask()
+-----------------+
| Retrieved Chunks|  (top-K similar chunks)
+--------+--------+
         |
         v  (LLM generates response)
+-----------------+
| AI-Augmented    |  (grounded answer based on real context)
| Response        |
+-----------------+
```

## The Hierarchy

```
+-----------------------------------+
|  Knowledge Base / Project          |
+-----------------------------------+
|  Namespaces (5-10 per project)    |
+-----------------------------------+
|  Domains (10-20 per namespace)    |
+-----------------------------------+
|  Chunks (hundreds per domain)     |
+-----------------------------------+
```

**Example:** `rag-canonical-v1-emb3large` Pinecone index

- Namespace: `ctf`
    - Domain: `web` -- chunks about web exploitation techniques
    - Domain: `linux` -- chunks about Linux privilege escalation
- Namespace: `cve`
    - Domain: `web` -- chunks about specific CVEs

## Universal vs Specific Knowledge

The framework supports three levels of reusability:

### Universal Chunks
- Can be used in any context
- Example: "What is SQL injection?"
- High reusability

### Scenario-Specific Chunks
- Applicable to similar scenarios
- Example: "UNION-based SQL injection technique"
- Medium reusability

### Machine-Specific Chunks
- Only for a specific target
- Example: "Gavel HTB machine .git exposure"
- Low reusability

## Key Metrics

| Metric | Definition | Good Value |
|--------|-----------|-----------|
| Chunk Size | Words per chunk | 300-500 |
| Chunk Precision | Answers one question? | Yes (100%) |
| Namespace Purity | Chunks in correct domain? | >95% |
| Embedding Dimensions | Vector size | 3072 (OpenAI) |
| Recall Rate | Correct chunks retrieved? | >85% |
| Latency | Search time | <100ms |

## Golden Rules

1. **One Chunk = One Question** -- Never violate this
2. **Namespace Isolation** -- Keep domains separate
3. **Metadata is Infrastructure** -- Invest in good metadata
4. **Reusability > Specificity** -- Design for reuse
5. **Track Everything** -- The registry keeps order
