import os
import subprocess
import logging
import sys
import io
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QProcess

class InteractiveConsole(QWidget):
    def __init__(self, embedded_python_path, code_editor, console_output, project_dir):
        super().__init__()
        self.embedded_python_path = embedded_python_path
        self.code_editor = code_editor
        self.console_output = console_output
        self.project_dir = project_dir if project_dir else os.getcwd()  # Standardpfad auf das Arbeitsverzeichnis setzen
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.console = QPlainTextEdit(self)
        self.console.setReadOnly(True)
        self.input_line = QLineEdit(self)
        self.input_line.returnPressed.connect(self.send_input)

        layout.addWidget(self.console)
        layout.addWidget(self.input_line)
        self.setLayout(layout)
        self.process = None

    def run_code(self, script_path, project_dir):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.print_output)
        self.process.readyReadStandardError.connect(self.print_output)
        if project_dir:
            self.process.setWorkingDirectory(project_dir)
        self.process.start(self.embedded_python_path, [script_path])

    def run_interactive_script(self):
        code = self.code_editor.toPlainText()
        # Nutze das Verzeichnis des ursprünglichen Skripts oder das Arbeitsverzeichnis
        script_dir = os.path.dirname(self.code_editor.current_file) if self.code_editor.current_file else self.project_dir
        if not script_dir:
            script_dir = os.getcwd()  # Fallback auf das aktuelle Arbeitsverzeichnis
        
        script_path = os.path.join(script_dir, "temp_script.py")

        # Füge Code hinzu, um die Standardausgabe auf UTF-8 zu setzen
        code_with_utf8 = """
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

""" + code

        with open(script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(code_with_utf8)
        logging.debug(f"Script gespeichert: {script_path}")
        self.console_output.appendPlainText(f"Script gespeichert: {script_path}")
        self.code_editor.current_file = script_path  # Setze den aktuellen Dateipfad
        
        # Setze das Arbeitsverzeichnis auf das Verzeichnis des Skripts
        self.run_code(script_path, script_dir)

    def print_output(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        self.console.appendPlainText(output)

    def send_input(self):
        if self.process and self.process.state() == QProcess.Running:
            input_text = self.input_line.text() + '\n'
            self.process.write(input_text.encode('utf-8'))
            self.input_line.clear()

    def clear(self):
        self.console.clear()
