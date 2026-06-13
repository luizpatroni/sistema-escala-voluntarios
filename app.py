from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "escala.db"


def conn():
    return sqlite3.connect(DB)


def init_db():
    c = conn()

    # Tabela de voluntários
    c.execute("""
    CREATE TABLE IF NOT EXISTS voluntarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        parceiro_id INTEGER,
        FOREIGN KEY(parceiro_id)
            REFERENCES voluntarios(id)
    )
    """)

    # Tabela de celebrações
    c.execute("""
    CREATE TABLE IF NOT EXISTS celebracoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        descricao TEXT NOT NULL
    )
    """)

    # Tabela de escalas
    c.execute("""
    CREATE TABLE IF NOT EXISTS escalas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voluntario_id INTEGER NOT NULL,
        celebracao_id INTEGER NOT NULL,
        funcao TEXT,
        FOREIGN KEY(voluntario_id)
            REFERENCES voluntarios(id),
        FOREIGN KEY(celebracao_id)
            REFERENCES celebracoes(id)
    )
    """)

    c.commit()
    c.close()


@app.route("/")
def index():

    c = conn()

    voluntarios = c.execute("""
    SELECT
        v.id,
        v.nome,
        v.telefone,
        p.nome
    FROM voluntarios v
    LEFT JOIN voluntarios p
        ON v.parceiro_id = p.id
    """).fetchall()

    c.close()

    return render_template(
        "index.html",
        voluntarios=voluntarios
    )


@app.route("/adicionar", methods=["POST"])
def adicionar():

    nome = request.form["nome"]
    telefone = request.form["telefone"]

    c = conn()

    c.execute(
        """
        INSERT INTO voluntarios(nome, telefone)
        VALUES (?, ?)
        """,
        (nome, telefone)
    )

    c.commit()
    c.close()

    return redirect("/")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    c = conn()

    if request.method == "POST":

        nome = request.form["nome"]
        telefone = request.form["telefone"]
        parceiro_id = request.form["parceiro_id"]

        c.execute(
            """
            UPDATE voluntarios
            SET nome = ?,
                telefone = ?,
                parceiro_id = ?
            WHERE id = ?
            """,
            (
                nome,
                telefone,
                parceiro_id if parceiro_id else None,
                id
            )
        )

        c.commit()
        c.close()

        return redirect("/")
    voluntario = c.execute(
        """
        SELECT *
        FROM voluntarios
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    voluntarios = c.execute(
        """
        SELECT id, nome
        FROM voluntarios
        WHERE id != ?
        """,
        (id,)
    ).fetchall()

    c.close()

    return render_template(
        "editar.html",
        voluntario=voluntario,
        voluntarios=voluntarios
    )


@app.route("/excluir/<int:id>")
def excluir(id):

    c = conn()

    c.execute(
        """
        DELETE FROM voluntarios
        WHERE id = ?
        """,
        (id,)
    )

    c.commit()
    c.close()

    return redirect("/")


@app.route("/gerar")
def gerar():

    c = conn()

    voluntarios = c.execute(
        """
        SELECT id, nome, parceiro_id
        FROM voluntarios
        """
    ).fetchall()

    # Limpa dados antigos
    c.execute("DELETE FROM escalas")
    c.execute("DELETE FROM celebracoes")

    celebracoes = [
        ("2026-06-07", "1º Domingo"),
        ("2026-06-14", "2º Domingo"),
        ("2026-06-21", "3º Domingo"),
        ("2026-06-28", "4º Domingo")
    ]

    celebracao_ids = []

    for data, descricao in celebracoes:

        cursor = c.execute(
            """
            INSERT INTO celebracoes(data, descricao)
            VALUES (?, ?)
            """,
            (data, descricao)
        )

        celebracao_ids.append(cursor.lastrowid)


    indice = 0

    for celebracao_id in celebracao_ids:

        vagas = 4

        usados_no_dia = set()

        while vagas > 0:

            voluntario = voluntarios[
                indice % len(voluntarios)
            ]

            voluntario_id = voluntario[0]
            parceiro_id = voluntario[2]
            if voluntario_id in usados_no_dia:
                indice += 1
                continue

            c.execute(
                """
                INSERT INTO escalas(
                    voluntario_id,
                    celebracao_id,
                    funcao
                )
                VALUES (?, ?, ?)
                """,
                (
                    voluntario_id,
                    celebracao_id,
                    "Voluntário"
                )
            )

            usados_no_dia.add(voluntario_id)

            vagas -= 1
            indice += 1

            if (
                parceiro_id
                and parceiro_id not in usados_no_dia
                and vagas > 0
            ):

                c.execute(
                    """
                    INSERT INTO escalas(
                        voluntario_id,
                        celebracao_id,
                        funcao
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        parceiro_id,
                        celebracao_id,
                        "Voluntário"
                    )
                )

                usados_no_dia.add(parceiro_id)

                vagas -= 1

    c.commit()

    resultado = c.execute("""
    SELECT
        celebracoes.descricao,
        voluntarios.nome
    FROM escalas
    JOIN voluntarios
        ON escalas.voluntario_id = voluntarios.id
    JOIN celebracoes
        ON escalas.celebracao_id = celebracoes.id
    ORDER BY celebracoes.id
    """).fetchall()

    c.close()

    escala = {}

    for celebracao, nome in resultado:

        if celebracao not in escala:
            escala[celebracao] = []

        escala[celebracao].append(nome)

    return render_template(
        "escala.html",
        escala=escala
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
