# temp_code.py

"""Modul zum Sortieren einer Liste von Tupeln nach dem zweiten Element."""

# Liste von Tupeln nach dem zweiten Element sortieren
sorted_list = sorted([(1, 'eins'), (2, 'zwei'), (3, 'drei')], key=lambda x: x[1])

print(sorted_list)
