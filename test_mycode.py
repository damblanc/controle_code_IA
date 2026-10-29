# test_mycode.py — les tests décrivent le comportement attendu (le « contrat »)
import pytest
from mycode import division, factorielle


class TestDivision:
    def test_positifs(self):
        assert division(10, 2) == 5.0

    def test_negatif_au_numerateur(self):
        assert division(-10, 2) == -5.0

    def test_numerateur_zero(self):
        assert division(0, 5) == 0.0

    def test_flottants(self):
        assert division(1, 3) == pytest.approx(0.333, rel=1e-2)

    def test_division_par_zero_leve_valueerror(self):
        with pytest.raises(ValueError):
            division(10, 0)


class TestFactorielle:
    def test_zero(self):
        assert factorielle(0) == 1

    def test_un(self):
        assert factorielle(1) == 1

    def test_cinq(self):
        assert factorielle(5) == 120

    def test_negatif_leve_valueerror(self):
        # ✍️ EXERCICE 2 : remplace la ligne ci-dessous par un test qui vérifie que
        # factorielle(-1) lève une ValueError (modèle : test_division_par_zero_leve_valueerror)
        pytest.fail("Test à écrire")

    def test_flottant_leve_valueerror(self):
        with pytest.raises(ValueError):
            factorielle(3.5)
