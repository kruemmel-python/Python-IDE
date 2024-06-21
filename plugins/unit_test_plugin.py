import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QDockWidget, QListWidget
)
from PyQt5.QtCore import Qt, QProcess
from plugin_interface import PluginInterface

class UnitTestPlugin(PluginInterface):
    def initialize(self):
        self.dock_widget = QDockWidget("Unit Test Plugin", self.ide)
        self.dock_widget.setObjectName("UnitTestPluginDockWidget")
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.test_list = QListWidget()
        self.browse_button = QPushButton("Durchsuchen")
        self.browse_button.clicked.connect(self.add_test_files)
        self.run_button = QPushButton("Tests ausführen")
        self.run_button.clicked.connect(self.run_tests)
        self.reset_button = QPushButton("Pytest zurücksetzen")
        self.reset_button.clicked.connect(self.reset_pytest)

        self.layout.addWidget(QLabel("Unit Test Dateien:"))
        self.layout.addWidget(self.test_list)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.reset_button)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["unit_test_plugin_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("Unit Test Plugin aktiviert")

        self.process = None

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("Unit Test Plugin deaktiviert")

    def add_test_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self.widget, "Unit Test Dateien auswählen", "", "Python Dateien (*.py)", options=options)
        if files:
            for file in files:
                self.test_list.addItem(file)

    def run_tests(self):
        test_files = [self.test_list.item(i).text() for i in range(self.test_list.count())]
        for test_file in test_files:
            process = subprocess.Popen([sys.executable, '-m', 'pytest', test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            self.ide.console_output.appendPlainText(stdout)
            if stderr:
                self.ide.console_output.appendPlainText(stderr)

    def reset_pytest(self):
        if self.process:
            self.process.kill()
        self.process = QProcess()
        self.ide.console_output.appendPlainText("Pytest wurde zurückgesetzt.")

def create_plugin(ide):
    return UnitTestPlugin(ide)
