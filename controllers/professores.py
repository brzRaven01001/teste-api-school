from flask import Blueprint, jsonify, request
from repository import professores
from models.professores import db

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/listar', methods=['GET'])
def listar_professores():
    return jsonify(professores.listar_professores(db.session))

@professores_bp.route('/filtrar/<int:idProfessor>', methods=['GET'])
def get_professor_by_id(idProfessor):
    result = professores.get_professor_by_id(db.session, idProfessor)
    status = 200 if "error" not in result else 404
    return jsonify(result), status

@professores_bp.route('/criar', methods=['POST'])
def criar_professor():
    dados = request.json
    result, status = professores.criar_professor(db.session, dados)
    return jsonify(result), status

@professores_bp.route('/atualizar/<int:idProfessor>', methods=['PUT'])
def atualizar_professor(idProfessor):
    dados = request.json
    result, status = professores.atualizar_professor(db.session, idProfessor, dados)
    return jsonify(result), status

@professores_bp.route('/<int:idProfessor>', methods=['DELETE'])
def deletar_professor(idProfessor):
    result, status = professores.deletar_professor(db.session, idProfessor)
    return jsonify(result), status

@professores_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    result, status = professores.resetar_dados(db.session)
    return jsonify(result), status
