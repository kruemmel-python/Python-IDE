# temp_code.py

"""Modul mit einer Funktion, die beliebige Argumente akzeptiert."""

def func(*args, **kwargs):
    """Eine Funktion, die alle übergebenen Positional- und Schlüsselwortargumente ausgibt."""
    print(args)
    print(kwargs)

# Beispielaufruf der Funktion
func(1, 2, drei='3', vier='4')
