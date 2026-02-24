"""
Chat - Interactive RAG chat with multiple LLM backends.

Backends:
    gemini   - Google Gemini 2.5 Flash (via LangChain)
    gpt      - OpenAI GPT-4o-mini (direct API, fast + cheap)
    ollama   - Ollama local/cloud models (e.g. gpt-oss:120b-cloud)

Usage:
    r.chat()                    # default: gemini
    r.chat("gpt")              # GPT-4o-mini
    r.chat("ollama")           # Ollama local

    response, sources = r.ask("question")
    response, sources = r.ask("question", backend="gpt")
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# Available backends
BACKENDS = {
    "gemini": "gemini-2.5-flash",
    "gpt": "gpt-4o-mini",
    "ollama": "gpt-oss:120b-cloud",
}

SYSTEM_PROMPT = (
    "You are an expert in CTF and cybersecurity. "
    "Answer questions based ONLY on the provided context. "
    "If you don't have enough information, say so clearly."
)


class Chat:
    """Interactive RAG chat with pluggable LLM backends."""

    def __init__(
        self,
        backend="gemini",
        model=None,
        retriever_k=4,
        ollama_url=None,
        index_name=None,
        namespace=None,
    ):
        """
        Args:
            backend: "gemini", "gpt", or "ollama".
            model: override the default model for the backend.
            retriever_k: number of documents to retrieve.
            ollama_url: Ollama server URL (default: http://localhost:11434).
            index_name: Pinecone index name (optional, uses config default if not provided).
            namespace: namespace to search in (optional, uses config default if not provided).
        """
        self.backend = backend.lower()
        self.model = model or BACKENDS.get(self.backend, BACKENDS["gemini"])
        self.retriever_k = retriever_k
        self.ollama_url = ollama_url or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )

        # Index and namespace configuration
        self.index_name = index_name or config.INDEX_NAME
        self.namespace = (
            config.resolve_namespace(namespace) if namespace else config.NAMESPACE
        )

        # Shared state
        self._openai_client = None
        self._pc_index = None
        self._retriever = None  # LangChain retriever (gemini only)
        self._chain = None  # LangChain chain (gemini only)
        self._embeddings_client = None  # OpenAI client for embeddings (gpt/ollama)
        self._initialized = False

    # ==================================================================
    # INITIALIZATION
    # ==================================================================

    def _init(self):
        if self._initialized:
            return

        if self.backend == "gemini":
            self._init_gemini()
        elif self.backend == "gpt":
            self._init_gpt()
        elif self.backend == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Unknown backend: {self.backend}. Use: {list(BACKENDS)}")

        self._initialized = True

    def _init_gemini(self):
        """Initialize Gemini via LangChain."""
        from dotenv import load_dotenv

        load_dotenv(str(config.ENV_DIR / "openai.env"))
        load_dotenv(str(config.ENV_DIR / "gemini.env"))
        load_dotenv(str(config.ENV_DIR / "pinecone.env"))

        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        pinecone_key = os.getenv("PINECONE_API_KEY")

        missing = []
        if not openai_key:
            missing.append("OPENAI_API_KEY")
        if not google_key:
            missing.append("GOOGLE_API_KEY")
        if not pinecone_key:
            missing.append("PINECONE_API_KEY")
        if missing:
            raise EnvironmentError(f"Missing keys: {', '.join(missing)}")

        from langchain_openai import OpenAIEmbeddings
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_pinecone import PineconeVectorStore
        from pinecone import Pinecone
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser

        embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            dimensions=config.EMBEDDING_DIM,
            openai_api_key=openai_key,
        )

        llm = ChatGoogleGenerativeAI(model=self.model, google_api_key=google_key)

        pc = Pinecone(api_key=pinecone_key)
        index = pc.Index(self.index_name)

        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
            text_key="content",
            namespace=self.namespace,
        )

        self._retriever = vectorstore.as_retriever(
            search_kwargs={"k": self.retriever_k}
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT + "\n\nContexto:\n{context}"),
                ("human", "{input}"),
            ]
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self._chain = (
            {"context": self._retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def _init_gpt(self):
        """Initialize GPT-4o-mini (direct OpenAI API, no LangChain chain)."""
        from openai import OpenAI
        from pinecone import Pinecone

        openai_key = config.get_openai_key()
        pinecone_key = config.get_pinecone_key()

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        self._pc_index = pc.Index(self.index_name)

    def _init_ollama(self):
        """Initialize Ollama (embeddings via OpenAI, LLM via Ollama API)."""
        import requests
        from openai import OpenAI
        from pinecone import Pinecone

        openai_key = config.get_openai_key()
        pinecone_key = config.get_pinecone_key()

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        self._pc_index = pc.Index(self.index_name)

        # Check Ollama connectivity
        try:
            resp = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                models = [m.get("name", "") for m in resp.json().get("models", [])]
                if self.model not in models:
                    print(f"Warning: model '{self.model}' not found in Ollama")
                    print(f"  Available: {', '.join(models) if models else 'none'}")
                    print(f"  Run: ollama pull {self.model}")
            else:
                print(f"Warning: Ollama returned status {resp.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Warning: Ollama not running at {self.ollama_url}")
            print(f"  Start with: ollama serve")

    # ==================================================================
    # RETRIEVAL (shared by gpt/ollama backends)
    # ==================================================================

    def _embed_query(self, text):
        """Generate embedding via OpenAI."""
        response = self._openai_client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=text,
            dimensions=config.EMBEDDING_DIM,
        )
        return response.data[0].embedding

    def _search_pinecone(self, embedding, namespace=None):
        """Search Pinecone and return docs."""
        ns = config.resolve_namespace(namespace) if namespace else self.namespace

        results = self._pc_index.query(
            vector=embedding,
            top_k=self.retriever_k,
            include_metadata=True,
            namespace=ns,
        )
        docs = []
        for match in results.get("matches", []):
            docs.append(
                {
                    "content": match["metadata"].get("content", ""),
                    "chunk_id": match["metadata"].get("chunk_id", "unknown"),
                    "score": match.get("score", 0),
                }
            )
        return docs

    def _build_context(self, docs):
        """Build context string from retrieved docs."""
        return "\n\n---\n\n".join(f"[{d['chunk_id']}]\n{d['content']}" for d in docs)

    # ==================================================================
    # LLM CALLS
    # ==================================================================

    def _call_gpt(self, context, query):
        """Call GPT-4o-mini."""
        response = self._openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()

    def _call_ollama(self, context, query):
        """Call Ollama local/cloud model."""
        import requests

        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=120,
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            raise RuntimeError(
                f"Ollama error ({response.status_code}): {response.text}"
            )

    # ==================================================================
    # ASK (unified interface)
    # ==================================================================

    def ask(self, question, namespace=None):
        """
        Ask a single question. Returns (response_text, sources_list).

        Args:
            question: the question to ask.
            namespace: namespace to search in (optional, uses instance default if not provided).

        Works with all backends.
        """
        self._init()

        if self.backend == "gemini":
            return self._ask_gemini(question)
        else:
            return self._ask_direct(question, namespace=namespace)

    def _ask_gemini(self, question):
        """Ask via LangChain chain (Gemini)."""
        docs = self._retriever.invoke(question)
        response = self._chain.invoke(question)

        sources = []
        for doc in docs:
            source = (
                doc.metadata.get("source")
                or doc.metadata.get("chunk_id")
                or doc.metadata.get("domain")
                or "unknown"
            )
            sources.append(source)
        return response, sources

    def _ask_direct(self, question, namespace=None):
        """Ask via direct API (GPT/Ollama)."""
        embedding = self._embed_query(question)
        docs = self._search_pinecone(embedding, namespace=namespace)

        if not docs:
            return "No relevant documents found.", []

        context = self._build_context(docs)

        if self.backend == "gpt":
            response = self._call_gpt(context, question)
        else:
            response = self._call_ollama(context, question)

        sources = [d["chunk_id"] for d in docs]
        return response, sources

    # ==================================================================
    # INTERACTIVE LOOP
    # ==================================================================

    def interactive(self):
        """Start interactive chat loop in terminal."""
        self._init()

        ns_display = self.namespace if self.namespace else "__default__"
        print(f"\nRAG Chat ({self.backend}: {self.model})")
        print(f"Index: {self.index_name}:{ns_display} | Top-{self.retriever_k}")
        print("Type 'exit' to leave.\n")

        while True:
            try:
                query = input("\n[Pregunta]: ").strip()

                if query.lower() in ("exit", "quit", "salir", "q"):
                    print("Saliendo...")
                    break

                if not query:
                    continue

                response, sources = self.ask(query)

                print(f"\n[Respuesta]:\n{response}")
                print("\n[FUENTES]:")
                for i, s in enumerate(sources, 1):
                    print(f"  [{i}] {s}")

            except KeyboardInterrupt:
                print("\n\nInterrumpido.")
                break
            except Exception as e:
                print(f"\n[Error]: {e}")

    # ==================================================================
    # Display
    # ==================================================================

    def __repr__(self):
        status = "ready" if self._initialized else "not initialized"
        ns_display = self.namespace if self.namespace else "__default__"
        return f"Chat(backend={self.backend}, model={self.model}, index={self.index_name}:{ns_display}, k={self.retriever_k}, {status})"
