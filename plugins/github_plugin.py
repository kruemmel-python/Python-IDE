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

        # GitHub credentials input for upload
        self.user_label = QLabel("GitHub Benutzername (nur für Upload):")
        self.user_input = QLineEdit()
        self.token_label = QLabel("GitHub Personal Access Token (nur für Upload):")
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)

        # Repository input
        self.repo_label = QLabel("Repository Name:")
        self.repo_input = QLineEdit()
        self.repo_info_label = QLabel("Bitte so eingeben: Benutzername/Repositorie Name")

        # Buttons for upload and download
        self.upload_button = QPushButton("Projekt hochladen")
        self.upload_button.clicked.connect(self.upload_project)
        self.download_button = QPushButton("Projekt herunterladen")
        self.download_button.clicked.connect(self.download_project)

        # Add widgets to layout
        self.layout.addWidget(self.user_label)
        self.layout.addWidget(self.user_input)
        self.layout.addWidget(self.token_label)
        self.layout.addWidget(self.token_input)
        self.layout.addWidget(self.repo_label)
        self.layout.addWidget(self.repo_input)
        self.layout.addWidget(self.repo_info_label)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.download_button)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["github_plugin_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("GitHub Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("GitHub Plugin deaktiviert")

    def upload_project(self):
        username = self.user_input.text()
        token = self.token_input.text()
        repo_name = self.repo_input.text()

        if not username or not token or not repo_name:
            QMessageBox.warning(self.widget, "Fehler", "Bitte geben Sie alle Felder ein.")
            return

        repo_path = QFileDialog.getExistingDirectory(self.widget, "Projektverzeichnis auswählen", "")
        if not repo_path:
            return

        # Create repository on GitHub
        create_repo_url = "https://api.github.com/user/repos"
        repo_data = {
            "name": repo_name.split('/')[-1],  # Extract the repo name
            "private": False  # Set to True if you want the repo to be private
        }
        response = requests.post(create_repo_url, json=repo_data, auth=(username, token))

        if response.status_code == 201:
            QMessageBox.information(self.widget, "Erfolg", "Repository wurde auf GitHub erstellt.")
        else:
            QMessageBox.warning(self.widget, "Fehler", f"Fehler beim Erstellen des Repositories: {response.json().get('message', 'Unbekannter Fehler')}")
            return

        # Initialize git in the project directory and push to GitHub
        remote_url = f"https://github.com/{repo_name}.git"
        os.system(f'cd "{repo_path}" && git init && git remote add origin {remote_url}')
        os.system(f'cd "{repo_path}" && git add . && git commit -m "Initial commit" && git push -u origin master')

        self.ide.console_output.appendPlainText("Projekt wurde auf GitHub hochgeladen.")

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
