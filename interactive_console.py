# interactive_console.py
import os
import sys
import subprocess
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import QProcess

class InteractiveConsole(QWidget):
    def __init__(self, embedded_python_path):
        super().__init__()
        self.embedded_python_path = embedded_python_path
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.console = QPlainTextEdit(self)
        self.console.setReadOnly(True)
        layout.addWidget(self.console)
        self.setLayout(layout)
        self.process = None

    def run_code(self, script_path):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.print_output)
        self.process.readyReadStandardError.connect(self.print_output)
        self.process.start(self.embedded_python_path, [script_path])

    def print_output(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        self.console.appendPlainText(output)

    def clear(self):
        self.console.clear()
