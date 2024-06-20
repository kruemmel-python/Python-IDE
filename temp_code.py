import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class Schuelerverwaltung(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('schuelerverwaltung.db')
        self.curs = self.conn.cursor()
        self.create_table()
        self.initUI()

    def create_table(self):
        self.curs.execute('''CREATE TABLE IF NOT EXISTS klassen (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS schueler (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                klasse_id INTEGER,
                                FOREIGN KEY(klasse_id) REFERENCES klassen(id))''')
        self.conn.commit()

    def initUI(self):
        self.title("Schülerverwaltung")
        self.geometry("600x400")

        # Hauptlayout
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.daten_eingeben_btn = tk.Button(main_frame, text="Daten eingeben", command=self.daten_eingeben)
        self.daten_eingeben_btn.pack(fill=tk.X, pady=5)

        self.daten_anzeigen_btn = tk.Button(main_frame, text="Daten anzeigen", command=self.daten_anzeigen)
        self.daten_anzeigen_btn.pack(fill=tk.X, pady=5)

        self.beenden_btn = tk.Button(main_frame, text="Beenden", command=self.quit)
        self.beenden_btn.pack(fill=tk.X, pady=5)

    def daten_eingeben(self):
        self.eingabe_fenster = tk.Toplevel(self)
        self.eingabe_fenster.title("Daten eingeben")
        self.eingabe_fenster.geometry("300x200")

        layout = tk.Frame(self.eingabe_fenster)
        layout.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(layout, text="Name").pack()
        self.name_input = tk.Entry(layout)
        self.name_input.pack(fill=tk.X)

        tk.Label(layout, text="Klasse").pack()
        self.klasse_input = ttk.Combobox(layout)
        self.curs.execute("SELECT id, name FROM klassen")
        klassen = self.curs.fetchall()
        self.klasse_input['values'] = [f"{klasse[1]} (ID: {klasse[0]})" for klasse in klassen]
        self.klasse_input.pack(fill=tk.X)

        self.speichern_btn = tk.Button(layout, text="Speichern", command=self.speichern_daten)
        self.speichern_btn.pack(pady=10)

    def speichern_daten(self):
        name = self.name_input.get()
        klasse = self.klasse_input.get()
        
        if name and klasse:
            klasse_id = self.get_klasse_id(klasse)
            if klasse_id is None:
                self.curs.execute("INSERT INTO klassen (name) VALUES (?)", (klasse.split(" (ID: ")[0],))
                klasse_id = self.curs.lastrowid
            
            self.curs.execute("INSERT INTO schueler (name, klasse_id) VALUES (?, ?)", (name, klasse_id))
            self.conn.commit()
            messagebox.showinfo("Erfolg", "Schülerdaten gespeichert.")
            self.eingabe_fenster.destroy()
        else:
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen.")

    def get_klasse_id(self, klasse):
        self.curs.execute("SELECT id FROM klassen WHERE name = ?", (klasse.split(" (ID: ")[0],))
        row = self.curs.fetchone()
        return row[0] if row else None

    def daten_anzeigen(self):
        self.anzeigen_fenster = tk.Toplevel(self)
        self.anzeigen_fenster.title("Daten anzeigen")
        self.anzeigen_fenster.geometry("600x400")

        layout = tk.Frame(self.anzeigen_fenster)
        layout.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.table_widget = ttk.Treeview(layout, columns=("ID", "Name", "Klasse"), show="headings")
        self.table_widget.heading("ID", text="ID")
        self.table_widget.heading("Name", text="Name")
        self.table_widget.heading("Klasse", text="Klasse")
        self.table_widget.pack(fill=tk.BOTH, expand=True)

        self.curs.execute('''
            SELECT s.id, s.name, k.name 
            FROM schueler s
            LEFT JOIN klassen k ON s.klasse_id = k.id
        ''')
        for record in self.curs.fetchall():
            self.table_widget.insert('', tk.END, values=(record[0], record[1], record[2]))

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = Schuelerverwaltung()
    app.mainloop()
