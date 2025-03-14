from flask import request, jsonify, render_template, Blueprint

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    return jsonify(dici["alunos"])

@alunos_bp.route('/', methods=['POST'])
def create_aluno():
    dados = request.json
    if not dados.get("nome") or not dados.get("idade"):
        return jsonify({"erro": "Nome e idade são obrigatórios"}), 400

    novo_id = max([aluno["id"] for aluno in dici["alunos"]], default=0) + 1
    novo_aluno = {
        "id": novo_id,
        "nome": dados["nome"],
        "idade": dados["idade"]
    }
    dici['alunos'].append(novo_aluno)
    return jsonify(novo_aluno), 201  # Status 201 <---

@alunos_bp.route("/alunos/<int:idAluno>", methods=['PUT'])
def update_aluno(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            aluno['nome'] = dados.get("nome", aluno['nome'])
            aluno['idade'] = dados.get("idade", aluno['idade'])
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@alunos_bp.route("/alunos/<int:idAluno>", methods=['DELETE'])
def delete_aluno(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dici["alunos"].remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    return jsonify({"erro": "Aluno não encontrado"}), 404
