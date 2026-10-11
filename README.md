# 2ª Igreja Presbiteriana Renovada de Sumaré — site

Identidade visual e páginas públicas da 2ª IPR Sumaré, igreja local da Igreja Presbiteriana Renovada do Brasil.

| Caminho | O que é |
|---|---|
| `index.html` | Guia de identidade visual: logo, regras de uso, paleta, tipografia |
| `guia-wordpress.html` | O mesmo guia, para colar no WordPress |
| `links/index.html` | Página de links (substitui o Linktree) com a agenda da semana |
| `logo/` | Logo em SVG (vetor) e `logo/png/` em alta resolução |
| `logo/legado/` | Logos originais em PNG, usados como referência no redesenho |
| `qrcode/` | QR codes para `iprsumare.com.br/links` (SVG, PNG, com logo e cartaz) |
| `ferramentas/` | Scripts que geram o logo, as páginas e os QR codes |

## Identidade

- **Cores:** Azul Renovado `#102A43`, Azul Céu `#4FB8CF`, Preto `#0B0D10`, Branco `#FFFFFF`. A chama (`#FFCB3D → #F7931E → #E23B2E`) só aparece no logo.
- **Fontes:** Montserrat (títulos), Inter (textos), Lora Italic (versículos).

## Agenda

A página de links lê a planilha **IPRS - Agenda de encontros** no Google Drive:

- **Programação fixa:** a regra da semana.
- **Exceções:** cancelar, alterar ou adicionar encontros em datas específicas.

A planilha precisa estar compartilhada como "Qualquer pessoa com o link: Leitor". Se ela não responder, a página usa a programação fixa que está em `links/template.html`.

## Editar

As páginas publicadas (`index.html` e `links/index.html`) são geradas. Edite os modelos e rode o build:

```bash
python3 -m venv .venv && .venv/bin/pip install -r ferramentas/requirements.txt
.venv/bin/python ferramentas/build_links.py   # links/template.html → links/index.html
.venv/bin/python ferramentas/build_guia.py    # guia.template.html → index.html e guia-wordpress.html
.venv/bin/python ferramentas/build_logo.py    # só se mudar o desenho do logo
```

## Publicar a página de links (WordPress)

A página fica em **https://iprsumare.com.br/links/** como uma página comum do WordPress.
O build gera `links/wordpress.html`, que vai inteiro num bloco **HTML personalizado**. A página roda isolada (Shadow DOM): o tema não muda o visual dela e ela não interfere no resto do site.

**Uma vez só — modelo em branco:** Aparência → Editor → Modelos → Adicionar modelo → *Modelo personalizado* "Em branco", com apenas o bloco **Conteúdo** (sem cabeçalho, rodapé nem título).

**Publicar ou atualizar:**
1. `.venv/bin/python ferramentas/build_links.py && LANG=en_US.UTF-8 pbcopy < links/wordpress.html` (copia o código)
2. WordPress → Páginas → Link Tree (endereço `links`) → apague o conteúdo → bloco **HTML personalizado** → cole.
3. Painel lateral → Modelo: **Em branco** → Atualizar.

**Prévia no WhatsApp e ícone:** envie `links/compartilhar.png` como Imagem destacada da página e `links/icone-site-512.png` em Configurações/Identidade do site → Ícone do site.

## Publicar o guia (WordPress)

Mesmo processo da página de links, numa página própria (sugestão: `identidade-visual`, modelo **Em branco**):

```bash
.venv/bin/python ferramentas/build_guia.py && LANG=en_US.UTF-8 pbcopy < guia-wordpress.html
```

Os logos vão embutidos uma vez só (colorido e uma cor); as outras versões e os downloads em SVG e PNG são gerados no navegador. As conversões para o WordPress ficam em `ferramentas/wordpress.py`, usado pelas duas páginas.

Para mudar o endereço, edite `URL` em `ferramentas/build_links.py` e em `ferramentas/gerar_qrcode.py` (e rode `.venv/bin/python ferramentas/gerar_qrcode.py`).

Créditos: Montserrat (SIL Open Font License, ver `ferramentas/OFL-Montserrat.txt`) e mapa Natural Earth (domínio público).

## Guia publicado (GitHub Pages)

**https://iprsumare.github.io/iprs-site/**: atualiza sozinho a cada `push` na `main` que mude o guia, os logos ou os QR codes (`.github/workflows/pages.yml`). Só vão para o site `index.html`, `logo/` (sem o legado) e `qrcode/`.
