"""Gera links/compartilhar.png (prévia no WhatsApp/redes, 1200x630) e links/icone.png (ícone do celular, 180x180).
Precisa do Google Chrome instalado."""
import os, subprocess, tempfile
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
simbolo = "file://" + os.path.abspath(os.path.join(RAIZ, "logo", "iprs-simbolo-cor-negativo.svg"))
FONTES = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800&display=swap" rel="stylesheet">'
FAIXAS = ('<svg class="faixas" viewBox="160 92 125 125"><path fill="#4FB8CF" fill-rule="evenodd" d="'
          'M171,100.25H222.75A54.25,54.25 0 0 1 222.75,208.75H171Z M171,116.25H222.2A37.875,37.875 0 0 1 222.2,192H171Z '
          'M171,124.1H221.5A30.25,30.25 0 0 1 221.5,184.6H171Z M171,141H216.2A13.875,13.875 0 0 1 216.2,168.75H171Z"/></svg>')

COMPARTILHAR = f"""<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>
body{{margin:0;width:1200px;height:630px;background:#102A43;color:#fff;font-family:Montserrat,sans-serif;overflow:hidden;position:relative}}
.faixas{{position:absolute;right:-120px;top:-60px;width:620px;opacity:.13}}
.c{{position:absolute;left:90px;top:0;bottom:0;display:flex;align-items:center;gap:56px}}
img{{width:250px;height:250px}}
.o{{display:block;font-size:120px;font-weight:800;color:#4FB8CF;line-height:.9;letter-spacing:-.03em}}
.n{{display:block;font-size:50px;font-weight:800;line-height:1;text-transform:uppercase;margin-top:10px}}
.s{{display:block;font-size:28px;font-weight:600;color:rgba(255,255,255,.75);margin-top:26px}}
</style></head><body>{FAIXAS}<div class="c"><img src="{simbolo}"><div>
<span class="o">2ª</span><span class="n">Igreja Presbiteriana<br>Renovada de Sumaré</span>
<span class="s">Horários · Avisos · Como chegar</span></div></div></body></html>"""

ICONE = f"""<!doctype html><html><body style="margin:0;width:180px;height:180px;background:#102A43;display:grid;place-items:center">
<img src="{simbolo}" style="width:150px;height:150px"></body></html>"""

def foto(html, saida, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=4000", f"--window-size={w},{h}", f"--screenshot={saida}", "file://" + t.name],
                   check=True, capture_output=True)
    os.unlink(t.name); print(saida)

foto(COMPARTILHAR, os.path.join(RAIZ, "links", "compartilhar.png"), 1200, 630)
foto(ICONE, os.path.join(RAIZ, "links", "icone.png"), 180, 180)
