"""
Vectorizer - Granular pipeline for processing chunks into Pinecone vectors.

Supports markdown WITH and WITHOUT frontmatter:
    - WITH frontmatter (---YAML---): Use metadata from YAML
    - WITHOUT frontmatter: Auto-generate metadata, save to Pinecone directly

Each phase is an independent method you can call individually or chain together.

Phases:
    1. discover()  - Find .md files from path (directory or single file)
    2. parse()     - Split frontmatter YAML + body from each file
    3. validate()  - Validate metadata (optional: allow missing chunk_id)
    4. embed()     - Generate 3072D embeddings via OpenAI
    5. upsert()    - Upload vectors to Pinecone (with auto-metadata for plain markdown)
    6. register()  - Update chunk_registry.json

    run()          - Execute the full pipeline (1-6)
"""

import os
import sys
import glob
import yaml
import warnings
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

warnings.filterwarnings("ignore")


# ------------------------------------------------------------------
# Data structures for pipeline stages
# ------------------------------------------------------------------


@dataclass
class ParsedChunk:
    """Result of parsing a single .md file."""

    file_path: str
    metadata: Dict[str, Any]  # YAML frontmatter as dict
    body: str  # Content after frontmatter
    raw: str  # Original file content
    metadata_text: str = ""  # Flattened frontmatter as string
    valid: bool = True
    error: Optional[str] = None


@dataclass
class EmbeddedChunk:
    """A parsed chunk with its embedding attached."""

    chunk_id: str
    file_path: str
    metadata: Dict[str, Any]
    body: str
    embedding: List[float] = field(default_factory=list)
    metadata_text: str = ""


class Vectorizer:
    """
    Granular vectorization pipeline.

    Usage (full pipeline):
        v = Vectorizer()
        v.run("/path/to/chunks")

    Usage (phase by phase):
        v = Vectorizer()
        files = v.discover("/path/to/chunks")
        parsed = v.parse(files)
        validated = v.validate(parsed)
        embedded = v.embed(validated)
        v.upsert(embedded)
        v.register(files)
    """

    def __init__(
        self, pinecone_key=None, openai_key=None, index_name=None, namespace=None
    ):
        self._pinecone_key = pinecone_key
        self._openai_key = openai_key
        self._pc = None
        self._index = None
        self._openai = None

        # Pipeline config (overridable)
        self.index_name = index_name or config.INDEX_NAME
        self.namespace = (
            config.resolve_namespace(namespace) if namespace else config.NAMESPACE
        )
        self.embedding_model = config.EMBEDDING_MODEL
        self.embedding_dim = config.EMBEDDING_DIM
        self.batch_size = 100

    # ------------------------------------------------------------------
    # Lazy initialization of API clients
    # ------------------------------------------------------------------

    def _ensure_keys(self):
        if not self._pinecone_key:
            self._pinecone_key = config.get_pinecone_key()
        if not self._openai_key:
            self._openai_key = config.get_openai_key()

    def _get_index(self):
        if self._index is None:
            self._ensure_keys()
            from pinecone import Pinecone

            self._pc = Pinecone(api_key=self._pinecone_key)
            self._index = self._pc.Index(self.index_name)
        return self._index

    def _get_openai(self):
        if self._openai is None:
            self._ensure_keys()
            from openai import OpenAI

            self._openai = OpenAI(api_key=self._openai_key)
        return self._openai

    # ==================================================================
    # PHASE 1 - DISCOVER
    # ==================================================================

    def discover(self, path):
        """
        Find .md chunk files from a path.

        Args:
            path: directory, single .md file, or name to resolve from RAG_ROOT.

        Returns:
            List of absolute file paths.
        """
        path = str(path)

        # Single .md file
        if path.endswith(".md"):
            resolved = path if os.path.isabs(path) else os.path.abspath(path)
            if not os.path.isfile(resolved):
                raise FileNotFoundError(f"File not found: {resolved}")
            return [resolved]

        # Existing directory
        if os.path.isdir(path):
            return self._find_md_files(path)

        # Absolute path that doesn't exist
        if os.path.isabs(path):
            raise FileNotFoundError(f"Path not found: {path}")

        # Try resolving from RAG_ROOT
        test_path = str(config.RAG_ROOT / path)
        if os.path.isdir(test_path):
            return self._find_md_files(test_path)

        raise FileNotFoundError(f"Cannot resolve path: {path}")

    @staticmethod
    def _find_md_files(directory):
        """Recursively find all .md files in a directory."""
        files = sorted(glob.glob(f"{directory}/**/*.md", recursive=True))
        if not files:
            raise FileNotFoundError(f"No .md files found in {directory}")
        return files

    # ==================================================================
    # PHASE 2 - PARSE
    # ==================================================================

    def parse(self, file_paths):
        """
        Parse YAML frontmatter and body from each file.

        Supports:
            1. Markdown WITH frontmatter (---YAML---): Extract metadata + body
            2. Markdown WITHOUT frontmatter: Treat entire content as body, auto-generate chunk_id

        Args:
            file_paths: list of .md file paths.

        Returns:
            List of ParsedChunk objects (both with & without frontmatter).
        """
        results = []

        for fp in file_paths:
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    raw = f.read()

                # Case 1: WITH frontmatter
                if raw.startswith("---"):
                    parts = raw.split("---", 2)
                    try:
                        metadata = yaml.safe_load(parts[1]) or {}
                        body = parts[2].strip() if len(parts) > 2 else ""
                        metadata_text = " ".join(
                            f"{k}: {v}" for k, v in metadata.items()
                        )

                        results.append(
                            ParsedChunk(
                                file_path=fp,
                                metadata=metadata,
                                body=body,
                                raw=raw,
                                metadata_text=metadata_text,
                                valid=True,  # Will be validated in PHASE 3
                            )
                        )
                    except Exception as e:
                        # Malformed frontmatter
                        results.append(
                            ParsedChunk(
                                file_path=fp,
                                metadata={},
                                body=raw,
                                raw=raw,
                                valid=False,
                                error=f"Malformed frontmatter: {e}",
                            )
                        )

                # Case 2: WITHOUT frontmatter (plain markdown)
                else:
                    # Auto-generate chunk_id from filename
                    filename = Path(fp).stem
                    auto_chunk_id = f"chunk::{filename}"

                    metadata = {
                        "chunk_id": auto_chunk_id,
                        "source": str(fp),
                        "chunk_type": "plain-markdown",
                        "requires_metadata_edit": True,  # Flag for manual editing
                    }
                    metadata_text = " ".join(f"{k}: {v}" for k, v in metadata.items())

                    results.append(
                        ParsedChunk(
                            file_path=fp,
                            metadata=metadata,
                            body=raw,
                            raw=raw,
                            metadata_text=metadata_text,
                            valid=True,  # Will be reviewed in validation
                        )
                    )

            except Exception as e:
                results.append(
                    ParsedChunk(
                        file_path=fp,
                        metadata={},
                        body="",
                        raw="",
                        valid=False,
                        error=str(e),
                    )
                )

        return results

    # ==================================================================
    # PHASE 3 - VALIDATE
    # ==================================================================

    def validate(self, parsed_chunks, strict=False):
        """
        Validate parsed chunks.

        Allows:
            1. Chunks WITH frontmatter + chunk_id (strict requirement)
            2. Plain markdown WITHOUT frontmatter (auto-generated chunk_id)

        Args:
            parsed_chunks: list of ParsedChunk.
            strict: if True, reject plain markdown. If False, auto-generate chunk_id.

        Returns:
            List of ParsedChunk with valid=True/False updated.
        """
        for chunk in parsed_chunks:
            if not chunk.valid:
                continue

            # Must have chunk_id in metadata (auto-generated is OK)
            if "chunk_id" not in chunk.metadata:
                if strict:
                    chunk.valid = False
                    chunk.error = "Missing chunk_id in frontmatter"
                else:
                    # Auto-generate chunk_id for plain markdown
                    filename = Path(chunk.file_path).stem
                    chunk.metadata["chunk_id"] = f"chunk::{filename}"
                    chunk.metadata["chunk_type"] = "plain-markdown"
                    chunk.metadata["requires_metadata_edit"] = True

        valid = [c for c in parsed_chunks if c.valid]
        invalid = [c for c in parsed_chunks if not c.valid]

        if invalid:
            for c in invalid:
                print(f"  invalid: {Path(c.file_path).name} - {c.error}")

        plain_markdown = sum(
            1 for c in valid if c.metadata.get("chunk_type") == "plain-markdown"
        )
        print(
            f"Validated: {len(valid)} valid ({plain_markdown} plain markdown), {len(invalid)} invalid"
        )

        if plain_markdown > 0:
            print(f"\n  ⚠️  {plain_markdown} plain markdown file(s) detected!")
            print(f"  These will be vectorized WITH auto-generated metadata.")
            print(
                f"  To customize metadata, edit in Pinecone console or vectorize with proper frontmatter.\n"
            )

        return parsed_chunks

    # ==================================================================
    # PHASE 4 - EMBED
    # ==================================================================

    def embed(self, parsed_chunks):
        """
        Generate 3072D embeddings for valid parsed chunks.

        Works with both:
            1. Chunks with full frontmatter metadata
            2. Plain markdown with auto-generated metadata

        Args:
            parsed_chunks: list of ParsedChunk (only valid ones are embedded).

        Returns:
            List of EmbeddedChunk with embeddings attached.
        """
        client = self._get_openai()
        results = []

        valid = [c for c in parsed_chunks if c.valid]
        print(
            f"Embedding {len(valid)} chunks ({self.embedding_model}, {self.embedding_dim}D)..."
        )

        for i, chunk in enumerate(valid):
            # Ensure chunk_id exists (auto-generate if missing)
            if "chunk_id" not in chunk.metadata:
                filename = Path(chunk.file_path).stem
                chunk.metadata["chunk_id"] = f"chunk::{filename}"
                chunk.metadata["chunk_type"] = "plain-markdown"
                chunk.metadata["requires_metadata_edit"] = True

            text_to_embed = f"{chunk.metadata_text} {chunk.body}"

            try:
                response = client.embeddings.create(
                    model=self.embedding_model,
                    input=text_to_embed,
                    dimensions=self.embedding_dim,
                )
                embedding = response.data[0].embedding

                results.append(
                    EmbeddedChunk(
                        chunk_id=chunk.metadata["chunk_id"],
                        file_path=chunk.file_path,
                        metadata=chunk.metadata,
                        body=chunk.body,
                        embedding=embedding,
                        metadata_text=chunk.metadata_text,
                    )
                )
                chunk_type = chunk.metadata.get("chunk_type", "unknown")
                print(
                    f"  [{i + 1}/{len(valid)}] {chunk.metadata['chunk_id']} ({chunk_type})"
                )

            except Exception as e:
                print(f"  FAIL: {Path(chunk.file_path).name} - {e}")

        return results

    # ==================================================================
    # PHASE 5 - UPSERT
    # ==================================================================

    def upsert(self, embedded_chunks, namespace=None):
        """
        Upload embedded chunks to Pinecone.

        Args:
            embedded_chunks: list of EmbeddedChunk.
            namespace: override namespace (optional).

        Returns:
            Number of vectors upserted.
        """
        if not embedded_chunks:
            print("Nothing to upsert.")
            return 0

        idx = self._get_index()
        ns = config.resolve_namespace(namespace) if namespace else self.namespace

        vectors = []
        for ec in embedded_chunks:
            vectors.append(
                {
                    "id": ec.chunk_id,
                    "values": ec.embedding,
                    "metadata": {
                        **ec.metadata,
                        "content": ec.body,
                        "content_length": len(ec.body),
                    },
                }
            )

        ns_display = f":{ns}" if ns else ":__default__"
        print(f"Upserting {len(vectors)} vectors to {self.index_name}{ns_display}...")

        for i in range(0, len(vectors), self.batch_size):
            batch = vectors[i : i + self.batch_size]
            idx.upsert(vectors=batch, namespace=ns)
            print(f"  batch {i // self.batch_size + 1}: {len(batch)} vectors")

        return len(vectors)

    # ==================================================================
    # PHASE 6 - REGISTER
    # ==================================================================

    def register(self, file_paths, registry=None):
        """
        Update chunk_registry.json with newly processed files.

        Args:
            file_paths: list of .md file paths that were vectorized.
            registry: optional Registry instance (creates one if not provided).

        Returns:
            Registry instance.
        """
        from rag.registry import Registry

        reg = registry or Registry()
        mapping = reg.build_from_files(file_paths)
        reg.add_many(mapping)
        reg.save()
        print(f"Registry updated: +{len(mapping)} entries ({reg.count()} total)")
        return reg

    # ==================================================================
    # FULL PIPELINE
    # ==================================================================

    def run(self, path, registry=None, namespace=None):
        """
        Execute the full vectorization pipeline.

        Supports both:
            1. Markdown WITH frontmatter (YAML metadata)
            2. Markdown WITHOUT frontmatter (auto-generated metadata in Pinecone)

        Args:
            path: directory, file, or name.
            registry: optional Registry instance.
            namespace: Pinecone namespace (optional, override instance default).

        Returns:
            dict with pipeline stats.
        """
        ns = config.resolve_namespace(namespace) if namespace else self.namespace
        ns_display = f":{ns}" if ns else ":__default__"

        print(f"\n{'=' * 60}")
        print(f"VECTORIZER - {self.embedding_model} ({self.embedding_dim}D)")
        print(f"{'=' * 60}")
        print(f"Path: {path}")
        print(f"Index: {self.index_name}{ns_display}")
        print(f"Supports: .md WITH & WITHOUT frontmatter\n")

        # Phase 1
        files = self.discover(path)
        print(f"Discovered: {len(files)} file(s)")

        # Phase 2
        parsed = self.parse(files)

        # Phase 3
        self.validate(parsed)

        # Phase 4
        embedded = self.embed(parsed)

        if not embedded:
            print("No vectors generated.")
            return {"files": len(files), "embedded": 0, "upserted": 0}

        # Phase 5
        upserted = self.upsert(embedded, namespace=ns)

        # Phase 6
        self.register(files, registry=registry)

        # Stats
        stats = self._stats()

        result = {
            "files": len(files),
            "embedded": len(embedded),
            "upserted": upserted,
            "index_total": stats.get("total_vector_count", "?"),
        }

        print(f"\nDone: {result['embedded']} embedded, {result['upserted']} upserted")
        return result

    def _stats(self):
        """Get index statistics."""
        try:
            idx = self._get_index()
            return idx.describe_index_stats()
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        return f"Vectorizer(index={self.index_name}, model={self.embedding_model}, dim={self.embedding_dim})"
