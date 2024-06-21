from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent, QFont

class ZoomablePlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_level = 0

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
            event.accept()
        else:
            super().wheelEvent(event)

    def zoomIn(self):
        self.zoom_level += 1
        self.setFontPointSize(self.font().pointSize() + 1)

    def zoomOut(self):
        if self.zoom_level > 0:
            self.zoom_level -= 1
            self.setFontPointSize(self.font().pointSize() - 1)

    def setFontPointSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
