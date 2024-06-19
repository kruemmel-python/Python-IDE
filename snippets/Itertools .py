# temp_code.py

"""Modul zur Generierung aller möglichen Kombinationen von Paaren in einer Liste."""

import itertools

# Alle möglichen Kombinationen von Paaren in einer Liste
pairs = list(itertools.combinations([1, 2, 3], 2))

print(pairs)
