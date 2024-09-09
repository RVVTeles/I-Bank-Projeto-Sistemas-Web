from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import select, update, delete
from models import Cliente, Conta, db

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes")
def clientes():
    return render_template("clientes.html")

@clientes_bp.route("/criarcliente")
def criar_cliente_page():
    return render_template("criacliente.html")


@clientes_bp.route("/editacliente", methods=["POST"])
def editar_cliente():
    cpf = request.form.get("cpf")
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()
   
    return render_template("editacliente.html", cliente=cliente)

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
        return jsonify({'status': 'error', 'message': 'Todos os dados precisam ser inseridos'}), 400
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is not None:
        return jsonify({'status': 'error', 'message': 'CPF já cadastrado'}), 400

    novo_cliente = Cliente(cpf=cpf, nome=nome, numero_telefone=numero_telefone, endereco=endereco, numero_endereco=numero_endereco, cidade=cidade, estado=estado)

    db.session.add(novo_cliente)
    db.session.commit()  

    return jsonify({'status': 'success', 'message': 'Cliente criado com sucesso!', 'redirect_url': url_for('clientes.listar_clientes')}), 200


@clientes_bp.route("/atualizacliente", methods=["POST"])
def atualizar_cliente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")
    numero_telefone = request.form.get("numero_telefone")
    endereco = request.form.get("endereco")
    numero_endereco = request.form.get("numero_endereco")
    cidade = request.form.get("cidade")
    estado = request.form.get("estado")
    
    stmt = select(Cliente).where(Cliente.cpf == cpf)
    cliente = db.session.execute(stmt).scalars().first()
    
    if not nome and not numero_telefone and not endereco and not numero_endereco and not cidade and not estado:
        return jsonify({'status': 'error', 'message': 'É necessário inserir no mínimo um dado para realizar a alteração'}), 400
    
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

    return jsonify({'status': 'success', 'message': 'Informações do Cliente atualizadas com sucesso!', 'redirect_url': url_for('clientes.listar_clientes')}), 200

@clientes_bp.route("/deletacliente", methods=["POST"])
def deletar_cliente():
    cpf = request.form.get("cpf")
    
    conta_stmt = select(Conta).where(Conta.cliente_cpf == cpf)
    contas = db.session.execute(conta_stmt).scalars().first()
    
    if contas is not None:
        return jsonify({'status': 'error', 'message': 'Não é possível deletar um cliente com contas associadas'}), 400
    
    del_stmt = delete(Cliente).where(Cliente.cpf == cpf)
    db.session.execute(del_stmt)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Cliente deletado com sucesso!'}), 200