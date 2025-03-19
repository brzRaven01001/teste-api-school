from flask import Flask, redirect, url_for
from professores import professor_bp
from alunos import alunos_bp
from turmas import turmas_bp

app = Flask(__name__, template_folder='templates')


app.register_blueprint(professor_bp, url_prefix='/professor')
app.register_blueprint(alunos_bp, url_prefix='/alunos')
app.register_blueprint(turmas_bp, url_prefix='/turmas')



@app.route('/')
def home():
    return redirect(url_for('login_bp.login'))


if __name__ == '__main__':
    app.run(debug=True)