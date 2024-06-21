import os
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QMessageBox, QDockWidget
)
from PyQt5.QtCore import Qt
from plugin_interface import PluginInterface

class PyInstallerPlugin(PluginInterface):
    def initialize(self):
        self.dock_widget = QDockWidget("PyInstaller Plugin", self.ide)
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # Python file input
        self.file_label = QLabel("Python Datei:")
        self.file_input = QLineEdit()
        self.browse_button = QPushButton("Durchsuchen")
        self.browse_button.clicked.connect(self.browse_file)

        # Additional files and directories input
        self.add_files_label = QLabel("Zusätzliche Dateien und Verzeichnisse:")
        self.add_files_input = QLineEdit()
        self.add_files_button = QPushButton("Durchsuchen")
        self.add_files_button.clicked.connect(self.browse_additional_files)

        # Output directory input
        self.output_label = QLabel("Ausgabeverzeichnis:")
        self.output_input = QLineEdit()
        self.output_browse_button = QPushButton("Durchsuchen")
        self.output_browse_button.clicked.connect(self.browse_output_directory)

        # Checkboxes for PyInstaller options
        self.one_file_checkbox = QCheckBox("Eine Datei")
        self.console_checkbox = QCheckBox("Konsole anzeigen")

        # Create button
        self.create_button = QPushButton("Erstellen")
        self.create_button.clicked.connect(self.create_executable)

        # Add widgets to layout
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.add_files_label)
        self.layout.addWidget(self.add_files_input)
        self.layout.addWidget(self.add_files_button)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_input)
        self.layout.addWidget(self.output_browse_button)
        self.layout.addWidget(self.one_file_checkbox)
        self.layout.addWidget(self.console_checkbox)
        self.layout.addWidget(self.create_button)

        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.ide.dock_widgets["pyinstaller_plugin_dock"] = self.dock_widget

        self.ide.console_output.appendPlainText("PyInstaller Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.console_output.appendPlainText("PyInstaller Plugin deaktiviert")

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.widget, "Python Datei auswählen", "", "Python Dateien (*.py)")
        if file_name:
            self.file_input.setText(file_name)

    def browse_additional_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_names, _ = file_dialog.getOpenFileNames(self.widget, "Zusätzliche Dateien und Verzeichnisse auswählen", "", "Alle Dateien (*.*)")
        if file_names:
            self.add_files_input.setText(";".join(file_names))

    def browse_output_directory(self):
        output_directory = QFileDialog.getExistingDirectory(self.widget, "Ausgabeverzeichnis auswählen", "")
        if output_directory:
            self.output_input.setText(output_directory)

    def create_executable(self):
        python_file = self.file_input.text()
        additional_files = self.add_files_input.text()
        output_directory = self.output_input.text()

        if not python_file or not os.path.exists(python_file):
            QMessageBox.warning(self.widget, "Fehler", "Bitte wählen Sie eine gültige Python Datei aus.")
            return

        options = ["pyinstaller"]
        if self.one_file_checkbox.isChecked():
            options.append("--onefile")
        if not self.console_checkbox.isChecked():
            options.append("--noconsole")
        if additional_files:
            for item in additional_files.split(';'):
                options.append('--add-data')
                options.append(f"{item};{item}")
        if output_directory:
            options.append("--distpath")
            options.append(output_directory)
        options.append(python_file)

        process = subprocess.Popen(options, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        self.ide.console_output.appendPlainText(stdout)
        if stderr:
            self.ide.console_output.appendPlainText(stderr)
        QMessageBox.information(self.widget, "Fertig", "Die ausführbare Datei wurde erstellt.")

def create_plugin(ide):
    return PyInstallerPlugin(ide)
