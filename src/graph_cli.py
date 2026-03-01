#!/usr/bin/env python3
"""
GraphRAG CLI Tool - Build and visualize knowledge graphs
========================================================

Usage:
  graph_cli.py build [--namespace NAMESPACE] [--output OUTPUT.html]
  graph_cli.py plot OUTPUT.html
  graph_cli.py stats [--namespace NAMESPACE]
"""

import sys
import os
import json
import webbrowser
from pathlib import Path
from typing import Optional

# Add parent directory to path for Atlas imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from atlas_engine.graph import SemanticGraph, build_graph_from_registry


def build_graph_command(namespace: str = "default", output: str = "graph.html") -> int:
    """Build a graph from the chunk registry."""
    registry_path = Path(__file__).parent.parent / "chunk_registry.json"

    if not registry_path.exists():
        print(f"❌ Registry not found: {registry_path}")
        return 1

    print(f"📊 Building graph for namespace: {namespace}")
    print(f"   Loading: {registry_path}")

    try:
        with open(registry_path) as f:
            registry = json.load(f)

        # Handle both list and dict formats
        if isinstance(registry, dict):
            chunks = list(registry.values()) if registry else []
        else:
            chunks = registry if isinstance(registry, list) else []

        # Filter by namespace if specified
        if namespace != "default":
            chunks = [c for c in chunks if c.get("namespace") == namespace]

        if not chunks:
            print(f"⚠️  No chunks found for namespace: {namespace}")
            return 1

        print(f"   Found {len(chunks)} chunks")

        # Build graph
        graph = SemanticGraph(namespace=namespace)
        graph.build_from_chunks(chunks)

        stats = graph.stats()
        print(f"\n✓ Graph built:")
        print(f"   Nodes: {stats['nodes']}")
        print(f"   Edges: {stats['edges']}")
        print(f"   Density: {stats['density']:.3f}")

        # Export
        html_path = graph.export_html(output)
        print(f"\n✓ Exported: {html_path}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


def plot_command(html_path: str) -> int:
    """Open the graph HTML file in a browser."""
    path = Path(html_path)

    if not path.exists():
        print(f"❌ File not found: {html_path}")
        return 1

    print(f"🌐 Opening: {html_path}")
    try:
        webbrowser.open(f"file://{path.resolve()}")
        print(f"✓ Opened in browser")
        return 0
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print(f"   Open manually: file://{path.resolve()}")
        return 0


def stats_command(namespace: str = "default") -> int:
    """Show graph statistics without building HTML."""
    registry_path = Path(__file__).parent.parent / "chunk_registry.json"

    if not registry_path.exists():
        print(f"❌ Registry not found: {registry_path}")
        return 1

    try:
        with open(registry_path) as f:
            registry = json.load(f)

        # Handle both list and dict formats
        if isinstance(registry, dict):
            chunks = list(registry.values()) if registry else []
        else:
            chunks = registry if isinstance(registry, list) else []

        # Filter by namespace
        if namespace != "default":
            chunks = [c for c in chunks if c.get("namespace") == namespace]

        if not chunks:
            print(f"⚠️  No chunks found for namespace: {namespace}")
            return 1

        # Build graph
        graph = SemanticGraph(namespace=namespace)
        graph.build_from_chunks(chunks)

        stats = graph.stats()
        print(f"📊 Graph Statistics for '{namespace}':")
        print(f"   Nodes: {stats['nodes']}")
        print(f"   Edges: {stats['edges']}")
        print(f"   Density: {stats['density']:.3f}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def main():
    """Parse CLI arguments and dispatch commands."""
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command = sys.argv[1].lower()

    if command == "build":
        namespace = "default"
        output = "graph.html"

        # Parse optional args
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--namespace" and i + 1 < len(sys.argv):
                namespace = sys.argv[i + 1]
            elif arg == "--output" and i + 1 < len(sys.argv):
                output = sys.argv[i + 1]

        return build_graph_command(namespace=namespace, output=output)

    elif command == "plot":
        if len(sys.argv) < 3:
            print("Usage: graph_cli.py plot <html_path>")
            return 1
        return plot_command(sys.argv[2])

    elif command == "stats":
        namespace = "default"
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--namespace" and i + 1 < len(sys.argv):
                namespace = sys.argv[i + 1]
        return stats_command(namespace=namespace)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
