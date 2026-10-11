"""Gera avatares quadrados em logo/png/ a partir do símbolo.
- avatar-github.png (1000x1000): Azul Renovado com respiro para o canto arredondado do GitHub
Precisa do Google Chrome instalado."""
import os, subprocess, tempfile
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
simbolo = "file://" + os.path.abspath(os.path.join(RAIZ, "logo", "iprs-simbolo-cor-negativo.svg"))

def foto(html, saida, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=3000", f"--window-size={w},{h}", f"--screenshot={saida}", "file://" + t.name],
                   check=True, capture_output=True)
    os.unlink(t.name); print(saida)

GITHUB = f"""<!doctype html><html><body style="margin:0;width:1000px;height:1000px;background:#102A43;display:grid;place-items:center">
<img src="{simbolo}" style="width:720px;height:720px"></body></html>"""
foto(GITHUB, os.path.join(RAIZ, "logo", "png", "avatar-github.png"), 1000, 1000)
