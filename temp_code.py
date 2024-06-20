import tkinter as tk
import pyautogui

# Erweiterung der Liste um 30 zusätzliche Windows 11 Tastenkürzel
additional_shortcuts = {
    "alt+esc": "Durchlaufen sie geöffnete Fenster",
    "alt+f4": "Aktives Fenster schließen",
    "alt+f8": "Zeigt das eingegebene Kennwort auf dem Anmeldebildschirm an",
    "alt+left": "Zurück",
    "alt+pgdn": "Um einen Bildschirm nach unten navigieren",
    "alt+pgup": "Um einen Bildschirm nach oben verschieben",
    "alt+right": "Vorwärts",
    "alt+space": "Kontextmenü für das aktive Fenster öffnen",
    "alt+tab": "Wechseln Sie zwischen geöffneten Apps",
    "ctrl+alt+tab": "Geöffnete Apps anzeigen",
    "ctrl+arrow keys": "Startmenügröße ändern",
    "ctrl+arrow keys (zur Auswahl) + space": "Wählen Sie mehrere Elemente auf dem Desktop oder Explorer aus",
    "ctrl+klicken auf eine gruppierte App-Schaltfläche": "Durchlaufen Sie Fenster in der Gruppe von der Taskleiste aus",
    "ctrl+down": "Bewegen Sie den Cursor an den Anfang des nächsten Absatzes",
    "ctrl+f5": "Aktuelles Fenster aktualisieren",
    "ctrl+left": "Bewegen Sie den Cursor an den Anfang des vorherigen Worts",
    "ctrl+right": "Bewegen Sie den Cursor an den Anfang des nächsten Worts",
    "ctrl+shift": "Tastaturlayout wechseln",
    "ctrl+shift+arrow keys": "Textblock auswählen",
    "ctrl+shift+app-click": "Führen Sie die App über die Taskleiste als Administrator aus",
    "ctrl+shift+esc": "Task-Manager öffnen",
    "ctrl+space": "Aktivieren oder deaktivieren Sie den chinesischen IME",
    "ctrl+up": "Bewegen des Cursors an den Anfang des vorherigen Absatzes",
    "shift+arrow keys": "Wählen Sie mehrere Elemente aus",
    "shift+app-click": "Öffnen Sie eine weitere Instanz einer App über die Taskleiste",
    "shift+f10": "Kontextmenü für ausgewähltes Element öffnen",
    "shift+right-click app-button": "Fenstermenü für die App über die Taskleiste anzeigen",
    "shift+right-click grouped app-button": "Fenstermenü für die Gruppe auf der Taskleiste anzeigen",
    "win+tab": "Vorgangsansicht öffnen",
    "win+ctrl+d": "Hinzufügen eines virtuellen Desktops",
    "win+ctrl+right": "Wechseln Sie zwischen virtuellen Desktops, die Sie auf der rechten Seite erstellt haben",
    "win+ctrl+left": "Wechseln Sie zwischen virtuellen Desktops, die Sie auf der linken Seite erstellt haben",
    "win+ctrl+f4": "Schließen Sie den virtuellen Desktop, den Sie verwenden",
    "win": "Startmenü öffnen",
    "win+a": "Öffnen Sie das Info-Center",
    "win+alt+d": "Datum und Uhrzeit des Öffnens in der Taskleiste",
    "win+alt+number (0-9)": "Öffnen Sie die Sprungliste der App in der Zahlenposition auf der Taskleiste",
    "win+b": "Legen Sie den Fokusbenachrichtigungsbereich auf der Taskleiste fest",
    "win+c": "Copilot öffnen/schließen",
    "win+,": "Vorübergehender Blick auf den Desktop",
    "win+ctrl+d": "Erstellen eines virtuellen Desktops",
    "win+ctrl+enter": "Sprachausgabe öffnen",
    "win+ctrl+f": "Öffnen Sie die Suche nach dem Gerät in einem Domänennetzwerk",
    "win+ctrl+f4": "Schließen Sie den aktiven virtuellen Desktop",
    "win+ctrl+left": "Wechseln Sie zum virtuellen Desktop auf der linken Seite",
    "win+ctrl+number (0-9)": "Wechseln Sie zum letzten aktiven Fenster der App in der Nummernposition auf der Taskleiste",
    "win+ctrl+q": "Öffnen Sie Schnellhilfe",
    "win+ctrl+right": "Wechseln Sie zum virtuellen Desktop auf der rechten Seite",
    "win+ctrl+shift+b": "Reaktivieren Sie das Gerät, wenn sie schwarz oder leer ist",
    "win+ctrl+shift+number (0-9)": "Öffnen Sie eine weitere Instanz als Administrator der App in der Nummerposition auf der Taskleiste",
    "win+ctrl+space": "Ändern Sie die zuvor ausgewählte Eingabeoption",
    "win+d": "Anzeigen und Ausblenden des Desktops",
    "win+down": "App-Fenster minimieren",
    "win+e": "Öffnen Sie Explorer",
    "win+esc": "Bildschirmlupe beenden",
    "win+f": "Starten Sie die Feedback-Hub-App",
    "win+/": "Starten Sie die IME-Neuversion",
    "win+g": "Starten Sie die Spieleleisten-App",
    "win+h": "Funktion zum Öffnen des Diktats",
    "win+home": "Minimieren oder maximieren Sie alle außer dem aktiven Desktopfenster",
    "win+i": "Einstellungen öffnen",
    "win+j": "Legen Sie den Fokus auf einen Tipp für Windows 10 fest, falls zutreffend",
    "win+k": "Öffnen Sie die Verbindungseinstellungen",
    "win+l": "Sperrt den Computer",
    "win+left": "App oder Fenster nach links ausrichten",
    "win+m": "Minimieren Sie alle Fenster",
    "win+-": "Verkleinern Sie die Bildschirmlupe",
    "win+number (0-9)": "Öffnen Sie die App an der Position der Zahl auf der Taskleiste",
    "win+o": "Geräteausrichtung sperren",
    "win+p": "Öffnen Sie die Projekteinstellungen",
    "win+pause": "Dialogfeld 'Systemeigenschaften anzeigen'",
    "win+.;": "Emoji-Bereich öffnen",
    "win+=": "Vergrößern Sie die Bildschirmlupe",
    "win+prtscn": "Erfassen Sie einen vollständigen Screenshot im Ordner 'Screenshots'"
}

# Funktion zum Ausführen eines Shortcuts
def execute_shortcut(shortcut):
    try:
        keys = shortcut.lower().split('+')
        pyautogui.hotkey(*keys)
    except Exception as e:
        print(f"Fehler: {e}")

# Funktion zum Scrollen mit dem Mausrad
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Windows 11 Tastenkombinationen")
root.geometry('940x680')  # Setzt die Fenstergröße auf 640x480

# Scrollbar erstellen
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Canvas erstellen
canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar konfigurieren
scrollbar.config(command=canvas.yview)

# Frame für Buttons erstellen
frame_buttons = tk.Frame(canvas)

# Canvas mit Frame verbinden
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Funktion zum Aktualisieren der Scrollregion
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

frame_buttons.bind('<Configure>', on_configure)

# Binden des Mausrads an die Canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Buttons für jeden Shortcut im Frame erstellen
for shortcut, description in additional_shortcuts.items():
    button = tk.Button(frame_buttons, text=f"{shortcut.upper()}: {description}", command=lambda sc=shortcut: execute_shortcut(sc))
    button.pack(fill='x', padx=10, pady=5)

# Hauptloop starten
root.mainloop()
