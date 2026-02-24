"""
Registry - Manages chunk_registry.json mapping chunk_ids to file paths.

Handles sync between filesystem and registry, lookups, and content extraction.
"""

import json
import re
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class Registry:
    """Manages the chunk registry that maps chunk_ids to local file paths."""

    def __init__(self, registry_path=None):
        self.path = Path(registry_path) if registry_path else config.CHUNK_REGISTRY
        self._data = {}
        self._load()

    def _load(self):
        """Load registry from disk."""
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}

    def _save(self):
        """Persist registry to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(dict(sorted(self._data.items())), f, indent=2)

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get(self, chunk_id):
        """Get file path for a chunk_id. Returns None if not found."""
        return self._data.get(chunk_id)

    def get_content(self, chunk_id):
        """Read chunk body (without frontmatter) from filesystem."""
        file_path = self.get(chunk_id)
        if not file_path or not Path(file_path).exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content
        except Exception:
            return None

    def list(self):
        """Return all chunk_ids."""
        return list(self._data.keys())

    def count(self):
        """Number of registered chunks."""
        return len(self._data)

    def __contains__(self, chunk_id):
        return chunk_id in self._data

    def __len__(self):
        return len(self._data)

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add(self, chunk_id, file_path):
        """Register a single chunk."""
        self._data[chunk_id] = str(file_path)

    def add_many(self, mapping):
        """Merge a dict of {chunk_id: file_path} into the registry."""
        self._data.update(mapping)

    def remove(self, chunk_id):
        """Remove a chunk from the registry."""
        self._data.pop(chunk_id, None)

    def save(self):
        """Persist changes to disk."""
        self._save()

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_chunk_id(file_path):
        """Extract chunk_id from YAML frontmatter."""
        for encoding in ["utf-8", "latin-1", "iso-8859-1"]:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return None

        match = re.search(r"chunk_id:\s*(.+?)(?:\n|$)", content)
        return match.group(1).strip() if match else None

    def sync(self, target_dir=None, verbose=True):
        """
        Rebuild registry from filesystem .md files.
        Returns (valid_count, missing_count).
        """
        target = Path(target_dir) if target_dir else config.DEFAULT_CHUNKS_DIR

        if not target.exists():
            if verbose:
                print(f"Directory not found: {target}")
            return 0, 0

        new_registry = {}
        skipped = 0

        for md_file in sorted(target.rglob("*.md")):
            chunk_id = self._extract_chunk_id(md_file)
            if chunk_id:
                new_registry[chunk_id] = str(md_file)
            else:
                skipped += 1
                if verbose:
                    print(f"  skip (no chunk_id): {md_file.name}")

        # Validate all paths exist
        valid = {k: v for k, v in new_registry.items() if Path(v).exists()}
        missing = len(new_registry) - len(valid)

        self._data = valid
        self._save()

        if verbose:
            print(
                f"Registry synced: {len(valid)} chunks ({missing} missing, {skipped} skipped)"
            )

        return len(valid), missing

    def build_from_files(self, chunk_files):
        """
        Build registry entries from a list of file paths.
        Returns dict of {chunk_id: file_path}.
        """
        mapping = {}
        for f in chunk_files:
            chunk_id = self._extract_chunk_id(f)
            if chunk_id:
                mapping[chunk_id] = str(f)
        return mapping

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        return f"Registry({len(self._data)} chunks, path={self.path})"

    def info(self):
        """Print registry summary."""
        print(f"Registry: {self.path}")
        print(f"  Chunks: {len(self._data)}")
        if self._data:
            sample = list(self._data.keys())[:5]
            for cid in sample:
                print(f"    - {cid}")
            if len(self._data) > 5:
                print(f"    ... and {len(self._data) - 5} more")
