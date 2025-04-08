professores = {
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

def listar_professores():
    return professores

def get_professor_by_id(idProfessor):
    professor = next((prof for prof in professores["professores"] if prof["id"] == idProfessor), None)
    if professor:
        return professor,
    return {"error": "Professor não encontrado"}, 404

def criar_professor(dados):
    if not dados.get("nome"):
        return {"error": "Nome é obrigatório."}, 400

    if "id" in dados and any(prof["id"] == dados["id"] for prof in professores["professores"]):
        return {"error": "ID já utilizado."}, 400

    novo_id = max([prof["id"] for prof in professores["professores"]], default=0) + 1

    novo_professor = {
        "id": dados.get("id", novo_id),
        "nome": dados["nome"],
        "idade": dados.get("idade"),
        "data_nascimento": dados.get("data_nascimento"),
        "disciplina": dados.get("disciplina"),
        "salario": dados.get("salario")
    }

    professores["professores"].append(novo_professor)
    return {"message": "Professor cadastrado com sucesso!", "professor": novo_professor}, 201

def atualizar_professor(idProfessor, dados):
    professor = next((prof for prof in professores["professores"] if prof["id"] == idProfessor), None)
    if professor:
        if "nome" not in dados or not dados["nome"]:
            return {"error": "Professor sem nome"}, 400

        professor['nome'] = dados.get("nome", professor['nome'])
        professor['idade'] = dados.get("idade", professor['idade'])
        professor['data_nascimento'] = dados.get("data_nascimento", professor['data_nascimento'])
        professor['disciplina'] = dados.get("disciplina", professor['disciplina'])
        professor['salario'] = dados.get("salario", professor['salario'])

        return {"message": "Professor atualizado com sucesso!", "professor": professor}, 200

    return {"error": "Professor não encontrado."}, 404

def deletar_professor(idProfessor):
    professor = next((prof for prof in professores["professores"] if prof["id"] == idProfessor), None)
    if professor:
        professores["professores"].remove(professor)
        return {"message": "Professor removido com sucesso!"}, 200

    return {"error": "Professor não encontrado."}, 404

def resetar_dados():
    professores["professores"].clear()
    return {"message": "Dados resetados com sucesso!"}, 200
