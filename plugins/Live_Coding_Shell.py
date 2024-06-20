from plugin_interface import PluginInterface
from PyQt5.QtWidgets import QDockWidget, QPlainTextEdit
from PyQt5.QtCore import Qt
import code
import threading

class LiveCodingPlugin(PluginInterface):
    def initialize(self):
        self.console_output = QPlainTextEdit(self.ide)
        self.console_output.setReadOnly(True)

        self.dock_widget = QDockWidget("Live Coding Shell", self.ide)
        self.dock_widget.setWidget(self.console_output)
        self.ide.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)

        self.shell_thread = threading.Thread(target=self.start_shell, daemon=True)
        self.shell_thread.start()
        
        # Connect the code editor to the shell
        self.ide.code_editor.textChanged.connect(self.execute_code)

        self.ide.console_output.appendPlainText("Live Coding Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("Live Coding Plugin deaktiviert")

    def start_shell(self):
        console_locals = {'ide': self.ide}
        self.shell = code.InteractiveConsole(locals=console_locals)
        
        # Capture shell output
        def write(data):
            self.console_output.appendPlainText(data)
        
        self.shell.write = write
        self.shell.interact()

    def execute_code(self):
        code = self.ide.code_editor.toPlainText()
        self.shell.runsource(code, symbol='exec')

def create_plugin(ide):
    return LiveCodingPlugin(ide)
