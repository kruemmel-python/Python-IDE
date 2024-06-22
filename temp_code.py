import sqlite3
import tkinter as tk
from tkinter import messagebox
import os
import json
import random

# Pfad zur Speicherdatei
speicherdatei_pfad = 'quiz_fortschritt.json'
# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Hauptfenster der Anwendung
root = tk.Tk()
root.title("Python Multiple Choice Test")

# Globale Variablen für die Punkte und die aktuelle Frage
punkte = 0
aktuelle_frage_id = 1
gesamtpunkte = 0
gesamtwiederholungen = 0  # Gesamtanzahl der Wiederholungen



# Funktion, um eine zufällige Frage-ID zu erhalten
def zufaellige_frage_id_erhalten():
    cursor.execute('SELECT id FROM fragen')
    fragen_ids = [id[0] for id in cursor.fetchall()]
    random.shuffle(fragen_ids)  # Mische die Liste der Frage-IDs
    return fragen_ids

# Globale Variable für die Liste der zufälligen Frage-IDs
zufaellige_fragen_ids = zufaellige_frage_id_erhalten()

# Funktion, um den Fortschritt zu speichern
def fortschritt_speichern(fortschritt):
    with open(speicherdatei_pfad, 'w') as f:
        json.dump(fortschritt, f)

# Funktion, um den Fortschritt zu laden oder eine neue Datei zu erstellen
def fortschritt_laden_oder_erstellen():
    if not os.path.exists(speicherdatei_pfad):
        # Kein Fortschritt vorhanden, leere Datei erstellen
        fortschritt_speichern({'punkte': 0, 'aktuelle_frage_id': 1, 'gesamtwiederholungen': 0})
        return {'punkte': 0, 'aktuelle_frage_id': 1, 'gesamtwiederholungen': 0}
    else:
        # Fortschritt laden
        with open(speicherdatei_pfad, 'r') as f:
            return json.load(f)

# Beim Start des Programms den Fortschritt laden oder eine neue Datei erstellen
fortschritt = fortschritt_laden_oder_erstellen()

def alten_test_fortsetzen():
    fortschritt = fortschritt_laden_oder_erstellen()
    if fortschritt:
        fortsetzen = messagebox.askyesno("Fortschritt gefunden", "Möchten Sie den alten Test fortsetzen?")
        if fortsetzen:
            global punkte, aktuelle_frage_id, gesamtwiederholungen
            punkte = fortschritt['punkte']
            aktuelle_frage_id = fortschritt['aktuelle_frage_id']
            gesamtwiederholungen = fortschritt['gesamtwiederholungen']
        else:
            # Alten Fortschritt löschen und neue Werte setzen
            os.remove(speicherdatei_pfad)
            punkte = 0
            aktuelle_frage_id = 1
            gesamtwiederholungen = 0
    else:
        # Kein Fortschritt vorhanden, neue Werte setzen
        punkte = 0
        aktuelle_frage_id = 1
        gesamtwiederholungen = 0
    naechste_frage()  # Nächste Frage laden, unabhängig von der Entscheidung

# Funktion, um die Gesamtpunktzahl zu berechnen
def gesamtpunkte_berechnen():
    global gesamtpunkte
    cursor.execute('SELECT COUNT(*) FROM fragen')
    gesamtpunkte = cursor.fetchone()[0]

# Funktion, um die nächste Frage zu laden und anzuzeigen
def naechste_frage(wiederholen=False):
    global aktuelle_frage_id, gesamtwiederholungen
    if wiederholen:
        # Wenn die Frage wiederholt werden soll, behalten wir die aktuelle_frage_id bei
        pass
    elif zufaellige_fragen_ids:
        # Wenn nicht wiederholt wird, wählen wir eine neue zufällige Frage aus
        aktuelle_frage_id = zufaellige_fragen_ids.pop()
    else:
        messagebox.showinfo("Ende des Tests", f"Der Test ist beendet. Sie haben {punkte} von {gesamtpunkte} Punkten erreicht.")
        root.destroy()
        return
    cursor.execute('SELECT * FROM fragen WHERE id = ?', (aktuelle_frage_id,))
    frage = cursor.fetchone()
    
    if frage:
        frage_label.config(text=f"Frage {aktuelle_frage_id}: {frage[1]}")
        for var in check_vars:
            var.set(0)  # Auswahl zurücksetzen
        antwort1_check.config(text=frage[2])
        antwort2_check.config(text=frage[3])
        antwort3_check.config(text=frage[4])
        antwort4_check.config(text=frage[5])
        punkte_label.config(text=f"Bisher erreichte Punkte: {punkte}/{gesamtpunkte}")
        wiederholungen_label.config(text=f"Gesamtwiederholungen: {gesamtwiederholungen}")
    else:
        messagebox.showinfo("Ende des Tests", f"Der Test ist beendet. Sie haben {punkte} von {gesamtpunkte} Punkten erreicht.")
        root.destroy()


# Funktion, die aufgerufen wird, wenn die Antwort falsch ist
def antwort_falsch():
    global gesamtwiederholungen
    wiederholen = messagebox.askyesno("Falsch", "Ihre Antwort ist falsch. Möchten Sie die Frage wiederholen?")
    if wiederholen:
        gesamtwiederholungen += 1  # Gesamtanzahl der Wiederholungen erhöhen
        naechste_frage(wiederholen=True)
    else:
        naechste_frage(wiederholen=False)

# Funktion, um die ausgewählte Antwort zu überprüfen und ggf. die Frage zu wiederholen
def antwort_ueberpruefen():
    global punkte, aktuelle_frage_id
    cursor.execute('SELECT korrekte_antwort, korrekte_antworten FROM fragen WHERE id = ?', (aktuelle_frage_id,))
    korrekte_antwort, korrekte_antworten = cursor.fetchone()
    
    # Überprüfen, ob mehrere Antworten möglich sind
    if korrekte_antworten and korrekte_antworten.strip("[]").replace(" ", "").isdigit():
        korrekte_antworten_liste = {int(x) for x in korrekte_antworten.strip("[]").split(',') if x.strip().isdigit()}
        ausgewahlte_antworten = {i + 1 for i, var in enumerate(check_vars) if var.get() == 1}
        if ausgewahlte_antworten == korrekte_antworten_liste:
            punkte += 1
            messagebox.showinfo("Richtig", "Ihre Antwort ist richtig!")
            aktuelle_frage_id += 1
            # Fortschritt speichern
            fortschritt_speichern({'punkte': punkte, 'aktuelle_frage_id': aktuelle_frage_id, 'gesamtwiederholungen': gesamtwiederholungen})
            naechste_frage()
        else:
            antwort_falsch()
    else:
        # Index der korrekten Antwort ermitteln (beginnend bei 0)
        korrekte_antwort_index = korrekte_antwort - 1
        # Überprüfen, ob die ausgewählte Antwort korrekt ist
        if check_vars[korrekte_antwort_index].get() == 1:
            punkte += 1
            messagebox.showinfo("Richtig", "Ihre Antwort ist richtig!")
            aktuelle_frage_id += 1
            # Fortschritt speichern
            fortschritt_speichern({'punkte': punkte, 'aktuelle_frage_id': aktuelle_frage_id, 'gesamtwiederholungen': gesamtwiederholungen})
            naechste_frage()
        else:
            antwort_falsch()      

# GUI-Elemente
frage_label = tk.Label(root, text="", font=('Helvetica', 16))
frage_label.pack(pady=20)

punkte_label = tk.Label(root, text="", font=('Helvetica', 14))
punkte_label.pack(pady=10)

wiederholungen_label = tk.Label(root, text="Gesamtwiederholungen: 0", font=('Helvetica', 14))
wiederholungen_label.pack(pady=10)

check_vars = [tk.IntVar() for _ in range(4)]
antwort1_check = tk.Checkbutton(root, text="", variable=check_vars[0])
antwort2_check = tk.Checkbutton(root, text="", variable=check_vars[1])
antwort3_check = tk.Checkbutton(root, text="", variable=check_vars[2])
antwort4_check = tk.Checkbutton(root, text="", variable=check_vars[3])
antwort1_check.pack()
antwort2_check.pack()
antwort3_check.pack()
antwort4_check.pack()

bestaetigen_button = tk.Button(root, text="Antwort bestätigen", command=antwort_ueberpruefen)
bestaetigen_button.pack(pady=20)

# Gesamtpunktzahl beim Start berechnen und erste Frage laden
# Beim Start des Programms nach altem Test fragen
alten_test_fortsetzen()
gesamtpunkte_berechnen()
naechste_frage()

# Hauptloop der Anwendung
root.mainloop()
