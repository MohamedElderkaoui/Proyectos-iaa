"""Find the newest local AccessAI checkpoint for the four-class prototype."""

from __future__ import annotations

import os
from pathlib import Path


def _checkpoint_roots(
    project_root: Path,
    home_dir: Path,
    extra_roots: list[Path] | None = None,
) -> list[Path]:
    roots = [
        project_root / "runs" / "detect",
        home_dir / "runs" / "detect",
        *(Path(item) for item in os.environ.get("ACCESSAI_MODEL_SEARCH_PATHS", "").split(os.pathsep) if item),
        *(extra_roots or []),
    ]

    unique_roots: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        resolved = root.expanduser().resolve()
        key = str(resolved).casefold()
        if key not in seen:
            unique_roots.append(resolved)
            seen.add(key)
    return unique_roots


def find_latest_four_class_checkpoint(
    project_root: Path,
    home_dir: Path,
    extra_roots: list[Path] | None = None,
) -> Path | None:
    """Return the newest AccessAI ``best.pt`` marked as a four-class run."""
    candidates: set[Path] = set()
    for root in _checkpoint_roots(project_root, home_dir, extra_roots):
        if not root.is_dir():
            continue
        try:
            for checkpoint in root.rglob("best.pt"):
                path_parts = [part.casefold() for part in checkpoint.parts]
                if (
                    checkpoint.parent.name.casefold() == "weights"
                    and any("accessai" in part for part in path_parts)
                    and any(
                        "4clases" in part.replace("_", "").replace("-", "")
                        for part in path_parts
                    )
                    and checkpoint.is_file()
                ):
                    candidates.add(checkpoint.resolve())
        except OSError:
            # A missing or inaccessible model-search directory should not stop
            # the application from checking the remaining roots.
            continue

    if not candidates:
        return None

    return max(candidates, key=lambda path: path.stat().st_mtime)
