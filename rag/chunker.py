"""
Chunker - Split PDFs and text files into RAG-ready markdown chunks.

Uses LangChain RecursiveCharacterTextSplitter with settings optimized
for dense cybersecurity documents.

Defaults:
    chunk_size:    700 tokens (~2800 chars)
    chunk_overlap: 10-15% (~80 tokens / ~320 chars)
    splitter:      RecursiveCharacterTextSplitter

Usage (via RAG framework):
    r = RAG()
    chunks = r.chunk("/path/to/file.pdf")
    chunks = r.chunk("/path/to/pdfs/")
    chunks = r.chunk("/path/to/file.pdf", chunk_size=500, overlap=50)

Usage (standalone):
    from rag.chunker import Chunker
    c = Chunker()
    chunks = c.process("/path/to/file.pdf")
    c.save(chunks, output_dir="/path/to/output")

    # Granular:
    files = c.discover("/path/to/pdfs/")
    docs = c.load(files)
    chunks = c.split(docs)
    c.save(chunks, output_dir="./chunks")
"""

import os
import sys
import re
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))
import config


@dataclass
class Chunk:
    """A single chunk ready for vectorization."""

    chunk_id: str
    content: str  # The actual text content
    source_file: str  # Original file path
    page: Optional[int] = None  # Page number (PDFs)
    chunk_index: int = 0  # Position within the source
    total_chunks: int = 0  # Total chunks from this source
    metadata: Dict[str, Any] = field(default_factory=dict)


class Chunker:
    """
    Split PDFs and text files into RAG-ready chunks with YAML frontmatter.

    Supports: .pdf, .txt, .md, .html, .csv

    Pipeline:
        1. discover()  - Find supported files
        2. load()      - Load documents (PDF pages, text content)
        3. split()     - Split into chunks via RecursiveCharacterTextSplitter
        4. save()      - Write chunks as .md files with YAML frontmatter
        5. process()   - Full pipeline (1-4)
    """

    # Supported file extensions
    SUPPORTED = {".pdf", ".txt", ".md", ".html", ".csv"}

    def __init__(self, chunk_size=2800, chunk_overlap=320):
        """
        Args:
            chunk_size: max characters per chunk (~700 tokens at 4 chars/token).
            chunk_overlap: overlap between consecutive chunks (~80 tokens).
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ==================================================================
    # PHASE 1 - DISCOVER
    # ==================================================================

    def discover(self, path):
        """
        Find supported files from a path (file or directory).

        Returns:
            List of absolute file paths.
        """
        path = str(path)

        # Single file
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext not in self.SUPPORTED:
                raise ValueError(
                    f"Unsupported format: {ext}. Supported: {self.SUPPORTED}"
                )
            return [os.path.abspath(path)]

        # Directory
        if os.path.isdir(path):
            files = []
            for root, _, filenames in os.walk(path):
                for fname in sorted(filenames):
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in self.SUPPORTED:
                        files.append(os.path.join(root, fname))
            if not files:
                raise FileNotFoundError(f"No supported files in {path}")
            return files

        # Try from RAG_ROOT
        test_path = str(config.RAG_ROOT / path)
        if os.path.isdir(test_path):
            return self.discover(test_path)

        raise FileNotFoundError(f"Path not found: {path}")

    # ==================================================================
    # PHASE 2 - LOAD
    # ==================================================================

    def load(self, file_paths):
        """
        Load documents from files. Uses appropriate loader per file type.

        Returns:
            List of LangChain Document objects.
        """
        all_docs = []

        for fp in file_paths:
            ext = os.path.splitext(fp)[1].lower()
            try:
                if ext == ".pdf":
                    docs = self._load_pdf(fp)
                elif ext == ".html":
                    docs = self._load_html(fp)
                elif ext == ".csv":
                    docs = self._load_csv(fp)
                else:
                    # .txt, .md
                    docs = self._load_text(fp)

                all_docs.extend(docs)
                print(f"  loaded: {Path(fp).name} ({len(docs)} pages/sections)")

            except Exception as e:
                print(f"  FAIL: {Path(fp).name} - {e}")

        print(f"Total loaded: {len(all_docs)} documents from {len(file_paths)} files")
        return all_docs

    def _load_pdf(self, path):
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(path)
        return loader.load()

    def _load_text(self, path):
        from langchain_core.documents import Document

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return [Document(page_content=content, metadata={"source": path})]

    def _load_html(self, path):
        try:
            from langchain_community.document_loaders import BSHTMLLoader

            loader = BSHTMLLoader(path)
            return loader.load()
        except ImportError:
            # Fallback to text loading
            return self._load_text(path)

    def _load_csv(self, path):
        try:
            from langchain_community.document_loaders import CSVLoader

            loader = CSVLoader(path)
            return loader.load()
        except ImportError:
            return self._load_text(path)

    # ==================================================================
    # PHASE 3 - SPLIT
    # ==================================================================

    def split(self, documents, chunk_size=None, chunk_overlap=None):
        """
        Split documents into chunks using RecursiveCharacterTextSplitter.

        Args:
            documents: list of LangChain Document objects.
            chunk_size: override default chunk_size.
            chunk_overlap: override default chunk_overlap.

        Returns:
            List of Chunk dataclass objects.
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        size = chunk_size or self.chunk_size
        overlap = chunk_overlap or self.chunk_overlap

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        split_docs = splitter.split_documents(documents)

        # Group by source to assign indices
        source_groups = {}
        for doc in split_docs:
            source = doc.metadata.get("source", "unknown")
            if source not in source_groups:
                source_groups[source] = []
            source_groups[source].append(doc)

        chunks = []
        for source, docs in source_groups.items():
            source_name = self._make_source_name(source)
            for idx, doc in enumerate(docs):
                chunk_id = f"chunk::{source_name}::{idx + 1:03d}"
                page = doc.metadata.get("page", None)

                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        content=doc.page_content,
                        source_file=source,
                        page=page,
                        chunk_index=idx,
                        total_chunks=len(docs),
                        metadata={
                            "source": source,
                            "page": page,
                            "chunk_type": "pdf-chunk"
                            if source.endswith(".pdf")
                            else "text-chunk",
                            "domain": "document",
                        },
                    )
                )

        print(
            f"Split: {len(documents)} docs -> {len(chunks)} chunks "
            f"(size={size}, overlap={overlap})"
        )
        return chunks

    @staticmethod
    def _make_source_name(source_path):
        """Create a clean name from a file path for use in chunk_id."""
        name = Path(source_path).stem
        # Clean: lowercase, replace spaces/special chars
        name = re.sub(r"[^a-z0-9_-]", "-", name.lower())
        name = re.sub(r"-+", "-", name).strip("-")
        return name[:60]  # cap length

    # ==================================================================
    # PHASE 4 - SAVE
    # ==================================================================

    def save(self, chunks, output_dir=None, domain="document", tags=None):
        """
        Save chunks as .md files with YAML frontmatter (RAG-ready).

        Args:
            chunks: list of Chunk objects.
            output_dir: where to save. Defaults to RAG/chunks/
            domain: metadata domain field.
            tags: optional list of tags.

        Returns:
            List of saved file paths.
        """
        out_dir = Path(output_dir) if output_dir else config.CHUNKS_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        saved = []
        for chunk in chunks:
            filename = f"{chunk.chunk_id.replace('::', '_')}.md"
            filepath = out_dir / filename

            frontmatter = {
                "chunk_id": chunk.chunk_id,
                "chunk_type": chunk.metadata.get("chunk_type", "text-chunk"),
                "domain": domain,
                "source": str(chunk.source_file),
                "page": chunk.page,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "created": datetime.now().strftime("%Y-%m-%d"),
            }
            if tags:
                frontmatter["tags"] = tags

            # Build YAML frontmatter
            yaml_lines = ["---"]
            for k, v in frontmatter.items():
                if v is not None:
                    if isinstance(v, list):
                        yaml_lines.append(f"{k}: [{', '.join(str(x) for x in v)}]")
                    else:
                        yaml_lines.append(f"{k}: {v}")
            yaml_lines.append("---\n")

            content = "\n".join(yaml_lines) + chunk.content

            filepath.write_text(content, encoding="utf-8")
            saved.append(str(filepath))

        print(f"Saved: {len(saved)} chunks to {out_dir}")
        return saved

    # ==================================================================
    # FULL PIPELINE
    # ==================================================================

    def process(
        self,
        path,
        output_dir=None,
        domain="document",
        tags=None,
        chunk_size=None,
        chunk_overlap=None,
    ):
        """
        Full pipeline: discover -> load -> split -> save.

        Args:
            path: file or directory path.
            output_dir: where to save chunks. Defaults to RAG/chunks/
            domain: metadata domain.
            tags: optional tags list.
            chunk_size: override chunk size.
            chunk_overlap: override overlap.

        Returns:
            dict with pipeline stats and list of saved file paths.
        """
        print(f"\n{'=' * 60}")
        print(f"CHUNKER - RecursiveCharacterTextSplitter")
        print(f"{'=' * 60}")
        print(f"Path: {path}")
        print(f"Chunk size: {chunk_size or self.chunk_size} chars")
        print(f"Overlap: {chunk_overlap or self.chunk_overlap} chars\n")

        # Phase 1
        files = self.discover(path)
        print(f"Discovered: {len(files)} file(s)")

        # Phase 2
        docs = self.load(files)
        if not docs:
            print("No documents loaded.")
            return {"files": len(files), "docs": 0, "chunks": 0, "saved": []}

        # Phase 3
        chunks = self.split(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if not chunks:
            print("No chunks generated.")
            return {"files": len(files), "docs": len(docs), "chunks": 0, "saved": []}

        # Phase 4
        saved = self.save(chunks, output_dir=output_dir, domain=domain, tags=tags)

        result = {
            "files": len(files),
            "docs": len(docs),
            "chunks": len(chunks),
            "saved": saved,
            "output_dir": str(output_dir or config.CHUNKS_DIR),
        }

        print(f"\nDone: {len(files)} files -> {len(docs)} docs -> {len(chunks)} chunks")
        return result

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"Chunker(chunk_size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}, "
            f"formats={self.SUPPORTED})"
        )
