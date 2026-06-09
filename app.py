from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "escala.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    c.execute("""CREATE TABLE IF NOT EXISTS voluntarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT
    )""")
    c.commit()
    c.close()

@app.route("/")
def index():
    c = conn()
    vols = c.execute("SELECT * FROM voluntarios").fetchall()
    c.close()
    return render_template("index.html", voluntarios=vols)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    c = conn()
    c.execute("INSERT INTO voluntarios(nome,telefone) VALUES(?,?)",(nome,telefone))
    c.commit()
    c.close()
    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    c = conn()
    c.execute("DELETE FROM voluntarios WHERE id = ?", (id,))
    c.commit()
    c.close()
    return redirect("/")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    c = conn()

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]

        c.execute(
            "UPDATE voluntarios SET nome = ?, telefone = ? WHERE id = ?",
            (nome, telefone, id)
        )
        c.commit()
        c.close()

        return redirect("/")

    voluntario = c.execute(
        "SELECT * FROM voluntarios WHERE id = ?",
        (id,)
    ).fetchone()

    c.close()

    return render_template(
        "editar.html",
        voluntario=voluntario
    )

@app.route("/gerar")
def gerar():
    c = conn()
    vols = c.execute("SELECT nome FROM voluntarios").fetchall()
    c.close()

    nomes = [v[0] for v in vols]
    escala = []
    idx = 0

    for domingo in ["1º Domingo","2º Domingo","3º Domingo","4º Domingo"]:
        grupo = []
        for _ in range(4):
            if nomes:
                grupo.append(nomes[idx % len(nomes)])
                idx += 1
        escala.append((domingo, grupo))

    return render_template("escala.html", escala=escala)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
