from flask import request, jsonify, Blueprint
from sqlalchemy import Null, null

dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Gustavo",
            "idade": 20,
            "data_nascimento": "15/03/2005",
            "nota_primeiro_semestre": 9.1,
            "nota_segundo_semestre": 7.9,
            "media_final": None
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

        if any(aluno["id"] == dados.get("id") for aluno in dici["alunos"]):
            return jsonify({"error": "ID já utilizado"}), 400

        novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
        novo_aluno = {
            "id": novo_id,
            "nome": dados["nome"],
            "idade": dados["idade"],
            "data_nascimento": dados.get("data_nascimento"),
            "nota_primeiro_semestre": dados.get("nota_primeiro_semestre"),
            "nota_segundo_semestre": dados.get("nota_segundo_semestre"),
            "media_final": dados.get("media_final")
        }
        dici['alunos'].append(novo_aluno)

        return jsonify({"message": "Aluno adicionado com sucesso!", "aluno": novo_aluno}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar aluno.', 'details': str(e)}), 500
    

@alunos_bp.route('/filtrar/<int:idAluno>', methods=['GET'])
def filtrar_aluno(idAluno):
    aluno = next((aluno for aluno in dici["alunos"] if aluno["id"] == idAluno), None)
    if aluno:
        return jsonify(aluno)
    return jsonify({"error": "Aluno não encontrado"}), 404


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
                aluno['nota_primeiro_semestre'] = dados.get("nota_primeiro_semestre", aluno['nota_primeiro_semestre'])
                aluno['nota_segundo_semestre'] = dados.get("nota_segundo_semestre", aluno['nota_segundo_semestre'])
                aluno['media_final'] = dados.get("media_final", aluno['media_final'])
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

@alunos_bp.route('/reseta', methods=['POST', 'DELETE'])
def resetar_dados():
    dici["alunos"].clear()
    return jsonify({"message": "Dados resetados com sucesso!"}), 200
