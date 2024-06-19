from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ShortcutsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tastenkürzel")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        
        shortcuts_info = """
        Tastenkürzel Übersicht:
        - Interaktives Programm ausführen: Ctrl+I
        - Lint Code: Ctrl+Shift+F
        - Git Commit: Ctrl+Shift+C
        - Snippet hinzufügen: Ctrl+Shift+N
        - Code formatieren: Ctrl+Shift+B
        - Git Status: Ctrl+G
        - Debugger starten: Ctrl+D
        - Konsole löschen: Ctrl+L
        - Interaktive Konsole löschen: Ctrl+Shift+L
        - Projekt öffnen: Ctrl+O
        - Neues Projekt: Ctrl+N
        - Datei speichern: Ctrl+S
        - Info anzeigen: Ctrl+H
        - Tastenkürzel anzeigen: Ctrl+K
        - Projektdateien ein-/ausblenden: Ctrl+T
        - Layout speichern: Ctrl+Shift+S
        - Text übersetzen: Ctrl+T
        """
        
        label = QLabel(shortcuts_info)
        layout.addWidget(label)
        
        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

def show_shortcuts():
    dialog = ShortcutsDialog()
    dialog.exec_()
