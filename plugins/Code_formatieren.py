import subprocess
from PyQt5.QtWidgets import QAction
from plugin_interface import PluginInterface

class CodeFormatterPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.action = QAction("Code formatieren", self.ide)
        self.action.triggered.connect(self.format_code)
    
    def initialize(self):
        self.ide.add_action_to_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Code Formatter Plugin aktiviert.")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.console_output.appendPlainText("Code Formatter Plugin deaktiviert.")
    
    def format_code(self):
        self.ide.console_output.appendPlainText("Code wird formatiert...")
        file_path = self.ide.code_editor.current_file
        if file_path:
            try:
                result = subprocess.run(['black', file_path], capture_output=True, text=True)
                self.ide.console_output.appendPlainText(result.stdout)
                self.ide.console_output.appendPlainText(result.stderr)
                self.ide.console_output.appendPlainText("Code erfolgreich formatiert.")
            except Exception as e:
                self.ide.console_output.appendPlainText(f"Fehler beim Formatieren des Codes: {str(e)}")
        else:
            self.ide.console_output.appendPlainText("Keine Datei zum Formatieren geladen.")