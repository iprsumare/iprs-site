// Monta as imagens e os downloads do guia a partir de 2 logos embutidos uma única vez
// (colorido e uma cor). As outras versões são derivadas trocando a cor ou tirando o texto.
(function () {
  const PRETO = "#0B0D10", BRANCO = "#FFFFFF", AZUL = "#102A43";
  const ATIVOS = {};
  document.querySelectorAll('script[type="text/x-ativo"]').forEach(s => { ATIVOS[s.dataset.nome] = s.textContent.trim(); });
  const texto = b64 => new TextDecoder().decode(Uint8Array.from(atob(b64), c => c.charCodeAt(0)));

  // O texto em curva é o primeiro <g> com a cor da tinta; o símbolo é o logo sem ele e com o quadro recortado.
  const semTexto = svg => svg.replace(/<g fill="#0B0D10">.*?<\/g>/s, "").replace('viewBox="0 11 320 295"', 'viewBox="28 39.5 264 264"');
  const tinta = (svg, cor) => svg.split(PRETO).join(cor);
  function svgDe(nome) {
    const cor = texto(ATIVOS["logo-cor"]), mono = texto(ATIVOS["logo-mono"]);
    const tabela = {
      "iprs-logo-cor": cor,
      "iprs-logo-cor-negativo": tinta(cor, BRANCO),
      "iprs-logo-preto": mono,
      "iprs-logo-branco": tinta(mono, BRANCO),
      "iprs-logo-azul": tinta(mono, AZUL),
      "qrcode-links": texto(ATIVOS["qrcode"]),
    };
    if (tabela[nome]) return tabela[nome];
    // símbolo: tira o texto primeiro (ele é achado pela cor preta) e só depois troca a cor
    const simbolos = {
      "iprs-simbolo-cor": semTexto(cor),
      "iprs-simbolo-cor-negativo": tinta(semTexto(cor), BRANCO),
      "iprs-simbolo-preto": semTexto(mono),
      "iprs-simbolo-branco": tinta(semTexto(mono), BRANCO),
      "iprs-simbolo-azul": tinta(semTexto(mono), AZUL),
    };
    if (simbolos[nome]) return simbolos[nome];
    throw new Error("imagem desconhecida: " + nome);
  }

  const urls = {};
  function url(nome) {
    if (nome === "antigo") return "data:image/png;base64," + ATIVOS["antigo"];
    if (!urls[nome]) urls[nome] = URL.createObjectURL(new Blob([svgDe(nome)], { type: "image/svg+xml" }));
    return urls[nome];
  }
  document.querySelectorAll("[data-img]").forEach(el => {
    const u = url(el.dataset.img);
    if (el.tagName.toLowerCase() === "image") el.setAttribute("href", u); else el.src = u;
  });

  // PNG gerado na hora: logo 2000 px, símbolo e QR 1600 px, avatar 1080 px em Azul Renovado
  async function png(nome) {
    const avatar = nome === "avatar";
    const img = new Image();
    img.src = url(avatar ? "iprs-simbolo-cor-negativo" : nome);
    await img.decode();
    const quadrado = avatar || nome.startsWith("iprs-simbolo") || nome === "qrcode-links";
    const W = avatar ? 1080 : quadrado ? 1600 : 2000, H = quadrado ? W : Math.round(W * 295 / 320);
    const c = document.createElement("canvas"); c.width = W; c.height = H;
    const g = c.getContext("2d");
    if (nome === "qrcode-links") g.imageSmoothingEnabled = false;
    if (avatar) { g.fillStyle = AZUL; g.fillRect(0, 0, W, H); g.drawImage(img, 130, 130, 820, 820); }
    else g.drawImage(img, 0, 0, W, H);
    return new Promise(r => c.toBlob(r, "image/png"));
  }
  function baixar(blob, arquivo) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = arquivo;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }
  document.querySelectorAll("[data-baixar]").forEach(a => a.addEventListener("click", async e => {
    e.preventDefault();
    const nome = a.dataset.baixar;
    if (a.dataset.formato === "svg") baixar(new Blob([svgDe(nome)], { type: "image/svg+xml" }), nome + ".svg");
    else baixar(await png(nome), (nome === "avatar" ? "avatar-instagram" : nome) + ".png");
  }));
})();
