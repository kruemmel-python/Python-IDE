# temp_code.py

"""Modul zur Fehlerbehandlung beim Öffnen einer Datei."""

try:
    with open('file.txt', 'r', encoding='utf-8') as file:  # Spezifizierung der Kodierung
        contents = file.read()
except FileNotFoundError:
    print("Die Datei wurde nicht gefunden.")
