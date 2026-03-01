"""
RAG - Main orchestrator class that unifies all framework components.

Usage:
    from atlas_engine import Atlas

    atlas = Atlas()

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

    # Chat (4 backends)
    r.chat()                    # Gemini (default)
    r.chat("gpt")              # GPT-4o-mini
    r.chat("groq")             # Groq API
    r.chat("ollama")           # Ollama local

    r.ask("How does LFI work?")
    r.ask("question", backend="gpt")
    r.ask("question", backend="groq")

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
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

from atlas_engine.registry import Registry
from atlas_engine.vectorizer import Vectorizer
from atlas_engine.chunker import Chunker
from atlas_engine.query import QueryEngine
from atlas_engine.telegram import Telegram
from atlas_engine.chat import Chat


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
        max_chars=None,
    ):
        """
        Search the RAG index.

        Args:
            text: search query.
            top_k: number of results (default: 5).
            machine: filter by machine name.
            domain: filter by domain.
            phase: filter by phase.
            show: print results to terminal (default: True).
            namespace: namespace to search in (optional, uses instance default).
            max_chars: max characters to show per chunk (default: None = full content).

        Returns:
            List of result dicts.

        Examples:
            atlas.query("XXE exploitation")
            atlas.query("buffer overflow", top_k=10)
            atlas.query("RCE", top_k=3, max_chars=1000, show=True)
            atlas.query("LFI", namespace="cve", show=False)  # No terminal output
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
            self.query_engine.format_terminal(results, query=text, max_chars=max_chars)
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

    def delete(self, chunk_id, namespace=None):
        """
        Delete a specific chunk by ID.

        Args:
            chunk_id: the chunk ID.
            namespace: namespace to delete from (optional, uses instance default).
        """
        deleted = self.query_engine.delete(chunk_id, namespace=namespace)
        if deleted:
            print(f"Deleted chunk: {chunk_id}")
        return deleted

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

    def vectorize_text(
        self,
        text,
        chunk_id,
        path=None,
        namespace=None,
        domain=None,
        tags=None,
        metadata=None,
    ):
        """
        Create a markdown chunk from raw text and vectorize it.

        Args:
            text: raw markdown content.
            chunk_id: chunk ID to store in frontmatter.
            path: output .md path (optional, defaults under CHUNKS_DIR).
            namespace: namespace to vectorize into (optional).
            domain: metadata domain to store in frontmatter.
            tags: list of tags to store in frontmatter.
            metadata: dict of extra metadata fields to store in frontmatter.
        """
        if not chunk_id:
            raise ValueError("chunk_id is required")

        if path:
            target = Path(path)
            if not target.is_absolute():
                target = (config.RAG_ROOT / target).resolve()
        else:
            safe_name = chunk_id.replace("::", "_")
            target = (config.CHUNKS_DIR / f"{safe_name}.md").resolve()

        target.parent.mkdir(parents=True, exist_ok=True)

        frontmatter = {"chunk_id": chunk_id}
        if domain:
            frontmatter["domain"] = domain
        if tags:
            frontmatter["tags"] = tags
        if metadata:
            for k, v in metadata.items():
                if k not in frontmatter:
                    frontmatter[k] = v

        yaml_block = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
        content = f"---\n{yaml_block}---\n\n{text.strip()}\n"
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        return self.vectorize(str(target), namespace=namespace)

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
            backend: "gemini" (default), "gpt", "groq", or "ollama".
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
            backend: "gemini", "gpt", "groq", or "ollama". None = current.
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

    def build_graph(self, namespace: str = None, max_chunks: int = None):
        """
        Build a semantic knowledge graph from chunks in the given namespace.
        Returns SemanticGraph instance.

        Usage:
            graph = atlas.build_graph(namespace="ctf")
            subgraph = graph.query_by_similarity("chunk_id::001", depth=2)
            html_path = graph.export_html("knowledge_graph.html")
        """
        try:
            from atlas_engine.graph import SemanticGraph
        except ImportError as e:
            print(f"GraphRAG module not available: {e}")
            return None

        ns = namespace or self.namespace
        chunks = self._registry.list()
        chunks_in_ns = [c for c in chunks if c.get("namespace", "root") == ns]

        if max_chunks:
            chunks_in_ns = chunks_in_ns[:max_chunks]

        if not chunks_in_ns:
            print(f"No chunks found in namespace: {ns}")
            return None

        graph = SemanticGraph(namespace=ns)
        graph.build_from_chunks(chunks_in_ns, embeddings=None)
        print(f"Built graph: {graph.stats()}")
        return graph

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
 Atlas Engine v2.0 - Quick Reference
 ======================================

 INITIALIZATION:
   atlas = Atlas()                              # default index & namespace
   atlas = Atlas(namespace="cve")              # namespace preset

 CORE COMMANDS:
   atlas.query("LFI", top_k=5)                 # search
   atlas.ask("What is LFI?")                   # single answer
   atlas.chat()                                 # interactive chat (default backend)
   atlas.chat(backend="gpt")                   # switch backend
   atlas.chat(backend="groq")                  # switch backend
   atlas.fetch("chunk_id::here")              # fetch a chunk
   atlas.delete("chunk_id::here")             # delete a chunk
   atlas.vectorize("/path/file.md")           # vectorize chunks
   atlas.vectorize_text("...", chunk_id="...") # create + vectorize
   atlas.stats()                                # index stats
   atlas.help()                                 # this reference

 NAMESPACE OVERRIDES:
   atlas.query("LFI", namespace="cve")        # search in namespace
   atlas.vectorize("/path", namespace="ctf")  # vectorize into namespace
   atlas.delete("chunk_id", namespace="ctf")  # delete from namespace
""")
