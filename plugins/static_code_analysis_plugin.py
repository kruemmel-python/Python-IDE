import subprocess
from PyQt5.QtWidgets import QAction
from plugin_interface import PluginInterface

class StaticCodeAnalysisPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.action = QAction("Statische Codeanalyse", self.ide)
        self.action.triggered.connect(self.run_analysis)
    
    def initialize(self):
        self.ide.add_action_to_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Static Code Analysis Plugin aktiviert.")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Static Code Analysis Plugin deaktiviert.")
    
    def run_analysis(self):
        self.ide.console_output.appendPlainText("Statische Codeanalyse wird durchgeführt...")
        file_path = self.ide.code_editor.current_file
        if file_path:
            try:
                result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
                self.ide.console_output.appendPlainText(result.stdout)
                self.ide.console_output.appendPlainText(result.stderr)
                self.ide.console_output.appendPlainText("Codeanalyse abgeschlossen.")
            except Exception as e:
                self.ide.console_output.appendPlainText(f"Fehler bei der Codeanalyse: {str(e)}")
        else:
            self.ide.console_output.appendPlainText("Keine Datei zur Analyse geladen.")