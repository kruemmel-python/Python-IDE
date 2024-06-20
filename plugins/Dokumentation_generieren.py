import subprocess
import os
from PyQt5.QtWidgets import QAction
from plugin_interface import PluginInterface

class DocumentationGeneratorPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.action = QAction("Dokumentation generieren", self.ide)
        self.action.triggered.connect(self.generate_docs)
    
    def initialize(self):
        self.ide.add_action_to_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Documentation Generator Plugin aktiviert.")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Documentation Generator Plugin deaktiviert.")
    
    def generate_docs(self):
        self.ide.console_output.appendPlainText("Dokumentation wird generiert...")

        sphinx_apidoc_cmd = os.path.join(self.ide.embedded_python_path, 'Scripts', 'sphinx-apidoc.exe')
        if not os.path.exists(sphinx_apidoc_cmd):
            sphinx_apidoc_cmd = 'sphinx-apidoc'  # Fallback to the system sphinx-apidoc

        try:
            result = subprocess.run([sphinx_apidoc_cmd, '-o', 'docs', self.ide.project_dir], capture_output=True, text=True)
            self.ide.console_output.appendPlainText(result.stdout)
            self.ide.console_output.appendPlainText(result.stderr)

            make_cmd = 'make.bat' if os.name == 'nt' else 'make'
            result = subprocess.run([make_cmd, 'html'], cwd='docs', capture_output=True, text=True, shell=True)
            self.ide.console_output.appendPlainText(result.stdout)
            self.ide.console_output.appendPlainText(result.stderr)
            self.ide.console_output.appendPlainText("Dokumentation erfolgreich generiert.")
        except Exception as e:
            self.ide.console_output.appendPlainText(f"Fehler bei der Dokumentationserstellung: {str(e)}")
