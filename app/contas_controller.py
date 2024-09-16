from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from datetime import datetime
from .models import Conta, Cliente, db
from sqlalchemy import and_, delete, select, update

contas_bp = Blueprint("contas", __name__)

@contas_bp.route("/criar")
def cria_conta():
    return render_template("criarconta.html")

@contas_bp.route("/editar", methods=["POST"])
def edita_conta():
    id = request.form.get("id")
    
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    return render_template("editaconta.html", conta=conta)  

@contas_bp.route("/pagar", methods=["POST"])
def paga_conta():
    id = request.form.get("id")
    
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    return render_template("pagarconta.html", conta=conta)  

@contas_bp.route("/criarconta", methods=["POST"])
def criar_conta():
    cliente_cpf = request.form.get("cliente_cpf")
    valor = request.form.get("valor")
    juros = request.form.get("juros")
    data_emissao = request.form.get("data_emissao")
    data_vencimento = request.form.get("data_vencimento")

    if not cliente_cpf or not valor or not juros or not data_emissao or not data_vencimento:
        return jsonify({'status': 'error', 'message': 'Por favor, preencha todos os campos'}), 400
    
    if data_vencimento < data_emissao:
        return jsonify({'status': 'error', 'message': 'A data de vencimento precisa ser maior do que a data de emissão'}), 400
    
    stmt = select(Cliente).where(Cliente.cpf == cliente_cpf)
    cliente = db.session.execute(stmt).scalars().first()

    if cliente is None:
        return jsonify({'status': 'error', 'message': 'CPF não cadastrado'}), 400


    nova_conta = Conta(cliente_cpf=cliente_cpf, valor=valor, juros=juros, data_emissao=data_emissao, data_vencimento=data_vencimento)

    db.session.add(nova_conta)
    db.session.commit()  

    return jsonify({'status': 'success', 'message': 'Conta criada com sucesso!', 'redirect_url': url_for('contas.listar_contas')}), 200

@contas_bp.route("/listacontas", methods=["GET"])
def listar_contas():    
    stmt = select(Conta).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()
    return render_template("listacontas.html", contas=contas)

@contas_bp.route("/pagaconta", methods=["POST"])
def pagar_conta():
    id = request.form.get("id")
    data_pagamento = request.form.get("data_pagamento")
       
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()
    
    if not data_pagamento:
        return jsonify({'status': 'error', 'message': 'É necessário inserir a data de pagamento'}), 400
    
    att_stmt = update(Conta).where(Conta.id == id).values(data_pagamento=data_pagamento)
    db.session.execute(att_stmt)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Pagamento realizado com sucesso!', 'redirect_url': url_for('contas.listar_contas')}), 200

@contas_bp.route("/editaconta", methods=["POST"])
def editar_conta():
    id = request.form.get("id")
    cliente_cpf = request.form.get("cliente_cpf")
    valor = request.form.get("valor")
    juros = request.form.get("juros")
    data_vencimento = request.form.get("data_vencimento")

    if not id:
        return jsonify({'status': 'error', 'message': 'ID da conta precisa ser inserida.'}), 400
       
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    if not conta:
        return jsonify({'status': 'error', 'message': 'Nenhuma conta associada ao ID {id}'}), 400
    
    if not cliente_cpf and not valor and not juros and not data_vencimento:
        return jsonify({'status': 'error', 'message': 'É necessário inserir no mínimo um dado para realizar a alteração'}), 400
    
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

    
    return jsonify({'status': 'success', 'message': 'Conta atualizada com sucesso!', 'redirect_url': url_for('contas.listar_contas')}), 200

@contas_bp.route("/deletar", methods=["POST"])
def deletar_conta():
    id = request.form.get("id")
    
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    del_stmt = delete(Conta).where(Conta.id == id)
    db.session.execute(del_stmt)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Conta deletada com sucesso!'}), 200


@contas_bp.route("/listacredores", methods=["GET"])
def listar_credores():    
    stmt = select(Conta).where(Conta.data_pagamento == None).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()
    clientes = []
    cliente_contas_nao_pagas = {}

    cpfs = set()

    for conta in contas:
        if conta.cliente_cpf not in cpfs:
            clientes_stmt = select(Cliente).where(Cliente.cpf == conta.cliente_cpf)
            cliente = db.session.execute(clientes_stmt).scalars().first()

            if cliente:
                clientes.append(cliente)
                cpfs.add(conta.cliente_cpf)
                contador_contas_nao_pagas = sum(1 for c in contas if c.cliente_cpf == conta.cliente_cpf)
                cliente_contas_nao_pagas[conta.cliente_cpf] = contador_contas_nao_pagas
        
    return render_template("listacredores.html", clientes=clientes, cliente_contas_nao_pagas=cliente_contas_nao_pagas)