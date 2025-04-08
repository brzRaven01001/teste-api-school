from flask import Blueprint, jsonify, request
from models import alunos

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/listar', methods=['GET'])
def listar_alunos():
    return jsonify(alunos.listar_alunos())

@alunos_bp.route('/criar', methods=['POST'])
def criar_aluno():
    dados = request.json
    result, status = alunos.adicionar_aluno(dados)
    return jsonify(result), status

@alunos_bp.route('/filtrar/<int:idAluno>', methods=['GET'])
def filtrar_aluno(idAluno):
    aluno = alunos.buscar_aluno(idAluno)
    if aluno:
        return jsonify(aluno)
    return jsonify({"error": "Aluno não encontrado"}), 404

@alunos_bp.route('/atualizar/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    dados = request.json
    result, status = alunos.atualizar_aluno(idAluno, dados)
    return jsonify(result), status

@alunos_bp.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    result, status = alunos.deletar_aluno(idAluno)
    return jsonify(result), status

@alunos_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    result, status = alunos.resetar_dados()
    return jsonify(result), status
