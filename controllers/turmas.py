from flask import request, jsonify, Blueprint
from models import turmas

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/listar', methods=['GET'])
def listar_turmas():
    return jsonify(turmas.listar_turmas())

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

        nova_turma = turmas.adicionar_turma(
            nome=data["nome"],
            turno=data["turno"],
            ativo=data["ativo"]
        )
        return jsonify({'message': 'Turma adicionada com sucesso!', "turma": nova_turma}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar turma.', 'details': str(e)}), 500

@turmas_bp.route('/filtrar/<int:idTurma>', methods=['GET'])
def filtrar_turma(idTurma):
    turma = turmas.filtrar_por_id(idTurma)
    if turma:
        return jsonify(turma)
    return jsonify({"error": "Turma não encontrada"}), 404

@turmas_bp.route('/atualizar/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    try:
        data = request.json

        if not data.get('nome'):
            return jsonify({'erro': 'turmas sem nome'}), 400

        turma_atualizada = turmas.atualizar_turma(
            idTurma,
            nome=data.get('nome'),
            turno=data.get('turno'),
            ativo=data.get('ativo')
        )
        if turma_atualizada:
            return jsonify({'message': 'Turma atualizada com sucesso!'}), 200
        return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar turma.', 'details': str(e)}), 500

@turmas_bp.route('/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    try:
        if turmas.deletar_turma(turma_id):
            return jsonify({'message': 'Turma deletada com sucesso!'}), 200
        return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar turma.', 'details': str(e)}), 500

@turmas_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    turmas.resetar_turmas()
    return jsonify({"message": "Dados resetados com sucesso!"}), 200
