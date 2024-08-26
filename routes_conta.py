from flask import Blueprint, flash, redirect, render_template, request, url_for
from models import Conta, Cliente, db
from sqlalchemy import delete, select, update

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

@contas_bp.route("/listacontas", methods=["GET"])
def listar_contas():    
    stmt = select(Conta).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()
    return render_template("listacontas.html", contas=contas)
    

@contas_bp.route("/listaconta", methods=["GET"])
def listar_conta():
    cliente_cpf = request.args.get("cliente_cpf")

    stmt = select(Cliente).where(Cliente.cpf == cliente_cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("contas.contas"))
    
    stmt = select(Conta).where(Conta.cliente_cpf == cliente_cpf).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()

    if not contas:
        flash(f"Nenhuma conta associada ao CPF {cliente_cpf}")
        return redirect(url_for("contas.contas"))

    return render_template("listaconta.html", contas=contas)

@contas_bp.route("/atualizaconta", methods=["POST"])
def atualizar_conta():
    id = request.form.get("id")
    cliente_cpf = request.form.get("cliente_cpf")
    valor = request.form.get("valor")
    juros = request.form.get("juros")
    data_vencimento = request.form.get("data_vencimento")

    if not id:
        flash("ID da conta precisa ser inserida.")
        return redirect(url_for("contas.contas")) 
       
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    if not conta:
        flash(f"Nenhuma conta associada ao ID {id}")
        return redirect(url_for("contas.contas"))
    
    if not cliente_cpf:
        cliente_cpf = conta.cliente_cpf
    if not valor:
        valor = conta.valor
    if not juros:
        juros = conta.juros
    if not data_vencimento:
        data_vencimento = conta.data_vencimento

    att_stmt = update(Conta).where(Conta.id == id).values(cliente_cpf=cliente_cpf, valor=valor, juros=juros, data_vencimento=data_vencimento)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Conta atualizada com sucesso")
    return redirect(url_for("contas.contas"))


@contas_bp.route("/deletaconta", methods=["POST"])
def deletar_conta():
    id = request.form.get("id")

    if not id:
        flash("ID da conta precisa ser inserido.")
        return redirect(url_for("contas.contas"))
    
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    if conta is None:
        flash("Conta com este ID não existe")
        return redirect(url_for("contas.contas"))

    del_stmt = delete(Conta).where(Conta.id == id)
    db.session.execute(del_stmt)
    db.session.commit()

    flash("Conta deletada com sucesso")
    return redirect(url_for("contas.contas"))