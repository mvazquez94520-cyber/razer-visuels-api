"""Construit le site statique (GitHub Pages) à partir de images/ et price_list.csv.

Usage : python build.py   (BASE_URL optionnel)
"""
import os
import sys
from collections import defaultdict
from pathlib import Path

from visuels.catalog import CsvCatalog
from visuels.exporter import JsonExporter
from visuels.matching import Matcher
from visuels.models import Report

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_BASE_URL = "https://mvazquez94520-cyber.github.io/razer-visuels-api"


def list_images(folder: Path) -> list[Path]:
    return sorted(p for p in folder.rglob("*") if p.suffix.lower() in EXTENSIONS)


def main() -> int:
    products = CsvCatalog(ROOT / "price_list.csv").load()
    matcher = Matcher(products)
    exporter = JsonExporter(ROOT / "site", os.environ.get("BASE_URL", DEFAULT_BASE_URL))
    exporter.reset()

    report = Report()
    by_product = defaultdict(list)
    audit = []

    for img in list_images(IMAGES):
        rel = img.relative_to(IMAGES).as_posix()
        match, ambiguous = matcher.match(img.stem)
        if match:
            by_product[match.product.pn].append(rel)
            exporter.copy_image(img, rel)
            audit.append({"photo": rel, "pn": match.product.pn, "par": match.by})
        elif ambiguous:
            report.photos_ambigues.append({"photo": rel, "produits": [p.pn for p in ambiguous]})
        else:
            report.photos_sans_produit.append(rel)

    index = []
    for p in products:
        rels = by_product.get(p.pn)
        if rels:
            index.append(exporter.write_product(p, rels))
        else:
            report.produits_sans_photo.append({"pn": p.pn, "ean": p.ean, "model": p.model})

    exporter.write_index(index)
    exporter.write_report(
        {
            "produits_avec_photos": len(index),
            "produits_sans_photo": report.produits_sans_photo,
            "photos_sans_produit": report.photos_sans_produit,
            "photos_ambigues": report.photos_ambigues,
            "associations": audit,
        }
    )

    print(f"{len(index)}/{len(products)} produits avec photos, {len(audit)} photos associées")
    print(f"Sans photo : {len(report.produits_sans_photo)} | "
          f"Photos sans produit : {len(report.photos_sans_produit)} | "
          f"Ambiguës : {len(report.photos_ambigues)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
