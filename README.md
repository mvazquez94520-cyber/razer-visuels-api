# razer-visuels-api

API statique de visuels produits Razer, publiée via GitHub Pages.
Le client appelle un PN (ou un EAN) et reçoit les liens des photos.

## Appels
- Par PN  : `https://mvazquez94520-cyber.github.io/razer-visuels-api/produits/<PN>.json`
- Par EAN : `https://mvazquez94520-cyber.github.io/razer-visuels-api/ean/<EAN>.json`
- Liste   : `.../index.json`
- Contrôle : `.../rapport.json` (photos sans produit, produits sans photo, ambiguïtés)

## Ajouter des produits ou des photos
1. Ajouter la ligne dans `price_list.csv` (EAN, Product Code, Product Description).
2. Déposer les photos dans `images/`.
   - Nom de fichier contenant le **PN complet** (le plus sûr), ou le **Model name** (ex. `Viper V3 HyperSpeed 01.png`).
   - Ordre alphabétique : la première photo est la principale (`01`, `02`...).
3. Commit + push sur `main` : le site se reconstruit et se publie seul.

## Règles d'association (0 erreur)
- PN dans le nom du fichier, sinon Model name (le plus long gagne).
- Cas incertain ou ambigu : la photo n'est rattachée à rien et apparaît dans `rapport.json`.

## Structure
- `visuels/catalog.py` lit la price list
- `visuels/matching.py` associe photo et produit
- `visuels/exporter.py` écrit les JSON
- `build.py` orchestre
