"""Monta links/index.html (página completa) e links/wordpress.html (para colar num bloco HTML personalizado do WordPress)
a partir de template.html e dos SVGs do logo."""
import base64, os, re
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(RAIZ, "links")
LOGO = os.path.join(RAIZ, "logo")
URL = "https://iprsumare.com.br/links/"  # endereço onde a página fica publicada
read = lambda p: open(p, encoding="utf-8").read()

simbolo = read(os.path.join(LOGO, "iprs-simbolo-cor-negativo.svg")).strip()
simbolo = re.sub(r"<title>.*?</title>", "", simbolo).replace('role="img"', 'focusable="false"')
favicon = "data:image/svg+xml;base64," + base64.b64encode(read(os.path.join(LOGO, "iprs-simbolo-azul.svg")).encode()).decode()

# Faixas do bojo do R, ampliadas, como textura do topo
faixas = ('<svg class="faixas" viewBox="160 92 125 125" aria-hidden="true"><path fill="#4FB8CF" fill-rule="evenodd" d="'
          'M171,100.25H222.75A54.25,54.25 0 0 1 222.75,208.75H171Z M171,116.25H222.2A37.875,37.875 0 0 1 222.2,192H171Z '
          'M171,124.1H221.5A30.25,30.25 0 0 1 221.5,184.6H171Z M171,141H216.2A13.875,13.875 0 0 1 216.2,168.75H171Z"/></svg>')

html = read(os.path.join(D, "template.html"))
html = html.replace("{{URL}}", URL).replace("{{SIMBOLO}}", simbolo).replace("{{FAVICON}}", favicon).replace("{{FAIXAS}}", faixas)
open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(html)
print("index.html", len(html))

# ---------- Versão para WordPress (bloco "HTML personalizado") ----------
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wordpress import para_wordpress
wp = para_wordpress(html, "iprs-links", "2a IPR Sumare - pagina de links", "#F3F6F9", "#0B141E")
open(os.path.join(D, "wordpress.html"), "w", encoding="utf-8").write(wp)
print("wordpress.html", len(wp))
