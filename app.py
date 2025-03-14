from flask import Flask, redirect, url_for
from professores import professores_bp
from alunos import alunos_bp
from turmas import turmas_bp
from login import login_bp

app = Flask(__name__, template_folder='templates')

app.register_blueprint(professores_bp, url_prefix='/professores')
app.register_blueprint(alunos_bp, url_prefix='/alunos')
app.register_blueprint(turmas_bp, url_prefix='/turmas')
app.register_blueprint(login_bp, url_prefix='/login')


@app.route('/')
def index():
    return redirect(url_for('login.index'))


if __name__ == '__main__':
    app.run(debug=True)