from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DocWidget(QWidget):
    def __init__(self, docstring, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setLayout(QVBoxLayout())
        self.label = QLabel(docstring, self)
        self.layout().addWidget(self.label)

    def update_docstring(self, docstring):
        self.label.setText(docstring)

    def show_at(self, point):
        self.move(point)
        self.show()

    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)
