"""Gera os QR codes da página de links em qrcode/ e confere se cada um abre o endereço certo.
- qrcode-links.svg / .png: QR simples em Azul Renovado (gráfica, impressos, slides)
- qrcode-links-logo.png: QR com o símbolo no centro
- qrcode-links-cartaz.png: cartão pronto (QR + símbolo + chamada), bom para telão e stories
Precisa do Google Chrome instalado."""
import os, subprocess, tempfile
import segno, cv2

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(RAIZ, "qrcode")
URL = "https://iprsumare.com.br/links"
AZUL = "#102A43"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)

# Correção de erro alta (H): aguenta o símbolo cobrindo o centro
qr = segno.make(URL, error="h", micro=False)
qr.save(os.path.join(OUT, "qrcode-links.svg"), scale=10, border=4, dark=AZUL, light="#FFFFFF", title="QR code: " + URL)
qr.save(os.path.join(OUT, "qrcode-links.png"), scale=40, border=4, dark=AZUL, light="#FFFFFF")

qr_sem_borda = qr.svg_data_uri(scale=10, border=0, dark=AZUL, light="#FFFFFF")
simbolo = "file://" + os.path.abspath(os.path.join(RAIZ, "logo", "iprs-simbolo-cor-negativo.svg"))
FONTES = '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Inter:wght@500&display=swap" rel="stylesheet">'

def qr_com_logo(px):
    return f"""<div style="position:relative;width:{px}px;height:{px}px">
      <img src="{qr_sem_borda}" style="width:100%;height:100%;display:block;image-rendering:pixelated">
      <div style="position:absolute;left:50%;top:50%;width:{px*0.24:.0f}px;height:{px*0.24:.0f}px;transform:translate(-50%,-50%);
        background:#fff;border-radius:50%;display:grid;place-items:center">
        <img src="{simbolo}" style="width:88%;height:88%"></div></div>"""

LOGO = f"""<!doctype html><html><body style="margin:0;width:1200px;height:1200px;background:#fff;display:grid;place-items:center">
{qr_com_logo(1000)}</body></html>"""

CARTAZ = f"""<!doctype html><html><head><meta charset="utf-8">{FONTES}</head>
<body style="margin:0;width:1080px;height:1350px;background:{AZUL};font-family:Montserrat,sans-serif;color:#fff;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px">
  <img src="{simbolo}" style="width:150px;height:150px">
  <div style="text-align:center;line-height:1.05">
    <div style="font-size:30px;font-weight:700;letter-spacing:.14em;color:#4FB8CF">2ª IGREJA PRESBITERIANA</div>
    <div style="font-size:30px;font-weight:700;letter-spacing:.14em;color:#4FB8CF;margin-top:6px">RENOVADA DE SUMARÉ</div>
  </div>
  <div style="background:#fff;border-radius:36px;padding:44px">{qr_com_logo(560)}</div>
  <div style="text-align:center">
    <div style="font-size:46px;font-weight:800">Horários, avisos e como chegar</div>
    <div style="font-family:Inter,sans-serif;font-size:32px;color:rgba(255,255,255,.75);margin-top:14px">iprsumare.com.br/links</div>
  </div></body></html>"""

def foto(html, saida, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--virtual-time-budget=4000", f"--window-size={w},{h}", f"--screenshot={saida}", "file://" + t.name],
                   check=True, capture_output=True)
    os.unlink(t.name)

foto(LOGO, os.path.join(OUT, "qrcode-links-logo.png"), 1200, 1200)
foto(CARTAZ, os.path.join(OUT, "qrcode-links-cartaz.png"), 1080, 1350)

# Confere a leitura de cada imagem
leitor = cv2.QRCodeDetector()
for nome in ["qrcode-links.png", "qrcode-links-logo.png", "qrcode-links-cartaz.png"]:
    img = cv2.imread(os.path.join(OUT, nome))
    texto, _, _ = leitor.detectAndDecode(img)
    if not texto:  # imagens grandes: tenta reduzida
        texto, _, _ = leitor.detectAndDecode(cv2.resize(img, None, fx=0.5, fy=0.5))
    print(("OK  " if texto == URL else "ERRO"), nome, "→", texto or "(não leu)")
    assert texto == URL, nome
