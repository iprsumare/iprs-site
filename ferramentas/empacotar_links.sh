#!/bin/sh
# Gera dist/links.zip para enviar à Hostinger (descompactar dentro de public_html).
set -e
cd "$(dirname "$0")/.."
.venv/bin/python ferramentas/build_links.py
mkdir -p dist && rm -f dist/links.zip
zip -q -X dist/links.zip links/index.html links/compartilhar.png links/icone.png
unzip -l dist/links.zip
