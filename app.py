from flask import Flask, jsonify, request

dici = {
    "alunos": [
        {
            "id": 1,
            "nome": "Lucas Silva",
            "idade": "19"
        }
    ],
}

app = Flask(__name__)

# -------------------- ALUNOS -------------------- #

@app.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(dici["alunos"])

@app.route('/alunos', methods=['POST'])
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

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def update_aluno(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            aluno['nome'] = dados.get("nome", aluno['nome'])
            aluno['idade'] = dados.get("idade", aluno['idade'])
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@app.route("/alunos/<int:idAluno>", methods=['DELETE'])
def delete_aluno(idAluno):
    alunos = dici["alunos"]
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dici["alunos"].remove(aluno)
            return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
    return jsonify({"erro": "Aluno não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)
