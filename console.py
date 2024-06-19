import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPlainTextEdit, QMenuBar, QAction, QWidget,
    QListWidget, QMenu, QFileDialog, QMessageBox, QDockWidget, QInputDialog
)
from PyQt5.QtCore import Qt
import logging
from pathlib import Path
from layout import CustomPalette
from code_editor import CodeEditor
import info
import shortcuts  # Import the shortcuts module
from file_operations import (
    open_project, new_project, create_new_file, create_new_folder,
    delete_item, load_file, save_file, install_package, update_package,
    uninstall_package
)
from todo_list import update_todo_list, goto_todo
from interactive_console import InteractiveConsole
from process_manager import create_exe
from translator import translate_text  # Import the translator module

class Console(QMainWindow):
    def __init__(self, embedded_python_path):
        super().__init__()
        logging.debug("Console Initialisierung beginnt")
        self.embedded_python_path = embedded_python_path
        self.project_dir = None
        self.initUI()
        self.load_settings()  # Sicherstellen, dass die Einstellungen nach der UI-Initialisierung geladen werden
        logging.debug("Console Initialisierung abgeschlossen")

    def initUI(self):
        logging.debug("UI Initialisierung beginnt")
        CustomPalette.set_dark_palette(self)

        self.project_files = QListWidget(self)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.itemDoubleClicked.connect(self.load_file)
        
        self.code_editor = CodeEditor(console=self)
        self.console_output = QPlainTextEdit(self)
        self.console_output.setReadOnly(True)
        
        self.todo_list = QListWidget(self)
        self.todo_list.itemClicked.connect(self.goto_todo)

        self.interactive_console = InteractiveConsole(self.embedded_python_path)

        self.setup_dock_widgets()

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("QMenuBar { background-color: #353535; color: #FFFFFF; }")

        run_menu = menu_bar.addMenu('Code')
        create_exe_menu = menu_bar.addMenu('Programm erstellen')
        clear_output_menu = menu_bar.addMenu('Konsole')
        info_menu = menu_bar.addMenu('Info')
        library_menu = menu_bar.addMenu('Bibliotheken')
        project_menu = menu_bar.addMenu('Projekt')
        view_menu = menu_bar.addMenu('Ansicht')
        settings_menu = menu_bar.addMenu('Einstellungen')
        open_project_menu = project_menu.addMenu('Projekt öffnen')
        new_project_menu = project_menu.addMenu('Projekt erstellen')
        save_file_menu = menu_bar.addMenu('Speichern')

        run_interactive_action = QAction('Interaktives Programm ausführen', self)
        lint_action = QAction('Lint Code', self)
        git_commit_action = QAction('Git Commit', self)
        add_snippet_action = QAction('Snippet hinzufügen', self)
        create_exe_action = QAction('erstellen', self)
        clear_output_action = QAction('Ausgabe löschen', self)
        clear_interactive_console_action = QAction('Interaktive Konsole löschen', self)
        translate_action = QAction('Text übersetzen', self)  # Add action for translation
        info_action = QAction('Info', self)
        shortcuts_action = QAction('Tastenkürzel', self)  # Action for showing shortcuts
        install_package_action = QAction('Neues Paket installieren', self)
        update_package_action = QAction('Paket aktualisieren', self)
        uninstall_package_action = QAction('Paket deinstallieren', self)
        open_project_action = QAction('öffnen', self)
        new_project_action = QAction('erstellen', self)
        save_file_action = QAction('geladenen code speichern', self)
        save_layout_action = QAction('Layout speichern', self)
        
        toggle_project_files_action = self.project_files_dock.toggleViewAction()
        toggle_code_editor_action = self.code_editor_dock.toggleViewAction()
        toggle_terminal_action = self.console_output_dock.toggleViewAction()
        toggle_todo_list_action = self.todo_list_dock.toggleViewAction()
        toggle_interactive_console_action = self.interactive_console_dock.toggleViewAction()

        run_menu.addAction(run_interactive_action)
        run_menu.addAction(lint_action)
        run_menu.addAction(git_commit_action)
        run_menu.addAction(add_snippet_action)
        create_exe_menu.addAction(create_exe_action)
        clear_output_menu.addAction(clear_output_action)
        clear_output_menu.addAction(clear_interactive_console_action)  # Add action to clear interactive console
        info_menu.addAction(info_action)
        info_menu.addAction(shortcuts_action)  # Add shortcuts action to info menu
        info_menu.addAction(translate_action)  # Add translate action to info menu
        library_menu.addAction(install_package_action)
        library_menu.addAction(update_package_action)
        library_menu.addAction(uninstall_package_action)
        open_project_menu.addAction(open_project_action)
        new_project_menu.addAction(new_project_action)
        save_file_menu.addAction(save_file_action)
        view_menu.addAction(toggle_project_files_action)
        view_menu.addAction(toggle_code_editor_action)
        view_menu.addAction(toggle_terminal_action)
        view_menu.addAction(toggle_todo_list_action)
        view_menu.addAction(toggle_interactive_console_action)
        settings_menu.addAction(save_layout_action)

        run_interactive_action.triggered.connect(self.run_interactive_script)
        lint_action.triggered.connect(self.lint_code)
        git_commit_action.triggered.connect(self.git_commit)
        add_snippet_action.triggered.connect(self.add_snippet)
        create_exe_action.triggered.connect(lambda: create_exe(self))
        clear_output_action.triggered.connect(self.clear_output)
        clear_interactive_console_action.triggered.connect(self.clear_interactive_console)  # Connect action to clear interactive console
        translate_action.triggered.connect(self.translate_selected_text)  # Connect action to translate text
        info_action.triggered.connect(info.show_info)
        shortcuts_action.triggered.connect(shortcuts.show_shortcuts)  # Connect action to show shortcuts
        install_package_action.triggered.connect(lambda: install_package(self))
        update_package_action.triggered.connect(lambda: update_package(self))
        uninstall_package_action.triggered.connect(lambda: uninstall_package(self))
        open_project_action.triggered.connect(self.open_project)
        new_project_action.triggered.connect(self.new_project)
        save_file_action.triggered.connect(self.save_file)
        save_layout_action.triggered.connect(self.save_settings)

        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 1200, 800)
        logging.debug("UI Initialisierung abgeschlossen")

        # Add shortcuts for actions
        run_interactive_action.setShortcut('Ctrl+I')
        lint_action.setShortcut('Ctrl+Shift+F')
        git_commit_action.setShortcut('Ctrl+Shift+C')
        add_snippet_action.setShortcut('Ctrl+Shift+N')
        clear_output_action.setShortcut('Ctrl+L')
        clear_interactive_console_action.setShortcut('Ctrl+Shift+L')
        open_project_action.setShortcut('Ctrl+O')
        new_project_action.setShortcut('Ctrl+N')
        save_file_action.setShortcut('Ctrl+S')
        info_action.setShortcut('Ctrl+H')
        shortcuts_action.setShortcut('Ctrl+K')
        translate_action.setShortcut('Ctrl+Shift+T')
        toggle_project_files_action.setShortcut('Ctrl+T')
        save_layout_action.setShortcut('Ctrl+Shift+S')

    def setup_dock_widgets(self):
        logging.debug("Dock Widgets werden eingerichtet")
        
        self.project_files_dock = QDockWidget("Projekt Explorer", self)
        self.project_files_dock.setWidget(self.project_files)
        self.project_files_dock.setObjectName("project_files_dock")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_files_dock)

        self.code_editor_dock = QDockWidget("Code Editor", self)
        self.code_editor_dock.setWidget(self.code_editor)
        self.code_editor_dock.setObjectName("code_editor_dock")
        self.addDockWidget(Qt.RightDockWidgetArea, self.code_editor_dock)

        self.console_output_dock = QDockWidget("Konsole", self)
        self.console_output_dock.setWidget(self.console_output)
        self.console_output_dock.setObjectName("console_output_dock")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_output_dock)

        self.todo_list_dock = QDockWidget("TODO Liste", self)
        self.todo_list_dock.setWidget(self.todo_list)
        self.todo_list_dock.setObjectName("todo_list_dock")
        self.addDockWidget(Qt.RightDockWidgetArea, self.todo_list_dock)

        self.interactive_console_dock = QDockWidget("Interaktive Konsole", self)
        self.interactive_console_dock.setWidget(self.interactive_console)
        self.interactive_console_dock.setObjectName("interactive_console_dock")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.interactive_console_dock)

    def open_project(self):
        logging.debug("Projekt wird geöffnet")
        project_dir = QFileDialog.getExistingDirectory(self, 'Open Project', os.getcwd())
        if project_dir:
            self.project_dir = project_dir
            sys.path.insert(0, project_dir)
            self.project_files.clear()
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        self.project_files.addItem(file_path)
            logging.debug(f"Projektverzeichnis gesetzt: {project_dir}")

    def new_project(self):
        logging.debug("Neues Projekt wird erstellt")
        new_project(self)

    def open_context_menu(self, position):
        indexes = self.project_files.selectedIndexes()
        if len(indexes) > 0:
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

    def load_file(self, item):
        logging.debug(f"Datei wird geladen: {item.text()}")
        load_file(self, item)

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
            "dock_widget_states": {
                "project_files": self.project_files_dock.saveGeometry().toHex().data().decode(),
                "code_editor": self.code_editor_dock.saveGeometry().toHex().data().decode(),
                "console_output": self.console_output_dock.saveGeometry().toHex().data().decode(),
                "todo_list": self.todo_list_dock.saveGeometry().toHex().data().decode(),
                "interactive_console": self.interactive_console_dock.saveGeometry().toHex().data().decode()
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
                if "project_files" in dock_widget_states:
                    self.project_files_dock.restoreGeometry(bytes.fromhex(dock_widget_states["project_files"]))
                if "code_editor" in dock_widget_states:
                    self.code_editor_dock.restoreGeometry(bytes.fromhex(dock_widget_states["code_editor"]))
                if "console_output" in dock_widget_states:
                    self.console_output_dock.restoreGeometry(bytes.fromhex(dock_widget_states["console_output"]))
                if "todo_list" in dock_widget_states:
                    self.todo_list_dock.restoreGeometry(bytes.fromhex(dock_widget_states["todo_list"]))
                if "interactive_console" in dock_widget_states:
                    self.interactive_console_dock.restoreGeometry(bytes.fromhex(dock_widget_states["interactive_console"]))
            logging.debug("Einstellungen geladen")

    def run_interactive_script(self):
        code = self.code_editor.toPlainText()
        script_path = os.path.join(self.project_dir if self.project_dir else os.getcwd(), "temp_script.py")
        with open(script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(code)
        logging.debug(f"Script gespeichert: {script_path}")
        self.console_output.appendPlainText(f"Script gespeichert: {script_path}")
        self.interactive_console.run_code(script_path)

    def lint_code(self):
        code = self.code_editor.toPlainText()
        with open("temp_code.py", "w", encoding="utf-8") as file:
            file.write(code)
        pylint_path = self.get_pylint_path()
        process = subprocess.Popen([pylint_path, "temp_code.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        self.console_output.appendPlainText(stdout + "\n" + stderr)
        logging.debug("Code-Linting abgeschlossen")

    def get_pylint_path(self):
        pylint_path = os.path.join(self.embedded_python_path, "Scripts", "pylint.exe")
        if not os.path.exists(pylint_path):
            pylint_path = "pylint"  # Fallback to system pylint if not found in embedded path
        return pylint_path

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

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    main_win = Console('path_to_embedded_python')
    main_win.show()
    sys.exit(app.exec_())
