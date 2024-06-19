# temp_code.py

"""Modul für einen unendlichen Zählergenerator."""

def count_up(start=0):
    """Generator, der unendlich Zahlen ab einem Startwert hochzählt."""
    while True:
        yield start
        start += 1

# Beispielaufruf des Generators
counter = count_up()
for _ in range(5):
    print(next(counter))  # Ausgabe: 0, 1, 2, 3, 4
