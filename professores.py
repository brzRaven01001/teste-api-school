from flask import Flask, jsonify, request

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

app = Flask(__name__)

# -------------------- PROFESSORES-------------------- #

@app.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(dici["professores"])

@app.route('/professores/<int:idProfessores>', methods=['GET'])
def get_professor_by_id(idProfessores):
    # Filtra o professor pelo ID
    professor = next((prof for prof in dici["professores"] if prof["id"] == idProfessores), None)
    
    if professor:
        return jsonify(professor)
    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route('/professores', methods=['POST'])
def create_professores():
    dados = request.json
    if not dados.get("id") or not dados.get("nome"):
        return jsonify({"erro": "Nome e id são obrigatórios"}), 400

    novo_id = max([professor["id"] for professor in dici["professores"]], default=0) + 1
    novo_professor = {
        "id": novo_id,
        "nome": dados["nome"],
    }
    dici['professores'].append(novo_professor)
    return jsonify(novo_professor), 201  # Status 201 <---

@app.route("/professores/<int:idProfessores>", methods=['PUT'])
def update_professores(idProfessores):
    professores = next((professores for professores in dici["professores"] if professores["id"] == idProfessores), None)
    
    if professores:
        dados = request.json
        professores['nome'] = dados.get("nome", professores['nome'])
        return jsonify(professores)
    
    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route("/professores/<int:idProfessores>", methods=['DELETE'])
def delete_professores(idProfessores):
    professor = next((prof for prof in dici["professores"] if prof["id"] == idProfessores), None)
    
    if professor:
        dici["professores"].remove(professor)
        return jsonify({"mensagem": "Professor removido com sucesso"}), 200
    
    return jsonify({"erro": "Professor não encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)