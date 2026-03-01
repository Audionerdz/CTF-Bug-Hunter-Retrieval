"""
Metadata structures for RAG-Graph

Handles chunk metadata and graph-specific annotations.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
import yaml


@dataclass
class ChunkMetadata:
    """Metadata extracted from chunk YAML frontmatter"""

    chunk_id: str
    domain: str
    chunk_type: str
    confidence: Optional[str] = None
    reuse_level: Optional[str] = None
    source: Optional[str] = None
    creator: Optional[str] = None

    # Raw frontmatter
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "chunk_id": self.chunk_id,
            "domain": self.domain,
            "chunk_type": self.chunk_type,
            "confidence": self.confidence,
            "reuse_level": self.reuse_level,
            "source": self.source,
            "creator": self.creator,
        }

    @classmethod
    def from_yaml_dict(cls, data: Dict[str, Any]) -> "ChunkMetadata":
        """Create from YAML frontmatter dictionary"""
        return cls(
            chunk_id=data.get("chunk_id", ""),
            domain=data.get("domain", "unknown"),
            chunk_type=data.get("chunk_type", "chunk"),
            confidence=data.get("confidence"),
            reuse_level=data.get("reuse_level"),
            source=data.get("source"),
            creator=data.get("creator"),
            raw=data,
        )


@dataclass
class GraphMetadataExtension:
    """
    Optional graph metadata for chunks (in HTB/CTF contexts).

    This extends the base chunk metadata with graph-specific annotations
    without modifying the original chunk structure.
    """

    # Node relationships
    primary_nodes: List[str] = field(default_factory=list)
    secondary_nodes: List[str] = field(default_factory=list)

    # Edge information
    edges: List[Dict[str, Any]] = field(default_factory=list)

    # Attack phase information
    attack_phase: Optional[str] = None
    phase_relevance: Dict[str, float] = field(default_factory=dict)

    # Categorization
    tags: List[str] = field(default_factory=list)
    difficulty: Optional[str] = None  # easy, medium, hard, insane

    # CTF-specific
    htb_machine: Optional[str] = None
    cve_ids: List[str] = field(default_factory=list)

    # Relations to other chunks
    related_chunks: List[str] = field(default_factory=list)
    prerequisite_chunks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "primary_nodes": self.primary_nodes,
            "secondary_nodes": self.secondary_nodes,
            "edges": self.edges,
            "attack_phase": self.attack_phase,
            "phase_relevance": self.phase_relevance,
            "tags": self.tags,
            "difficulty": self.difficulty,
            "htb_machine": self.htb_machine,
            "cve_ids": self.cve_ids,
            "related_chunks": self.related_chunks,
            "prerequisite_chunks": self.prerequisite_chunks,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphMetadataExtension":
        """Create from dictionary"""
        return cls(
            primary_nodes=data.get("primary_nodes", []),
            secondary_nodes=data.get("secondary_nodes", []),
            edges=data.get("edges", []),
            attack_phase=data.get("attack_phase"),
            phase_relevance=data.get("phase_relevance", {}),
            tags=data.get("tags", []),
            difficulty=data.get("difficulty"),
            htb_machine=data.get("htb_machine"),
            cve_ids=data.get("cve_ids", []),
            related_chunks=data.get("related_chunks", []),
            prerequisite_chunks=data.get("prerequisite_chunks", []),
        )


class ChunkParser:
    """Utility for parsing chunk files and extracting metadata"""

    @staticmethod
    def parse_chunk(file_path: Path) -> tuple[Optional[ChunkMetadata], Optional[str]]:
        """
        Parse a markdown chunk file and extract YAML frontmatter.

        Returns:
            Tuple of (ChunkMetadata, content) or (None, None) if parsing fails
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML frontmatter
            if not content.startswith("---"):
                return None, content

            # Find end of frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                return None, content

            frontmatter_str = parts[1]
            markdown_content = parts[2].strip()

            # Parse YAML
            try:
                frontmatter = yaml.safe_load(frontmatter_str) or {}
            except yaml.YAMLError:
                return None, content

            metadata = ChunkMetadata.from_yaml_dict(frontmatter)
            return metadata, markdown_content

        except (IOError, OSError) as e:
            print(f"Error reading chunk file {file_path}: {e}")
            return None, None

    @staticmethod
    def extract_chunk_id_from_path(file_path: Path) -> Optional[str]:
        """
        Extract chunk_id from file path pattern.

        Examples:
            default/web/lua-rce/sandbox-escape_001.md
            -> technique::web::lua-rce::sandbox-escape::001
        """
        try:
            # Get relative path from default/
            relative = file_path.relative_to(file_path.parent.parent)

            # Extract parts
            parts = list(relative.parts)
            if not parts:
                return None

            # Last part is filename like "sandbox-escape_001.md"
            filename = parts[-1].replace(".md", "")

            if "_" not in filename:
                return None

            name, sequence = filename.rsplit("_", 1)

            # Reconstruct chunk_id: type::domain::category::name::sequence
            # For now, we'll use a simpler format
            return f"chunk::{':'.join(parts[:-1])}::{name}::{sequence}"

        except (ValueError, IndexError):
            return None
