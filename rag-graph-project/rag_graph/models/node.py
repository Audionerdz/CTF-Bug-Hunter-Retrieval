"""
Node data models for RAG-Graph

Defines node types and properties for graph construction.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


class NodeType(str, Enum):
    """Enumeration of node types in the knowledge graph"""

    # Core attack phase nodes
    ENUMERATION = "enumeration"
    FOOTHOLD = "foothold"
    POST_EXPLOITATION = "post_exploitation"
    PRIVILEGE_ESCALATION = "privilege_escalation"

    # Knowledge domain nodes
    RAG = "rag"
    PYTHON = "python"
    WEB_SECURITY = "web_security"
    LINUX_SECURITY = "linux_security"
    NETWORKING = "networking"
    WINDOWS_SECURITY = "windows_security"
    CRYPTOGRAPHY = "cryptography"
    REVERSE_ENGINEERING = "reverse_engineering"

    # Content nodes
    CHUNK = "chunk"
    TECHNIQUE = "technique"
    CONCEPT = "concept"
    EXPLOIT = "exploit"
    PROCEDURE = "procedure"
    GUIDELINE = "guideline"
    REFERENCE = "reference"


class NodeSeverity(str, Enum):
    """Severity/importance levels for nodes"""

    CRITICAL = "critical"  # Core to attack chain
    HIGH = "high"  # Important technique
    MEDIUM = "medium"  # Useful but optional
    LOW = "low"  # Supporting information


@dataclass
class GraphMetadata:
    """Graph-specific metadata for chunks"""

    attack_phase: Optional[str] = None
    relevance_to_phases: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    htb_related: bool = False
    cve_id: Optional[str] = None


@dataclass
class Node:
    """Represents a node in the knowledge graph"""

    node_id: str
    node_type: NodeType
    label: str
    description: Optional[str] = None

    # Metadata
    severity: NodeSeverity = NodeSeverity.MEDIUM
    confidence: float = 1.0  # 0.0 to 1.0

    # Source information
    source_chunk_id: Optional[str] = None  # If derived from chunk
    source_path: Optional[str] = None  # Path to source markdown

    # Graph metadata
    graph_metadata: Optional[GraphMetadata] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Custom properties
    properties: Dict[str, Any] = field(default_factory=dict)

    # Visual properties
    color: Optional[str] = None
    icon: Optional[str] = None
    size: float = 1.0

    def __post_init__(self):
        """Validate node after initialization"""
        if not self.node_id:
            raise ValueError("node_id cannot be empty")
        if not self.label:
            raise ValueError("label cannot be empty")

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary"""
        return {
            "id": self.node_id,
            "type": self.node_type.value,
            "label": self.label,
            "description": self.description,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "source_chunk_id": self.source_chunk_id,
            "source_path": self.source_path,
            "properties": self.properties,
            "color": self.color,
            "icon": self.icon,
            "size": self.size,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Create node from dictionary"""
        # Parse nested objects
        if isinstance(data.get("graph_metadata"), dict):
            graph_metadata = GraphMetadata(**data["graph_metadata"])
        else:
            graph_metadata = None

        return cls(
            node_id=data["id"],
            node_type=NodeType(data["type"]),
            label=data["label"],
            description=data.get("description"),
            severity=NodeSeverity(data.get("severity", "medium")),
            confidence=data.get("confidence", 1.0),
            source_chunk_id=data.get("source_chunk_id"),
            source_path=data.get("source_path"),
            graph_metadata=graph_metadata,
            properties=data.get("properties", {}),
            color=data.get("color"),
            icon=data.get("icon"),
            size=data.get("size", 1.0),
        )


@dataclass
class NodeCollection:
    """Container for managing multiple nodes"""

    nodes: Dict[str, Node] = field(default_factory=dict)

    def add(self, node: Node) -> None:
        """Add node to collection"""
        self.nodes[node.node_id] = node

    def get(self, node_id: str) -> Optional[Node]:
        """Get node by ID"""
        return self.nodes.get(node_id)

    def remove(self, node_id: str) -> bool:
        """Remove node from collection"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False

    def get_by_type(self, node_type: NodeType) -> List[Node]:
        """Get all nodes of a specific type"""
        return [n for n in self.nodes.values() if n.node_type == node_type]

    def count(self) -> int:
        """Get total number of nodes"""
        return len(self.nodes)

    def to_list(self) -> List[Dict[str, Any]]:
        """Convert all nodes to list of dictionaries"""
        return [node.to_dict() for node in self.nodes.values()]
