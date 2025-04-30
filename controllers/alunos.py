from flask import Blueprint, jsonify, request
from models import alunos
from database import db

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/listar', methods=['GET'])
def listar_alunos():
    return jsonify(alunos.listar_alunos(db.session))

@alunos_bp.route('/criar', methods=['POST'])
def criar_aluno():
    dados = request.json
    result, status = alunos.adicionar_aluno(db.session, dados)
    return jsonify(result), status

@alunos_bp.route('/filtrar/<int:idAluno>', methods=['GET'])
def filtrar_aluno(idAluno):
    result = alunos.filtrar_por_id(db.session, idAluno)
    status = 200 if "error" not in result else 404
    return jsonify(result), status

@alunos_bp.route('/atualizar/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    dados = request.json
    result, status = alunos.atualizar_aluno(db.session, idAluno, dados)
    return jsonify(result), status

@alunos_bp.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    result, status = alunos.deletar_aluno(db.session, idAluno)
    return jsonify(result), status

@alunos_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    result, status = alunos.resetar_dados(db.session)
    return jsonify(result), status
