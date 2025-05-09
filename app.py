from swagger.swagger_config import configure_swagger
import os
import sys
from config import app, db
from controllers.alunos import alunos_bp
from controllers.turmas import turmas_bp
from controllers.professores import professores_bp


app.register_blueprint(professores_bp, url_prefix='/professor')
app.register_blueprint(alunos_bp, url_prefix='/alunos')
app.register_blueprint(turmas_bp, url_prefix='/turmas')

configure_swagger(app)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
