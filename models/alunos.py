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

def listar_alunos():
    return dici["alunos"]

def adicionar_aluno(dados):
    if not dados.get("nome") or not dados.get("idade"):
        return {"error": "Nome e idade são obrigatórios."}, 400

    if any(aluno["id"] == dados.get("id") for aluno in dici["alunos"]):
        return {"error": "ID já utilizado"}, 400

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

    dici["alunos"].append(novo_aluno)
    return {"message": "Aluno adicionado com sucesso!", "aluno": novo_aluno}, 201

def buscar_aluno(idAluno):
    return next((aluno for aluno in dici["alunos"] if aluno["id"] == idAluno), None)

def atualizar_aluno(idAluno, dados):
    if not dados.get("nome"):
        return {"error": "alunos sem nome"}, 400

    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            aluno["nome"] = dados.get("nome", aluno["nome"])
            aluno["idade"] = dados.get("idade", aluno["idade"])
            aluno["data_nascimento"] = dados.get("data_nascimento", aluno["data_nascimento"])
            aluno["nota_primeiro_semestre"] = dados.get("nota_primeiro_semestre", aluno["nota_primeiro_semestre"])
            aluno["nota_segundo_semestre"] = dados.get("nota_segundo_semestre", aluno["nota_segundo_semestre"])
            aluno["media_final"] = dados.get("media_final", aluno["media_final"])
            return {"message": "Aluno atualizado com sucesso!", "aluno": aluno}, 200
    return {"error": "Aluno não encontrado."}, 404

def deletar_aluno(idAluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == idAluno:
            dici["alunos"].remove(aluno)
            return {"message": "Aluno removido com sucesso!"}, 200
    return {"error": "Aluno não encontrado."}, 404

def resetar_dados():
    dici["alunos"].clear()
    return {"message": "Dados resetados com sucesso!"}, 200
