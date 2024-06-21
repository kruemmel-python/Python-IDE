import subprocess
import requests
from PyQt5.QtWidgets import (
    QAction, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QMenu, QMessageBox, QInputDialog, QDockWidget, QLineEdit, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from plugin_interface import PluginInterface
from bs4 import BeautifulSoup

class FetchLibrariesThread(QThread):
    libraries_fetched = pyqtSignal(list)

    def run(self):
        try:
            response = requests.get('https://pypi.org/simple/')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            libraries = [a.text.strip() for a in soup.find_all('a')]
            self.libraries_fetched.emit(libraries)
        except requests.RequestException as e:
            self.libraries_fetched.emit([])

class AutoInstallPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.dock_widget = None
        self.installed_library_list = None
        self.available_library_list = None
        self.search_bar = None
        self.info_display = None
        self.create_actions()
        self.fetch_thread = None

    def create_actions(self):
        self.action_install = QAction("Paket installieren", self.ide)
        self.action_install.triggered.connect(self.install_package)
        
        self.action_update = QAction("Paket aktualisieren", self.ide)
        self.action_update.triggered.connect(self.update_package)
        
        self.action_uninstall = QAction("Paket deinstallieren", self.ide)
        self.action_uninstall.triggered.connect(self.uninstall_package)

        self.ide.add_action_to_menu('Bibliotheken', self.action_install)
        self.ide.add_action_to_menu('Bibliotheken', self.action_update)
        self.ide.add_action_to_menu('Bibliotheken', self.action_uninstall)

    def initialize(self):
        self.dock_widget = QDockWidget("Bibliotheken", self.ide)
        self.dock_widget.setObjectName("libraries_dock_widget")
        container = QWidget()
        layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Bibliothek suchen...")

        palette = self.search_bar.palette()
        palette.setColor(QPalette.Text, QColor(Qt.black))
        self.search_bar.setPalette(palette)

        self.search_bar.textChanged.connect(self.filter_libraries)

        splitter = QSplitter(Qt.Vertical)

        self.installed_library_list = QListWidget()
        self.installed_library_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.installed_library_list.customContextMenuRequested.connect(self.open_installed_context_menu)
        self.installed_library_list.itemClicked.connect(self.display_library_info)

        self.available_library_list = QListWidget()
        self.available_library_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.available_library_list.customContextMenuRequested.connect(self.open_available_context_menu)
        self.available_library_list.itemClicked.connect(self.display_library_info)

        splitter.addWidget(self.installed_library_list)
        splitter.addWidget(self.available_library_list)

        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)

        layout.addWidget(self.search_bar)
        layout.addWidget(splitter)
        layout.addWidget(self.info_display)
        container.setLayout(layout)
        self.dock_widget.setWidget(container)

        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.console_output.appendPlainText("Auto Install Plugin aktiviert.")
        self.refresh_libraries()
        self.start_fetching_libraries()

    def deinitialize(self):
        self.ide.remove_action_from_menu('Bibliotheken', self.action_install)
        self.ide.remove_action_from_menu('Bibliotheken', self.action_update)
        self.ide.remove_action_from_menu('Bibliotheken', self.action_uninstall)
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("Auto Install Plugin deaktiviert.")

    def refresh_libraries(self):
        self.installed_library_list.clear()
        result = subprocess.run([self.ide.embedded_python_path, "-m", "pip", "list"], capture_output=True, text=True)
        libraries = result.stdout.split("\n")[2:]
        for lib in libraries:
            if lib:
                item = QListWidgetItem(lib.split()[0])
                self.installed_library_list.addItem(item)
        self.ide.console_output.appendPlainText("Installierte Bibliotheken aktualisiert.")

    def start_fetching_libraries(self):
        self.fetch_thread = FetchLibrariesThread()
        self.fetch_thread.libraries_fetched.connect(self.update_available_libraries)
        self.fetch_thread.start()

    def update_available_libraries(self, libraries):
        self.available_library_list.clear()
        for lib in libraries:
            item = QListWidgetItem(lib)
            self.available_library_list.addItem(item)
        self.ide.console_output.appendPlainText("Verfügbare Bibliotheken aktualisiert.")

    def filter_libraries(self, text):
        for i in range(self.installed_library_list.count()):
            item = self.installed_library_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
        for i in range(self.available_library_list.count()):
            item = self.available_library_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def display_library_info(self, item):
        library_name = item.text()
        self.ide.console_output.appendPlainText(f"Informationen für Bibliothek '{library_name}' werden angezeigt...")
        try:
            result = subprocess.run([self.ide.embedded_python_path, "-m", "pip", "show", library_name], capture_output=True, text=True)
            self.info_display.setPlainText(result.stdout)
        except Exception as e:
            self.info_display.setPlainText(f"Fehler beim Abrufen der Bibliotheksinformationen: {str(e)}")

    def open_installed_context_menu(self, position):
        menu = QMenu()
        selected_item = self.installed_library_list.itemAt(position)
        update_action = QAction("Aktualisieren", self.ide)
        uninstall_action = QAction("Deinstallieren", self.ide)
        menu.addAction(update_action)
        menu.addAction(uninstall_action)
        if selected_item:
            update_action.triggered.connect(lambda: self.update_package(selected_item.text()))
            uninstall_action.triggered.connect(lambda: self.uninstall_package(selected_item.text()))
        menu.exec_(self.installed_library_list.viewport().mapToGlobal(position))

    def open_available_context_menu(self, position):
        menu = QMenu()
        selected_item = self.available_library_list.itemAt(position)
        install_action = QAction("Installieren", self.ide)
        menu.addAction(install_action)
        if selected_item:
            install_action.triggered.connect(lambda: self.install_package(selected_item.text()))
        menu.exec_(self.available_library_list.viewport().mapToGlobal(position))

    def install_package(self, package_name=None):
        if not package_name:
            package_name, ok = QInputDialog.getText(self.ide, 'Install Package', 'Bitte geben Sie den Namen des zu installierenden Pakets ein:')
            if not ok:
                return
        self.ide.console_output.appendPlainText(f"Paket '{package_name}' wird installiert...")
        subprocess.run([self.ide.embedded_python_path, "-m", "pip", "install", package_name])
        self.ide.console_output.appendPlainText(f"Paket '{package_name}' erfolgreich installiert.")
        self.refresh_libraries()

    def update_package(self, package_name=None):
        if not package_name:
            package_name, ok = QInputDialog.getText(self.ide, 'Update Package', 'Bitte geben Sie den Namen des zu aktualisierenden Pakets ein:')
            if not ok:
                return
        self.ide.console_output.appendPlainText(f"Bibliothek '{package_name}' wird aktualisiert...")
        subprocess.run([self.ide.embedded_python_path, "-m", "pip", "install", "--upgrade", package_name])
        self.ide.console_output.appendPlainText(f"Bibliothek '{package_name}' erfolgreich aktualisiert.")
        self.refresh_libraries()

    def uninstall_package(self, package_name=None):
        if not package_name:
            package_name, ok = QInputDialog.getText(self.ide, 'Uninstall Package', 'Bitte geben Sie den Namen des zu deinstallierenden Pakets ein:')
            if not ok:
                return
        self.ide.console_output.appendPlainText(f"Bibliothek '{package_name}' wird deinstalliert...")
        subprocess.run([self.ide.embedded_python_path, "-m", "pip", "uninstall", "-y", package_name])
        self.ide.console_output.appendPlainText(f"Bibliothek '{package_name}' erfolgreich deinstalliert.")
        self.refresh_libraries()
