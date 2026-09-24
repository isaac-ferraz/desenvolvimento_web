from datetime import date

# Notícias de exemplo. Para adicionar uma nova, inclua um dicionário no início da lista.
NOTICIAS = [
    {
        "slug": "semana-de-tecnologia-2026",
        "titulo": "Semana de Tecnologia 2026 reúne palestras e oficinas gratuitas",
        "data": date(2026, 9, 22),
        "categoria": "Eventos",
        "imagem": "auditorio",
        "resumo": "Cinco dias de programação no auditório da FaTech, com convidados da indústria e oficinas práticas abertas à comunidade.",
        "corpo": [
            "A FaTech realiza, em outubro, a Semana de Tecnologia 2026. O evento reúne palestras, mesas-redondas e oficinas práticas sobre desenvolvimento web, inteligência artificial, segurança da informação e carreira.",
            "Todas as atividades são gratuitas e abertas à comunidade. Alunos que participarem de pelo menos 70% da programação recebem certificado de horas complementares.",
            "A programação completa e o formulário de inscrição serão divulgados nos próximos dias na página de contato.",
        ],
    },
    {
        "slug": "vestibular-abre-inscricoes",
        "titulo": "Vestibular abre inscrições para os cursos de tecnologia",
        "data": date(2026, 9, 18),
        "categoria": "Vestibular",
        "imagem": "fachada",
        "resumo": "São 120 vagas distribuídas entre os três cursos superiores de tecnologia. Inscrições vão de 15 a 30 de outubro.",
        "corpo": [
            "Estão abertas as inscrições para o vestibular da FaTech. São oferecidas 40 vagas em cada um dos cursos: Desenvolvimento de Software Multiplataforma, Análise e Desenvolvimento de Sistemas e Gestão da Tecnologia da Informação.",
            "A prova será aplicada em 8 de novembro e o resultado sai em 15 de novembro. A matrícula acontece de 18 a 25 de novembro.",
            "A inscrição pode ser feita pela página do vestibular, em poucos minutos.",
        ],
    },
    {
        "slug": "novos-computadores-laboratorio",
        "titulo": "Laboratório de programação recebe novos computadores",
        "data": date(2026, 9, 10),
        "categoria": "Estrutura",
        "imagem": "laboratorio",
        "resumo": "Quarenta máquinas novas, com mais memória e monitores maiores, já estão disponíveis para as aulas práticas.",
        "corpo": [
            "O laboratório de programação foi renovado e agora conta com 40 computadores novos, com 16 GB de memória e SSD, além de monitores de 24 polegadas.",
            "Segundo a coordenação, a troca permite rodar ambientes de desenvolvimento mais pesados, como máquinas virtuais e contêineres, sem travamentos durante as aulas.",
            "O laboratório fica aberto aos alunos, fora do horário de aula, de segunda a sexta, das 18h às 21h.",
        ],
    },
    {
        "slug": "projetos-do-espaco-maker",
        "titulo": "Alunos apresentam projetos de robótica no Espaço Maker",
        "data": date(2026, 9, 3),
        "categoria": "Projetos",
        "imagem": "maker",
        "resumo": "Protótipos de robôs seguidores de linha e de estufas automatizadas foram apresentados em mostra aberta ao público.",
        "corpo": [
            "Equipes do segundo e do terceiro semestre apresentaram seus projetos integradores no Espaço Maker. Entre os destaques, estão robôs seguidores de linha e uma estufa automatizada que controla umidade e temperatura por sensores.",
            "Os trabalhos foram avaliados por professores e por convidados de empresas da região. Os melhores projetos seguem para a Semana de Tecnologia.",
        ],
    },
    {
        "slug": "biblioteca-acervo-digital",
        "titulo": "Biblioteca amplia horário e acervo digital",
        "data": date(2026, 8, 27),
        "categoria": "Biblioteca",
        "imagem": "biblioteca",
        "resumo": "A partir de setembro, a biblioteca abre mais cedo e passa a oferecer livros técnicos em formato digital.",
        "corpo": [
            "A biblioteca da FaTech passa a abrir às 8h, uma hora mais cedo que antes, e ganhou acesso a uma coleção de livros técnicos digitais, disponíveis para todos os alunos com o login institucional.",
            "O acervo inclui títulos de programação, bancos de dados, redes e gestão de projetos. Novas aquisições podem ser sugeridas diretamente no balcão de atendimento.",
        ],
    },
    {
        "slug": "feira-de-carreiras",
        "titulo": "Feira de Carreiras conecta alunos a empresas de tecnologia",
        "data": date(2026, 8, 14),
        "categoria": "Carreira",
        "imagem": "patio",
        "resumo": "Doze empresas estiveram no pátio da faculdade para conversar com estudantes e divulgar vagas de estágio.",
        "corpo": [
            "O pátio da FaTech recebeu, na semana passada, a Feira de Carreiras. Doze empresas da região participaram, com estandes, conversas rápidas e divulgação de vagas de estágio e trainee.",
            "Os alunos puderam entregar currículos e participar de mini-entrevistas. A coordenação informou que parte das vagas será preenchida ainda neste semestre.",
        ],
    },
]

_MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def data_br(d):
    return f"{d.day:02d} {_MESES[d.month - 1]} {d.year}"


def por_slug(slug):
    return next((n for n in NOTICIAS if n["slug"] == slug), None)


def categorias():
    return sorted({n["categoria"] for n in NOTICIAS})


def buscar(q="", categoria=""):
    q = q.strip().lower()
    resultado = NOTICIAS
    if categoria:
        resultado = [n for n in resultado if n["categoria"] == categoria]
    if q:
        resultado = [n for n in resultado
                     if q in n["titulo"].lower() or q in n["resumo"].lower()
                     or any(q in p.lower() for p in n["corpo"])]
    return resultado
