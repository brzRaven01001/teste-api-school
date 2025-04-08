from flask import request, jsonify, Blueprint
from models import professores

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/listar', methods=['GET'])
def listar_professores():
    return jsonify(professores.listar_professores())

@professores_bp.route('/filtrar/<int:idProfessor>', methods=['GET'])
def get_professor_by_id(idProfessor):
    resultado = professores.get_professor_by_id(idProfessor)
    return jsonify(resultado[0]), resultado[1] if len(resultado) > 1 else 200

@professores_bp.route('/criar', methods=['POST'])
def criar_professor():
    try:
        dados = request.json
        resultado = professores.criar_professor(dados)
        return jsonify(resultado[0]), resultado[1] if len(resultado) > 1 else 200
    except Exception as e:
        return jsonify({'error': 'Erro inesperado.', 'details': str(e)}), 500

@professores_bp.route("/atualizar/<int:idProfessor>", methods=['PUT'])
def atualizar_professor(idProfessor):
    try:
        dados = request.json
        resultado = professores.atualizar_professor(idProfessor, dados)
        return jsonify(resultado[0]), resultado[1] if len(resultado) > 1 else 200
    except Exception as e:
        return jsonify({'error': 'Erro inesperado.', 'details': str(e)}), 500

@professores_bp.route("/<int:idProfessor>", methods=['DELETE'])
def deletar_professor(idProfessor):
    resultado = professores.deletar_professor(idProfessor)
    return jsonify(resultado[0]), resultado[1] if len(resultado) > 1 else 200

@professores_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    resultado = professores.resetar_dados()
    return jsonify(resultado[0]), resultado[1] if len(resultado) > 1 else 200
