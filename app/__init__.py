from flask import Flask, render_template
from .models import db
from .clientes_controller import clientes_bp
from .contas_controller import contas_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(clientes_bp, url_prefix="/Clientes")
    app.register_blueprint(contas_bp, url_prefix="/Contas")
    
    @app.route("/")
    def index():
        return render_template('index.html')
    
    return app