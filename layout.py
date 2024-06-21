from PyQt5.QtGui import QPalette, QColor, QFont

class CustomPalette:
    @staticmethod
    def set_dark_palette(app):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        font = QFont("Helvetica", 10)
        app.setFont(font)
        app.setPalette(palette)

    @staticmethod
    def customize_palette(app, colors, font_name, font_size):
        role_map = {
            'Window': QPalette.Window,
            'WindowText': QPalette.WindowText,
            'Base': QPalette.Base,
            'AlternateBase': QPalette.AlternateBase,
            'ToolTipBase': QPalette.ToolTipBase,
            'ToolTipText': QPalette.ToolTipText,
            'Text': QPalette.Text,
            'Button': QPalette.Button,
            'ButtonText': QPalette.ButtonText,
            'BrightText': QPalette.BrightText,
            'Link': QPalette.Link,
            'Highlight': QPalette.Highlight,
            'HighlightedText': QPalette.HighlightedText
        }

        palette = QPalette()
        for role, color in colors.items():
            if role in role_map:
                palette.setColor(role_map[role], QColor(color))
        font = QFont(font_name, font_size)
        app.setFont(font)
        app.setPalette(palette)
