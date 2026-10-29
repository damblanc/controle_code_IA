# generate_pdf_report.py — transforme test_results.json en rapport PDF
import json
import os
import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

VERT = colors.HexColor("#E2EFDA")
ROUGE = colors.HexColor("#FFCCCC")
JAUNE = colors.HexColor("#FFF2CC")
BLEU = colors.HexColor("#1F4E79")


def charger_resultats(fichier="test_results.json"):
    with open(fichier, encoding="utf-8") as f:
        return json.load(f)


def tableau_resume(resume):
    total = resume.get("total", 0)
    reussis = resume.get("passed", 0)
    echoues = resume.get("failed", 0) + resume.get("error", 0)
    t = Table([["Total", "Réussis", "Échoués"], [total, reussis, echoues]],
              colWidths=[5.5 * cm] * 3)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (1, 1), (1, 1), VERT),
        ("BACKGROUND", (2, 1), (2, 1), ROUGE if echoues else VERT),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def tableau_detail(tests):
    lignes = [["#", "Test", "Classe", "Statut", "Durée (s)"]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLEU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (2, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]
    for i, test in enumerate(tests, start=1):
        morceaux = test.get("nodeid", "").split("::")   # fichier::Classe::test
        classe = morceaux[1] if len(morceaux) >= 3 else "-"
        statut = test.get("outcome", "inconnu")
        duree = test.get("call", {}).get("duration", 0)
        lignes.append([i, morceaux[-1], classe, statut.upper(), f"{duree:.4f}"])
        couleur = {"passed": VERT, "failed": ROUGE}.get(statut, JAUNE)
        style.append(("BACKGROUND", (0, i), (-1, i), couleur))
    t = Table(lignes, colWidths=[1 * cm, 7.5 * cm, 3.5 * cm, 2.5 * cm, 2.5 * cm], repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def generer_pdf(resultats, fichier="test_report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(fichier, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm,
                            leftMargin=2 * cm, rightMargin=2 * cm)
    contenu = [
        Paragraph("Rapport de tests Pytest", styles["Title"]),
        Paragraph(f"Généré le {datetime.now():%d/%m/%Y à %H:%M}", styles["Normal"]),
        Spacer(1, 0.5 * cm),
        tableau_resume(resultats.get("summary", {})),
        Spacer(1, 0.6 * cm),
        tableau_detail(resultats.get("tests", [])),
    ]
    doc.build(contenu)
    print(f"=> Rapport PDF généré : {fichier}")


if __name__ == "__main__":
    if not os.path.exists("test_results.json"):
        print("ERREUR : test_results.json introuvable (lancer d'abord pytest avec --json-report).")
        sys.exit(1)
    generer_pdf(charger_resultats())
