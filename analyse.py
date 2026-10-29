# analyse.py — fait relire mycode.py par Gemini et enregistre l'avis
import os
import sys

from google import genai

FICHIER_CODE = "mycode.py"
FICHIER_RESULTAT = "analyse_result.txt"

# Modèles essayés dans l'ordre : un alias qui suit les nouvelles versions de Google,
# puis un modèle stable de secours (liste à jour : ai.google.dev/gemini-api/docs/models)
MODELES = ["gemini-flash-latest", "gemini-3.5-flash-lite"]

# ✍️ EXERCICE 1 : remplace « À COMPLÉTER » par ta consigne pour Gemini.
# Indique : son rôle, ce qu'il doit produire, la forme de la réponse, la langue.
# Ne touche pas à la ligne {code} : c'est là que le code sera inséré.
PROMPT = """À COMPLÉTER

Code à analyser :
{code}
"""


def ecrire_resultat(texte):
    with open(FICHIER_RESULTAT, "w", encoding="utf-8") as f:
        f.write(texte)


def analyser(code, cle):
    """Envoie le code à Gemini. Renvoie (texte, modèle) ou (None, message d'erreur)."""
    client = genai.Client(api_key=cle)
    derniere_erreur = ""
    for modele in MODELES:
        try:
            reponse = client.models.generate_content(
                model=modele, contents=PROMPT.format(code=code))
            if reponse.text:
                return reponse.text, modele
            derniere_erreur = f"{modele} : réponse vide"
        except Exception as e:  # quota dépassé, modèle retiré, réseau…
            derniere_erreur = f"{modele} : {e}"
            print(f"AVERTISSEMENT : échec avec {derniere_erreur}", file=sys.stderr)
    return None, derniere_erreur


def main():
    cle = os.environ.get("GOOGLE_AI_KEY")
    if not cle:
        msg = "Analyse IA non réalisée : variable GOOGLE_AI_KEY absente."
        print(msg)
        ecrire_resultat(msg)
        return 0   # on ne bloque pas le pipeline

    with open(FICHIER_CODE, encoding="utf-8") as f:
        code = f.read()

    print("=> Envoi du code à Gemini...")
    texte, info = analyser(code, cle)
    if texte:
        print(f"=== ANALYSE GEMINI ({info}) ===\n")
        print(texte)
        ecrire_resultat(f"Modèle : {info}\n\n{texte}")
    else:
        msg = f"Analyse IA indisponible ({info})."
        print(msg)
        ecrire_resultat(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
