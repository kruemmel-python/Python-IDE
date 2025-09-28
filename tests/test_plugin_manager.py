from types import SimpleNamespace

from plugin_manager import PluginManager


def create_plugin(path, content):
    path.write_text(content, encoding="utf-8")
    return path


def test_plugin_loader_handles_valid_and_invalid_plugins(tmp_path, caplog):
    valid_plugin = tmp_path / "valid_plugin.py"
    create_plugin(
        valid_plugin,
        """
from plugin_interface import PluginInterface

def register(ide, plugin):
    ide.hooks.append("registered")

class SamplePlugin(PluginInterface):
    def initialize(self):
        self.ide.hooks.append("initialized")

    def deinitialize(self):
        self.ide.hooks.append("deinitialized")
""",
    )

    broken_plugin = tmp_path / "broken_plugin.py"
    create_plugin(broken_plugin, "raise RuntimeError('broken')\n")

    ide = SimpleNamespace(hooks=[])
    manager = PluginManager(ide)

    with caplog.at_level("WARNING"):
        manager.load_plugins(str(tmp_path))

    assert "SamplePlugin" in manager.plugins
    assert any("Failed to load plugin" in record.message for record in caplog.records)

    manager.initialize_plugin("SamplePlugin")
    assert ide.hooks[:2] == ["registered", "initialized"]

    manager.deinitialize_plugin("SamplePlugin")
    assert ide.hooks[-1] == "deinitialized"


def test_plugin_loader_skips_non_python_files(tmp_path):
    non_py = tmp_path / "README.txt"
    non_py.write_text("noop", encoding="utf-8")

    ide = SimpleNamespace(hooks=[])
    manager = PluginManager(ide)
    manager.load_plugins(str(tmp_path))

    assert not manager.plugins
