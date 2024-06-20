from plugin_interface import PluginInterface
from PyQt5.QtWidgets import QInputDialog  # Hinzufügen des Imports
import logging

class RefactorPlugin(PluginInterface):
    def initialize(self):
        self.action = self.ide.create_action('Code Refactoring', self.refactor_code, 'Ctrl+Shift+R')
        self.ide.add_action_to_menu('Code', self.action)
        logging.info("RefactorPlugin initialized")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action)
        logging.info("RefactorPlugin deinitialized")

    def refactor_code(self):
        self.ide.console_output.appendPlainText("Code Refactoring wird ausgeführt...")
        # Hier können Sie den Code zum Refactoring einfügen
        try:
            selected_text = self.ide.code_editor.textCursor().selectedText()
            if selected_text:
                new_name, ok = QInputDialog.getText(self.ide, 'Code Refactoring', f'Ersetzen "{selected_text}" durch:')
                if ok and new_name:
                    cursor = self.ide.code_editor.textCursor()
                    cursor.beginEditBlock()
                    cursor.removeSelectedText()
                    cursor.insertText(new_name)
                    cursor.endEditBlock()
                    self.ide.console_output.appendPlainText(f'"{selected_text}" wurde durch "{new_name}" ersetzt.')
            else:
                self.ide.console_output.appendPlainText("Kein Text ausgewählt.")
        except Exception as e:
            self.ide.console_output.appendPlainText(f"Fehler beim Refactoring: {str(e)}")
        logging.debug("Code Refactoring ausgeführt")
