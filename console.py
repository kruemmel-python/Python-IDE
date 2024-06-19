import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPlainTextEdit, QSplitter, QMenuBar, QAction, QWidget,
    QListWidget, QMenu, QFileDialog
)
from PyQt5.QtCore import QProcess, Qt
import logging
from pathlib import Path
from layout import CustomPalette
from code_editor import CodeEditor
import info
from file_operations import (
    open_project, new_project, create_new_file, create_new_folder,
    delete_item, load_file, save_file, install_package, update_package,
    uninstall_package, add_library_management_menu
)
from todo_list import update_todo_list, goto_todo
from process_manager import run_script, create_exe


class Console(QMainWindow):
    def __init__(self, embedded_python_path):
        super().__init__()
        self.embedded_python_path = embedded_python_path
        self.project_dir = None
        self.initUI()

    def initUI(self):
        CustomPalette.set_dark_palette(self)

        self.process = QProcess(self)
        self.terminal = QPlainTextEdit(self)
        self.terminal.setReadOnly(True)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(2)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)

        self.project_files = QListWidget(self)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.itemDoubleClicked.connect(self.load_file)
        self.code_editor = CodeEditor(console=self)
        self.todo_list = QListWidget(self)
        self.todo_list.itemClicked.connect(self.goto_todo)

        self.splitter.addWidget(self.code_editor)
        self.splitter.addWidget(self.terminal)

        self.main_splitter.addWidget(self.project_files)
        self.main_splitter.addWidget(self.splitter)
        self.main_splitter.addWidget(self.todo_list)

        layout = QVBoxLayout()
        layout.addWidget(self.main_splitter)

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
        open_project_menu = project_menu.addMenu('Projekt öffnen')
        new_project_menu = project_menu.addMenu('Projekt erstellen')
        save_file_menu = menu_bar.addMenu('Speichern')

        run_action = QAction('Code ausführen', self)
        run_selected_action = QAction('Markierten Code ausführen', self)
        create_exe_action = QAction('erstellen', self)
        clear_output_action = QAction('Ausgabe löschen', self)
        info_action = QAction('Info', self)
        install_package_action = QAction('Neues Paket installieren', self)
        update_package_action = QAction('Paket aktualisieren', self)
        uninstall_package_action = QAction('Paket deinstallieren', self)
        open_project_action = QAction('öffnen', self)
        new_project_action = QAction('erstellen', self)
        save_file_action = QAction('geladenen code speichern', self)
        toggle_project_files_action = QAction('Sichtbar Fenster Projekt', self)
        toggle_code_editor_action = QAction('Sichtbar Code editor', self)
        toggle_terminal_action = QAction('Sichtbar Konsole', self)
        toggle_todo_list_action = QAction('Sichtbar Todo Liste', self)

        run_menu.addAction(run_action)
        run_menu.addAction(run_selected_action)
        create_exe_menu.addAction(create_exe_action)
        clear_output_menu.addAction(clear_output_action)
        info_menu.addAction(info_action)
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

        run_action.triggered.connect(lambda: self.run_script(self.code_editor.toPlainText()))
        run_selected_action.triggered.connect(self.code_editor.run_selected_code)
        create_exe_action.triggered.connect(lambda: create_exe(self))
        clear_output_action.triggered.connect(self.clear_output)
        info_action.triggered.connect(info.show_info)
        install_package_action.triggered.connect(lambda: install_package(self))
        update_package_action.triggered.connect(lambda: update_package(self))
        uninstall_package_action.triggered.connect(lambda: uninstall_package(self))
        open_project_action.triggered.connect(self.open_project)
        new_project_action.triggered.connect(self.new_project)
        save_file_action.triggered.connect(self.save_file)
        toggle_project_files_action.triggered.connect(self.toggle_project_files)
        toggle_code_editor_action.triggered.connect(self.toggle_code_editor)
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        toggle_todo_list_action.triggered.connect(self.toggle_todo_list)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 1200, 800)

    def open_project(self):
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

    def new_project(self):
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
                create_new_file(self)
            elif action == new_folder_action:
                create_new_folder(self)
            elif action == delete_action:
                delete_item(self)

    def load_file(self, item):
        load_file(self, item)

    def save_file(self):
        save_file(self)

    def print_output(self):
        try:
            output = str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        except UnicodeDecodeError:
            output = str(self.process.readAllStandardOutput().data(), encoding='latin-1')
        self.terminal.appendPlainText(output)

    def print_error(self):
        try:
            error = str(self.process.readAllStandardError().data(), encoding='utf-8')
        except UnicodeDecodeError:
            error = str(self.process.readAllStandardError().data(), encoding='latin-1')
        self.terminal.appendPlainText(f"ERROR: {error}")

    def clear_output(self):
        self.terminal.clear()
        logging.info("Konsolen Inhalt gelöscht.")

    def closeEvent(self, event):
        open('log.txt', 'w').close()
        logging.info("Programm geschlossen und log Datei gelöscht.")

    def update_todo_list(self):
        update_todo_list(self)

    def goto_todo(self, item):
        goto_todo(self, item)

    def toggle_project_files(self):
        self.project_files.setVisible(not self.project_files.isVisible())

    def toggle_code_editor(self):
        self.code_editor.setVisible(not self.code_editor.isVisible())

    def toggle_terminal(self):
        self.terminal.setVisible(not self.terminal.isVisible())

    def toggle_todo_list(self):
        self.todo_list.setVisible(not self.todo_list.isVisible())

    def run_script(self, code=None):
        if code is None:
            code = self.code_editor.toPlainText()
        run_script(self, code)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    main_win = Console('path_to_embedded_python')
    main_win.show()
    sys.exit(app.exec_())
