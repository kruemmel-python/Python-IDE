from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QFontDialog, QScrollArea, QWidget
)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Einstellungen")
        
        # ScrollArea to contain the settings
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        
        self.color_inputs = {}
        color_roles = ['Window', 'WindowText', 'Base', 'AlternateBase', 'ToolTipBase', 'ToolTipText', 'Text', 'Button', 'ButtonText', 'BrightText', 'Link', 'Highlight', 'HighlightedText']
        for role in color_roles:
            label = QLabel(f"{role} Farbe:")
            line_edit = QLineEdit()
            self.color_inputs[role] = line_edit
            button = QPushButton("Farbe auswählen")
            button.clicked.connect(lambda _, r=role: self.select_color(r))
            self.layout.addWidget(label)
            self.layout.addWidget(line_edit)
            self.layout.addWidget(button)

        self.font_button = QPushButton("Schriftart auswählen")
        self.font_button.clicked.connect(self.select_font)
        self.layout.addWidget(self.font_button)

        self.save_button = QPushButton("Speichern")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)
        
        scroll_content.setLayout(self.layout)
        scroll.setWidget(scroll_content)
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(scroll)
        self.setLayout(dialog_layout)
        
        self.selected_font = None

        # Set default size
        self.resize(400, 300)  # Width: 400, Height: 300

    def select_color(self, role):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_inputs[role].setText(color.name())

    def select_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.selected_font = font

    def save_settings(self):
        colors = {role: self.color_inputs[role].text() for role in self.color_inputs}
        font_name = self.selected_font.family() if self.selected_font else "Helvetica"
        font_size = self.selected_font.pointSize() if self.selected_font else 10
        self.parent().apply_settings(colors, font_name, font_size)
        self.accept()
