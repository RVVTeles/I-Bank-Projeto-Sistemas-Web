from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/contasapagar'
db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'clientes'

    cpf = db.Column(db.String(11) , primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome

@app.route("/index")
def index():
  return render_template('index.html')  

@app.route('/clientes', methods=['POST'])
def create_item():
    data = request.json
    cpf = data.get("cpf")
    nome = data.get("nome")

    if not cpf or not nome:
        abort(400) # Bad request

    novo_cliente = Cliente(cpf=cpf, nome=nome)

    db.session.add(novo_cliente)
    db.session.commit()    
    
    return jsonify({'cpf': cpf, "nome": nome}), 201

# @app.route('/items', methods=['GET'])
# def get_items():
#     return jsonify({'items': items})

# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = next((item for item in items if item['id'] == item_id), None)
#     if item is None:
#         abort(404) # Not found
#     return jsonify({'item': item})

# @app.route('/items/<int:item_id>', methods=['PUT'])
# def update_item(item_id):
#     item = next((item for item in items if item['id'] == item_id), None)
#     if item is None:
#         abort(404)
#     if not request.json or 'name' not in request.json:
#         abort(400)
#     item['name'] = request.json['name']
#     return jsonify({'item': item})

# @app.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     item = next((item for item in items if item['id'] == item_id), None)
#     if item is None:
#         abort(404)
#     items.remove(item)
#     return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)