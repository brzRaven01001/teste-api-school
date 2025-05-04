from flask import Flask, redirect, url_for
from flask_restx import Api
from config import Config
from database import db
from controllers.alunos import alunos_bp
from controllers.turmas import turmas_bp
from controllers.professores import professores_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)

    api = Api(app, version='1.0', title='API School System', description='Uma API com Flask e Flask-RESTX')

    api.add_namespace(professores_bp, path='/professor')
    api.add_namespace(alunos_bp, path='/alunos')
    api.add_namespace(turmas_bp, path='/turmas')

    @app.route('/')
    def home():
       return redirect(url_for('alunos.listar_alunos'))
    
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)