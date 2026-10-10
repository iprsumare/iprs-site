"""Monta o guia (index.html) a partir de guia.template.html, embutindo os logos para o arquivo funcionar sozinho."""
import base64, os, re
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OLD = os.path.join(D, "logo", "legado", "iprs-logo-antigo-320px.png")

def data_uri(name):
    path = OLD if name == "old-logo.png" else os.path.join(D, "logo", name)
    mime = "image/png" if name.endswith(".png") else "image/svg+xml"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

html = open(os.path.join(D, "guia.template.html"), encoding="utf-8").read()
html = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: data_uri(m.group(1)), html)
open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(html)
print("index.html", len(html))
