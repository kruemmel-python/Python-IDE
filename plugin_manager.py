"""Plugin infrastructure for the Python IDE."""
from __future__ import annotations

import importlib.util
import inspect
import logging
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, Optional

from plugin_interface import PluginInterface

LOGGER = logging.getLogger(__name__)


@dataclass
class _PluginEntry:
    name: str
    module: ModuleType
    instance: PluginInterface
    register: Optional[Callable[[PluginInterface], None]]


class PluginManager:
    def __init__(self, ide):
        self.ide = ide
        self.plugins: Dict[str, _PluginEntry] = {}
        self.active_plugins: set[str] = set()

    def load_plugins(self, plugin_directory: str = "plugins") -> None:
        plugin_dir = Path(plugin_directory)
        plugin_dir.mkdir(exist_ok=True)
        LOGGER.debug("Loading plugins from %s", plugin_dir)

        for plugin_file in plugin_dir.iterdir():
            if plugin_file.suffix != ".py" or plugin_file.name.startswith("__"):
                LOGGER.debug("Skipping non-plugin file %s", plugin_file)
                continue

            try:
                entry = self._load_plugin_file(plugin_file)
            except Exception as exc:  # pragma: no cover - defensive logging
                LOGGER.exception("Failed to load plugin %s", plugin_file.name, exc_info=exc)
                continue

            if entry:
                self.plugins[entry.name] = entry
                LOGGER.info("Plugin %s loaded from %s", entry.name, plugin_file)

    def _load_plugin_file(self, plugin_file: Path) -> Optional[_PluginEntry]:
        spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
        if not spec or not spec.loader:
            raise ImportError(f"Unable to create module spec for {plugin_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        register_hook = self._resolve_register(module)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type)
                and issubclass(attribute, PluginInterface)
                and attribute is not PluginInterface
            ):
                plugin_instance = attribute(self.ide)
                if not register_hook and not callable(getattr(plugin_instance, "register", None)):
                    LOGGER.warning("Plugin %s does not implement register()", attribute_name)
                return _PluginEntry(
                    name=attribute_name,
                    module=module,
                    instance=plugin_instance,
                    register=register_hook,
                )

        LOGGER.warning("No PluginInterface implementation found in %s", plugin_file)
        return None

    def _resolve_register(self, module: ModuleType) -> Optional[Callable[[PluginInterface], None]]:
        module_register = getattr(module, "register", None)
        if callable(module_register):
            LOGGER.debug("Using module-level register() in %s", module.__name__)
            signature = inspect.signature(module_register)
            parameter_count = len(signature.parameters)

            def hook(plugin_instance: PluginInterface) -> None:
                try:
                    if parameter_count >= 2:
                        module_register(self.ide, plugin_instance)  # type: ignore[arg-type]
                    elif parameter_count == 1:
                        module_register(plugin_instance)
                    else:
                        module_register()
                except TypeError:
                    module_register(plugin_instance)

            return hook

        LOGGER.debug("No module-level register() in %s", module.__name__)
        return None

    def initialize_plugin(self, plugin_name: str) -> None:
        entry = self.plugins.get(plugin_name)
        if not entry or plugin_name in self.active_plugins:
            return

        try:
            if entry.register:
                entry.register(entry.instance)
            elif callable(getattr(entry.instance, "register", None)):
                entry.instance.register()  # type: ignore[call-arg]
            entry.instance.initialize()
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Failed to initialise plugin %s", plugin_name, exc_info=exc)
            return

        self.active_plugins.add(plugin_name)
        LOGGER.info("Plugin %s initialised", plugin_name)

    def deinitialize_plugin(self, plugin_name: str) -> None:
        entry = self.plugins.get(plugin_name)
        if not entry or plugin_name not in self.active_plugins:
            return

        try:
            entry.instance.deinitialize()
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Failed to deinitialise plugin %s", plugin_name, exc_info=exc)
            return

        self.active_plugins.remove(plugin_name)
        LOGGER.info("Plugin %s deinitialised", plugin_name)

    def toggle_plugin(self, plugin_name: str) -> None:
        if plugin_name in self.active_plugins:
            self.deinitialize_plugin(plugin_name)
        else:
            self.initialize_plugin(plugin_name)

    def get_plugins(self):
        return list(self.plugins.items())

    def is_plugin_active(self, plugin_name: str) -> bool:
        return plugin_name in self.active_plugins
