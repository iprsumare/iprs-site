"""Converte uma página completa (com <head>, <style>, <body> e <script>) num trecho para colar
num bloco "HTML personalizado" do WordPress.

- A página vai dentro de um Shadow DOM: o tema do WordPress não altera o visual dela,
  e o CSS dela não vaza para o resto do site.
- O WordPress troca "&" por "&#038;" dentro de <script> ao salvar, o que quebra o código.
  Por isso o script vai codificado em base64.
- Acentos e símbolos viram códigos (&#233; no HTML, \\e9 no CSS): o texto não se deforma
  se a cópia ou o WordPress usarem outra codificação. O resultado é só ASCII.
- O script da página pode usar document.getElementById/querySelector(All): aqui eles
  passam a procurar dentro da página (raiz)."""
import base64, re


def ascii_seguro(texto):
    partes = re.split(r"(<style>.*?</style>)", texto, flags=re.S)
    saida = []
    for parte in partes:
        if parte.startswith("<style>"):
            saida.append(re.sub(r"[^\x00-\x7f]", lambda m: "\\%x " % ord(m.group(0)), parte))
        else:
            saida.append(re.sub(r"[^\x00-\x7f]", lambda m: "&#%d;" % ord(m.group(0)), parte))
    return "".join(saida)


def para_wordpress(html, id_pagina, titulo, fundo_claro, fundo_escuro):
    estilo = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    corpo = re.search(r"<body>(.*?)<script>", html, re.S).group(1).strip()
    codigo = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    fontes = re.search(r'<link href="https://fonts.googleapis.com/css2[^>]*>', html).group(0)

    for a, b in [(':root[data-theme="dark"]', ':host([data-theme="dark"])'),
                 (':root:not([data-theme="light"])', ':host(:not([data-theme="light"]))'),
                 (":root", ":host"), ("  html { -webkit-text-size-adjust: 100%; }\n", ""), ("  body {", "  .pagina {")]:
        estilo = estilo.replace(a, b)
    assert ":host" in estilo and ".pagina {" in estilo
    for a in ["getElementById", "querySelectorAll", "querySelector"]:
        codigo = codigo.replace("document." + a, "raiz." + a)
    codigo_b64 = base64.b64encode(codigo.encode("utf-8")).decode()

    i = id_pagina
    wp = f"""<!-- {titulo}. Gerado pelas ferramentas do repositorio iprs-site - nao edite aqui. -->
{fontes}
<style>
  #{i} {{ width: 100vw; max-width: none !important; margin: 0 0 0 calc(50% - 50vw) !important; padding: 0 !important; min-height: 100vh; background: {fundo_claro}; }}
  @media (prefers-color-scheme: dark) {{ #{i} {{ background: {fundo_escuro}; }} }}
  body {{ overflow-x: clip; }}
  /* tira os respiros do tema só nesta página */
  body:has(#{i}) {{ background: {fundo_claro}; }}
  @media (prefers-color-scheme: dark) {{ body:has(#{i}) {{ background: {fundo_escuro}; }} }}
  body:has(#{i}) .wp-site-blocks {{ padding-top: 0 !important; padding-bottom: 0 !important; }}
  body:has(#{i}) .wp-site-blocks main > * {{ margin-block-start: 0 !important; }}
  body:has(#{i}) .wp-site-blocks main > .wp-block-group:empty {{ display: none; }}
  .wp-block-post-content:has(#{i}) > * {{ margin-block-start: 0 !important; }}
</style>
<div id="{i}"></div>
<template id="{i}-modelo"><style>{estilo}</style><div class="pagina">{corpo}</div></template>
<script>
(function () {{
  const host = document.getElementById("{i}");
  if (host.shadowRoot) return;
  const raiz = host.attachShadow({{ mode: "open" }});
  raiz.appendChild(document.getElementById("{i}-modelo").content.cloneNode(true));
  const bytes = Uint8Array.from(atob("{codigo_b64}"), c => c.charCodeAt(0));
  new Function("raiz", new TextDecoder().decode(bytes))(raiz);
}})();
</script>
"""
    wp = ascii_seguro(wp)
    assert wp.isascii()
    return wp
