from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import select, update, delete
from models import Cliente, db

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes")
def clientes():
    return render_template("clientes.html")


@clientes_bp.route("/criacliente", methods=["POST"])
def criar_cliente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")

    if not cpf or not nome:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is not None:
        flash("CPF já cadastrado")
        return redirect(url_for("clientes.clientes"))

    novo_cliente = Cliente(cpf=cpf, nome=nome)

    db.session.add(novo_cliente)
    db.session.commit()  

    flash("Cliente criado com sucesso!")
    return redirect(url_for("clientes.clientes"))

@clientes_bp.route("/listaclientes", methods=["GET"])
def listar_clientes():
    
    stmt = select(Cliente).order_by(Cliente.cpf)
    clientes = db.session.execute(stmt).scalars().all()
    return render_template("listaclientes.html", clientes=clientes)
    

@clientes_bp.route("/listacliente", methods=["GET"])
def listar_cliente():
    cpf = request.args.get("cpf")
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()
    return render_template("listacliente.html", cliente=cliente)

@clientes_bp.route("/atualizacliente", methods=["POST"])
def atualizar_cliente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")
    if not cpf or not nome:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("clientes.clientes"))

    att_stmt = update(Cliente).where(Cliente.cpf == cpf).values(nome=nome)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Cliente atualizado com sucesso")
    return redirect(url_for("clientes.clientes"))

@clientes_bp.route("/deletacliente", methods=["POST"])
def deletar_cliente():
    cpf = request.form.get("cpf")

    if not cpf:
        flash("CPF e Nome precisam ser inseridos.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("clientes.clientes"))

    att_stmt = delete(Cliente).where(Cliente.cpf == cpf)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Cliente deletado com sucesso")
    return redirect(url_for("clientes.clientes"))