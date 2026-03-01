from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  
    tipo = db.Column(db.String(10), nullable=False) 
    valor = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/saldo/add', methods=["POST"])
def adicionar_receita():
    data = request.json
    if 'nome' in data and 'receita' in data and 'gasto' in data:
        nova_receita = Transacao(
            nome=data["nome"],
            receita=data["receita"],
            gasto=data["gasto"],
        )
        db.session.add(nova_receita)
        db.session.commit()
        return jsonify({"message": "Receita cadastrada com sucesso"})
    return jsonify({"message": "Dados da receita inválidos!"}), 400

@app.route('/api/saldo/delete/<int:saldo_id>', methods=["DELETE"])
def deleteSaldo(saldo_id):
    saldo = Transacao.query.get(saldo_id)
    if saldo:
        db.session.delete(saldo)
        db.session.commit()
        return jsonify({"message": "Saldo deletado com sucesso"})
    return jsonify({"message": "Saldo não encontrado"}), 404

@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    valor = float(request.form["valor"])

    nova = Transacao(
        nome=nome,
        tipo=tipo,
        valor=valor
    )

    db.session.add(nova)
    db.session.commit()

    return "Transação salva!"

@app.route("/api/saldo")
def calcular_saldo():
    receitas = db.session.query(db.func.sum(Transacao.valor))\
        .filter(Transacao.tipo == "receita").scalar() or 0

    despesas = db.session.query(db.func.sum(Transacao.valor))\
        .filter(Transacao.tipo == "despesa").scalar() or 0

    saldo = receitas - despesas

    return {
        "total_receitas": receitas,
        "total_despesas": despesas,
        "saldo_atual": saldo
    }

if __name__ == '__main__':
    app.run(debug=True)