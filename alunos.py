from flask import request, jsonify, Blueprint

dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Gustavo",
            "idade": 20,
            "data_nascimento": "15/03/2005"
        }
    ],
}

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/listar', methods=['GET'])
def listar_alunos():
    return jsonify(dici["alunos"])


@alunos_bp.route('/criar', methods=['POST'])
def criar_aluno():
    try:
        dados = request.json
        if not dados.get("nome") or not dados.get("idade"):
            return jsonify({"error": "Nome e idade são obrigatórios."}), 400

        novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
        novo_aluno = {
            "id": novo_id,
            "nome": dados["nome"],
            "idade": dados["idade"],
            "data_nascimento": dados["data_nascimento"]
        }
        dici['alunos'].append(novo_aluno)

        return jsonify({"message": "Aluno adicionado com sucesso!", "aluno": novo_aluno}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar aluno.', 'details': str(e)}), 500


@alunos_bp.route('/atualizar/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    try:
        alunos = dici["alunos"]
        for aluno in alunos:
            if aluno['id'] == idAluno:
                dados = request.json
                aluno['nome'] = dados.get("nome", aluno['nome'])
                aluno['idade'] = dados.get("idade", aluno['idade'])
                aluno['data_nascimento'] = dados.get("data_nascimento", aluno['data_nascimento'])
                return jsonify({"message": "Aluno atualizado com sucesso!", "aluno": aluno}), 200

        return jsonify({"error": "Aluno não encontrado."}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar aluno.', 'details': str(e)}), 500


@alunos_bp.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    try:
        alunos = dici["alunos"]
        for aluno in alunos:
            if aluno['id'] == idAluno:
                dici["alunos"].remove(aluno)
                return jsonify({"message": "Aluno removido com sucesso!"}), 200

        return jsonify({"error": "Aluno não encontrado."}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar aluno.', 'details': str(e)}), 500
