# temp_code.py

"""Modul zum sicheren Öffnen und Lesen des Inhalts einer Datei."""

with open('file.txt', 'r', encoding='utf-8') as file:  # Spezifizierung der Kodierung
    contents = file.read()

print(contents)
