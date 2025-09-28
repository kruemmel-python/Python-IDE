"""Utilities for locating the Python executable used by the IDE."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def _embedded_candidates(base_dir: Path) -> list[Path]:
    """Return potential executable locations for an embedded Python runtime."""
    candidates: list[Path] = []
    if sys.platform.startswith("win"):
        candidates.append(base_dir / "python_embedded" / "python.exe")
    else:
        candidates.extend(
            [
                base_dir / "python_embedded" / "python",
                base_dir / "python_embedded" / "bin" / "python3",
            ]
        )
    return candidates


def get_python_executable() -> str:
    """Return the path to the preferred Python interpreter.

    The function first looks for an embedded interpreter shipped with the IDE
    and falls back to the interpreter running the application.  The behaviour is
    logged so that issues can be diagnosed easily by end users.
    """

    base_dir = Path(__file__).resolve().parent
    for candidate in _embedded_candidates(base_dir):
        if candidate.exists():
            LOGGER.debug("Using embedded Python interpreter at %s", candidate)
            return os.fspath(candidate)

    LOGGER.info("Embedded Python not found. Falling back to system interpreter")
    return sys.executable
