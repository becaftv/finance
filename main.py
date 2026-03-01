from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    receita = db.Column(db.Float, nullable=False)
    gasto = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/api/saldo/add', methods=["POST"])
def adicionar_receita():
    data = request.json
    if 'nome' in data and 'receita' in data and 'gasto' in data:
        nova_receita = Saldo(
            nome=data["nome"],
            receita=data["receita"],
            gasto=data["gasto"],
            descricao=data.get("descricao", "")
        )
        db.session.add(nova_receita)
        db.session.commit()
        return jsonify({"message": "Receita cadastrada com sucesso"})
    return jsonify({"message": "Dados da receita inválidos!"}), 400

@app.route('/api/saldo/delete/<int:saldo_id>', methods=["DELETE"])
def deleteSaldo(saldo_id):
    saldo = Saldo.query.get(saldo_id)
    if saldo:
        db.session.delete(saldo)
        db.session.commit()
        return jsonify({"message": "Saldo deletado com sucesso"})
    return jsonify({"message": "Saldo não encontrado"}), 404

@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]
    receita = float(request.form["receita"])
    gasto = float(request.form["gasto"])
    descricao = request.form.get("descricao", "")

    novo = Saldo(
        nome=nome,
        receita=receita,
        gasto=gasto,
        descricao=descricao
    )

    db.session.add(novo)
    db.session.commit()

    return "Dados salvos com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)