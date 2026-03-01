"""
Edge data models for RAG-Graph

Defines edge types and properties for graph connections.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


class EdgeType(str, Enum):
    """Enumeration of edge types in the knowledge graph"""

    # Semantic relationships
    PREREQUISITE = "prerequisite"  # Requires knowledge of
    ENABLES = "enables"  # Allows performing
    IMPLEMENTS = "implements"  # Implements concept
    REFERENCES = "references"  # Cites/references
    RELATED_TO = "related_to"  # Related concept
    EXPLOITS = "exploits"  # Exploits vulnerability

    # Attack chain relationships
    LEADS_TO = "leads_to"  # Conduces to next phase
    PART_OF = "part_of"  # Part of procedure
    DEPENDS_ON = "depends_on"  # Depends on knowledge

    # Domain relationships
    EXTENDS = "extends"  # Extends concept
    CONTRADICTS = "contradicts"  # Contradicts other
    SIMILAR_TO = "similar_to"  # Similar approach


class EdgeDirection(str, Enum):
    """Direction of edge relationships"""

    DIRECTED = "directed"
    UNDIRECTED = "undirected"


@dataclass
class Edge:
    """Represents an edge/relationship in the knowledge graph"""

    edge_id: str
    source_id: str
    target_id: str
    edge_type: EdgeType

    # Edge properties
    label: Optional[str] = None
    description: Optional[str] = None
    weight: float = 1.0  # 0.0 to 1.0, higher = stronger relationship
    direction: EdgeDirection = EdgeDirection.DIRECTED

    # Metadata
    confidence: float = 1.0  # 0.0 to 1.0
    source_chunk_id: Optional[str] = None  # If derived from chunk

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Custom properties
    properties: Dict[str, Any] = field(default_factory=dict)

    # Visual properties
    color: Optional[str] = None
    style: str = "solid"  # solid, dashed, dotted

    def __post_init__(self):
        """Validate edge after initialization"""
        if not self.edge_id:
            raise ValueError("edge_id cannot be empty")
        if not self.source_id or not self.target_id:
            raise ValueError("source_id and target_id cannot be empty")
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError("weight must be between 0.0 and 1.0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary"""
        return {
            "id": self.edge_id,
            "source": self.source_id,
            "target": self.target_id,
            "type": self.edge_type.value,
            "label": self.label,
            "description": self.description,
            "weight": self.weight,
            "direction": self.direction.value,
            "confidence": self.confidence,
            "source_chunk_id": self.source_chunk_id,
            "properties": self.properties,
            "color": self.color,
            "style": self.style,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        """Create edge from dictionary"""
        return cls(
            edge_id=data["id"],
            source_id=data["source"],
            target_id=data["target"],
            edge_type=EdgeType(data["type"]),
            label=data.get("label"),
            description=data.get("description"),
            weight=data.get("weight", 1.0),
            direction=EdgeDirection(data.get("direction", "directed")),
            confidence=data.get("confidence", 1.0),
            source_chunk_id=data.get("source_chunk_id"),
            properties=data.get("properties", {}),
            color=data.get("color"),
            style=data.get("style", "solid"),
        )


@dataclass
class EdgeCollection:
    """Container for managing multiple edges"""

    edges: Dict[str, Edge] = field(default_factory=dict)

    def add(self, edge: Edge) -> None:
        """Add edge to collection"""
        self.edges[edge.edge_id] = edge

    def get(self, edge_id: str) -> Optional[Edge]:
        """Get edge by ID"""
        return self.edges.get(edge_id)

    def remove(self, edge_id: str) -> bool:
        """Remove edge from collection"""
        if edge_id in self.edges:
            del self.edges[edge_id]
            return True
        return False

    def get_by_source(self, source_id: str) -> list["Edge"]:
        """Get all edges from a source node"""
        return [e for e in self.edges.values() if e.source_id == source_id]

    def get_by_target(self, target_id: str) -> list["Edge"]:
        """Get all edges to a target node"""
        return [e for e in self.edges.values() if e.target_id == target_id]

    def get_by_type(self, edge_type: EdgeType) -> list["Edge"]:
        """Get all edges of a specific type"""
        return [e for e in self.edges.values() if e.edge_type == edge_type]

    def get_neighbors(self, node_id: str) -> Dict[str, list["Edge"]]:
        """Get incoming and outgoing edges for a node"""
        return {
            "outgoing": self.get_by_source(node_id),
            "incoming": self.get_by_target(node_id),
        }

    def count(self) -> int:
        """Get total number of edges"""
        return len(self.edges)

    def to_list(self) -> list[Dict[str, Any]]:
        """Convert all edges to list of dictionaries"""
        return [edge.to_dict() for edge in self.edges.values()]
