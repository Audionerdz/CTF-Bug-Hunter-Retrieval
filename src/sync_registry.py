#!/usr/bin/env python3
"""
CLI wrapper for registry sync.
For programmatic use: from atlas_engine import RAG; r = RAG(); r.sync()
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from atlas_engine.registry import Registry


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    reg = Registry()
    reg.sync(target_dir=target_dir)


if __name__ == "__main__":
    main()
