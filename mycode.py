# mycode.py — version initiale (contient des défauts à trouver)


def division(a, b):
    """Divise a par b et retourne le résultat."""
    if b == 0: 
        raise ValueError("Division par zéro impossible")
    return a / b


def factorielle(n):
    """Calcule la factorielle de n (récursif)."""
    if not isinstance(n, int): 
        raise ValueError("n doit être un nombre entier") 
    if n < 0: 
        raise ValueError("n doit être positif ou nul") 
    if n == 0:
        return 1
    return n * factorielle(n - 1)
