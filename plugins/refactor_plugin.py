# plugins/refactor_plugin.py

from plugin_interface import PluginInterface
from PyQt5.QtWidgets import QAction, QInputDialog

class RefactorPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.action = QAction('Code Refactoring', self.ide)
        self.action.setShortcut('Ctrl+Shift+R')
        self.action.triggered.connect(self.refactor_code)

    def initialize(self):
        self.ide.add_action_to_menu('Code', self.action)

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)

    def refactor_code(self):
        self.ide.console_output.appendPlainText("Code Refactoring wird ausgeführt...")

        cursor = self.ide.code_editor.textCursor()
        selected_text = cursor.selectedText()

        if not selected_text:
            self.ide.console_output.appendPlainText("Kein Text ausgewählt zum Refaktorisieren.")
            return

        new_name, ok = QInputDialog.getText(self.ide, 'Code Refactoring', f'Ersetzen "{selected_text}" durch:')
        if ok and new_name:
            # Refactoring im gesamten Code durchführen
            code = self.ide.code_editor.toPlainText()
            updated_code = code.replace(selected_text, new_name)
            self.ide.code_editor.setPlainText(updated_code)
            self.ide.console_output.appendPlainText(f'"{selected_text}" wurde im gesamten Code durch "{new_name}" ersetzt.')
        else:
            self.ide.console_output.appendPlainText("Refaktorisieren abgebrochen.")
