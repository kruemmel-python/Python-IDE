import sys
import io
import subprocess
import jedi
import os
import tempfile
import shutil
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPlainTextEdit, QSplitter, QMenuBar,
    QAction, QWidget, QTextEdit, QInputDialog, QMessageBox, QFileDialog, QListWidget, QMenu, QCompleter
)
from PyQt5.QtCore import QProcess, Qt, QRect, QSize, QRegExp, QPoint
from PyQt5.QtGui import QPainter, QTextFormat, QColor, QSyntaxHighlighter, QTextCharFormat, QFont, QTextCursor
from Layout import CustomPalette
import info  # Importieren des neuen Moduls
import check_python  # Importieren des neuen Moduls

# Konfigurieren des Logging-Moduls
logging.basicConfig(filename='ide.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# Pfad zur eingebetteten oder systemweiten Python-Version
embedded_python_path = check_python.get_python_executable()

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.initializeFormats()

    def initializeFormats(self):
        self.highlightingRules = []

        # Keyword format
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0, 0, 255))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = [
            "\\band\\b", "\\bas\\b", "\\bassert\\b", "\\bbreak\\b", "\\bclass\\b", "\\bcontinue\\b",
            "\\bdef\\b", "\\bdel\\b", "\\belif\\b", "\\belse\\b", "\\bexcept\\b", "\\bFalse\\b",
            "\\bfinally\\b", "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b",
            "\\bin\\b", "\\bis\\b", "\\blambda\\b", "\\bNone\\b", "\\bnonlocal\\b", "\\bnot\\b",
            "\\bor\\b", "\\bpass\\b", "\\braise\\b", "\\breturn\\b", "\\bTrue\\b", "\\btry\\b",
            "\\bwhile\\b", "\\bwith\\b", "\\byield\\b"
        ]
        for keyword in keywords:
            self.highlightingRules.append((QRegExp(keyword), keywordFormat))

        # String format
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(255, 0, 0))
        self.highlightingRules.append((QRegExp("\".*\""), stringFormat))
        self.highlightingRules.append((QRegExp("'.*'"), stringFormat))

        # Number format
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor(255, 165, 0))
        self.highlightingRules.append((QRegExp("\\b[0-9]+\\b"), numberFormat))

        # Comment format
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(0, 128, 0))
        self.highlightingRules.append((QRegExp("#[^\n]*"), commentFormat))

        # Function and class format
        functionClassFormat = QTextCharFormat()
        functionClassFormat.setForeground(QColor(0, 0, 255))
        functionClassFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp("\\bdef\\s+\\w+"), functionClassFormat))
        self.highlightingRules.append((QRegExp("\\bclass\\s+\\w+"), functionClassFormat))

        # Operator format
        operatorFormat = QTextCharFormat()
        operatorFormat.setForeground(QColor(128, 0, 128))
        operators = ["=", "==", "!=", "<", ">", "<=", ">=", "\\+", "-", "\\*", "/", "//", "%", "\\*\\*", "\\+=",
                     "-=", "\\*=", "/=", "%=", "\\^", "\\|", "&", "~", ">>", "<<"]
        for operator in operators:
            self.highlightingRules.append((QRegExp(operator), operatorFormat))

        # Brackets and braces format
        bracketFormat = QTextCharFormat()
        bracketFormat.setForeground(QColor(255, 255, 0))
        brackets = ["\\(", "\\)", "\\{", "\\}", "\\[", "\\]"]
        for bracket in brackets:
            self.highlightingRules.append((QRegExp(bracket), bracketFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)

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


class Console(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        CustomPalette.set_dark_palette(self)  # Setzen Sie das benutzerdefinierte Farbschema

        self.process = QProcess(self)
        self.terminal = QPlainTextEdit(self)
        self.terminal.setReadOnly(True)

        # Erstellen Sie ein QSplitter-Widget für den Code-Editor und die Terminal-Ausgabe
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(2)

        # Erstellen Sie ein QSplitter-Widget für die Projektdateien und den Code-Editor/Terminal-Bereich
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)

        # Fügen Sie die Widgets zum QSplitter hinzu
        self.project_files = QListWidget(self)
        self.project_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_files.customContextMenuRequested.connect(self.open_context_menu)
        self.project_files.itemDoubleClicked.connect(self.load_file)
        self.code_editor = CodeEditor(self)
        self.todo_list = QListWidget(self)
        self.todo_list.itemClicked.connect(self.goto_todo)

        self.splitter.addWidget(self.code_editor)
        self.splitter.addWidget(self.terminal)

        self.main_splitter.addWidget(self.project_files)
        self.main_splitter.addWidget(self.splitter)
        self.main_splitter.addWidget(self.todo_list)

        # Layout für QSplitter
        layout = QVBoxLayout()
        layout.addWidget(self.main_splitter)

        # Menüleiste erstellen
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # In Ihrer Hauptklasse, nachdem Sie die Menüleiste erstellt haben:
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("QMenuBar { background-color: #353535; color: #FFFFFF; }")
        # Menüpunkte erstellen
        run_menu = menu_bar.addMenu('Code')
        create_exe_menu = menu_bar.addMenu('Programm erstellen')
        clear_output_menu = menu_bar.addMenu('Konsole')  # Neuer Menüpunkt
        info_menu = menu_bar.addMenu('Info')  # Neuer Menüpunkt
        install_package_menu = menu_bar.addMenu('Bibliotheken')  # Neuer Menüpunkt
        project_menu = menu_bar.addMenu('Projekt')  # Neues Menü für Projekte
        view_menu = menu_bar.addMenu('Ansicht')  # Neues Menü für das Ein- und Ausblenden der Bereiche
        open_project_menu = project_menu.addMenu('Projekt öffnen')  # Neuer Menüpunkt
        new_project_menu = project_menu.addMenu('Projekt erstellen')  # Neuer Menüpunkt
        save_file_menu = menu_bar.addMenu('Speichern')  # Neuer Menüpunkt

        # Aktionen für Menüpunkte erstellen
        run_action = QAction('Code ausführen', self)
        create_exe_action = QAction('erstellen', self)
        clear_output_action = QAction('Ausgabe löschen', self)  # Neuer Menüpunkt
        info_action = QAction('Info', self)  # Neue Aktion
        install_package_action = QAction('Neues Paket installieren', self)  # Neue Aktion
        open_project_action = QAction('öffnen', self)  # Neue Aktion
        new_project_action = QAction('erstellen', self)  # Neue Aktion
        save_file_action = QAction('geladenen code speichern', self)  # Neue Aktion
        toggle_project_files_action = QAction('Sichtbar Fenster Projekt', self)
        toggle_code_editor_action = QAction('Sichtbar Code editor', self)
        toggle_terminal_action = QAction('Sichtbar Konsole', self)
        toggle_todo_list_action = QAction('Sichtbar Todo Liste', self)

        # Aktionen zu Menüpunkten hinzufügen
        run_menu.addAction(run_action)
        create_exe_menu.addAction(create_exe_action)
        clear_output_menu.addAction(clear_output_action)  # Neuer Menüpunkt
        info_menu.addAction(info_action)  # Neue Aktion
        install_package_menu.addAction(install_package_action)  # Neue Aktion
        open_project_menu.addAction(open_project_action)  # Neue Aktion
        new_project_menu.addAction(new_project_action)  # Neue Aktion
        save_file_menu.addAction(save_file_action)  # Neue Aktion
        view_menu.addAction(toggle_project_files_action)
        view_menu.addAction(toggle_code_editor_action)
        view_menu.addAction(toggle_terminal_action)
        view_menu.addAction(toggle_todo_list_action)

        run_action.triggered.connect(self.run_script)
        create_exe_action.triggered.connect(self.create_exe)
        clear_output_action.triggered.connect(self.clear_output)  # Neues Slot verbinden
        info_action.triggered.connect(info.show_info)  # Neue Slot verbinden
        install_package_action.triggered.connect(self.install_package)  # Neue Slot verbinden
        open_project_action.triggered.connect(self.open_project)  # Neue Slot verbinden
        new_project_action.triggered.connect(self.new_project)  # Neue Slot verbinden
        save_file_action.triggered.connect(self.save_file)  # Neue Slot verbinden
        toggle_project_files_action.triggered.connect(self.toggle_project_files)
        toggle_code_editor_action.triggered.connect(self.toggle_code_editor)
        toggle_terminal_action.triggered.connect(self.toggle_terminal)
        toggle_todo_list_action.triggered.connect(self.toggle_todo_list)

        # Setzen des zentralen Widgets
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 1200, 800)

    def run_script(self):
        script = self.code_editor.toPlainText()
        
        if self.code_editor.current_file:
            project_dir = os.path.dirname(self.code_editor.current_file)
            sys.path.insert(0, project_dir)
            os.chdir(project_dir)

        # Skript in einer temporären Datei speichern und ausführen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_script:
            temp_script.write(script.encode('utf-8'))
            temp_script_path = temp_script.name
        try:            
        # Starten Sie einen neuen Subprozess, um das Skript auszuführen
            self.execute_script(temp_script_path)
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e}")
            self.terminal.appendPlainText(f"ERROR: Script execution failed: {e}")

    def execute_script(self, script_path):
        process = subprocess.Popen([embedded_python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ausgabe in die Konsole weiterleiten
        stdout, stderr = process.communicate()
        self.terminal.appendPlainText(stdout)
        if stderr:
            self.terminal.appendPlainText(f"ERROR: {stderr}")

    def create_exe(self):
        script = self.code_editor.toPlainText()
        with open('temp_script.py', 'w', encoding='utf-8') as file:
            file.write(script)
        
        exe_name, ok = QInputDialog.getText(self, 'Name der ausführbaren Datei', 'Bitte geben Sie den Namen der ausführbaren Datei ein:')
        
        if ok and exe_name:
            try:
                subprocess.run([embedded_python_path, "-m", "PyInstaller", "--onefile", "--noconfirm", "--name", exe_name, "temp_script.py"])
                logging.info(f"Executable created with name '{exe_name}' using pyinstaller.")
                self.terminal.appendPlainText(f"Executable created with name '{exe_name}' using pyinstaller.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Executable creation failed: {e}")
                self.terminal.appendPlainText(f"ERROR: Executable creation failed: {e}")

    def install_package(self):
        package_name, ok = QInputDialog.getText(self, 'Install Package', 'Bitte geben Sie den Namen des zu installierenden Pakets ein:')
        
        if ok and package_name:
            self.terminal.appendPlainText(f"Installing package '{package_name}'...")
            subprocess.run([embedded_python_path, "-m", "pip", "install", package_name])
            self.terminal.appendPlainText(f"Package '{package_name}' installed successfully.")
        else:
            self.terminal.appendPlainText("Package installation cancelled.")

    def open_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, 'Open Project', os.getcwd())
        if project_dir:
            self.project_files.clear()
            sys.path.insert(0, project_dir)  # Fügen Sie das Projektverzeichnis zu sys.path hinzu
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        self.project_files.addItem(file_path)

    def new_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, 'Select Directory for New Project', os.getcwd())
        if project_dir:
            project_name, ok = QInputDialog.getText(self, 'New Project', 'Bitte geben Sie den Namen des neuen Projekts ein:')
            if ok and project_name:
                new_project_path = os.path.join(project_dir, project_name)
                try:
                    os.makedirs(new_project_path)
                    self.terminal.appendPlainText(f"Created new project at: {new_project_path}")
                    # Optional: Grundlegende Projektstruktur anlegen
                    with open(os.path.join(new_project_path, 'main.py'), 'w', encoding='utf-8') as main_file:
                        main_file.write("# Start your new project here\n")
                    self.project_files.clear()
                    self.project_files.addItem(os.path.join(new_project_path, 'main.py'))
                except Exception as e:
                    self.terminal.appendPlainText(f"Failed to create new project: {str(e)}")

    def open_context_menu(self, position):
        indexes = self.project_files.selectedIndexes()
        if len(indexes) > 0:
            context_menu = QMenu(self)
            new_file_action = context_menu.addAction("New File")
            new_folder_action = context_menu.addAction("New Folder")
            delete_action = context_menu.addAction("Delete")
            action = context_menu.exec_(self.project_files.viewport().mapToGlobal(position))

            if action == new_file_action:
                self.create_new_file()
            elif action == new_folder_action:
                self.create_new_folder()
            elif action == delete_action:
                self.delete_item()

    def create_new_file(self):
        if self.project_files.currentItem():
            current_path = self.project_files.currentItem().text()
            if os.path.isdir(current_path):
                directory = current_path
            else:
                directory = os.path.dirname(current_path)
        else:
            directory = os.getcwd()

        file_name, ok = QInputDialog.getText(self, 'New File', 'Bitte geben Sie den Namen der neuen Datei ein:')
        if ok and file_name:
            new_file_path = os.path.join(directory, file_name)
            try:
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write("")
                self.terminal.appendPlainText(f"Neue Datei: {new_file_path}")
                self.project_files.addItem(new_file_path)
            except Exception as e:
                self.terminal.appendPlainText(f"Fehler: Keine neue Datei erstellt: {str(e)}")

    def create_new_folder(self):
        if self.project_files.currentItem():
            current_path = self.project_files.currentItem().text()
            if os.path.isdir(current_path):
                directory = current_path
            else:
                directory = os.path.dirname(current_path)
        else:
            directory = os.getcwd()

        folder_name, ok = QInputDialog.getText(self, 'Neuer Ordner', 'Bitte geben Sie den Namen des neuen Ordners ein:')
        if ok and folder_name:
            new_folder_path = os.path.join(directory, folder_name)
            try:
                os.makedirs(new_folder_path)
                self.terminal.appendPlainText(f"Neuer Ordner erstellt: {new_folder_path}")
                self.project_files.addItem(new_folder_path)
            except Exception as e:
                self.terminal.appendPlainText(f"Fehler; Es konnte kein Ordner erstellt werden: {str(e)}")

    def delete_item(self):
        if self.project_files.currentItem():
            item_path = self.project_files.currentItem().text()
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                self.terminal.appendPlainText(f"Markiertes Löschen: {item_path}")
                self.project_files.takeItem(self.project_files.currentRow())
            except Exception as e:
                self.terminal.appendPlainText(f"Fehler Löschen erfolglos: {str(e)}")

    def load_file(self, item):
        file_path = item.text()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.code_editor.setPlainText(file.read())
            self.code_editor.current_file = file_path
            self.terminal.appendPlainText(f"Datei geladen: {file_path}")
            self.update_todo_list()
        except Exception as e:
            self.terminal.appendPlainText(f"konnte Datei nicht laden: {file_path}\n{str(e)}")

    def save_file(self):
        if self.code_editor.current_file:
            try:
                with open(self.code_editor.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.code_editor.toPlainText())
                self.terminal.appendPlainText(f"Datei gespeichert: {self.code_editor.current_file}")
            except Exception as e:
                self.terminal.appendPlainText(f"Fehler beim Speichern: {self.code_editor.current_file}\n{str(e)}")
        else:
            self.terminal.appendPlainText("Keine Datei zum speichern geladen.")

    def print_output(self):
        try:
            output = str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        except UnicodeDecodeError:
            output = str(self.process.readAllStandardOutput().data(), encoding='latin-1')
        self.terminal.appendPlainText(output)

    def print_error(self):
        try:
            error = str(self.process.readAllStandardError().data(), encoding='utf-8')
        except UnicodeDecodeError:
            error = str(self.process.readAllStandardError().data(), encoding='latin-1')
        self.terminal.appendPlainText(f"ERROR: {error}")

    def clear_output(self):
        # Löschen Sie den Inhalt der Konsolenausgabe
        self.terminal.clear()
        logging.info("Konsolen Inhalt gelöscht.")

    def closeEvent(self, event):
        # Löschen Sie den Inhalt der Datei 'log.txt' beim Beenden des Programms
        open('log.txt', 'w').close()
        logging.info("Programm geschlossen und log Datei gelöscht.")

    def update_todo_list(self):
        self.todo_list.clear()
        text = self.code_editor.toPlainText()
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'TODO:' in line:
                self.todo_list.addItem(f"Line {i + 1}: {line.strip()}")

    def goto_todo(self, item):
        line_number = int(item.text().split()[1].strip(':'))
        cursor = self.code_editor.textCursor()
        cursor.setPosition(self.code_editor.document().findBlockByLineNumber(line_number - 1).position())
        self.code_editor.setTextCursor(cursor)
        self.code_editor.setFocus()

    def toggle_project_files(self):
        self.project_files.setVisible(not self.project_files.isVisible())

    def toggle_code_editor(self):
        self.code_editor.setVisible(not self.code_editor.isVisible())

    def toggle_terminal(self):
        self.terminal.setVisible(not self.terminal.isVisible())

    def toggle_todo_list(self):
        self.todo_list.setVisible(not self.todo_list.isVisible())


def main():
    app = QApplication(sys.argv)
    console = Console()
    console.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
