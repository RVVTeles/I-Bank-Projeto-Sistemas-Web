from flask import Flask, flash, jsonify, redirect, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Null, delete, select, update

app = Flask(__name__)
app.secret_key = "a"



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/contasapagar'
db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'clientes'

    cpf = db.Column(db.String(11) , primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome

class Conta(db.Model):
    __tablename__ = 'contas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_cpf = db.Column(db.String(11), db.ForeignKey('clientes.cpf'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    juros = db.Column(db.Float, nullable=False)
    data_emissao = db.Column(db.Date, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)

    def __init__(self, cliente_cpf, valor, juros, data_emissao, data_vencimento, data_pagamento=None):
        self.cliente_cpf = cliente_cpf
        self.valor = valor
        self.juros = juros
        self.data_emissao = data_emissao
        self.data_vencimento = data_vencimento
        self.data_pagamento = data_pagamento

@app.route("/")
def index():
    return render_template('index.html')  

@app.route("/contas")
def contas():
    return render_template('contas.html')  

@app.route("/clientes")
def clientes():
    return render_template('clientes.html')


@app.route('/criacliente', methods=['POST'])
def criar_cliente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")

    if not cpf or not nome:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for('clientes'))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is not None:
        flash("CPF já cadastrado")
        return redirect(url_for('clientes'))

    novo_cliente = Cliente(cpf=cpf, nome=nome)

    db.session.add(novo_cliente)
    db.session.commit()  

    flash('Cliente criado com sucesso!')
    return redirect(url_for('clientes'))

@app.route('/listaclientes', methods=['GET'])
def listar_clientes():
    
    stmt = select(Cliente).order_by(Cliente.cpf)
    clientes = db.session.execute(stmt).scalars().all()
    return render_template('listaclientes.html', clientes=clientes)
    

@app.route('/listacliente', methods=['GET'])
def listar_cliente():
    cpf = request.args.get('cpf')
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()
    return render_template('listacliente.html', cliente=cliente)

@app.route('/atualizacliente', methods=['POST'])
def atualizar_cliente():
    cpf = request.form.get('cpf')
    nome = request.form.get("nome")
    if not cpf or not nome:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for('clientes'))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for('clientes'))

    att_stmt = update(Cliente).where(Cliente.cpf == cpf).values(nome=nome)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Cliente atualizado com sucesso")
    return redirect(url_for('clientes'))

@app.route('/deletacliente', methods=['POST'])
def deletar_cliente():
    cpf = request.form.get('cpf')

    if not cpf:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for('clientes'))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for('clientes'))

    att_stmt = delete(Cliente).where(Cliente.cpf == cpf)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Cliente deletado com sucesso")
    return redirect(url_for('clientes'))

@app.route('/criaconta', methods=['POST'])
def criar_conta():
    cliente_cpf = request.form.get("cliente_cpf")
    valor = request.form.get("valor")
    juros = request.form.get("juros")
    data_emissao = request.form.get("data_emissao")
    data_vencimento = request.form.get("data_vencimento")

    if not cliente_cpf or not valor or not juros or not data_emissao or not data_vencimento:
        flash("Por favor, preencha todos os campos.")
        return redirect(url_for('contas'))
    
    if data_vencimento < data_emissao:
        flash("A data de vencimento precisa ser maior do que a data de emissão")
        return redirect(url_for('contas'))
    
    stmt = select(Cliente).where(Cliente.cpf == cliente_cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for('contas'))

    nova_conta = Conta(cliente_cpf=cliente_cpf, valor=valor, juros=juros, data_emissao=data_emissao, data_vencimento=data_vencimento)

    db.session.add(nova_conta)
    db.session.commit()  

    flash('Conta criada com sucesso!')
    return redirect(url_for('contas'))



if __name__ == '__main__':
    app.run(debug=True)