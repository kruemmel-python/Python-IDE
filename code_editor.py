from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QCompleter
from PyQt5.QtGui import QColor, QTextFormat, QTextCursor, QPainter
from PyQt5.QtCore import Qt, QRegExp, QRect
import jedi
from highlighter import PythonHighlighter
from line_number_area import LineNumberArea


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlighter = PythonHighlighter(self.document())
        self.current_file = None

        self.textChanged.connect(self.update_todo_list)
        self.completer = None
        self.completions = []

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(QRect(0, top, self.lineNumberArea.width(), self.fontMetrics().height()), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.transparent)  # Kein Hintergrund
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def update_todo_list(self):
        if hasattr(self.parent(), 'update_todo_list'):
            self.parent().update_todo_list()

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab):
                self.insert_completion(self.completer.currentCompletion())
                return
            elif event.key() == Qt.Key_Escape:
                self.completer.popup().hide()
                return
            else:
                super().keyPressEvent(event)
                return

        super().keyPressEvent(event)

        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab, Qt.Key_Backtab):
            return

        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        text = cursor.selectedText()
        if text:
            self.show_completions(text)

    def show_completions(self, text):
        script = jedi.Script(text, path=self.current_file)
        self.completions = script.complete()
        if self.completions:
            completion_strings = [c.name for c in self.completions]
            self.completer = QCompleter(completion_strings, self)
            self.completer.setWidget(self)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.completer.activated.connect(self.insert_completion)
            cursor_rect = self.cursorRect()
            cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0)
                                 + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cursor_rect)

    def insert_completion(self, completion):
        if self.completer.widget() != self:
            return
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        cursor.insertText(completion)
        self.setTextCursor(cursor)
