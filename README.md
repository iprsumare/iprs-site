# 2ª Igreja Presbiteriana Renovada de Sumaré — site

Identidade visual e páginas públicas da 2ª IPR Sumaré, igreja local da Igreja Presbiteriana Renovada do Brasil.

| Caminho | O que é |
|---|---|
| `index.html` | Guia de identidade visual: logo, regras de uso, paleta, tipografia |
| `links/index.html` | Página de links (substitui o Linktree) com a agenda da semana |
| `logo/` | Logo em SVG (vetor) e `logo/png/` em alta resolução |
| `logo/legado/` | Logos originais em PNG, usados como referência no redesenho |
| `ferramentas/` | Scripts que geram o logo e as páginas |

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
.venv/bin/python ferramentas/build_guia.py    # guia.template.html → index.html
.venv/bin/python ferramentas/build_logo.py    # só se mudar o desenho do logo
```

## Publicar a página de links (Hostinger)

A página fica em **https://iprsumare.com.br/links/**, como uma pasta comum ao lado do WordPress. Não precisa importar nada no WordPress.

1. Gere o pacote: `./ferramentas/empacotar_links.sh` → `dist/links.zip`
2. hPanel → Arquivos → Gerenciador de arquivos → `public_html`
3. Envie o `links.zip` e use **Extrair** ali mesmo. O resultado deve ser `public_html/links/index.html`.
4. Para atualizar depois, repita, sobrescrevendo os arquivos.

Não crie no WordPress uma página com o endereço `links`, para não disputar o mesmo endereço.
Para mudar o endereço, edite `URL` em `ferramentas/build_links.py`.

Créditos: Montserrat (SIL Open Font License, ver `ferramentas/OFL-Montserrat.txt`) e mapa Natural Earth (domínio público).
