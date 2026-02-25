# What is RAG?

RAG stands for **Retrieval-Augmented Generation**. It's a way to make AI models give better answers by feeding them real information before they respond.

## The Simple Analogy

Imagine you're a student with a massive library of textbooks and you need to answer a question.

**Without RAG (Bad):**
You try to remember everything from memory. You forget important details, mix up concepts, and your answer is generic and inaccurate.

**With RAG (Good):**

1. Search the library for **relevant books** (Retrieval)
2. Read the specific chapters that match your question (Context)
3. Use that information to **craft a better answer** (Augmented Generation)

Your answer is precise, sourced, and accurate.

## How RAG Works

```
User Question
    |
    v
Vector Database (Pinecone)
    |
    v
Retrieves Similar Chunks
    |
    v
AI Model Reads Retrieved Context
    |
    v
Generates Better Answer
```

Step by step:

1. **User asks a question** -- "What is SUID in Linux?"
2. **Question becomes a vector** -- Converted to a 3072-dimension embedding
3. **Vector database searches** -- Finds chunks with similar meaning
4. **Chunks are retrieved** -- Top matching knowledge units returned
5. **AI reads the chunks** -- Uses them as context
6. **Better answer is generated** -- Based on real knowledge, not hallucination

## The Three Layers

```
+-----------------------------+
|   AI Model (Generation)     |  <-- Answers based on context
+-----------------------------+
|  Vector DB (Retrieval)      |  <-- Pinecone, finds similar
+-----------------------------+
| Filesystem (Knowledge)      |  <-- Actual chunks, source truth
+-----------------------------+
```

### Layer 1: Filesystem (Source of Truth)
- Contains actual documents, chunks, metadata
- Format: Markdown files with YAML front matter
- Purpose: Persistent storage of knowledge

### Layer 2: Vector Database (Semantic Index)
- Contains embeddings (vector representations) of chunks
- Format: Numerical vectors (3072 dimensions via OpenAI)
- Purpose: Enable semantic search without reading all files

### Layer 3: AI Model (Intelligence)
- Reads context from retrieved vectors, generates responses
- Format: Natural language input/output
- Purpose: Synthesize knowledge into actionable answers

## Why This Matters

### LLM Without RAG

- Model tries to answer from training data alone
- Confident even when wrong
- Can't access recent information
- Can't access your private knowledge
- Result: **Hallucinations**

### LLM With RAG

- Model has real, verified information
- Can cite sources
- Knows about updates you've added
- Accesses your knowledge base
- Result: **Grounded answers**

## The Knowledge Chain

```
Raw Documents
    | (Chunking)
Semantic Units (Chunks)
    | (Embedding)
Vector Representations
    | (Indexing)
Vector Database (Pinecone)
    | (Search)
Retrieved Context
    | (Generation)
AI-Augmented Answers
```

Each step matters:

- **Bad chunking** = poor retrieval
- **Bad embeddings** = wrong vectors retrieved
- **Bad indexing** = slow search
- **Bad retrieval** = wrong context
- **Bad generation** = useless answers

## Real-World Example

**Question:** "How do I extract a .git directory vulnerability?"

**Without RAG:**
LLM says "You could use git clone... or maybe git pull... I think there's a tool..." -- generic, might be wrong.

**With RAG:**

1. Question is converted to an embedding
2. Pinecone finds a chunk about `.git` exposure
3. Chunk contains: "Use git-dumper for exposed .git directories"
4. Chunk includes the exact command, parameters, expected output
5. LLM generates a precise answer with the actual technique

## Core Components in This Framework

| Component | Purpose | Technology |
|-----------|---------|------------|
| Chunking Engine | Split documents into atomic units | LangChain RecursiveCharacterTextSplitter |
| Embedding Model | Convert text to vectors | OpenAI text-embedding-3-large (3072D) |
| Vector Database | Store and search vectors | Pinecone |
| Retrieval Logic | Find relevant chunks | Semantic similarity search |
| Generation Model | Create responses | Gemini, GPT-4o-mini, Ollama |

## Key Principles

1. **Granularity** -- Smaller chunks = better precision (300-500 words optimal)
2. **Metadata** -- Rich metadata enables better filtering and retrieval
3. **Naming** -- Semantic chunk IDs help with filtering and debugging
4. **Namespacing** -- Grouping chunks reduces noise during search
5. **Versioning** -- Track chunk versions and embeddings
