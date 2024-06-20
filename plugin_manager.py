import os
import importlib.util
from pathlib import Path
import logging
from plugin_interface import PluginInterface

class PluginManager:
    def __init__(self, ide):
        self.ide = ide
        self.plugins = {}
        self.active_plugins = set()

    def load_plugins(self, plugin_directory='plugins'):
        plugin_dir = Path(plugin_directory)
        if not plugin_dir.exists():
            plugin_dir.mkdir()

        for plugin_file in plugin_dir.glob('*.py'):
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, PluginInterface) and attribute is not PluginInterface:
                        self.plugins[attribute_name] = attribute(self.ide)
                        logging.info(f"Plugin {attribute_name} loaded from {plugin_file}")

    def initialize_plugin(self, plugin_name):
        plugin = self.plugins.get(plugin_name)
        if plugin and plugin_name not in self.active_plugins:
            plugin.initialize()
            self.active_plugins.add(plugin_name)
            logging.info(f"Plugin {plugin_name} initialized")

    def deinitialize_plugin(self, plugin_name):
        plugin = self.plugins.get(plugin_name)
        if plugin and plugin_name in self.active_plugins:
            plugin.deinitialize()
            self.active_plugins.remove(plugin_name)
            logging.info(f"Plugin {plugin_name} deinitialized")

    def toggle_plugin(self, plugin_name):
        if plugin_name in self.active_plugins:
            self.deinitialize_plugin(plugin_name)
        else:
            self.initialize_plugin(plugin_name)

    def get_plugins(self):
        return list(self.plugins.items())

    def is_plugin_active(self, plugin_name):
        return plugin_name in self.active_plugins
