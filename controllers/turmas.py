from flask import Blueprint, jsonify, request
from repository import turmas
from models.turmas import db

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/listar', methods=['GET'])
def listar_turmas():
    try:
        turmas_listadas = turmas.listar_turmas(db.session)
        return jsonify(turmas_listadas), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao listar turmas.', 'details': str(e)}), 500

@turmas_bp.route('/criar', methods=['POST'])
def criar_turma():
    try:
        data = request.json

        if not data.get("nome"):
            return jsonify({'error': 'Turma sem nome'}), 400
        if not data.get("turno"):
            return jsonify({'error': 'Turma sem turno'}), 400
        if "ativo" not in data:
            return jsonify({'error': 'Campo "ativo" obrigatório'}), 400

        nova_turma, status = turmas.adicionar_turma(db.session, data)
        return jsonify(nova_turma), status
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar turma.', 'details': str(e)}), 500

@turmas_bp.route('/filtrar/<int:idTurma>', methods=['GET'])
def filtrar_turma(idTurma):
    try:
        turma = turmas.filtrar_por_id(db.session, idTurma)       
        if "error" in turma:
            return jsonify(turma), 404
        return jsonify(turma), 200
    
    except Exception as e:
        return jsonify({'error': 'Erro ao filtrar turma.', 'details': str(e)}), 500

@turmas_bp.route('/atualizar/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    try:
        data = request.json

        if not data.get('nome'):
            return jsonify({'error': 'Turma sem nome'}), 400

        turma_atualizada, status = turmas.atualizar_turma(db.session, idTurma, data)
        if turma_atualizada:
            return jsonify(turma_atualizada), status
        return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar turma.', 'details': str(e)}), 500

@turmas_bp.route('/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    try:
        result, status = turmas.deletar_turma(db.session, turma_id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar turma.', 'details': str(e)}), 500

@turmas_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    try:
        result, status = turmas.resetar_turmas(db.session)
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': 'Erro ao resetar dados.', 'details': str(e)}), 500
