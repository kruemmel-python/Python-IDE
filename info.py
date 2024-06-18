from PyQt5.QtWidgets import QMessageBox

def show_info():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Python IDE Info")
    msg.setInformativeText("Dies ist eine  Python-IDE mit Syntaxhervorhebung, Codevervollständigung und mehr.")
    msg.setWindowTitle("Info")
    msg.setDetailedText(
        "Schlüsselwörter: Blau\n"
        "Zeichenfolgen: Rot\n"
        "Zahlen: Orange\n"
        "Kommentare: Grün\n"
        "Funktionen/Klassen: Blau (fett)\n"
        "Operatoren: Lila\n"
        "Klammern: Gelb"
    )
    msg.exec_()
