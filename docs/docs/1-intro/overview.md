# Overview of the Complete Methodology

This section gives you a high-level view of everything you'll learn and how it fits together.

## The Three Pillars

```
┌──────────────────────┐
│  Semantic Chunking   │  ← How to break down knowledge
├──────────────────────┤
│  Vector Database     │  ← How to store and search
├──────────────────────┤
│  RAG Architecture    │  ← How to integrate everything
└──────────────────────┘
```

### Pillar 1: Semantic Chunking (Part 2)

**What:** Breaking documents into meaningful, atomic units  
**Why:** Enables precise retrieval and reduces noise  
**You'll Learn:**
- Chunk design principles
- Chunk ID schema (`<origin>::<domain>::<subdomain>::<intent>::<nnn>`)
- Metadata structure (6 mandatory fields)
- Namespace organization
- Manifest.json for metadata tracking

**Real Example:**
- Document: "Complete guide to Linux Privilege Escalation"
- Instead of one big chunk → Multiple focused chunks:
  - `technique::linux::privilege-escalation::suid-enumeration::001`
  - `technique::linux::privilege-escalation::capability-abuse::001`
  - `concept::linux::privilege-escalation::definition::001`

### Pillar 2: Vector Database Setup (Part 3)

**What:** Setting up Pinecone for semantic search  
**Why:** Enables fast, relevant retrieval at scale  
**You'll Learn:**
- What vector databases are (the library analogy)
- Complete Pinecone setup from account creation
- Index creation and configuration
- Namespace management
- Vectorization with OpenAI embeddings
- Production configurations (3072D embeddings)
- Integration patterns

**Real Example:**
```
Query: "How to find SUID binaries?"
    ↓
Search vector database
    ↓
Get back: [suid-enumeration::001, suid-exploitation::001]
    ↓
Retrieve actual chunk content from filesystem
    ↓
Use in generation
```

### Pillar 3: RAG Architecture (Part 4)

**What:** Designing complete systems  
**Why:** Enables production-ready implementations  
**You'll Learn:**
- System-level design patterns
- Complete index guides
- Update and maintenance procedures
- Monitoring and validation

## The Information Flow

```
┌─────────────┐
│   Raw Docs  │
└──────┬──────┘
       │
       ↓ (CHUNKING)
┌──────────────────┐
│  Semantic Chunks │  ← 300-500 word units
│  + Metadata      │     with YAML front matter
└──────┬───────────┘
       │
       ↓ (EMBEDDING)
┌──────────────────┐
│  Vector Embeddings│  ← 3072 dimensional vectors
│  (3072D)         │     from OpenAI
└──────┬───────────┘
       │
       ↓ (INDEXING)
┌──────────────────┐
│  Pinecone Vector │  ← Fast semantic search
│  Database        │     with metadata filters
└──────┬───────────┘
       │
       ↓ (RETRIEVAL)
┌──────────────────┐
│ Retrieved Chunks │  ← Top-K similar chunks
└──────┬───────────┘
       │
       ↓ (GENERATION)
┌──────────────────┐
│ AI-Augmented     │  ← Answer based on context
│ Response         │
└──────────────────┘
```

## Learning Path

### **Phase 1: Understanding** (Part 1)
- Understand RAG fundamentals
- Know why chunking matters
- Learn the system architecture

### **Phase 2: Chunking** (Part 2)
- Master chunk design
- Learn chunk ID schema
- Understand namespaces and manifests
- Can design chunks for any domain

### **Phase 3: Pinecone** (Part 3)
- Set up Pinecone from scratch
- Configure indexes
- Understand vectorization
- Can integrate with AI models

### **Phase 4: Integration** (Part 4)
- Design complete RAG systems
- Manage knowledge bases
- Monitor and maintain
- Can build production systems

### **Phase 5: Advanced** (Part 5)
- Answer real-world questions
- Solve edge cases
- Optimize performance
- Reference industry patterns

## Key Metrics You'll Master

By completing this methodology, you'll understand:

| Metric | Definition | Good Value |
|--------|-----------|-----------|
| **Chunk Size** | Words per chunk | 300-500 |
| **Chunk Precision** | Answers one question? | Yes (100%) |
| **Namespace Purity** | Chunks in correct domain? | >95% |
| **Embedding Dimensions** | Vector size | 3072 (OpenAI) |
| **Recall Rate** | Correct chunks retrieved? | >85% |
| **Latency** | Search time | <100ms |

## The Hierarchy

```
┌─────────────────────────────────┐
│  Knowledge Base / Project        │
├─────────────────────────────────┤
│  Namespaces (5-10 per project)  │
├─────────────────────────────────┤
│  Domains (10-20 per namespace)  │
├─────────────────────────────────┤
│  Chunks (hundreds per domain)   │
└─────────────────────────────────┘
```

**Example:** `rag-canonical-v1-emb3large` Pinecone index
- Namespace: `chunking-guides`
  - Domain: `rag`
    - Chunks: `concept::rag::chunking::*`
- Namespace: `htb-machines`
  - Domain: `web`
    - Chunks: `htb::gavel::web::enum::*`

## Universal vs Specific Knowledge

The methodology distinguishes between:

### Universal Chunks
- Can be used in any context
- High reusability
- Example: "What is SQL injection?"
- Reuse Level: `universal`

### Scenario-Specific Chunks
- Applicable to similar scenarios
- Medium reusability
- Example: "UNION-based SQL injection technique"
- Reuse Level: `scenario-specific`

### Machine-Specific Chunks
- Only for specific target
- Low reusability
- Example: "Gavel HTB machine .git exposure"
- Reuse Level: `machine-specific`

## Best Practice Checklist

Before starting each phase, verify:

✅ **Understanding Phase**
- [ ] I know what RAG is
- [ ] I understand the three layers
- [ ] I can explain the chunking problem

✅ **Chunking Phase**
- [ ] I can design a chunk
- [ ] I can name chunks consistently
- [ ] I understand namespaces

✅ **Pinecone Phase**
- [ ] I have a Pinecone account
- [ ] My API key is configured
- [ ] I can create indexes

✅ **Integration Phase**
- [ ] I can design complete systems
- [ ] I can manage multiple namespaces
- [ ] I can handle updates

✅ **Advanced Phase**
- [ ] I can optimize performance
- [ ] I can solve edge cases
- [ ] I can mentor others

## Golden Rules

1. **One Chunk = One Question** - Never violate this
2. **Namespace Isolation** - Keep domains separate
3. **Metadata is Infrastructure** - Invest in good metadata
4. **Reusability > Specificity** - Design for reuse
5. **The Manifest Matters** - Track what you have

## What Success Looks Like

After completing this methodology:

✅ You can **design** chunks for any domain  
✅ You can **set up** Pinecone without help  
✅ You can **integrate** RAG into applications  
✅ You can **manage** knowledge bases at scale  
✅ You can **troubleshoot** semantic search issues  
✅ You can **mentor** others on the system  

---

**Ready to dive in?** Start with [Part 2: Chunking Methodology](../2-chunking-methodology/guia-madre.md)
