from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Conta, Cliente, db
from sqlalchemy import select

contas_bp = Blueprint("contas", __name__)

@contas_bp.route("/contas")
def contas():
    return render_template("contas.html")  


@contas_bp.route("/criaconta", methods=["POST"])
def criar_conta():
    cliente_cpf = request.form.get("cliente_cpf")
    valor = request.form.get("valor")
    juros = request.form.get("juros")
    data_emissao = request.form.get("data_emissao")
    data_vencimento = request.form.get("data_vencimento")

    if not cliente_cpf or not valor or not juros or not data_emissao or not data_vencimento:
        flash("Por favor, preencha todos os campos.")
        return redirect(url_for("contas.contas"))
    
    if data_vencimento < data_emissao:
        flash("A data de vencimento precisa ser maior do que a data de emissão")
        return redirect(url_for("contas.contas"))
    
    stmt = select(Cliente).where(Cliente.cpf == cliente_cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("contas.contas"))

    nova_conta = Conta(cliente_cpf=cliente_cpf, valor=valor, juros=juros, data_emissao=data_emissao, data_vencimento=data_vencimento)

    db.session.add(nova_conta)
    db.session.commit()  

    flash("Conta criada com sucesso!")
    return redirect(url_for("contas.contas"))