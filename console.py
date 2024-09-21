import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPlainTextEdit, QMenuBar, QAction, QWidget, QListWidget, QFileDialog, QMenu, QMessageBox, QDockWidget, QInputDialog, QTreeView, QFileSystemModel, QListWidgetItem, QTextEdit, QApplication
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPalette, QColor, QTextFormat, QTextCursor, QKeySequence, QClipboard
import logging
from pathlib import Path
from layout import CustomPalette
from settings_dialog import SettingsDialog
from code_editor import CodeEditor
import info
import shortcuts
from file_operations import open_project, new_project, create_new_file, create_new_folder, delete_item, load_file, save_file, install_package, update_package, uninstall_package
from todo_list import update_todo_list, goto_todo
from process_manager import create_exe
from plugin_manager import PluginManager
from plugin_interface import PluginInterface
from translator import translate_text
from zoomable_widget import ZoomablePlainTextEdit
from interactive_console import InteractiveConsole
import menu_manager  # Importiere das Menümodul

class Console(QMainWindow):
    def __init__(self, embedded_python_path):
        super().__init__()
        logging.debug("Console Initialisierung beginnt")
        self.embedded_python_path = embedded_python_path
        self.project_dir = None
        self.plugin_manager = PluginManager(self)
        self.dock_widgets = {}  # Dictionary zum Speichern aller Dock-Widgets
        self.error_list = QListWidget()  # Fehlerliste initialisieren
        self.error_selections = []  # Speicher für Fehler-Markierungen
        self.current_error_index = 0  # Aktueller Fehler-Index
        self.previous_settings = None  # Variable zum Speichern der vorherigen Einstellungen
        self.initUI()
        self.load_settings()
        self.save_default_dock_positions()  # Speichern der Standardpositionen
        self.plugin_manager.load_plugins()
        menu_manager.create_plugin_actions(self)
        logging.debug("Console Initialisierung abgeschlossen")
    
    def reset_editor(self):
        # Logik zum Zurücksetzen des Editors
        self.code_editor.clear()
        self.code_editor.current_file = None
        self.console_output.clear()
        self.interactive_console.clear()
        self.setWindowTitle("Dein Editor Name")  # Setze den Fenstertitel zurück oder zu einem Standardwert
    
    def create_action(self, name, function, shortcut=None):
        action = QAction(name, self)
        action.triggered.connect(function)
        if shortcut:
            action.setShortcut(shortcut)
        return action
    
    def add_action_to_menu(self, menu_name, action):
        menu = self.findChild(QMenu, menu_name)
        if menu:
            menu.addAction(action)

    def remove_action_from_menu(self, menu_name, action):
        menu = self.findChild(QMenu, menu_name)
        if menu and action in menu.actions():
            menu.removeAction(action)

    
    def initUI(self):
        self.setWindowTitle("Python IDE")
        
        # Widgets initialisieren
        self.project_files = QTreeView(self)
        self.file_system_model = QFileSystemModel(self.project_files)
        self.file_system_model.setRootPath('')
        self.project_files.setModel(self.file_system_model)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.doubleClicked.connect(self.load_file)

        self.code_editor = CodeEditor(console=self)
        self.console_output = ZoomablePlainTextEdit(self)
        self.console_output.setReadOnly(True)
        
        self.todo_list = QListWidget(self)
        self.todo_list.itemClicked.connect(self.goto_todo)

        self.interactive_console = InteractiveConsole(self.embedded_python_path, self.code_editor, self.console_output, self.project_dir)

        self.setup_dock_widgets()
        menu_manager.create_menus(self)  # Erstelle die Menüs über das Menümodul

        self.setGeometry(100, 100, 1200, 800)
        logging.debug("UI Initialisierung abgeschlossen")

        self.setup_clipboard_handling()

    def setup_dock_widgets(self):
        logging.debug("Dock Widgets werden eingerichtet")
        
        self.project_files_dock = QDockWidget("Projekt Explorer", self)
        self.project_files_dock.setWidget(self.project_files)
        self.project_files_dock.setObjectName("project_files_dock")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_files_dock)
        self.dock_widgets["project_files_dock"] = self.project_files_dock

        self.code_editor_dock = QDockWidget("Code Editor", self)
        self.code_editor_dock.setWidget(self.code_editor)
        self.code_editor_dock.setObjectName("code_editor_dock")
        self.addDockWidget(Qt.RightDockWidgetArea, self.code_editor_dock)
        self.dock_widgets["code_editor_dock"] = self.code_editor_dock

        self.console_output_dock = QDockWidget("Konsole", self)
        self.console_output_dock.setWidget(self.console_output)
        self.console_output_dock.setObjectName("console_output_dock")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_output_dock)
        self.dock_widgets["console_output_dock"] = self.console_output_dock

        self.todo_list_dock = QDockWidget("TODO Liste", self)
        self.todo_list_dock.setWidget(self.todo_list)
        self.todo_list_dock.setObjectName("todo_list_dock")
        self.addDockWidget(Qt.RightDockWidgetArea, self.todo_list_dock)
        self.dock_widgets["todo_list_dock"] = self.todo_list_dock

        self.interactive_console_dock = QDockWidget("Interaktive Konsole", self)
        self.interactive_console_dock.setWidget(self.interactive_console)
        self.interactive_console_dock.setObjectName("interactive_console_dock")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.interactive_console_dock)
        self.dock_widgets["interactive_console_dock"] = self.interactive_console_dock

        self.error_dock = QDockWidget("Fehlerliste", self)  # Fehlerliste hinzufügen
        self.error_dock.setWidget(self.error_list)
        self.error_dock.setObjectName("error_dock")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.error_dock)
        self.dock_widgets["error_dock"] = self.error_dock

    def open_project(self):
        logging.debug("Projekt wird geöffnet")
        project_dir = QFileDialog.getExistingDirectory(self, 'Open Project', os.getcwd())
        if project_dir:
            self.file_system_model.setRootPath(project_dir)
            self.project_files.setRootIndex(self.file_system_model.index(project_dir))
            self.project_dir = project_dir
            sys.path.insert(0, project_dir)
            logging.debug(f"Projektverzeichnis gesetzt: {project_dir}")

    def new_project(self):
        logging.debug("Neues Projekt wird erstellt")
        new_project(self)

    def open_context_menu(self, position):
        index = self.project_files.indexAt(position)
        if index.isValid():
            context_menu = QMenu(self)
            new_file_action = context_menu.addAction("New File")
            new_folder_action = context_menu.addAction("New Folder")
            delete_action = context_menu.addAction("Delete")
            action = context_menu.exec_(self.project_files.viewport().mapToGlobal(position))

            if action == new_file_action:
                logging.debug("Neue Datei wird erstellt")
                create_new_file(self)
            elif action == new_folder_action:
                logging.debug("Neuer Ordner wird erstellt")
                create_new_folder(self)
            elif action == delete_action:
                logging.debug("Datei/Ordner wird gelöscht")
                delete_item(self)

    def load_file(self, index: QModelIndex):
        file_path = self.file_system_model.filePath(index)
        logging.debug(f"Datei wird geladen: {file_path}")
        load_file(self, file_path)

    def save_file(self):
        logging.debug("Datei wird gespeichert")
        save_file(self)

    def clear_output(self):
        self.console_output.clear()
        logging.debug("Konsoleninhalt gelöscht")

    def clear_interactive_console(self):
        self.interactive_console.clear()
        logging.debug("Inhalt der interaktiven Konsole gelöscht")

    def closeEvent(self, event):
        self.save_settings()
        open('log.txt', 'w').close()
        logging.debug("Programm geschlossen und log Datei gelöscht")

    def update_todo_list(self):
        logging.debug("TODO-Liste wird aktualisiert")
        update_todo_list(self)

    def goto_todo(self, item):
        logging.debug(f"Springen zu TODO: {item.text()}")
        goto_todo(self, item)

    def save_settings(self):
        settings = {
            "geometry": self.saveGeometry().toHex().data().decode(),
            "window_state": self.saveState().toHex().data().decode(),
            "dock_widget_states": {name: dock.saveGeometry().toHex().data().decode() for name, dock in self.dock_widgets.items()},
            "custom_palette": {
                "colors": {
                    "Window": self.palette().color(QPalette.Window).name(),
                    "WindowText": self.palette().color(QPalette.WindowText).name(),
                    "Base": self.palette().color(QPalette.Base).name(),
                    "AlternateBase": self.palette().color(QPalette.AlternateBase).name(),
                    "ToolTipBase": self.palette().color(QPalette.ToolTipBase).name(),
                    "ToolTipText": self.palette().color(QPalette.ToolTipText).name(),
                    "Text": self.palette().color(QPalette.Text).name(),
                    "Button": self.palette().color(QPalette.Button).name(),
                    "ButtonText": self.palette().color(QPalette.ButtonText).name(),
                    "BrightText": self.palette().color(QPalette.BrightText).name(),
                    "Link": self.palette().color(QPalette.Link).name(),
                    "Highlight": self.palette().color(QPalette.Highlight).name(),
                    "HighlightedText": self.palette().color(QPalette.HighlightedText).name()
                },
                "font_name": self.font().family(),
                "font_size": self.font().pointSize()
            }
        }
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file)
        logging.debug("Einstellungen gespeichert")

    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as settings_file:
                settings = json.load(settings_file)
                self.restoreGeometry(bytes.fromhex(settings["geometry"]))
                self.restoreState(bytes.fromhex(settings["window_state"]))
                dock_widget_states = settings.get("dock_widget_states", {})
                for name, geometry in dock_widget_states.items():
                    if name in self.dock_widgets:
                        self.dock_widgets[name].restoreGeometry(bytes.fromhex(geometry))
                if "custom_palette" in settings:
                    colors = settings["custom_palette"]["colors"]
                    font_name = settings["custom_palette"]["font_name"]
                    font_size = settings["custom_palette"]["font_size"]
                    CustomPalette.customize_palette(self, colors, font_name, font_size)
            logging.debug("Einstellungen geladen")

    def save_previous_settings(self):
        """Speichert die vorherigen Einstellungen, bevor Änderungen vorgenommen werden."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as settings_file:
                self.previous_settings = json.load(settings_file)
            logging.debug("Vorherige Einstellungen gespeichert")

    def restore_previous_settings(self):
        """Stellt die vorherigen Einstellungen wieder her."""
        if self.previous_settings:
            with open("settings.json", "w") as settings_file:
                json.dump(self.previous_settings, settings_file)
            self.load_settings()
            logging.debug("Vorherige Einstellungen wiederhergestellt")

    def lint_code(self):
        code = self.code_editor.toPlainText()
        with open("temp_code.py", "w", encoding="utf-8") as file:
            file.write(code)
        pylint_path = self.get_pylint_path()
        process = subprocess.Popen([pylint_path, "temp_code.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        self.console_output.appendPlainText(stdout + "\n" + stderr)
        self.update_error_list(stdout)
        logging.debug("Code-Linting abgeschlossen")

    def get_pylint_path(self):
        pylint_path = os.path.join(self.embedded_python_path, "Scripts", "pylint.exe")
        if not os.path.exists(pylint_path):
            pylint_path = "pylint"  # Fallback to system pylint if not found in embedded path
        return pylint_path

    def update_error_list(self, lint_output):
        self.clear_error_highlights()
        self.error_list.clear()
        for line in lint_output.splitlines():
            if ':' in line:
                item = QListWidgetItem(line)
                self.error_list.addItem(item)
                self.highlight_error(item)
        if self.error_list.count() > 0:
            self.error_list.setCurrentRow(0)
            self.goto_error(self.error_list.item(0))

    def highlight_error(self, item):
        error_text = item.text()
        parts = error_text.split(':')
        if len(parts) > 1:
            try:
                line_number = int(parts[1].strip()) - 1
                extra_selection = QTextEdit.ExtraSelection()
                extra_selection.cursor = self.code_editor.textCursor()
                extra_selection.cursor.setPosition(self.code_editor.document().findBlockByLineNumber(line_number).position())
                extra_selection.cursor.select(QTextCursor.LineUnderCursor)
                extra_selection.format.setBackground(QColor(255, 0, 0, 100))  # Rot-Hinterlegung hinzufügen
                extra_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                self.error_selections.append(extra_selection)
            except ValueError:
                pass
        self.code_editor.setExtraSelections(self.error_selections)

    def clear_error_highlights(self):
        self.error_selections = []
        self.code_editor.setExtraSelections(self.error_selections)

    def goto_error(self, item):
        error_text = item.text()
        parts = error_text.split(':')
        if len(parts) > 1:
            try:
                line_number = int(parts[1].strip())
                cursor = self.code_editor.textCursor()
                cursor.setPosition(self.code_editor.document().findBlockByLineNumber(line_number - 1).position())
                self.code_editor.setTextCursor(cursor)
                self.code_editor.setFocus()
            except ValueError:
                pass

    def goto_next_error(self):
        self.current_error_index += 1
        if self.current_error_index >= self.error_list.count():
            self.current_error_index = 0
        self.error_list.setCurrentRow(self.current_error_index)
        self.goto_error(self.error_list.currentItem())

    def git_commit(self):
        commit_message, ok = QInputDialog.getText(self, 'Git Commit', 'Commit Message:')
        if ok and commit_message:
            process = subprocess.Popen(["git", "commit", "-am", commit_message], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            self.console_output.appendPlainText(stdout + "\n" + stderr)
            logging.debug("Git-Commit abgeschlossen")

    def add_snippet(self):
        snippet_name, ok = QInputDialog.getText(self, 'Snippet hinzufügen', 'Snippet Name:')
        if ok and snippet_name:
            code = self.code_editor.toPlainText()
            snippets_dir = "snippets"
            os.makedirs(snippets_dir, exist_ok=True)
            with open(os.path.join(snippets_dir, f"{snippet_name}.py"), "w", encoding="utf-8") as file:
                file.write(code)
            self.console_output.appendPlainText(f"Snippet '{snippet_name}' gespeichert.")
            logging.debug(f"Snippet '{snippet_name}' gespeichert")

    def translate_selected_text(self):
        # Helper function to get selected text from any widget
        def get_selected_text(widget):
            cursor = widget.textCursor()
            return cursor.selectedText()

        selected_text = ""
        if self.code_editor.hasFocus():
            selected_text = get_selected_text(self.code_editor)
        elif self.console_output.hasFocus():
            selected_text = get_selected_text(self.console_output)
        elif self.interactive_console.hasFocus():
            selected_text = get_selected_text(self.interactive_console)

        if not selected_text:
            QMessageBox.warning(self, "Übersetzung", "Kein Text ausgewählt!")
            return
        
        translated_text = translate_text(selected_text)
        self.console_output.appendPlainText(f"Original: {selected_text}\nÜbersetzt: {translated_text}")
        QMessageBox.information(self, "Übersetzung", f"Übersetzter Text:\n{translated_text}")

    def open_settings_dialog(self):
        self.save_previous_settings()  # Vorherige Einstellungen speichern
        dialog = SettingsDialog(self)
        dialog.load_current_settings(self.current_settings())  # Aktuelle Einstellungen laden
        if dialog.exec_() == dialog.Rejected:
            self.restore_previous_settings()  # Vorherige Einstellungen wiederherstellen, wenn das Dialogfeld abgebrochen wird

    def current_settings(self):
        """Gibt die aktuellen Einstellungen zurück."""
        current_palette = self.palette()
        return {
            "colors": {
                "Window": current_palette.color(QPalette.Window).name(),
                "WindowText": current_palette.color(QPalette.WindowText).name(),
                "Base": current_palette.color(QPalette.Base).name(),
                "AlternateBase": current_palette.color(QPalette.AlternateBase).name(),
                "ToolTipBase": current_palette.color(QPalette.ToolTipBase).name(),
                "ToolTipText": current_palette.color(QPalette.ToolTipText).name(),
                "Text": current_palette.color(QPalette.Text).name(),
                "Button": current_palette.color(QPalette.Button).name(),
                "ButtonText": current_palette.color(QPalette.ButtonText).name(),
                "BrightText": current_palette.color(QPalette.BrightText).name(),
                "Link": current_palette.color(QPalette.Link).name(),
                "Highlight": current_palette.color(QPalette.Highlight).name(),
                "HighlightedText": current_palette.color(QPalette.HighlightedText).name()
            },
            "font_name": self.font().family(),
            "font_size": self.font().pointSize()
        }

    def apply_settings(self, colors, font_name, font_size):
        CustomPalette.customize_palette(self, colors, font_name, font_size)
        self.save_settings()

    def save_default_dock_positions(self):
        """Saves the default dock positions and states."""
        self.default_dock_positions = {
            "geometry": self.saveGeometry().toHex().data().decode(),
            "window_state": self.saveState().toHex().data().decode(),
            "dock_widget_states": {name: dock.saveGeometry().toHex().data().decode() for name, dock in self.dock_widgets.items()}
        }
        logging.debug("Standard-Dock-Positionen gespeichert")

    def reset_dock_positions(self):
        """Resets the dock positions to their default states."""
        self.restoreGeometry(bytes.fromhex(self.default_dock_positions["geometry"]))
        self.restoreState(bytes.fromhex(self.default_dock_positions["window_state"]))
        dock_widget_states = self.default_dock_positions.get("dock_widget_states", {})
        for name, geometry in dock_widget_states.items():
            if name in self.dock_widgets:
                self.dock_widgets[name].restoreGeometry(bytes.fromhex(geometry))
        logging.debug("Dock-Positionen auf Standard zurückgesetzt")

    def setup_clipboard_handling(self):
        clipboard = QApplication.clipboard()
        self.code_editor.copyAvailable.connect(lambda available: self.copy_text(available, self.code_editor))
        self.console_output.copyAvailable.connect(lambda available: self.copy_text(available, self.console_output))
        self.interactive_console.console.copyAvailable.connect(lambda available: self.copy_text(available, self.interactive_console.console))

    def copy_text(self, available, source):
        if available:
            text = source.textCursor().selectedText()
            QApplication.clipboard().setText(text)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_win = Console('path_to_embedded_python')
    main_win.show()
    sys.exit(app.exec_())
