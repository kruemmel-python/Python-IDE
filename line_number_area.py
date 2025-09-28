from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, QRect, Qt
from PySide6.QtGui import QPainter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)
