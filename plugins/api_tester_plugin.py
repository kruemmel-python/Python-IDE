import requests
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDockWidget, QComboBox, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from plugin_interface import PluginInterface

class ApiTesterPlugin(PluginInterface):
    def initialize(self):
        self.dock_widget = QDockWidget("API Tester", self.ide)
        self.dock_widget.setObjectName("ApiTesterDockWidget")
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.method_combobox = QComboBox()
        self.method_combobox.addItems(["GET", "POST", "PUT", "DELETE"])
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("API URL hier eingeben...")
        self.headers_input = QTextEdit()
        self.headers_input.setPlaceholderText("Header im JSON-Format eingeben...")
        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Anfragetext (JSON)...")
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        self.send_button = QPushButton("Anfrage senden")
        self.send_button.clicked.connect(self.send_request)

        self.layout.addWidget(QLabel("HTTP-Methode:"))
        self.layout.addWidget(self.method_combobox)
        self.layout.addWidget(QLabel("URL:"))
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(QLabel("Header:"))
        self.layout.addWidget(self.headers_input)
        self.layout.addWidget(QLabel("Body:"))
        self.layout.addWidget(self.body_input)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(QLabel("Antwort:"))
        self.layout.addWidget(self.response_output)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["api_tester_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("API Tester Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("API Tester Plugin deaktiviert")

    def send_request(self):
        method = self.method_combobox.currentText()
        url = self.url_input.text()
        headers = self.parse_json(self.headers_input.toPlainText())
        body = self.parse_json(self.body_input.toPlainText())

        if not url:
            QMessageBox.warning(self.widget, "Fehler", "Bitte geben Sie eine URL ein.")
            return

        try:
            response = requests.request(method, url, headers=headers, json=body)
            self.response_output.setPlainText(response.text)
        except requests.RequestException as e:
            QMessageBox.critical(self.widget, "Anfragefehler", str(e))

    def parse_json(self, text):
        if not text:
            return None
        try:
            return json.loads(text)
        except ValueError:
            QMessageBox.warning(self.widget, "Fehler", "Ungültiges JSON-Format.")
            return None

def create_plugin(ide):
    return ApiTesterPlugin(ide)
