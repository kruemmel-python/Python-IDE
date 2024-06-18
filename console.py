from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPlainTextEdit, QSplitter, QMenuBar, QAction, QWidget, QInputDialog, QListWidget, QFileDialog, QMenu
from PyQt5.QtCore import QProcess, Qt
import os
import logging
import sys
from layout import CustomPalette
from code_editor import CodeEditor
import info
from file_operations import open_project, new_project, create_new_file, create_new_folder, delete_item, load_file, save_file
from todo_list import update_todo_list, goto_todo
from process_manager import run_script, create_exe, install_package

class Console(QMainWindow):
    def __init__(self, embedded_python_path):
        super().__init__()
        self.embedded_python_path = embedded_python_path
        self.initUI()

    def initUI(self):
        CustomPalette.set_dark_palette(self)  # Setzen Sie das benutzerdefinierte Farbschema

        self.process = QProcess(self)
        self.terminal = QPlainTextEdit(self)
        self.terminal.setReadOnly(True)

        # Erstellen Sie ein QSplitter-Widget für den Code-Editor und die Terminal-Ausgabe
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(2)

        # Erstellen Sie ein QSplitter-Widget für die Projektdateien und den Code-Editor/Terminal-Bereich
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)

        # Fügen Sie die Widgets zum QSplitter hinzu
        self.project_files = QListWidget(self)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.itemDoubleClicked.connect(self.load_file)
        self.code_editor = CodeEditor(self)
        self.todo_list = QListWidget(self)
        self.todo_list.itemClicked.connect(self.goto_todo)

        self.splitter.addWidget(self.code_editor)
        self.splitter.addWidget(self.terminal)

        self.main_splitter.addWidget(self.project_files)
        self.main_splitter.addWidget(self.splitter)
        self.main_splitter.addWidget(self.todo_list)

        # Layout für QSplitter
        layout = QVBoxLayout()
        layout.addWidget(self.main_splitter)

        # Menüleiste erstellen
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # In Ihrer Hauptklasse, nachdem Sie die Menüleiste erstellt haben:
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("QMenuBar { background-color: #353535; color: #FFFFFF; }")
        # Menüpunkte erstellen
        run_menu = menu_bar.addMenu('Code')
        create_exe_menu = menu_bar.addMenu('Programm erstellen')
        clear_output_menu = menu_bar.addMenu('Konsole')  # Neuer Menüpunkt
        info_menu = menu_bar.addMenu('Info')  # Neuer Menüpunkt
        install_package_menu = menu_bar.addMenu('Bibliotheken')  # Neuer Menüpunkt
        project_menu = menu_bar.addMenu('Projekt')  # Neues Menü für Projekte
        view_menu = menu_bar.addMenu('Ansicht')  # Neues Menü für das Ein- und Ausblenden der Bereiche
        open_project_menu = project_menu.addMenu('Projekt öffnen')  # Neuer Menüpunkt
        new_project_menu = project_menu.addMenu('Projekt erstellen')  # Neuer Menüpunkt
        save_file_menu = menu_bar.addMenu('Speichern')  # Neuer Menüpunkt

        # Aktionen für Menüpunkte erstellen
        run_action = QAction('Code ausführen', self)
        create_exe_action = QAction('erstellen', self)
        clear_output_action = QAction('Ausgabe löschen', self)  # Neuer Menüpunkt
        info_action = QAction('Info', self)  # Neue Aktion
        install_package_action = QAction('Neues Paket installieren', self)  # Neue Aktion
        open_project_action = QAction('öffnen', self)  # Neue Aktion
        new_project_action = QAction('erstellen', self)  # Neue Aktion
        save_file_action = QAction('geladenen code speichern', self)  # Neue Aktion
        toggle_project_files_action = QAction('Sichtbar Fenster Projekt', self)
        toggle_code_editor_action = QAction('Sichtbar Code editor', self)
        toggle_terminal_action = QAction('Sichtbar Konsole', self)
        toggle_todo_list_action = QAction('Sichtbar Todo Liste', self)

        # Aktionen zu Menüpunkten hinzufügen
        run_menu.addAction(run_action)
        create_exe_menu.addAction(create_exe_action)
        clear_output_menu.addAction(clear_output_action)  # Neuer Menüpunkt
        info_menu.addAction(info_action)  # Neue Aktion
        install_package_menu.addAction(install_package_action)  # Neue Aktion
        open_project_menu.addAction(open_project_action)  # Neue Aktion
        new_project_menu.addAction(new_project_action)  # Neue Aktion
        save_file_menu.addAction(save_file_action)  # Neue Aktion
        view_menu.addAction(toggle_project_files_action)
        view_menu.addAction(toggle_code_editor_action)
        view_menu.addAction(toggle_terminal_action)
        view_menu.addAction(toggle_todo_list_action)

        run_action.triggered.connect(lambda: run_script(self, self.code_editor.toPlainText()))
        create_exe_action.triggered.connect(lambda: create_exe(self))
        clear_output_action.triggered.connect(self.clear_output)  # Neues Slot verbinden
        info_action.triggered.connect(info.show_info)  # Neue Slot verbinden
        install_package_action.triggered.connect(lambda: install_package(self))  # Neue Slot verbinden
        open_project_action.triggered.connect(self.open_project)  # Neue Slot verbinden
        new_project_action.triggered.connect(self.new_project)  # Neue Slot verbinden
        save_file_action.triggered.connect(self.save_file)  # Neue Slot verbinden
        toggle_project_files_action.triggered.connect(self.toggle_project_files)
        toggle_code_editor_action.triggered.connect(self.toggle_code_editor)
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        toggle_todo_list_action.triggered.connect(self.toggle_todo_list)

        # Setzen des zentralen Widgets
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 1200, 800)

    def open_project(self):
        open_project(self)

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
        # Löschen Sie den Inhalt der Konsolenausgabe
        self.terminal.clear()
        logging.info("Konsolen Inhalt gelöscht.")

    def closeEvent(self, event):
        # Löschen Sie den Inhalt der Datei 'log.txt' beim Beenden des Programms
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
