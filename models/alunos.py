from database import db, Aluno
from sqlalchemy.orm import Session

def listar_alunos(db: Session):
    alunos = db.query(Aluno).all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(db: Session, dados: dict):
    if not dados.get("nome") or not dados.get("idade"):
        return {"error": "Nome e idade são obrigatórios."}, 400

    novo_aluno = Aluno(
        nome=dados["nome"],
        idade=dados["idade"],
        data_nascimento=dados.get("data_nascimento"),
        nota_primeiro_semestre=dados.get("nota_primeiro_semestre"),
        nota_segundo_semestre=dados.get("nota_segundo_semestre"),
        media_final=dados.get("media_final")
    )

    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return {"message": "Aluno adicionado com sucesso!", "aluno": novo_aluno.to_dict()}, 201

def filtrar_por_id(db: Session, idAluno: int):
    aluno = db.query(Aluno).filter(Aluno.id == idAluno).first()
    if aluno:
        return aluno.to_dict_completo()
    return {"error": "Aluno não encontrado"}

def atualizar_aluno(db: Session, idAluno: int, dados: dict):
    aluno = db.query(Aluno).filter(Aluno.id == idAluno).first()
    if not aluno:
        return {"error": "Aluno não encontrado"}, 404

    aluno.nome = dados.get("nome", aluno.nome)
    aluno.idade = dados.get("idade", aluno.idade)
    aluno.data_nascimento = dados.get("data_nascimento", aluno.data_nascimento)
    aluno.nota_primeiro_semestre = dados.get("nota_primeiro_semestre", aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = dados.get("nota_segundo_semestre", aluno.nota_segundo_semestre)
    aluno.media_final = dados.get("media_final", aluno.media_final)
    aluno.turma_id = dados.get("turma_id", aluno.turma_id)


    db.commit()
    db.refresh(aluno)
    return {"message": "Aluno atualizado com sucesso!", "aluno": aluno.to_dict()}, 200

def deletar_aluno(db: Session, idAluno: int):
    aluno = db.query(Aluno).filter(Aluno.id == idAluno).first()
    if not aluno:
        return {"error": "Aluno não encontrado"}, 404

    db.delete(aluno)
    db.commit()
    return {"message": "Aluno removido com sucesso!"}, 200

def resetar_alunos(db: Session):
    db.query(Aluno).delete()
    db.commit()
    return {"message": "Dados dos alunos resetados com sucesso!"}, 200
