from dataclasses import dataclass, field


@dataclass(frozen=True)
class Product:
    ean: str
    pn: str
    model: str


@dataclass(frozen=True)
class Match:
    product: Product
    by: str  # "pn" ou "model"


@dataclass
class Report:
    produits_sans_photo: list = field(default_factory=list)
    photos_sans_produit: list = field(default_factory=list)
    photos_ambigues: list = field(default_factory=list)
