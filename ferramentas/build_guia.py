"""Monta o guia de identidade a partir de guia.template.html:
- index.html: página completa (abre sozinha no navegador)
- guia-wordpress.html: para colar num bloco "HTML personalizado" do WordPress
Os logos entram uma única vez (colorido e uma cor); o script deriva as outras versões
e gera os downloads (SVG e PNG) na hora."""
import base64, io, os, sys
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wordpress import para_wordpress

b64 = lambda dados: base64.b64encode(dados).decode()
ler = lambda *p: open(os.path.join(D, *p), "rb").read()

# Exemplo do "não faça": o PNG antigo, reduzido (de propósito fica ruim)
antigo = Image.open(os.path.join(D, "logo", "legado", "iprs-logo-antigo-320px.png")).convert("RGBA").resize((110, 110))
buf = io.BytesIO(); antigo.save(buf, "PNG", optimize=True)

ativos = {"logo-cor": ler("logo", "iprs-logo-cor.svg"), "logo-mono": ler("logo", "iprs-logo-preto.svg"),
          "qrcode": ler("qrcode", "qrcode-links.svg"), "antigo": buf.getvalue()}
ativos_html = "\n".join(f'<script type="text/x-ativo" data-nome="{n}">{b64(v)}</script>' for n, v in ativos.items())

html = open(os.path.join(D, "guia.template.html"), encoding="utf-8").read()
html = (html.replace("{{ATIVOS}}", ativos_html)
            .replace("{{SCRIPT}}", open(os.path.join(D, "ferramentas", "guia.js"), encoding="utf-8").read())
            .replace("{{FAVICON}}", "data:image/svg+xml;base64," + b64(ler("logo", "iprs-simbolo-azul.svg"))))
open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(html)
print("index.html", len(html))

wp = para_wordpress(html, "iprs-guia", "2a IPR Sumare - guia de identidade visual", "#FFFFFF", "#0B0D10")
open(os.path.join(D, "guia-wordpress.html"), "w", encoding="utf-8").write(wp)
print("guia-wordpress.html", len(wp))
