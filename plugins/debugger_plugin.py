# plugins/debugger_plugin.py
from plugin_interface import PluginInterface
import subprocess
import logging

class DebuggerPlugin(PluginInterface):
    def initialize(self):
        self.action = self.ide.create_action('Debugger starten', self.start_debugger, 'Ctrl+D')
        self.ide.add_action_to_menu('Code', self.action)
        self.ide.console_output.appendPlainText("DebuggerPlugin geladen.")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        self.ide.console_output.appendPlainText("DebuggerPlugin deinitialisiert.")

    def start_debugger(self):
        self.ide.console_output.appendPlainText("Debugger wird gestartet...")
        try:
            # Beispiel: Starten des Debuggers in einer neuen Konsole
            debugger_cmd = [
                self.ide.embedded_python_path, '-m', 'pdb', self.ide.code_editor.current_file
            ]
            process = subprocess.Popen(debugger_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.ide.console_output.appendPlainText("Debugger wurde gestartet.")
            self.ide.console_output.appendPlainText(f"Debugger PID: {process.pid}")
        except Exception as e:
            self.ide.console_output.appendPlainText(f"Fehler beim Starten des Debuggers: {str(e)}")
        logging.debug("Debugger gestartet")
