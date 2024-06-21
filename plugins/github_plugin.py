import os
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QDockWidget
)
from PyQt5.QtCore import Qt
from plugin_interface import PluginInterface

class GitHubPlugin(PluginInterface):
    def initialize(self):
        self.dock_widget = QDockWidget("GitHub Plugin", self.ide)
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # Repository input
        self.repo_label = QLabel("Repository Name:")
        self.repo_input = QLineEdit()
        self.repo_info_label = QLabel("Bitte so eingeben: Benutzername/Repositorie Name")

        # Button for download
        self.download_button = QPushButton("Projekt herunterladen")
        self.download_button.clicked.connect(self.download_project)

        # Add widgets to layout
        self.layout.addWidget(self.repo_label)
        self.layout.addWidget(self.repo_input)
        self.layout.addWidget(self.repo_info_label)
        self.layout.addWidget(self.download_button)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["github_plugin_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("GitHub Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("GitHub Plugin deaktiviert")

    def download_project(self):
        repo_name = self.repo_input.text()

        if not repo_name:
            QMessageBox.warning(self.widget, "Fehler", "Bitte geben Sie den Repository-Namen ein.")
            return

        download_path = QFileDialog.getExistingDirectory(self.widget, "Verzeichnis auswählen, um das Projekt zu speichern", "")
        if not download_path:
            return

        remote_url = f"https://github.com/{repo_name}.git"
        os.system(f'cd "{download_path}" && git clone {remote_url}')

        self.ide.console_output.appendPlainText("Projekt wurde von GitHub heruntergeladen.")

def create_plugin(ide):
    return GitHubPlugin(ide)
