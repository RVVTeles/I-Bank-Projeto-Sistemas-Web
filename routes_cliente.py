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
    numero_telefone = request.form.get("numero_telefone")
    endereco = request.form.get("endereco")
    numero_endereco = request.form.get("numero_endereco")
    cidade = request.form.get("cidade")
    estado = request.form.get("estado")

    if not cpf or not nome or not numero_telefone or not endereco or not numero_endereco or not cidade or not estado:
        flash("Todos os dados precisam ser inseridos.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is not None:
        flash("CPF já cadastrado")
        return redirect(url_for("clientes.clientes"))

    novo_cliente = Cliente(cpf=cpf, nome=nome, numero_telefone=numero_telefone, endereco=endereco, numero_endereco=numero_endereco, cidade=cidade, estado=estado)

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
    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("clientes.clientes"))

    return render_template("listacliente.html", cliente=cliente)

@clientes_bp.route("/atualizacliente", methods=["POST"])
def atualizar_cliente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")
    numero_telefone = request.form.get("numero_telefone")
    endereco = request.form.get("endereco")
    numero_endereco = request.form.get("numero_endereco")
    cidade = request.form.get("cidade")
    estado = request.form.get("estado")

    if not cpf:
        flash("CPF precisa ser inserido.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("clientes.clientes"))
    
    if not nome and not numero_telefone and not endereco and not numero_endereco and not cidade and not estado:
        flash(f"É necessário inserir no mínimo um dado para realizar a alteração")
        return redirect(url_for("clientes.clientes"))
    
    if not nome:
        nome = cliente.nome
    if not numero_telefone:
        numero_telefone = cliente.numero_telefone
    if not endereco:
        endereco = cliente.endereco
    if not numero_endereco:
        numero_endereco = cliente.numero_endereco
    if not cidade:
        cidade = cliente.cidade
    if not estado:
        estado = cliente.estado

    att_stmt = update(Cliente).where(Cliente.cpf == cpf).values(nome=nome, numero_telefone=numero_telefone, endereco=endereco, numero_endereco=numero_endereco, cidade=cidade, estado=estado)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Cliente atualizado com sucesso")
    return redirect(url_for("clientes.clientes"))

@clientes_bp.route("/deletacliente", methods=["POST"])
def deletar_cliente():
    cpf = request.form.get("cpf")

    if not cpf:
        flash("CPF precisa ser inserido.")
        return redirect(url_for("clientes.clientes"))
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("clientes.clientes"))

    del_stmt = delete(Cliente).where(Cliente.cpf == cpf)
    db.session.execute(del_stmt)
    db.session.commit()

    flash("Cliente deletado com sucesso")
    return redirect(url_for("clientes.clientes"))