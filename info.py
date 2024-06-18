from PyQt5.QtWidgets import QMessageBox

def show_info():
    info_text = """
    <h2>Farbliche Bedeutung im Code-Editor:</h2>
    <ul>
        <li><span style="color: blue; font-weight: bold;">Schlüsselwörter (blau, fett)</span>: Schlüsselwörter wie <code>def</code>, <code>class</code>, <code>import</code>, <code>if</code>, <code>else</code>, etc.</li>
        <li><span style="color: red;">Strings (rot)</span>: Zeichenfolgen, die in Anführungszeichen stehen, z.B. <code>"text"</code> oder <code>'text'</code>.</li>
        <li><span style="color: green;">Kommentare (grün)</span>: Kommentare, die mit <code>#</code> beginnen.</li>
        <li><span style="color: blue; font-weight: bold;">Funktionen und Klassen (blau, fett)</span>: Namen von Funktionen und Klassen.</li>
        <li><span style="color: orange;">Zahlen (orange)</span>: Ganzzahlen und Gleitkommazahlen.</li>
        <li><span style="color: purple;">Operatoren (lila)</span>: Operatoren wie <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, etc.</li>
        <li><span style="color: yellow;">Klammern und geschweifte Klammern (gelb)</span>: <code>()</code>, <code>{}</code>, <code>[]</code>.</li>
    </ul>
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(info_text)
    msg.setWindowTitle("Info")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
