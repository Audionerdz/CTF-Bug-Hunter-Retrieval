# Building an AI-Powered RAG Chat System: Complete Step-by-Step Guide

**Goal:** Create an interactive terminal RAG chat using LangChain, Pinecone, OpenAI embeddings, and Google Gemini LLM.

**Stack Overview:**
- **Embeddings Model:** `text-embedding-3-large` (3072 dimensions) from OpenAI
- **Vector Store:** Pinecone (`rag-canonical-v1-emb3large` index)
- **LLM:** `gemini-2.5-flash` from Google AI
- **Framework:** LangChain with LCEL (LangChain Expression Language)
- **Interface:** Interactive Python terminal loop

---

## Prerequisites

Before starting, ensure you have:

1. **API Keys** stored in `/root/.openskills/env/`:
   - `openai.env` - Contains `OPENAI_API_KEY`
   - `gemini.env` - Contains `GOOGLE_API_KEY`
   - `pinecone.env` - Contains `PINECONE_API_KEY` and index name

2. **Python Virtual Environment** activated:
   ```bash
   source /root/.openskills/venv/bin/activate
   ```

3. **Existing Pinecone Index:**
   - Index name: `rag-canonical-v1-emb3large`
   - Dimensions: 3072
   - Metric: cosine
   - Status: Contains vectorized documents (148 vectors in our case)

4. **Basic understanding of:**
   - RAG (Retrieval-Augmented Generation) concepts
   - LangChain chains and runnables
   - Pinecone vector database

---

## Step 1: Install Required Dependencies

### 1.1 Activate the Python Environment

```bash
source /root/.openskills/venv/bin/activate
```

### 1.2 Install LangChain and Related Packages

```bash
pip install langchain langchain-core langchain-community langchain-openai langchain-google-genai langchain-pinecone -q
```

**What each package does:**

| Package | Purpose |
|---------|---------|
| `langchain` | Core framework for building RAG applications |
| `langchain-core` | LangChain Expression Language (LCEL) for composing chains |
| `langchain-community` | Community integrations (not required but useful) |
| `langchain-openai` | OpenAI embeddings and LLM integration |
| `langchain-google-genai` | Google Gemini LLM integration |
| `langchain-pinecone` | PineconeVectorStore wrapper for easy retrieval |

### 1.3 Verify Installation

```bash
python -c "from langchain_openai import OpenAIEmbeddings; print('✓ LangChain installed')"
```

Expected output:
```
✓ LangChain installed
```

---

## Step 2: Load Environment Variables

### 2.1 Verify API Keys Exist

```bash
cat /root/.openskills/env/openai.env
cat /root/.openskills/env/gemini.env
cat /root/.openskills/env/pinecone.env
```

Example output:
```
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
PINECONE_API_KEY=pcsk_...
```

### 2.2 Create the Environment Loading Module

This step is **embedded in the final script** (Section 5), but here's how it works:

```python
from dotenv import load_dotenv
import os

# Load environment files
load_dotenv('/root/.openskills/env/openai.env')
load_dotenv('/root/.openskills/env/gemini.env')
load_dotenv('/root/.openskills/env/pinecone.env')

# Verify keys are loaded
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")

print(f"OpenAI: {'✓' if openai_key else '✗'}")
print(f"Google: {'✓' if google_key else '✗'}")
print(f"Pinecone: {'✓' if pinecone_key else '✗'}")
```

---

## Step 3: Initialize Embeddings Model

### 3.1 Import OpenAI Embeddings

```python
from langchain_openai import OpenAIEmbeddings

# Initialize with 3072 dimensions (required for rag-canonical-v1-emb3large)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=3072,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

**Why 3072 dimensions?**
- Your Pinecone index was created with 3072-dimensional vectors
- `text-embedding-3-large` natively supports this
- This ensures embedding compatibility with stored vectors

### 3.2 Test the Embeddings

```bash
python << 'EOF'
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv('/root/.openskills/env/openai.env')

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=3072,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Generate embedding for test query
test_embedding = embeddings.embed_query("LFI exploitation")
print(f"✓ Embedding generated: {len(test_embedding)} dimensions")
EOF
```

Expected output:
```
✓ Embedding generated: 3072 dimensions
```

---

## Step 4: Initialize LLM (Gemini)

### 4.1 Import ChatGoogleGenerativeAI

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

**Why gemini-2.5-flash?**
- Fast response time (optimal for interactive chat)
- Supports 3072-dimensional context (from retriever)
- Free tier available
- Language understanding is excellent for CTF domains

### 4.2 Alternative Models (if needed)

```python
# For more powerful reasoning:
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Check available models:
# python3 << 'EOF'
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# load_dotenv('/root/.openskills/env/gemini.env')
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(f"  - {m.name}")
# EOF
```

### 4.3 Test the LLM

```bash
python << 'EOF'
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv('/root/.openskills/env/gemini.env')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

response = llm.invoke("What is LFI?")
print(f"✓ LLM Response: {response.content[:100]}...")
EOF
```

---

## Step 5: Connect to Pinecone Vector Store

### 5.1 Initialize Pinecone Index

```python
from pinecone import Pinecone

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Get your index
index = pc.Index("rag-canonical-v1-emb3large")

# Verify index stats
stats = index.describe_index_stats()
print(f"Index: {stats['vector_count']} vectors, {stats['dimension']} dimensions")
```

### 5.2 Create PineconeVectorStore Wrapper

```python
from langchain_pinecone import PineconeVectorStore

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="content"  # CRITICAL: Your documents use "content" field, not "text"
)
```

**Important Note on `text_key="content"`:**

Your Pinecone documents store content in a metadata field called `content`:
```json
{
  "id": "technique::web::lfi::parameter-discovery::001",
  "metadata": {
    "chunk_id": "technique::web::lfi::parameter-discovery::001",
    "content": "# Identificación de puntos de entrada para LFI...",
    "domain": "web",
    "chunk_type": "technique"
  }
}
```

If your documents use a different field name, update this parameter accordingly.

### 5.3 Create a Retriever

```python
# Get top-4 most relevant documents
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)
```

### 5.4 Test the Retriever

```bash
python << 'EOF'
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv('/root/.openskills/env/openai.env')
load_dotenv('/root/.openskills/env/pinecone.env')

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=3072,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="content"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Test retrieval
docs = retriever.invoke("What is LFI")
print(f"✓ Retrieved {len(docs)} documents")
for i, doc in enumerate(docs, 1):
    source = doc.metadata.get("chunk_id", "Unknown")
    print(f"  [{i}] {source}")
EOF
```

Expected output:
```
✓ Retrieved 4 documents
  [1] technique::web::lfi::parameter-discovery::001
  [2] reference::linux::web-security::lfi-target-files::001
  [3] procedure::web::lua-detection::vulnerability-testing::001
  [4] technique::network::enumeration::parameter-fuzzing-get::001
```

---

## Step 6: Build the RAG Chain with LCEL

### 6.1 Understand LCEL (LangChain Expression Language)

LCEL is a declarative way to compose chains. Think of it as:

```
Input → [Retriever] → Documents → [Format] → Context
     ↓
     [Prompt Template] (with context + input)
     ↓
     [LLM]
     ↓
     [Output Parser]
     ↓
     Final Response
```

### 6.2 Create Helper Function to Format Documents

```python
def format_docs(docs):
    """Combine multiple documents into a single text string."""
    return "\n\n".join(doc.page_content for doc in docs)
```

This function:
- Takes a list of retrieved documents
- Joins them with double newlines
- Returns a single string (required by prompt template)

### 6.3 Create the Prompt Template

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert assistant in CTF and cybersecurity.
Answer the question using ONLY the provided context.
If you don't have sufficient information, say so clearly.

Context:
{context}"""
    ),
    ("human", "{input}"),
])
```

**What this does:**
- System message: Sets the assistant's role and constraints
- `{context}`: Will be filled with retrieved documents
- `{input}`: Will be filled with user's question
- `("human", "{input}")`: Follows OpenAI chat format

### 6.4 Build the Chain Using LCEL

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# LCEL chain composition
chain = (
    {
        "context": retriever | format_docs,  # Pass user input to retriever, format output
        "input": RunnablePassthrough()        # Pass user input as-is
    }
    | prompt                                  # Feed context + input to prompt
    | llm                                     # Feed formatted prompt to LLM
    | StrOutputParser()                       # Parse LLM output to string
)
```

**Step-by-step breakdown:**

1. `{"context": retriever | format_docs, "input": RunnablePassthrough()}`
   - Creates a dict with two keys
   - `context`: retrieves top-4 docs and formats them
   - `input`: passes the user's query unchanged
   - This dict is passed to the prompt template

2. `| prompt`
   - Pipes the dict into the prompt template
   - Fills `{context}` with retrieved docs
   - Fills `{input}` with user query

3. `| llm`
   - Sends formatted prompt to Gemini
   - LLM generates response

4. `| StrOutputParser()`
   - Converts LLM output (AIMessage object) to plain string

### 6.5 Test the Chain

```bash
python << 'EOF'
# ... (previous initialization code) ...

# Test chain
response = chain.invoke("What is LFI and how to exploit it?")
print(f"✓ Response: {response}")
EOF
```

---

## Step 7: Create the Interactive Terminal Interface

### 7.1 Build the Main Loop

```python
def format_sources(documents):
    """Format retrieved documents with their metadata."""
    sources = []
    for i, doc in enumerate(documents, 1):
        # Try multiple metadata fields
        source = (
            doc.metadata.get("source")
            or doc.metadata.get("chunk_id")
            or doc.metadata.get("domain")
            or "Unknown"
        )
        sources.append(f"  [{i}] {source}")
    return "\n".join(sources)


def main():
    print("Initializing RAG system...")
    # Initialize components
    llm, retriever = initialize_components()
    chain, retriever = build_chain(llm, retriever)
    
    print(f"Ready. Index: rag-canonical-v1-emb3large | Top-4 documents\n")
    print("Type 'exit', 'quit', or 'salir' to exit.\n")

    while True:
        try:
            # Get user input
            query = input("\n[Question]: ").strip()

            # Exit commands
            if query.lower() in ["exit", "quit", "salir"]:
                print("Exiting...")
                break

            # Skip empty queries
            if not query:
                continue

            # Retrieve documents and generate response
            docs = retriever.invoke(query)
            response = chain.invoke(query)

            # Display response
            print(f"\n[Response]:\n{response}")

            # Display sources
            print("\n[SOURCES]:")
            print(format_sources(docs))

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")
```

**Key features:**

- **Infinite loop:** Keeps accepting queries until user exits
- **Error handling:** Gracefully handles Ctrl+C and exceptions
- **Dual output:** Shows both response and source documents
- **Source attribution:** Displays `chunk_id` or other metadata for traceability

---

## Step 8: Create the Complete Script

### 8.1 Full Script: `src/rag_terminal.py`

Create the file at `/home/kali/Desktop/RAG/src/rag_terminal.py`:

```python
#!/usr/bin/env python3
"""
RAG Terminal Chat with LangChain + Pinecone + Gemini.

Interactive terminal interface for querying the CTF/cybersecurity knowledge base.

Usage:
    python3 rag_terminal.py

Environment files (loaded from /root/.openskills/env/):
    - openai.env: OPENAI_API_KEY (for embeddings)
    - gemini.env: GOOGLE_API_KEY (for LLM)
    - pinecone.env: PINECONE_API_KEY (for vector store)

Stack:
    - Embeddings: text-embedding-3-large (3072 dims) via OpenAI
    - LLM: gemini-2.5-flash via Google
    - Vector Store: Pinecone (rag-canonical-v1-emb3large)
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

OPENAI_ENV_PATH = "/root/.openskills/env/openai.env"
GEMINI_ENV_PATH = "/root/.openskills/env/gemini.env"
PINECONE_ENV_PATH = "/root/.openskills/env/pinecone.env"

load_dotenv(OPENAI_ENV_PATH)
load_dotenv(GEMINI_ENV_PATH)
load_dotenv(PINECONE_ENV_PATH)

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMS = 3072
LLM_MODEL = "gemini-2.5-flash"
PINECONE_INDEX_NAME = "rag-canonical-v1-emb3large"
RETRIEVER_K = 4


def load_environment():
    """Load and validate API keys from environment files."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    pinecone_key = os.getenv("PINECONE_API_KEY")

    if not all([openai_key, google_key, pinecone_key]):
        missing = [
            k
            for k, v in {
                "OPENAI_API_KEY": openai_key,
                "GOOGLE_API_KEY": google_key,
                "PINECONE_API_KEY": pinecone_key,
            }.items()
            if not v
        ]
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

    return openai_key, google_key, pinecone_key


def initialize_components():
    """Initialize embeddings, LLM, and vector store."""
    openai_key, google_key, pinecone_key = load_environment()

    # Initialize embeddings model
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL, 
        dimensions=EMBEDDING_DIMS, 
        openai_api_key=openai_key
    )

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL, 
        google_api_key=google_key
    )

    # Connect to Pinecone
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index(PINECONE_INDEX_NAME)

    # Create vector store wrapper
    vectorstore = PineconeVectorStore(
        index=index, 
        embedding=embeddings, 
        text_key="content"
    )

    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})

    return llm, retriever


def format_docs(docs):
    """Combine retrieved documents into a single text string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(llm, retriever):
    """Build LCEL chain for RAG."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert assistant in CTF and cybersecurity. 
Answer the question using ONLY the provided context.
If you don't have sufficient information, say so clearly.

Context:
{context}""",
            ),
            ("human", "{input}"),
        ]
    )

    # LCEL chain composition
    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def format_sources(documents):
    """Format retrieved documents with metadata for display."""
    sources = []
    for i, doc in enumerate(documents, 1):
        source = (
            doc.metadata.get("source")
            or doc.metadata.get("chunk_id")
            or doc.metadata.get("domain")
            or "Unknown"
        )
        sources.append(f"  [{i}] {source}")
    return "\n".join(sources)


def main():
    """Main interactive loop."""
    print("Initializing RAG system...")
    llm, retriever = initialize_components()
    chain, retriever = build_chain(llm, retriever)
    print(
        f"Ready. Index: {PINECONE_INDEX_NAME} | Retrieving top-{RETRIEVER_K} documents.\n"
    )
    print("Type 'exit', 'quit', or 'salir' to exit.\n")

    while True:
        try:
            query = input("\n[Question]: ").strip()

            if query.lower() in ["exit", "quit", "salir"]:
                print("Exiting...")
                break

            if not query:
                continue

            # Retrieve documents and generate response
            docs = retriever.invoke(query)
            response = chain.invoke(query)

            # Display response
            print(f"\n[Response]:\n{response}")

            # Display sources
            print("\n[SOURCES]:")
            print(format_sources(docs))

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")


if __name__ == "__main__":
    main()
```

### 8.2 Save the Script

```bash
# Create file
cat > /home/kali/Desktop/RAG/src/rag_terminal.py << 'SCRIPT_EOF'
# (Paste the full script above)
SCRIPT_EOF

# Make it executable
chmod +x /home/kali/Desktop/RAG/src/rag_terminal.py
```

---

## Step 9: Create Requirements File

### 9.1 Create `requirements.txt`

```bash
cat > /home/kali/Desktop/RAG/requirements.txt << 'EOF'
# RAG System Dependencies
# LangChain Core
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0

# LangChain Integrations
langchain-openai>=0.2.0
langchain-google-genai>=2.0.0
langchain-pinecone>=0.1.0

# Vector Store
pinecone>=5.0.0

# Embeddings & LLM Providers
openai>=1.0.0
google-generativeai>=0.8.0

# Utilities
python-dotenv>=1.0.0
EOF
```

---

## Step 10: Set Up Aliases

### 10.1 Add to `~/.zshrc`

```bash
echo "alias rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'" >> ~/.zshrc

# Reload shell config
source ~/.zshrc
```

### 10.2 Verify Alias

```bash
alias | grep rag-chat
```

Expected output:
```
rag-chat='/root/.openskills/venv/bin/python3 /home/kali/Desktop/RAG/src/rag_terminal.py'
```

---

## Step 11: Test the Complete System

### 11.1 Run the RAG Chat

```bash
rag-chat
```

### 11.2 Test Queries

Once the script starts, try these queries:

```
[Question]: What is LFI?
```

Expected output:
```
[Response]:
LFI (Local File Inclusion) occurs when a web application allows a user to control 
the name or path of a file that the server should load...

[SOURCES]:
  [1] technique::web::lfi::parameter-discovery::001
  [2] reference::linux::web-security::lfi-target-files::001
  [3] procedure::web::lua-detection::vulnerability-testing::001
  [4] technique::network::enumeration::parameter-fuzzing-get::001
```

### 11.3 More Test Queries

```
[Question]: How to discover LFI parameters?
[Question]: SQL injection blind techniques
[Question]: exit
```

---

## Step 12: Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'langchain'"

**Solution:**
```bash
source /root/.openskills/venv/bin/activate
pip install -r /home/kali/Desktop/RAG/requirements.txt
```

### Issue: "OPENAI_API_KEY not found"

**Solution:**
```bash
# Verify env file exists
cat /root/.openskills/env/openai.env

# If missing, create it:
echo "OPENAI_API_KEY=your_key_here" > /root/.openskills/env/openai.env
```

### Issue: "models/gemini-1.5-flash is not found"

**Solution:**
This model is deprecated. Use `gemini-2.5-flash` instead (already configured in the script).

To check available models:
```bash
python << 'EOF'
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('/root/.openskills/env/gemini.env')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")
EOF
```

### Issue: "Found document with no `content` key"

**Solution:**
Your Pinecone documents use a different metadata field. Update the `text_key` parameter:

```python
# In rag_terminal.py, change:
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="your_field_name"  # Check your document structure
)
```

To find the correct field:
```bash
python << 'EOF'
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv('/root/.openskills/env/pinecone.env')

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-canonical-v1-emb3large")

results = index.query(
    vector=[0] * 3072,  # Dummy vector
    top_k=1,
    include_metadata=True
)

if results.matches:
    metadata = results.matches[0].metadata
    print("Available metadata fields:")
    for key in metadata.keys():
        print(f"  - {key}")
EOF
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Question                           │
│                  "What is LFI?"                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │   Embeddings Model           │
            │  (text-embedding-3-large)    │
            │   (3072 dimensions)          │
            └──────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │   Pinecone Vector Store      │
            │ (rag-canonical-v1-emb3large) │
            │   (Semantic Search)          │
            └──────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │   Retrieved Documents (k=4)  │
            │  + Document Formatting       │
            └──────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │    Prompt Template           │
            │  (System + Context + Input)  │
            └──────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │    LLM (Gemini 2.5 Flash)    │
            │  (Generates Response)        │
            └──────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │   String Output Parser       │
            │  (Format LLM Response)       │
            └──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Response + Sources                     │
│                                                              │
│ [Response]:                                                  │
│ LFI (Local File Inclusion) occurs when...                  │
│                                                              │
│ [SOURCES]:                                                   │
│   [1] technique::web::lfi::parameter-discovery::001         │
│   [2] reference::linux::web-security::lfi-target-files::001 │
│   ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## How This Differs from Simple Query

| Aspect | Simple Query | RAG Chat |
|--------|--------------|----------|
| **Retrieval** | ✓ Searches Pinecone | ✓ Searches Pinecone |
| **Output** | Raw document text | ✓ AI-synthesized response |
| **Context** | User must connect dots | LLM connects multiple docs |
| **Quality** | Technical but verbose | Clear, structured answers |
| **Speed** | Instant | Fast (Gemini is optimized) |
| **Language** | As written in notes | Adapted to question |

**Example:**

Your notes have 3 separate chunks:
1. "LFI detection with fuzzing"
2. "LFI exploitation via directory traversal"
3. "Common LFI bypass techniques"

**Simple query:** Returns all 3 texts, you manually synthesize.

**RAG Chat:** Gemini reads all 3, extracts relevant info, and gives you a single structured answer about "how to exploit LFI."

---

## Deployment to Another VPS

### Step 1: Transfer the Script
```bash
scp /home/kali/Desktop/RAG/src/rag_terminal.py user@new_vps:/home/user/RAG/src/
scp /home/kali/Desktop/RAG/requirements.txt user@new_vps:/home/user/RAG/
```

### Step 2: Install Dependencies
```bash
ssh user@new_vps

# Create env directory
mkdir -p ~/.openskills/env

# Create environment files with your keys
echo "OPENAI_API_KEY=your_key" > ~/.openskills/env/openai.env
echo "GOOGLE_API_KEY=your_key" > ~/.openskills/env/gemini.env
echo "PINECONE_API_KEY=your_key" > ~/.openskills/env/pinecone.env

# Install requirements
cd /home/user/RAG
pip install -r requirements.txt
```

### Step 3: Run
```bash
python3 src/rag_terminal.py
```

---

## Summary

You've built a **multi-layer AI system** that:

1. **Retrieves** relevant knowledge from Pinecone
2. **Synthesizes** answers using Gemini LLM
3. **Attributes** sources for transparency
4. **Serves** results via interactive terminal

This is **RAG (Retrieval-Augmented Generation)** in action: combining your custom knowledge base with LLM intelligence.

