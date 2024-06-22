from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint
from pathlib import Path
import json

class DocWidget(QWidget):
    def __init__(self, docstring: str, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setLayout(QVBoxLayout())
        self.label = QLabel(docstring, self)
        self.layout().addWidget(self.label)
        self.settings_file = Path("doc_widget_settings.json")
        self.load_settings()

    def update_docstring(self, docstring: str) -> None:
        self.label.setText(docstring)

    def show_at(self, point: QPoint) -> None:
        self.move(point)
        self.show()

    def focusOutEvent(self, event) -> None:
        self.hide()
        self.save_settings()
        super().focusOutEvent(event)

    def save_settings(self) -> None:
        settings = {
            "position": {"x": self.pos().x(), "y": self.pos().y()}
        }
        with self.settings_file.open("w") as file:
            json.dump(settings, file)

    def load_settings(self) -> None:
        if self.settings_file.exists():
            with self.settings_file.open("r") as file:
                settings = json.load(file)
                pos = settings.get("position", {"x": 100, "y": 100})
                self.move(QPoint(pos["x"], pos["y"]))
