from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = "clientes"

    cpf = db.Column(db.String(11) , primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome

class Conta(db.Model):
    __tablename__ = "contas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_cpf = db.Column(db.String(11), db.ForeignKey("clientes.cpf"), nullable=False)
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