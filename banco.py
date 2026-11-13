"""Conexão com o MySQL que roda na instância EC2 do banco de dados.

Os dados de acesso ficam no arquivo .env (fora do git). Veja o .env.example.
"""
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

ErroBanco = pymysql.MySQLError


def conectar():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "desenv_web"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        # Mostra as datas no horário de Brasília (o servidor do banco usa UTC)
        init_command="SET time_zone = '-03:00'",
    )


def salvar_envio(form):
    """Insere um envio dos formulários (vestibular ou contato) na tabela envios."""
    sql = (
        "INSERT INTO envios (origem, nome, email, curso, mensagem) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    valores = (
        form.get("origem", "").strip(),
        form.get("nome", "").strip(),
        form.get("email", "").strip(),
        form.get("curso", "").strip() or None,
        form.get("msg", "").strip() or None,
    )
    with conectar() as conexao, conexao.cursor() as cursor:
        cursor.execute(sql, valores)
        conexao.commit()


def listar_envios():
    """Todos os registros da tabela envios, do mais recente para o mais antigo."""
    sql = (
        "SELECT id, origem, nome, email, curso, mensagem, criado_em "
        "FROM envios ORDER BY id DESC"
    )
    with conectar() as conexao, conexao.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()
