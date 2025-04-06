turmas = [
    {
        "id": 1,
        "nome": "Sistemas",
        "turno": "Matutino",
        "ativo": True
    }
]

def listar_turmas():
    return turmas

def adicionar_turma(nome, turno, ativo):
    novo_id = max([t["id"] for t in turmas], default=0) + 1
    nova_turma = {"id": novo_id, "nome": nome, "turno": turno, "ativo": bool(ativo)}
    turmas.append(nova_turma)
    return nova_turma

def filtrar_por_id(turma_id):
    return next((t for t in turmas if t["id"] == turma_id), None)

def atualizar_turma(turma_id, nome=None, turno=None, ativo=None):
    turma = filtrar_por_id(turma_id)
    if turma:
        turma["nome"] = nome if nome is not None else turma["nome"]
        turma["turno"] = turno if turno is not None else turma["turno"]
        turma["ativo"] = ativo if ativo is not None else turma["ativo"]
        return turma
    return None

def deletar_turma(turma_id):
    turma = filtrar_por_id(turma_id)
    if turma:
        turmas.remove(turma)
        return True
    return False

def resetar_turmas():
    turmas.clear()
