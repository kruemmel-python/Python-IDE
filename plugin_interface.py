"""Base interface for IDE plugins."""
from __future__ import annotations

from typing import Any


class PluginInterface:
    def __init__(self, ide: Any):
        self.ide = ide

    def register(self) -> None:
        """Optional hook invoked before :meth:`initialize` if available."""

    def initialize(self) -> None:
        raise NotImplementedError("Plugins must implement the initialize method")

    def deinitialize(self) -> None:
        raise NotImplementedError("Plugins must implement the deinitialize method")
