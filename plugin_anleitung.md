# Anleitung zum Erstellen von Plugins für die Python IDE

Diese Anleitung beschreibt, wie man Plugins für die Python IDE schreibt und diese integriert, ohne dass Änderungen am Hauptprogrammcode erforderlich sind.

## Voraussetzungen
- Grundkenntnisse in Python
- Installierte Python IDE (die oben beschriebenen Version)
- Verständnis von Python Klassen und Methoden

## Verzeichnisstruktur
Die Plugins sollten in einem speziellen Ordner namens `plugins` abgelegt werden. Die Verzeichnisstruktur sieht wie folgt aus:

/Python_IDE
/plugins
example_plugin.py
main.py
console.py
...


## Schritt 1: Erstellen eines Plugins
Ein Plugin muss von der `PluginInterface`-Klasse erben und die Methoden `initialize` und `deinitialize` implementieren.

**Beispiel: Unit Test Plugin**

Erstellen Sie eine neue Datei im `plugins`-Ordner, z.B. `unit_test_plugin.py`:
```python
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
```

Schritt 2: Plugins automatisch laden
Die IDE lädt automatisch alle Plugins aus dem plugins-Ordner beim Start. Sie müssen sicherstellen, dass die PluginManager-Klasse korrekt konfiguriert ist.

Beispiel: Plugin Manager

Stellen Sie sicher, dass der plugin_manager.py wie folgt aussieht:
```python
# plugin_manager.py
import os
import importlib.util
from pathlib import Path
import logging
from plugin_interface import PluginInterface

class PluginManager:
    def __init__(self, ide):
        self.ide = ide
        self.plugins = {}
        self.active_plugins = set()

    def load_plugins(self, plugin_directory='plugins'):
        plugin_dir = Path(plugin_directory)
        if not plugin_dir.exists():
            plugin_dir.mkdir()

        for plugin_file in plugin_dir.glob('*.py'):
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, PluginInterface) and attribute is not PluginInterface:
                        self.plugins[attribute_name] = attribute(self.ide)
                        logging.info(f"Plugin {attribute_name} loaded from {plugin_file}")

    def initialize_plugin(self, plugin_name):
        plugin = self.plugins.get(plugin_name)
        if plugin and plugin_name not in self.active_plugins:
            plugin.initialize()
            self.active_plugins.add(plugin_name)
            logging.info(f"Plugin {plugin_name} initialized")

    def deinitialize_plugin(self, plugin_name):
        plugin = self.plugins.get(plugin_name)
        if plugin and plugin_name in self.active_plugins:
            plugin.deinitialize()
            self.active_plugins.remove(plugin_name)
            logging.info(f"Plugin {plugin_name} deinitialized")

    def toggle_plugin(self, plugin_name):
        if plugin_name in self.active_plugins:
            self.deinitialize_plugin(plugin_name)
        else:
            self.initialize_plugin(plugin_name)

    def get_plugins(self):
        return list(self.plugins.items())

    def is_plugin_active(self, plugin_name):
        return plugin_name in self.active_plugins
```
Schritt 3: Plugins im Menü anzeigen
Die Console-Klasse muss das Plugin-Menü enthalten und die Möglichkeit bieten, Plugins zu aktivieren oder zu deaktivieren.

Beispiel: Console Klasse

Stellen Sie sicher, dass die Console-Klasse wie folgt aussieht:

```python

# console.py
# ... andere Importe
from plugin_manager import PluginManager
from plugin_interface import PluginInterface
# ... andere Importe

class Console(QMainWindow):
    def __init__(self, embedded_python_path):
        super().__init__()
        self.embedded_python_path = embedded_python_path
        self.project_dir = None
        self.plugin_manager = PluginManager(self)
        self.initUI()
        self.load_settings()  
        self.plugin_manager.load_plugins()
        self.add_plugin_actions(self.plugin_menu)
    
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
        if menu:
            menu.removeAction(action)

    def initUI(self):
        self.project_files = QTreeView(self)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.doubleClicked.connect(self.load_file)

        self.file_system_model = QFileSystemModel(self.project_files)
        self.file_system_model.setRootPath('')
        self.project_files.setModel(self.file_system_model)
        
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
        self.plugin_menu = menu_bar.addMenu('Plugins')  # Add a menu for plugins

        run_interactive_action = self.create_action('Interaktives Programm ausführen', self.run_interactive_script, 'Ctrl+I')
        lint_action = self.create_action('Lint Code', self.lint_code, 'Ctrl+Shift+F')
        git_commit_action = self.create_action('Git Commit', self.git_commit, 'Ctrl+Shift+C')
        add_snippet_action = self.create_action('Snippet hinzufügen', self.add_snippet, 'Ctrl+Shift+N')
        create_exe_action = self.create_action('erstellen', lambda: create_exe(self))

        # Aktionen zu den Menüs hinzufügen
        run_menu.addAction(run_interactive_action)
        run_menu.addAction(lint_action)
        run_menu.addAction(git_commit_action)
        run_menu.addAction(add_snippet_action)
        create_exe_menu.addAction(create_exe_action)

        # Shortcuts für Aktionen hinzufügen
        run_interactive_action.setShortcut('Ctrl+I')
        lint_action.setShortcut('Ctrl+Shift+F')
        git_commit_action.setShortcut('Ctrl+Shift+C')
        add_snippet_action.setShortcut('Ctrl+Shift+N')

    def setup_dock_widgets(self):
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
        project_dir = QFileDialog.getExistingDirectory(self, 'Open Project', os.getcwd())
        if project_dir:
            self.file_system_model.setRootPath(project_dir)
            self.project_files.setRootIndex(self.file_system_model.index(project_dir))
            self.project_dir = project_dir
            sys.path.insert(0, project_dir)

    def new_project(self):
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
                create_new_file(self)
            elif action == new_folder_action:
                create_new_folder(self)
            elif action == delete_action:
                delete_item(self)

    def load_file(self, index: QModelIndex):
        load_file(self, index)

    def save_file(self):
        save_file(self)

    def clear_output(self):
        self.console_output.clear()

    def clear_interactive_console(self):
        self.interactive_console.clear()

    def closeEvent(self, event):
        self.save_settings()
        open('log.txt', 'w').close()

    def update_todo_list(self):
        update_todo_list(self)

    def goto_todo(self, item):
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

    def run_interactive_script(self):
        code = self.code_editor.toPlainText()
        script_path = os.path.join(self.project_dir if self.project_dir else os.getcwd(), "temp_script.py")
        with open(script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(code)
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

    def add_snippet(self):
        snippet_name, ok = QInputDialog.getText(self, 'Snippet hinzufügen', 'Snippet Name:')
        if ok and snippet_name:
            code = self.code_editor.toPlainText()
            snippets_dir = "snippets"
            os.makedirs(snippets_dir, exist_ok=True)
            with open(os.path.join(snippets_dir, f"{snippet_name}.py"), "w", encoding="utf-8") as file:
                file.write(code)
            self.console_output.appendPlainText(f"Snippet '{snippet_name}' gespeichert.")

    def translate_selected_text(self):
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

    def add_plugin_actions(self, plugin_menu):
        plugins = self.plugin_manager.get_plugins()
        for plugin_name, _ in plugins:
            action = QAction(f"{plugin_name} aktivieren/deaktivieren", self)
            action.setCheckable(True)
            action.setChecked(self.plugin_manager.is_plugin_active(plugin_name))
            action.toggled.connect(lambda checked, name=plugin_name: self.plugin_manager.toggle_plugin(name))
            plugin_menu.addAction(action)

    def run_unit_tests(self):
        self.console_output.appendPlainText("Unit Tests werden ausgeführt...")
        try:
            result = subprocess.run([self.embedded_python_path, '-m', 'unittest', 'discover'], cwd=self.project_dir, capture_output=True, text=True)
            self.console_output.appendPlainText(result.stdout)
            self.console_output.appendPlainText(result.stderr)
        except Exception as e:
            self.console_output.appendPlainText(f"Fehler beim Ausführen der Unit-Tests: {str(e)}")

    def refactor_code(self):
        self.console_output.appendPlainText("Code Refactoring wird ausgeführt...")

    def start_debugger(self):
        self.console_output.appendPlainText("Debugger wird gestartet...")
        code = self.code_editor.toPlainText()
        script_path = os.path.join(self.project_dir if self.project_dir else os.getcwd(), "temp_script.py")
        with open(script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(code)
        self.console_output.appendPlainText(f"Script gespeichert: {script_path}")
        debugger_process = subprocess.Popen([self.embedded_python_path, "-m", "pdb", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.console_output.appendPlainText(f"Debugger PID: {debugger_process.pid}")

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    main_win = Console('path_to_embedded_python')
    main_win.show()
    sys.exit(app.exec_())

```


## Schritt 4: Plugins hinzufügen und aktivieren
Nach dem Erstellen und Speichern des Plugins können Sie die IDE starten. Im Menü "Plugins" sehen Sie die Liste der verfügbaren Plugins. Aktivieren oder deaktivieren Sie die gewünschten Plugins, indem Sie darauf klicken.

Das war's! Sie haben erfolgreich ein Plugin für die Python IDE erstellt und integriert.

