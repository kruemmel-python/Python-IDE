from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint
import json
import os

class DocWidget(QWidget):
    def __init__(self, docstring, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setLayout(QVBoxLayout())
        self.label = QLabel(docstring, self)
        self.layout().addWidget(self.label)
        self.settings_file = "doc_widget_settings.json"
        self.load_settings()

    def update_docstring(self, docstring):
        self.label.setText(docstring)

    def show_at(self, point):
        self.move(point)
        self.show()

    def focusOutEvent(self, event):
        self.hide()
        self.save_settings()
        super().focusOutEvent(event)

    def save_settings(self):
        settings = {
            "position": {"x": self.pos().x(), "y": self.pos().y()}
        }
        with open(self.settings_file, "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                pos = settings.get("position", {"x": 100, "y": 100})
                self.move(QPoint(pos["x"], pos["y"]))
