from flask import Flask, render_template
from models import db
from routes_cliente import clientes_bp
from routes_conta import contas_bp

app = Flask(__name__)
app.secret_key = "a"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/contasapagar'
db.init_app(app)

app.register_blueprint(clientes_bp)
app.register_blueprint(contas_bp)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)