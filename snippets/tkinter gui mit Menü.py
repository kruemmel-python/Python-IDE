"""Modul zur Erstellung einer GUI mit Menüleiste in Tkinter."""

import tkinter as tk

def main():
    """Hauptfunktion zum Erstellen und Anzeigen des Hauptfensters."""
    root = tk.Tk()
    root.title("Mein Programm")

    menubar = tk.Menu(root)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Neu", command=None)
    filemenu.add_command(label="Öffnen", command=None)
    filemenu.add_command(label="Speichern", command=None)
    filemenu.add_command(label="Speichern unter...", command=None)
    filemenu.add_separator()
    filemenu.add_command(label="Beenden", command=root.quit)
    menubar.add_cascade(label="Datei", menu=filemenu)

    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Rückgängig", command=None)
    editmenu.add_command(label="Wiederholen", command=None)
    editmenu.add_separator()
    editmenu.add_command(label="Ausschneiden", command=None)
    editmenu.add_command(label="Kopieren", command=None)
    editmenu.add_command(label="Einfügen", command=None)
    editmenu.add_command(label="Löschen", command=None)
    editmenu.add_separator()
    editmenu.add_command(label="Suchen", command=None)
    editmenu.add_command(label="Ersetzen", command=None)
    menubar.add_cascade(label="Bearbeiten", menu=editmenu)

    viewmenu = tk.Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Zoomen", command=None)
    viewmenu.add_command(label="Vollbild", command=None)
    viewmenu.add_command(label="Symbolleiste", command=None)
    viewmenu.add_command(label="Statusleiste", command=None)
    menubar.add_cascade(label="Ansicht", menu=viewmenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Hilfe", command=None)
    helpmenu.add_command(label="Über", command=None)
    menubar.add_cascade(label="Hilfe", menu=helpmenu)

    root.config(menu=menubar)
    root.mainloop()

if __name__ == "__main__":
    main()
