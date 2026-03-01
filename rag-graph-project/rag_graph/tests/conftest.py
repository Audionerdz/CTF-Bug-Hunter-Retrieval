"""
Pytest configuration and fixtures for RAG-Graph tests
"""

import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
