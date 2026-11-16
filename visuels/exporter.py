import json
import shutil
from pathlib import Path
from urllib.parse import quote


class JsonExporter:
    """Écrit le site statique : produits/<PN>.json, ean/<EAN>.json, index.json, rapport.json."""

    def __init__(self, out: Path, base_url: str):
        self.out = out
        self.base_url = base_url.rstrip("/")

    def reset(self):
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)

    def copy_image(self, src: Path, rel: str):
        dst = self.out / "images" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def image_url(self, rel: str) -> str:
        return f"{self.base_url}/images/{quote(rel)}"

    def _write(self, rel: str, data):
        path = self.out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_product(self, product, rels: list[str]):
        data = {
            "pn": product.pn,
            "ean": product.ean,
            "model": product.model,
            "count": len(rels),
            "images": [
                {"url": self.image_url(r), "principal": i == 0} for i, r in enumerate(rels)
            ],
        }
        self._write(f"produits/{product.pn}.json", data)
        self._write(f"ean/{product.ean}.json", data)
        return {"pn": product.pn, "ean": product.ean, "model": product.model, "count": len(rels)}

    def write_index(self, entries):
        self._write("index.json", entries)

    def write_report(self, data):
        self._write("rapport.json", data)
