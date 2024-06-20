# unit_test_plugin.py
from plugin_interface import PluginInterface
from PyQt5.QtWidgets import QAction
import subprocess

class UnitTestPlugin(PluginInterface):
    def initialize(self):
        self.action = QAction('Unit Tests ausführen', self.ide)
        self.action.triggered.connect(self.run_unit_tests)
        self.ide.add_action_to_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Unit Test Plugin geladen")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Unit Test Plugin entladen")

    def run_unit_tests(self):
        self.ide.console_output.appendPlainText("Unit Tests werden ausgeführt...")
        try:
            result = subprocess.run([self.ide.embedded_python_path, '-m', 'unittest', 'discover'], cwd=self.ide.project_dir, capture_output=True, text=True)
            self.ide.console_output.appendPlainText(result.stdout)
            self.ide.console_output.appendPlainText(result.stderr)
        except Exception as e:
            self.ide.console_output.appendPlainText(f"Fehler beim Ausführen der Unit-Tests: {str(e)}") 