"""Gera a versão estática do site (pasta build/) para publicar no GitHub Pages."""
from flask_frozen import Freezer

import noticias as base_noticias
from app import app

# Links relativos, para o site funcionar em https://<usuario>.github.io/<repositorio>/
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_DESTINATION"] = "build"

freezer = Freezer(app)


@freezer.register_generator
def noticia():
    for n in base_noticias.NOTICIAS:
        yield {"slug": n["slug"]}


if __name__ == "__main__":
    freezer.freeze()
    print("Site estático gerado em build/")
