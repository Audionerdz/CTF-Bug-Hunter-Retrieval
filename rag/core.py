"""
RAG - Main orchestrator class that unifies all framework components.

Usage:
    from rag import RAG

    r = RAG()

    # Query
    results = r.query("LFI exploitation")
    results = r.query("RCE", top_k=10, machine="gavel")

    # Chunk PDFs
    r.chunk("/path/to/file.pdf")
    r.chunk("/path/to/pdfs/", domain="cve", tags=["malware"])

    # Vectorize
    r.vectorize("/path/to/chunks")

    # Granular vectorize
    files = r.vectorizer.discover("/path/to/chunks")
    parsed = r.vectorizer.parse(files)
    validated = r.vectorizer.validate(parsed)
    embedded = r.vectorizer.embed(validated)
    r.vectorizer.upsert(embedded)
    r.vectorizer.register(files)

    # Chunk + Vectorize in one shot
    r.ingest("/path/to/file.pdf")

    # Chat (3 backends)
    r.chat()                    # Gemini (default)
    r.chat("gpt")              # GPT-4o-mini
    r.chat("ollama")           # Ollama local

    r.ask("How does LFI work?")
    r.ask("question", backend="gpt")

    # Telegram
    r.send("message text")
    r.send("/path/to/file.md")
    r.send(results)

    # Utilities
    r.sync()
    r.stats()
    r.chunks()
    r.fetch("chunk_id::technique::001")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

from rag.registry import Registry
from rag.vectorizer import Vectorizer
from rag.chunker import Chunker
from rag.query import QueryEngine
from rag.telegram import Telegram
from rag.chat import Chat


class RAG:
    """
    Unified RAG framework.

    All components share the same registry and credentials.
    Lazy initialization: components are only created when first accessed.
    """

    def __init__(self, index_name=None, namespace=None):
        """
        Args:
            index_name: Pinecone index name (optional, uses config default).
            namespace: namespace to use (optional, uses config default).
        """
        # Shared registry
        self._registry = Registry()

        # Index and namespace configuration
        self.index_name = index_name or config.INDEX_NAME
        self.namespace = (
            config.resolve_namespace(namespace) if namespace else config.NAMESPACE
        )

        # Lazy component instances
        self._vectorizer = None
        self._chunker = None
        self._query_engine = None
        self._telegram = None
        self._chat = None
        self._chat_backend = "gemini"

        ns_display = self.namespace if self.namespace else "__default__"
        print(f"RAG Framework v2.0")
        print(f"  Index: {self.index_name}:{ns_display}")
        print(f"  Chunks: {self._registry.count()}")
        print(f"  Root: {config.RAG_ROOT}")

    # ==================================================================
    # Component access (lazy)
    # ==================================================================

    @property
    def vectorizer(self):
        """Access the Vectorizer component."""
        if self._vectorizer is None:
            self._vectorizer = Vectorizer(
                index_name=self.index_name, namespace=self.namespace
            )
        return self._vectorizer

    @property
    def chunker(self):
        """Access the Chunker component."""
        if self._chunker is None:
            self._chunker = Chunker()
        return self._chunker

    @property
    def query_engine(self):
        """Access the QueryEngine component."""
        if self._query_engine is None:
            self._query_engine = QueryEngine(
                registry=self._registry,
                index_name=self.index_name,
                namespace=self.namespace,
            )
        return self._query_engine

    @property
    def telegram(self):
        """Access the Telegram component."""
        if self._telegram is None:
            self._telegram = Telegram()
        return self._telegram

    @property
    def chat_engine(self):
        """Access the Chat component (current backend)."""
        if self._chat is None or self._chat.backend != self._chat_backend:
            self._chat = Chat(
                backend=self._chat_backend,
                index_name=self.index_name,
                namespace=self.namespace,
            )
        return self._chat

    # ==================================================================
    # QUERY - r.query("...")
    # ==================================================================

    def query(
        self,
        text,
        top_k=5,
        machine=None,
        domain=None,
        phase=None,
        show=True,
        namespace=None,
    ):
        """
        Search the RAG index.

        Args:
            text: search query.
            top_k: number of results.
            machine: filter by machine name.
            domain: filter by domain.
            phase: filter by phase.
            show: print results to terminal.
            namespace: namespace to search in (optional, uses instance default).

        Returns:
            List of result dicts.
        """
        results = self.query_engine.search(
            text,
            top_k=top_k,
            machine=machine,
            domain=domain,
            phase=phase,
            namespace=namespace,
        )
        if show:
            self.query_engine.format_terminal(results, query=text)
        return results

    def fetch(self, chunk_id, namespace=None):
        """
        Fetch a specific chunk by ID.

        Args:
            chunk_id: the chunk ID.
            namespace: namespace to fetch from (optional, uses instance default).
        """
        result = self.query_engine.fetch(chunk_id, namespace=namespace)
        if result:
            meta = result["metadata"]
            print(f"\nChunk: {chunk_id}")
            print("=" * 60)
            for k, v in meta.items():
                if k == "content":
                    continue
                print(f"  {k}: {v}")
            content = result.get("content", "")
            if content:
                print(f"\nContent ({len(content)} chars):")
                print("-" * 60)
                print(content)
        else:
            print(f"Chunk not found: {chunk_id}")
        return result

    # ==================================================================
    # CHUNK - r.chunk("file.pdf")
    # ==================================================================

    def chunk(
        self,
        path,
        output_dir=None,
        domain="document",
        tags=None,
        chunk_size=None,
        chunk_overlap=None,
    ):
        """
        Chunk PDFs/text files into RAG-ready markdown with frontmatter.

        Args:
            path: file or directory.
            output_dir: where to save (default: RAG/chunks/).
            domain: metadata domain field.
            tags: optional tags list.
            chunk_size: chars per chunk (default: 2800 ~ 700 tokens).
            chunk_overlap: overlap chars (default: 320 ~ 80 tokens).

        Returns:
            dict with stats and saved file paths.

        For granular control use r.chunker directly:
            files = r.chunker.discover(path)
            docs = r.chunker.load(files)
            chunks = r.chunker.split(docs)
            r.chunker.save(chunks)
        """
        return self.chunker.process(
            path,
            output_dir=output_dir,
            domain=domain,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    # ==================================================================
    # VECTORIZE - r.vectorize("...")
    # ==================================================================

    def vectorize(self, path, namespace=None, domain=None, tags=None, metadata=None):
        """
        Run the full vectorization pipeline on .md chunks.

        Args:
            path: path to chunks directory or file.
            namespace: namespace to vectorize into (optional, uses instance default).
            domain: metadata domain to inject (e.g. "cve", "web").
            tags: list of tags to inject (e.g. ["exploit", "2026"]).
            metadata: dict of extra metadata fields to merge into each chunk.

        For granular control, use r.vectorizer directly.
        """
        return self.vectorizer.run(
            path,
            registry=self._registry,
            namespace=namespace,
            domain=domain,
            tags=tags,
            metadata=metadata,
        )

    # ==================================================================
    # INGEST - r.ingest("file.pdf") = chunk + vectorize
    # ==================================================================

    def ingest(
        self,
        path,
        domain="document",
        tags=None,
        chunk_size=None,
        chunk_overlap=None,
        namespace=None,
    ):
        """
        Full ingest pipeline: chunk PDF/text -> vectorize -> register.

        This is chunk() + vectorize() in one call.

        Args:
            path: PDF, text file, or directory.
            domain: metadata domain.
            tags: optional tags.
            chunk_size: override chunk size.
            chunk_overlap: override overlap.
            namespace: namespace to vectorize into (optional, uses instance default).

        Returns:
            dict with combined stats.
        """
        print(f"\n{'=' * 60}")
        print(f"INGEST PIPELINE: chunk -> vectorize -> register")
        print(f"{'=' * 60}\n")

        # Step 1: Chunk
        chunk_result = self.chunk(
            path,
            domain=domain,
            tags=tags,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        if not chunk_result.get("saved"):
            print("No chunks generated. Aborting.")
            return chunk_result

        # Step 2: Vectorize the output directory
        output_dir = chunk_result.get("output_dir", str(config.CHUNKS_DIR))
        vec_result = self.vectorize(output_dir, namespace=namespace)

        return {
            "chunk_result": chunk_result,
            "vectorize_result": vec_result,
        }

    # ==================================================================
    # CHAT - r.chat() / r.ask("...")
    # ==================================================================

    def chat(self, backend=None):
        """
        Start interactive chat.

        Args:
            backend: "gemini" (default), "gpt", or "ollama".
        """
        if backend:
            self._chat_backend = backend.lower()
            self._chat = None  # Force re-init
        self.chat_engine.interactive()

    def ask(self, question, backend=None, namespace=None):
        """
        Ask a single question.

        Args:
            question: your question.
            backend: "gemini", "gpt", or "ollama". None = current.
            namespace: namespace to search in (optional, uses instance default).

        Returns:
            (response_text, sources_list)
        """
        if backend:
            self._chat_backend = backend.lower()
            self._chat = None
        return self.chat_engine.ask(question, namespace=namespace)

    # ==================================================================
    # TELEGRAM - r.send("...")
    # ==================================================================

    def send(self, content, caption=None):
        """
        Send content to Telegram (auto-detects type).

        Args:
            content: message string, file path, directory path, or query results list.
            caption: optional caption for files.
        """
        return self.telegram.send(content, caption=caption)

    # ==================================================================
    # UTILITIES
    # ==================================================================

    def sync(self, target_dir=None):
        """Sync chunk_registry.json with filesystem."""
        return self._registry.sync(target_dir=target_dir)

    def stats(self):
        """Show Pinecone index statistics."""
        return self.query_engine.stats()

    def chunks(self):
        """List registered chunks."""
        self._registry.info()
        return self._registry.list()

    def save(self, results, query):
        """Save query results as markdown file."""
        return self.query_engine.save_markdown(results, query)

    # ==================================================================
    # Display
    # ==================================================================

    def __repr__(self):
        ns_display = self.namespace if self.namespace else "__default__"
        return (
            f"RAG(index={self.index_name}:{ns_display}, "
            f"chunks={self._registry.count()}, "
            f"root={config.RAG_ROOT})"
        )

    def help(self):
        """Show available commands."""
        print("""
RAG Framework v2.0 - Quick Reference
======================================

INITIALIZATION (with namespace support):
  r = RAG()                                # default index & namespace
  r = RAG(index="my-index")               # custom index
  r = RAG(namespace="cve")                # custom namespace preset
  r = RAG(index="my-index", namespace="ctf")  # both custom

  Namespace presets: "root" (default), "cve", "technique", "ctf", "tools", "payloads"

QUERY (with namespace override):
  r.query("LFI exploitation")             # search (top 5)
  r.query("RCE", top_k=10)                # more results
  r.query("privesc", machine="gavel")     # filter by machine
  r.query("text", namespace="cve")        # search in specific namespace
  r.fetch("chunk_id::here")               # fetch specific chunk
  r.fetch("chunk_id", namespace="ctf")    # fetch from specific namespace

CHUNK (PDF/text -> markdown):
  r.chunk("/path/to/file.pdf")             # chunk a PDF
  r.chunk("/path/to/pdfs/")               # chunk all PDFs in dir
  r.chunk("file.pdf", domain="cve")       # with domain tag
  r.chunk("file.pdf", chunk_size=1500)    # custom size

  # Granular:
  files = r.chunker.discover("/path")
  docs = r.chunker.load(files)
  chunks = r.chunker.split(docs)
  r.chunker.save(chunks)

VECTORIZE (.md chunks -> Pinecone):
  r.vectorize("/path/to/chunks")           # full pipeline (default namespace)
  r.vectorize("my_chunk.md")              # single file
  r.vectorize("/path", namespace="cve")   # vectorize into specific namespace

  Supports:
    - Markdown WITH frontmatter (---YAML---): Use metadata from YAML
    - Markdown WITHOUT frontmatter: Auto-generate metadata, edit in Pinecone

  # Granular:
  files = r.vectorizer.discover("/path")
  parsed = r.vectorizer.parse(files)                    # handles both cases
  validated = r.vectorizer.validate(parsed)             # auto-generates chunk_id if missing
  embedded = r.vectorizer.embed(validated)
  r.vectorizer.upsert(embedded)
  r.vectorizer.register(files)

INGEST (chunk + vectorize in one shot):
  r.ingest("/path/to/file.pdf")            # PDF -> chunks -> Pinecone
  r.ingest("/path/to/pdfs/", domain="cve") # batch + domain
  r.ingest("/path", namespace="ctf")      # ingest into specific namespace

CHAT (3 backends):
  r.chat()                                 # Gemini (default)
  r.chat("gpt")                           # GPT-4o-mini
  r.chat("ollama")                         # Ollama local
  response, sources = r.ask("question")
  response, sources = r.ask("q", backend="gpt")
  response, sources = r.ask("q", namespace="cve")  # ask within specific namespace

TELEGRAM:
  r.send("hello")                          # send message
  r.send("/path/to/file.md")             # send file
  r.send(results)                          # send query results

UTILITIES:
  r.sync()                                 # sync registry
  r.stats()                                # index statistics
  r.chunks()                               # list chunks
  r.save(results, "query")               # save as markdown
  r.help()                                 # this reference
""")
