"""
FastAPI server for RAG-Graph REST API

Provides endpoints for querying and manipulating the knowledge graph.
"""

import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from rag_graph.builders.graph_builder import GraphBuilder

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG-Graph API",
    description="Knowledge visualization and querying API for RAG chunks",
    version="0.1.0",
)

# Global graph builder instance
graph_builder: Optional[GraphBuilder] = None


class GraphStats(BaseModel):
    """Graph statistics response"""

    total_nodes: int
    total_edges: int
    processed_chunks: int


class NodeResponse(BaseModel):
    """Single node response"""

    id: str
    type: str
    label: str
    description: Optional[str] = None
    severity: str = "medium"
    confidence: float = 1.0


class EdgeResponse(BaseModel):
    """Single edge response"""

    id: str
    source: str
    target: str
    type: str
    weight: float = 1.0
    label: Optional[str] = None


class GraphResponse(BaseModel):
    """Complete graph response"""

    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    stats: Dict[str, int]


@app.on_event("startup")
async def startup_event():
    """Initialize graph on startup"""
    global graph_builder
    logger.info("Starting RAG-Graph API server...")

    try:
        chunks_dir = Path(__file__).parent.parent.parent / "default"
        graph_builder = GraphBuilder(chunks_dir=chunks_dir)

        if graph_builder.build_graph(include_core_topics=True):
            logger.info("Graph built successfully")
        else:
            logger.warning("Graph build reported issues, but continuing")

    except Exception as e:
        logger.error(f"Failed to initialize graph: {e}", exc_info=True)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rag-graph-api",
        "version": "0.1.0",
    }


@app.get("/api/graph", response_model=GraphResponse, tags=["Graph"])
async def get_graph():
    """Get the complete knowledge graph"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    return GraphResponse(
        nodes=graph_builder.nodes.to_list(),
        edges=graph_builder.edges.to_list(),
        stats=graph_builder.get_stats(),
    )


@app.get("/api/graph/stats", response_model=GraphStats, tags=["Graph"])
async def get_stats():
    """Get graph statistics"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    stats = graph_builder.get_stats()
    return GraphStats(**stats)


@app.get("/api/graph/nodes", tags=["Nodes"])
async def list_nodes():
    """List all nodes in the graph"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    return {
        "total": graph_builder.nodes.count(),
        "nodes": graph_builder.nodes.to_list(),
    }


@app.get("/api/graph/edges", tags=["Edges"])
async def list_edges():
    """List all edges in the graph"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    return {
        "total": graph_builder.edges.count(),
        "edges": graph_builder.edges.to_list(),
    }


@app.get("/api/node/{node_id}", tags=["Nodes"])
async def get_node(node_id: str):
    """Get a specific node"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    node = graph_builder.nodes.get(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node not found: {node_id}")

    return node.to_dict()


@app.get("/api/node/{node_id}/neighbors", tags=["Nodes"])
async def get_neighbors(node_id: str):
    """Get incoming and outgoing edges for a node"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    # Verify node exists
    if graph_builder.nodes.get(node_id) is None:
        raise HTTPException(status_code=404, detail=f"Node not found: {node_id}")

    neighbors = graph_builder.edges.get_neighbors(node_id)

    return {
        "node_id": node_id,
        "outgoing": [e.to_dict() for e in neighbors["outgoing"]],
        "incoming": [e.to_dict() for e in neighbors["incoming"]],
    }


@app.post("/api/graph/rebuild", tags=["Graph"])
async def rebuild_graph():
    """Rebuild the graph from chunks"""
    global graph_builder

    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph builder not initialized")

    try:
        # Reset graph
        graph_builder = GraphBuilder(chunks_dir=graph_builder.chunks_dir)

        # Rebuild
        success = graph_builder.build_graph(include_core_topics=True)

        if not success:
            raise HTTPException(status_code=500, detail="Graph rebuild failed")

        return {
            "status": "success",
            "stats": graph_builder.get_stats(),
        }

    except Exception as e:
        logger.error(f"Error rebuilding graph: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Rebuild error: {str(e)}")


@app.get("/api/node/{node_id}/type/{node_type}", tags=["Nodes"])
async def get_nodes_by_type(node_type: str):
    """Get all nodes of a specific type"""
    if graph_builder is None:
        raise HTTPException(status_code=503, detail="Graph not initialized")

    try:
        from rag_graph.models.node import NodeType

        node_type_enum = NodeType(node_type)
        nodes = graph_builder.nodes.get_by_type(node_type_enum)

        return {
            "type": node_type,
            "total": len(nodes),
            "nodes": [n.to_dict() for n in nodes],
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown node type: {node_type}")


def run_server(host: str = "0.0.0.0", port: int = 8001, reload: bool = False):
    """Run the API server"""
    import uvicorn

    uvicorn.run(
        "rag_graph.api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    run_server()
