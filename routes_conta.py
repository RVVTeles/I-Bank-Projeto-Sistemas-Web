from flask import Blueprint, flash, redirect, render_template, request, url_for
from datetime import datetime
from models import Conta, Cliente, db
from sqlalchemy import and_, delete, select, update

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

    return render_template("listacontas.html", contas=contas)

@contas_bp.route("/pagaconta", methods=["POST"])
def pagar_conta():
    id = request.form.get("id")
    data_pagamento = request.form.get("data_pagamento")
    if not id:
        flash("ID da conta precisa ser inserida.")
        return redirect(url_for("contas.contas")) 
       
    stmt = select(Conta).where(Conta.id == id)
    conta = db.session.execute(stmt).scalars().first()

    if not conta:
        flash(f"Nenhuma conta associada ao ID {id}")
        return redirect(url_for("contas.contas"))
    
    if not id and not data_pagamento:
        flash(f"É necessário inserir o ID da conta e a data de pagamento")
        return redirect(url_for("contas.contas"))
    
    att_stmt = update(Conta).where(Conta.id == id).values(data_pagamento=data_pagamento)
    db.session.execute(att_stmt)
    db.session.commit()

    flash("Conta paga com sucesso")
    return redirect(url_for("contas.contas"))

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
    
    if not cliente_cpf and not valor and not juros and not data_vencimento:
        flash(f"É necessário inserir no mínimo um dado para realizar a alteração")
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

@contas_bp.route("/contasapagar", methods=["POST"])
def contas_a_pagar():
    data_inicial = request.form.get("data_inicial")
    data_final = request.form.get("data_final")

    if not data_inicial or not data_final:
        flash("É necessário inserir a data inicial e a data final da pesquisa.")
        return redirect(url_for("contas.contas"))
    
    stmt = select(Conta).where(and_(Conta.data_vencimento >= data_inicial, Conta.data_vencimento <= data_final, Conta.data_pagamento == None)).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()

    return render_template("listacontas.html", contas=contas)

@contas_bp.route("/contaspagas", methods=["POST"])
def contas_pagas():
    data_inicial = request.form.get("data_inicial")
    data_final = request.form.get("data_final")

    if not data_inicial or not data_final:
        flash("É necessário inserir a data inicial e a data final da pesquisa.")
        return redirect(url_for("contas.contas"))
    
    stmt = select(Conta).where(and_(Conta.data_vencimento >= data_inicial, Conta.data_vencimento <= data_final, Conta.data_pagamento != None)).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()

    return render_template("listacontas.html", contas=contas)

@contas_bp.route("/listacontascliente", methods=["GET"])
def listar_contas_cliente():    
    stmt = select(Conta).order_by(Conta.data_emissao)
    contas = db.session.execute(stmt).scalars().all()
    return render_template("listacontas.html", contas=contas)

@contas_bp.route("/listacontastatus", methods=["GET"])
def listar_conta_status():
    cliente_cpf = request.args.get("cliente_cpf")
    status = request.args.get("status")

    stmt = select(Cliente).where(Cliente.cpf == cliente_cpf)
    cliente = db.session.execute(stmt).scalars().first()
    data_atual = datetime.now().date()

    if cliente is None:
        flash("CPF não cadastrado")
        return redirect(url_for("contas.contas"))
    
    if status == "em atraso":
        stmt = select(Conta).where(Conta.cliente_cpf == cliente_cpf, Conta.data_pagamento == None, Conta.data_vencimento < data_atual).order_by(Conta.data_emissao)
    elif status == "paga":
        stmt = select(Conta).where(Conta.cliente_cpf == cliente_cpf, Conta.data_pagamento != None).order_by(Conta.data_emissao)
    else:
        stmt = select(Conta).where(Conta.cliente_cpf == cliente_cpf, Conta.data_pagamento == None, Conta.data_vencimento > data_atual).order_by(Conta.data_emissao)

    contas = db.session.execute(stmt).scalars().all()

    return render_template("listacontas.html", contas=contas)