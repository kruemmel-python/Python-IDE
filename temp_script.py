import os
import zipfile
import tkinter as tk
from tkinter import filedialog

def entpacke_zip(quellverzeichnis, zielverzeichnis):
    # Gehe durch jedes Datei im Quellverzeichnis
    for datei in os.listdir(quellverzeichnis):
        if datei.endswith('.zip'):
            # Erstelle einen Pfad zur ZIP-Datei
            zip_pfad = os.path.join(quellverzeichnis, datei)
            # Erstelle einen Ordner im Zielverzeichnis mit dem gleichen Namen wie die ZIP-Datei (ohne die .zip-Endung)
            ordner_name = datei[:-4]
            extraktions_pfad = os.path.join(zielverzeichnis, ordner_name)
            os.makedirs(extraktions_pfad, exist_ok=True)
            
            # Entpacke die ZIP-Datei in den neu erstellten Ordner
            with zipfile.ZipFile(zip_pfad, 'r') as zip_ref:
                zip_ref.extractall(extraktions_pfad)

    print('Alle ZIP-Dateien wurden erfolgreich entpackt.')

def ordner_auswaehlen():
    root = tk.Tk()
    root.withdraw()  # Verstecke das Tkinter-Hauptfenster

    # Öffne den Dialog zur Auswahl des Quellverzeichnisses
    quellverzeichnis = filedialog.askdirectory(title='Wähle das Verzeichnis mit den ZIP-Dateien')
    if not quellverzeichnis:
        print("Kein Quellverzeichnis ausgewählt.")
        return

    # Öffne den Dialog zur Auswahl des Zielverzeichnisses
    zielverzeichnis = filedialog.askdirectory(title='Wähle das Zielverzeichnis für das Entpacken')
    if not zielverzeichnis:
        print("Kein Zielverzeichnis ausgewählt.")
        return

    entpacke_zip(quellverzeichnis, zielverzeichnis)

ordner_auswaehlen()
