from flask import request, jsonify, Blueprint

dici = {
    "turmas": [
        {
            "id": 1,
            "nome": "Sistemas",
            "turno": "Matutino",
            "ativo": True
        }
    ],
}

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/listar', methods=['GET'])
def listar_turmas():
    return jsonify(dici["turmas"])

@turmas_bp.route('/criar', methods=['POST'])
def criar_turma():
    try:
        data = request.json

        novo_id = max([turma["id"] for turma in dici["turmas"]], default=0) + 1
        nova_turma = {
            "id": novo_id,
            "nome": data["nome"],
            "turno": data["turno"],
            "ativo": bool(data["ativo"])
        }
        dici['turmas'].append(nova_turma)

        return jsonify({'message': 'Turma adicionada com sucesso!', "turma": nova_turma}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar turma.', 'details': str(e)}), 500
    
@turmas_bp.route('/filtrar/<int:idTurma>', methods=['GET'])
def filtrar_turma(idTurma):
    turma = next((turma for turma in dici["turmas"] if turma["id"] == idTurma), None)
    
    if turma:
        return jsonify(turma)
    return jsonify({"error": "Turma não encontrado"}), 404

@turmas_bp.route('/atualizar/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    turmas = dici['turmas']

    try:
        data = request.json
        for turma in turmas:
            if turma['id'] == idTurma:
                turma['nome'] = data.get('nome', turma['nome'])
                turma['turno'] = data.get('turno', turma['turno'])
                turma['ativo'] = data.get('ativo', turma['ativo'])
                return jsonify({'message': 'Turma atualizada com sucesso!'}), 200

        return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar turma.', 'details': str(e)}), 500


@turmas_bp.route('/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    try:
        turmas = dici['turmas']
        for turma in turmas:
            if turma['id'] == turma_id:
                dici['turmas'].remove(turma)
                return jsonify({'message': 'Turma deletada com sucesso!'}), 200

        return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar turma.', 'details': str(e)}), 500

@turmas_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    dici["turmas"].clear()
    return jsonify({"message": "Dados resetados com sucesso!"}), 200