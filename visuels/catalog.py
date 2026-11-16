import csv
from pathlib import Path
from .models import Product


class CsvCatalog:
    """Source des produits : price list CSV (EAN, Product Code, Product Description)."""

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> list[Product]:
        products, seen = [], set()
        with self.path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                p = Product(
                    ean=row["EAN"].strip(),
                    pn=row["Product Code"].strip(),
                    model=row["Product Description"].strip(),
                )
                if not p.pn or not p.ean:
                    raise ValueError(f"Ligne incomplète dans la price list : {row}")
                if p.pn in seen:
                    raise ValueError(f"PN en double dans la price list : {p.pn}")
                seen.add(p.pn)
                products.append(p)
        return products
