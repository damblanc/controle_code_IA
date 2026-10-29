# mycode.py — version initiale (contient des défauts à trouver)


def division(a, b):
    """Divise a par b et retourne le résultat."""
    return a / b


def factorielle(n):
    """Calcule la factorielle de n (récursif)."""
    if n == 0:
        return 1
    return n * factorielle(n - 1)
