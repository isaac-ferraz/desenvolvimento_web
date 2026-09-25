# desenvolvimento_web
Projeto criado para a aula de Desenvolvimento Web na Fatec SJC

## Estrutura

```
app.py              rotas do Flask
noticias.py         dados das notícias
freeze.py           gera a versão estática do site (pasta build/)
templates/          páginas HTML (Jinja)
static/css/         estilos
static/js/          busca de notícias e formulários na versão estática
static/img/         imagens
.github/workflows/  publicação automática no GitHub Pages
```

## Como rodar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000

## Publicar no GitHub Pages

O GitHub Pages só hospeda arquivos estáticos, então o `freeze.py` (Frozen-Flask)
transforma as rotas do Flask em páginas HTML na pasta `build/`.

1. No GitHub, abra **Settings → Pages** e, em **Source**, escolha **GitHub Actions**.
2. Faça push na branch `main`. O workflow `.github/workflows/pages.yml` gera o site e publica em
   https://isaac-ferraz.github.io/desenvolvimento_web/

Para gerar a versão estática localmente:

```bash
python freeze.py
python -m http.server -d build
```
