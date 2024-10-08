from .models import Cliente, Conta, db
from flask import Blueprint, jsonify, render_template, request, url_for, make_response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from sqlalchemy import select, update, delete

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/criar")
def criar_cliente_page():
    return render_template("criarcliente.html")


@clientes_bp.route("/editar", methods=["POST"])
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


@clientes_bp.route("/editacliente", methods=["POST"])
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

@clientes_bp.route("/deletar", methods=["POST"])
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

@clientes_bp.route('/imprimir_clientes', methods=['POST'])
def imprimir_clientes():
    clientes = request.json.get('clientes', [])
    contas_nao_pagas = request.json.get('contas_nao_pagas', None)

    if not clientes:
        return {'status': 'error', 'message': 'Nenhum cliente disponível.'}, 400
    
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, height - 50, "Relatório de Clientes")
    
    headers = ['CPF', 'Nome', 'N° Telefone', 'Endereço', 'N° Endereço', 'Cidade', 'Estado']
    
    if contas_nao_pagas:
        headers.append('Contas não Pagas')

    pdf.setFont("Helvetica-Bold", 12)
    col_widths = []

    for header in headers:
        col_widths.append(pdf.stringWidth(header, "Helvetica-Bold", 12))
    
    pdf.setFont("Helvetica", 10)
    for cliente in clientes:
        col_widths[0] = max(col_widths[0], pdf.stringWidth(cliente['cpf'], "Helvetica", 10))
        col_widths[1] = max(col_widths[1], pdf.stringWidth(cliente['nome'], "Helvetica", 10))
        col_widths[2] = max(col_widths[2], pdf.stringWidth(cliente['numero_telefone'], "Helvetica", 10))
        col_widths[3] = max(col_widths[3], pdf.stringWidth(cliente['endereco'], "Helvetica", 10))
        col_widths[4] = max(col_widths[4], pdf.stringWidth(cliente['numero_endereco'], "Helvetica", 10))
        col_widths[5] = max(col_widths[5], pdf.stringWidth(cliente['cidade'], "Helvetica", 10))
        col_widths[6] = max(col_widths[6], pdf.stringWidth(cliente['estado'], "Helvetica", 10))

        if contas_nao_pagas:
            col_widths.append(pdf.stringWidth(cliente.get('contas_nao_pagas', 'N/A'), "Helvetica", 10))

    col_widths = [w + 20 for w in col_widths]

    x_offset = 50
    y_offset = height - 100
    row_height = 20

    pdf.setFont("Helvetica-Bold", 12)
    for i, header in enumerate(headers):
        pdf.drawString(x_offset, y_offset, header)
        x_offset += col_widths[i]

    pdf.setFont("Helvetica", 10)
    y_offset -= row_height
    for cliente in clientes:
        x_offset = 50
        pdf.drawString(x_offset, y_offset, cliente['cpf'])
        x_offset += col_widths[0]
        pdf.drawString(x_offset, y_offset, cliente['nome'])
        x_offset += col_widths[1]
        pdf.drawString(x_offset, y_offset, cliente['numero_telefone'])
        x_offset += col_widths[2]
        pdf.drawString(x_offset, y_offset, cliente['endereco'])
        x_offset += col_widths[3]
        pdf.drawString(x_offset, y_offset, cliente['numero_endereco'])
        x_offset += col_widths[4]
        pdf.drawString(x_offset, y_offset, cliente['cidade'])
        x_offset += col_widths[5]
        pdf.drawString(x_offset, y_offset, cliente['estado'])

        if contas_nao_pagas:
            x_offset += col_widths[6]
            pdf.drawString(x_offset, y_offset, cliente.get('contas_nao_pagas', 'N/A'))
        
        y_offset -= row_height

        if y_offset < 50:
            pdf.showPage()
            y_offset = height - 100

    pdf.save()

    pdf_output = buffer.getvalue()
    buffer.close()

    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=clientes.pdf'

    return response
