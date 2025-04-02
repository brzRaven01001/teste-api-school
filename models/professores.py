from flask import request, jsonify, Blueprint

dici = {
    "professores": [
        {
            "id": 1,
            "nome": "Estevão Ferreira",
            "idade": 43,
            "data_nascimento": "01/07/1983",
            "disciplina": "Sistemas",
            "salario": 3750.00
        }
    ],
}

professor_bp = Blueprint('professor', __name__)


@professor_bp.route('/listar', methods=['GET'])
def listar_professores():
    return jsonify(dici["professores"])


@professor_bp.route('/filtrar/<int:idProfessor>', methods=['GET'])
def get_professor_by_id(idProfessor):
    professor = next((prof for prof in dici["professores"] if prof["id"] == idProfessor), None)
    
    if professor:
        return jsonify(professor)
    return jsonify({"error": "Professor não encontrado"}), 404


@professor_bp.route('/criar', methods=['POST'])
def criar_professor():
    try:
        dados = request.json

        if not dados.get("nome"):
            return jsonify({"error": "Nome é obrigatório."}), 400

        if "id" in dados and any(prof["id"] == dados["id"] for prof in dici["professores"]):
            return jsonify({"error": "ID já utilizado."}), 400

        novo_id = max([prof["id"] for prof in dici["professores"]], default=0) + 1

        novo_professor = {
            "id": dados.get("id", novo_id),
            "nome": dados["nome"],
            "idade": dados.get("idade"),
            "data_nascimento": dados.get("data_nascimento"),
            "disciplina": dados.get("disciplina"),
            "salario": dados.get("salario")
        }

        dici["professores"].append(novo_professor)

        return jsonify({"message": "Professor adicionado com sucesso!", "professor": novo_professor}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar professor.', 'details': str(e)}), 500



@professor_bp.route("/atualizar/<int:idProfessor>", methods=['PUT'])
def atualizar_professor(idProfessor):
    professor = next((prof for prof in dici["professores"] if prof["id"] == idProfessor), None)
    
    if professor:
        try:
            dados = request.json
            professor['nome'] = dados.get("nome", professor['nome'])
            professor['idade'] = dados.get("idade", professor['idade'])
            professor['data_nascimento'] = dados.get("data_nascimento", professor['data_nascimento'])
            professor['disciplina'] = dados.get("disciplina", professor['disciplina'])
            professor['salario'] = dados.get("salario", professor['salario'])
            
            return jsonify({"message": "Professor atualizado com sucesso!", "professor": professor}), 200
        except Exception as e:
            return jsonify({'error': 'Erro ao atualizar professor.', 'details': str(e)}), 500

    return jsonify({"error": "Professor não encontrado."}), 404


@professor_bp.route("/<int:idProfessor>", methods=['DELETE'])
def deletar_professor(idProfessor):
    professor = next((prof for prof in dici["professores"] if prof["id"] == idProfessor), None)
    
    if professor:
        dici["professores"].remove(professor)
        return jsonify({"message": "Professor removido com sucesso!"}), 200
    
    return jsonify({"error": "Professor não encontrado."}), 404

@professor_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    dici["professores"].clear()
    return jsonify({"message": "Dados resetados com sucesso!"}), 200