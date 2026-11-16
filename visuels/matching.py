import re
from .models import Match, Product

_BRACKETS = re.compile(r"\[[^\]]*\]|\([^)]*\)")


def normalize(text: str) -> str:
    """minuscules, sans les [2021] / (xx), uniquement lettres et chiffres."""
    return re.sub(r"[^a-z0-9]+", "", _BRACKETS.sub("", text).lower())


class Matcher:
    """Associe un nom de fichier à un produit.

    Règle 1 : le PN complet est dans le nom du fichier (le plus sûr).
    Règle 2 : le Model name est dans le nom du fichier ; le plus long gagne.
    Égalité entre deux produits => ambigu, jamais de choix au hasard.
    """

    def __init__(self, products: list[Product]):
        self.products = products

    def match(self, filename_stem: str):
        """Retourne (Match | None, ambigu: list[Product])."""
        stem = normalize(filename_stem)

        by_pn = [p for p in self.products if normalize(p.pn) in stem]
        if len(by_pn) == 1:
            return Match(by_pn[0], "pn"), []
        if len(by_pn) > 1:
            return None, by_pn

        hits = [(p, normalize(p.model)) for p in self.products]
        hits = [(p, n) for p, n in hits if n and n in stem]
        if not hits:
            return None, []
        longest = max(len(n) for _, n in hits)
        best = [p for p, n in hits if len(n) == longest]
        if len(best) == 1:
            return Match(best[0], "model"), []
        return None, best
