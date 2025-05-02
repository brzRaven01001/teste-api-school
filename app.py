from flask import Flask, redirect, url_for
from config import Config
from database import db
from controllers.alunos import alunos_bp
from controllers.turmas import turmas_bp
from controllers.professores import professores_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(professores_bp, url_prefix='/professor')
    app.register_blueprint(alunos_bp, url_prefix='/alunos')
    app.register_blueprint(turmas_bp, url_prefix='/turmas')

    @app.route('/')
    def home():
       return redirect(url_for('alunos.listar_alunos'))

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
