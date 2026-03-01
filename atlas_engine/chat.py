"""
Chat - Interactive RAG chat with multiple LLM backends.

Backends:
    gemini   - Google Gemini 2.5 Flash (via LangChain)
    gpt      - OpenAI GPT-4o-mini (via LangChain ChatOpenAI)
    groq     - Groq API (via LangChain ChatGroq)
    ollama   - Ollama local/cloud models (via LangChain ChatOllama)

All backends include:
    - Context memory (k=3 sliding window via InMemoryChatMessageHistory)
    - ChatML/ShareGPT JSONL export for fine-tuning (Unsloth-compatible)

Usage:
    r.chat()                    # default: gemini
    r.chat("gpt")              # GPT-4o-mini
    r.chat("groq")             # Groq API
    r.chat("ollama")           # Ollama local

    response, sources = r.ask("question")
    response, sources = r.ask("question", backend="gpt")
"""

import os
import sys
import json
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Available backends
BACKENDS = {
    "gemini": "gemini-2.5-flash",
    "gpt": "gpt-4o-mini",
    "groq": "openai/gpt-oss-20b",
    "ollama": "gpt-oss:120b-cloud",
}

SYSTEM_PROMPT = (
    "Identity: You are Atlas Engine, a high-efficiency technical intelligence system.\n"
    "Mission: Provide precise, context-aware assistance by synthesizing information "
    "from the provided RAG context and your internal knowledge.\n\n"
    "OPERATIONAL PROTOCOLS:\n"
    "1. CONTEXT FIRST: Prioritize the 'Context:' block for all answers. "
    "If the information is missing, state so clearly and provide the best possible "
    "solution based on general expertise.\n"
    "2. NO VERBOSITY: Eliminate conversational fillers, politeness, and redundant "
    "introductions. Go straight to the technical core.\n"
    "3. STRUCTURE:\n"
    "   - Use Markdown code blocks for scripts, commands, or configuration files.\n"
    "   - Use bullet points for multi-step analysis or feature lists.\n"
    "   - Keep paragraphs short and high-density.\n"
    "4. CONTINUITY: Reference the provided conversation history to maintain logical "
    "flow and avoid repeating previously established facts.\n"
    "5. OBJECTIVE: Deliver maximum technical value per token."
)

# Memory window: 3 exchanges = 6 messages (human + ai pairs)
MEMORY_K = 3
MEMORY_WINDOW = MEMORY_K * 2


class Chat:
    """Interactive RAG chat with pluggable LLM backends and context memory."""

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
            backend: "gemini", "gpt", "groq", or "ollama".
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

        # LangChain LLM instances
        self._llm = None  # LangChain chat model (gpt/groq/ollama)

        # Context memory (shared by all backends)
        self._memory = InMemoryChatMessageHistory()
        self._session_file = None  # ChatML JSONL path

        # Semantic cache (initialized after backend init)
        self.cache = None

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
        elif self.backend == "groq":
            self._init_groq()
        elif self.backend == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Unknown backend: {self.backend}. Use: {list(BACKENDS)}")

        # Initialize semantic cache (all backends)
        if self._openai_client and self._pc_index:
            from atlas_engine.cache import SemanticCache

            self.cache = SemanticCache(self._openai_client, self._pc_index)

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
        from langchain_core.runnables import RunnablePassthrough

        embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            dimensions=config.EMBEDDING_DIM,
            openai_api_key=openai_key,
        )

        from openai import OpenAI

        self._llm = ChatGoogleGenerativeAI(model=self.model, google_api_key=google_key)

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        index = pc.Index(self.index_name)
        self._pc_index = index

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
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self._chain = (
            {"context": self._retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | self._llm
            | StrOutputParser()
        )

    def _init_gpt(self):
        """Initialize GPT-4o-mini via LangChain with conversation memory."""
        from langchain_openai import ChatOpenAI
        from openai import OpenAI
        from pinecone import Pinecone

        openai_key = config.get_openai_key()
        pinecone_key = config.get_pinecone_key()

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        self._pc_index = pc.Index(self.index_name)

        self._llm = ChatOpenAI(
            model=self.model,
            api_key=openai_key,
            temperature=0.7,
            max_tokens=500,
        )

    def _init_groq(self):
        """Initialize Groq via LangChain ChatGroq with conversation memory."""
        from langchain_groq import ChatGroq
        from openai import OpenAI
        from pinecone import Pinecone

        openai_key = config.get_openai_key()
        groq_key = config.get_groq_key()
        pinecone_key = config.get_pinecone_key()

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        self._pc_index = pc.Index(self.index_name)

        self._llm = ChatGroq(
            model=self.model,
            api_key=groq_key,
            temperature=0.7,
            max_tokens=500,
        )

    def _init_ollama(self):
        """Initialize Ollama via LangChain with conversation memory."""
        import requests
        from langchain_community.chat_models import ChatOllama
        from openai import OpenAI
        from pinecone import Pinecone

        openai_key = config.get_openai_key()
        pinecone_key = config.get_pinecone_key()

        self._openai_client = OpenAI(api_key=openai_key)
        pc = Pinecone(api_key=pinecone_key)
        self._pc_index = pc.Index(self.index_name)

        self._llm = ChatOllama(
            model=self.model,
            base_url=self.ollama_url,
            temperature=0.7,
        )

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
    # RETRIEVAL (shared by gpt/groq/ollama backends)
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
    # CONTEXT MEMORY
    # ==================================================================

    def _get_history(self):
        """Get last k exchanges from memory (sliding window)."""
        return trim_messages(
            self._memory.messages,
            max_tokens=MEMORY_WINDOW,
            token_counter=len,
            strategy="last",
            allow_partial=False,
        )

    def _save_to_memory(self, query, response):
        """Save exchange to in-memory history."""
        self._memory.add_message(HumanMessage(content=query))
        self._memory.add_message(AIMessage(content=response))

    def _save_turn(self, context, query, response, history):
        """Append conversation turn to ChatML JSONL for fine-tuning."""
        history_dir = config.RAG_ROOT / "chat_history"
        history_dir.mkdir(exist_ok=True)

        if not self._session_file:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self._session_file = (
                history_dir / f"session_{self.backend}_{ts}_chatml.jsonl"
            )

        # Build ChatML/ShareGPT format
        conversations = [{"from": "system", "value": SYSTEM_PROMPT}]
        for msg in history:
            role = "human" if msg.type == "human" else "gpt"
            conversations.append({"from": role, "value": msg.content})
        conversations.append(
            {
                "from": "human",
                "value": f"Context:\n{context}\n\nQuestion: {query}",
            }
        )
        conversations.append({"from": "gpt", "value": response})

        entry = {"conversations": conversations}
        with open(self._session_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ==================================================================
    # LLM CALLS (unified for gpt/groq/ollama via LangChain)
    # ==================================================================

    def _call_llm(self, context, query):
        """Call LLM via LangChain with conversation memory (gpt/groq/ollama)."""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT + "\n\nContext:\n{context}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        chain = prompt | self._llm

        # Get sliding window history (last k=3 exchanges)
        history = self._get_history()

        result = chain.invoke(
            {
                "context": context,
                "history": history,
                "input": query,
            }
        )
        response = result.content.strip()

        # Save to memory + ChatML JSONL
        self._save_to_memory(query, response)
        self._save_turn(context, query, response, history)

        return response

    # ==================================================================
    # ASK (unified interface)
    # ==================================================================

    def ask(self, question, namespace=None, use_graph=False):
        """
        Ask a single question. Returns (response_text, sources_list).

        Args:
            question: the question to ask.
            namespace: namespace to search in (optional, uses instance default).
            use_graph: if True, expand retrieval with GraphRAG (2 hops semantic graph).

        Works with all backends. Memory persists across calls.
        """
        self._init()

        if self.backend == "gemini":
            return self._ask_gemini(question, use_graph=use_graph)
        else:
            return self._ask_direct(question, namespace=namespace, use_graph=use_graph)

    def _ask_gemini(self, question, use_graph=False):
        """Ask via LangChain chain (Gemini) with memory + semantic cache + optional GraphRAG."""
        # Cache lookup
        if self.cache:
            cached = self.cache.lookup(question)
            if cached:
                response = cached["response"]
                sources = cached["sources"].split(",") if cached["sources"] else []
                self._save_to_memory(question, response)
                print(f"  [CACHE HIT] score={cached['score']:.4f}")
                return response, sources

        docs = self._retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        # GraphRAG expansion (2 hops)
        if use_graph and docs:
            try:
                from atlas_engine.graph import SemanticGraph

                graph = SemanticGraph(namespace=self.namespace)
                # Build from registry
                from atlas_engine.core import Atlas

                atlas = Atlas(namespace=self.namespace)
                all_chunks = atlas._registry.list()
                graph.build_from_chunks(all_chunks)

                # Expand from first result
                seed_id = docs[0].metadata.get("chunk_id", "")
                if seed_id:
                    expansion = graph.query_by_similarity(seed_id, depth=2)
                    if expansion.get("node_ids"):
                        # Add context note
                        context = (
                            f"[GRAPHRAG EXPANSION: +{len(expansion['node_ids'])} related chunks]\n\n"
                            + context
                        )
            except Exception as e:
                print(f"  [GRAPHRAG SKIP] {e}")
                pass
        history = self._get_history()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT + "\n\nContexto:\n{context}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        chain = prompt | self._llm | StrOutputParser()

        response = chain.invoke(
            {
                "context": context,
                "history": history,
                "input": question,
            }
        )

        # Save to memory + ChatML
        self._save_to_memory(question, response)
        self._save_turn(context, question, response, history)

        sources = []
        for doc in docs:
            source = (
                doc.metadata.get("source")
                or doc.metadata.get("chunk_id")
                or doc.metadata.get("domain")
                or "unknown"
            )
            sources.append(source)

        # Cache store
        if self.cache:
            self.cache.store(question, response, sources, self.backend)

        return response, sources

    def _ask_direct(self, question, namespace=None, use_graph=False):
        """Ask via LangChain LLM (GPT/Groq/Ollama) with memory + semantic cache + optional GraphRAG."""
        # Cache lookup
        if self.cache:
            cached = self.cache.lookup(question)
            if cached:
                response = cached["response"]
                sources = cached["sources"].split(",") if cached["sources"] else []
                self._save_to_memory(question, response)
                print(f"  [CACHE HIT] score={cached['score']:.4f}")
                return response, sources

        embedding = self._embed_query(question)
        docs = self._search_pinecone(embedding, namespace=namespace)

        if not docs:
            return "No relevant documents found.", []

        context = self._build_context(docs)

        # GraphRAG expansion (2 hops)
        if use_graph:
            try:
                from atlas_engine.graph import SemanticGraph

                graph = SemanticGraph(namespace=namespace or self.namespace)
                # Build from registry
                all_chunks = self._registry.list()
                graph.build_from_chunks(all_chunks)

                # Expand from first result
                seed_id = docs[0].get("chunk_id", "")
                if seed_id:
                    expansion = graph.query_by_similarity(seed_id, depth=2)
                    if expansion.get("node_ids"):
                        context = (
                            f"[GRAPHRAG: +{len(expansion['node_ids'])} related chunks]\n\n"
                            + context
                        )
            except Exception as e:
                pass  # Silently skip if graph unavailable

        response = self._call_llm(context, question)

        sources = [d["chunk_id"] for d in docs]

        # Cache store
        if self.cache:
            self.cache.store(question, response, sources, self.backend)

        return response, sources

    # ==================================================================
    # INTERACTIVE LOOP
    # ==================================================================

    def interactive(self):
        """Start interactive chat loop in terminal."""
        self._init()

        ns_display = self.namespace if self.namespace else "__default__"
        cache_status = "ON" if self.cache else "OFF"
        print(f"\nRAG Chat ({self.backend}: {self.model})")
        print(f"Index: {self.index_name}:{ns_display} | Top-{self.retriever_k}")
        print(
            f"Memory: last {MEMORY_K} exchanges | Semantic Cache: {cache_status} | ChatML: ON"
        )
        print("Type 'exit' to leave.\n")

        while True:
            try:
                query = input("\n[Pregunta]: ").strip()

                if query.lower() in ("exit", "quit", "salir", "q"):
                    print("Saliendo...")
                    if self.cache:
                        self.cache.stats()
                    if self._session_file:
                        print(f"Session saved: {self._session_file}")
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
                if self._session_file:
                    print(f"Session saved: {self._session_file}")
                break
            except Exception as e:
                print(f"\n[Error]: {e}")

    # ==================================================================
    # Display
    # ==================================================================

    def __repr__(self):
        status = "ready" if self._initialized else "not initialized"
        ns_display = self.namespace if self.namespace else "__default__"
        mem_count = len(self._memory.messages) // 2
        return (
            f"Chat(backend={self.backend}, model={self.model}, "
            f"index={self.index_name}:{ns_display}, k={self.retriever_k}, "
            f"memory={mem_count}/{MEMORY_K}, {status})"
        )
