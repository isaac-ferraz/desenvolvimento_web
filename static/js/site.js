// No GitHub Pages o site é estático: não há servidor para ler a URL.
// Este script faz no navegador o que o Flask faz no servidor:
// busca/filtro de notícias e exibição dos dados enviados pelos formulários.

const ROTULOS = {
  origem: "Formulário",
  nome: "Nome",
  email: "E-mail",
  curso: "Curso desejado",
  msg: "Mensagem",
};

const params = new URLSearchParams(location.search);

function preencherBusca() {
  const campo = document.querySelector('.busca input[name="q"]');
  if (campo) campo.value = params.get("q") || "";
}

function filtrarNoticias() {
  const filtros = document.getElementById("filtros-noticias");
  if (!filtros) return;

  const q = (params.get("q") || "").trim().toLowerCase();
  const categoria = params.get("categoria") || "";

  let total = 0;
  document.querySelectorAll(".noticia").forEach((artigo) => {
    const visivel =
      (!categoria || artigo.dataset.categoria === categoria) &&
      (!q || artigo.dataset.busca.includes(q));
    artigo.hidden = !visivel;
    if (visivel) total++;
  });

  filtros.querySelectorAll("a").forEach((link) => {
    const url = new URL(link.href);
    if (q) url.searchParams.set("q", params.get("q"));
    else url.searchParams.delete("q");
    link.href = url;
    link.classList.toggle("ativo", link.dataset.categoria === categoria);
  });

  const resultado = document.getElementById("resultado-busca");
  resultado.hidden = !(q || categoria);
  let texto = `${total} resultado(s)`;
  if (q) texto += ` para “${params.get("q").trim()}”`;
  if (categoria) texto += ` em ${categoria}`;
  resultado.querySelector("span").textContent = texto + ".";

  document.getElementById("sem-resultados").hidden = total > 0;
}

function mostrarDadosEnviados() {
  const tabela = document.getElementById("dados-enviados");
  if (!tabela || !tabela.hasAttribute("data-vazio") || ![...params].length) return;

  tabela.replaceChildren();
  for (const [chave, valor] of params) {
    const linha = tabela.insertRow();
    const th = document.createElement("th");
    th.style.width = "180px";
    th.textContent = ROTULOS[chave] || chave;
    linha.appendChild(th);
    linha.insertCell().textContent = valor;
  }
}

preencherBusca();
filtrarNoticias();
mostrarDadosEnviados();
