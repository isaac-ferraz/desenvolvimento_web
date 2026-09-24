from flask import Flask, abort, render_template, request

import noticias as base_noticias

app = Flask(__name__)
app.jinja_env.filters["data_br"] = base_noticias.data_br

# Menu lateral, agrupado: (título do grupo, [(rota, texto), ...])
MENU = [
    ("Início", [
        ("index", "Página inicial"),
        ("noticias", "Notícias"),
    ]),
    ("A faculdade", [
        ("institucional", "Institucional"),
        ("campus", "Campus"),
        ("cursos", "Cursos"),
    ]),
    ("Ingresso", [
        ("vestibular", "Vestibular"),
        ("contato", "Contato"),
    ]),
]

ROTULOS = {
    "origem": "Formulário",
    "nome": "Nome",
    "email": "E-mail",
    "curso": "Curso desejado",
    "msg": "Mensagem",
}


@app.context_processor
def injetar_menu():
    return {"menu": MENU}


@app.route("/")
def index():
    return render_template("index.html", ultimas=base_noticias.NOTICIAS[:3])


@app.route("/noticias")
def noticias():
    q = request.args.get("q", "")
    categoria = request.args.get("categoria", "")
    return render_template(
        "noticias.html",
        lista=base_noticias.buscar(q, categoria),
        categorias=base_noticias.categorias(),
        q=q,
        categoria=categoria,
    )


@app.route("/noticias/<slug>")
def noticia(slug):
    item = base_noticias.por_slug(slug)
    if item is None:
        abort(404)
    outras = [n for n in base_noticias.NOTICIAS if n["slug"] != slug][:3]
    return render_template("noticia.html", n=item, outras=outras)


@app.route("/cursos")
def cursos():
    return render_template("cursos.html")


@app.route("/institucional")
def institucional():
    return render_template("institucional.html")


@app.route("/campus")
def campus():
    return render_template("campus.html")


@app.route("/vestibular")
def vestibular():
    return render_template("vestibular.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/enviar", methods=["POST"])
def enviar():
    dados = [(ROTULOS.get(chave, chave), valor) for chave, valor in request.form.items()]
    return render_template("obrigado.html", dados=dados)


if __name__ == "__main__":
    app.run(debug=True)
