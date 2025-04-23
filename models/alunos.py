from sqlalchemy.orm import Session
from database import Alunos

def listar_alunos(db: Session):
    return db.query(Alunos).all()

def adicionar_aluno(db: Session, dados: dict):
    if not dados.get("nome") or not dados.get("idade"):
        return {"error": "Nome e idade são obrigatórios."}, 400

    novo_aluno = Alunos(
        nome=dados["nome"],
        idade=dados["idade"],
        data_nascimento=dados.get("data_nascimento", ""),
        nota_primeiro_semestre=dados.get("nota_primeiro_semestre"),
        nota_segundo_semestre=dados.get("nota_segundo_semestre"),
        media_final=dados.get("media_final")
    )
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)

    return {"message": "Aluno adicionado com sucesso!", "aluno": novo_aluno}, 201

def buscar_aluno(db: Session, idAluno: int):
    aluno = db.query(Alunos).filter(Alunos.id == idAluno).first()
    if aluno:
        return aluno
    return {"error": "Aluno não encontrado."}, 404

def atualizar_aluno(db: Session, idAluno: int, dados: dict):
    aluno = db.query(Alunos).filter(Alunos.id == idAluno).first()
    if not aluno:
        return {"error": "Aluno não encontrado."}, 404

    if not dados.get("nome"):
        return {"error": "Aluno sem nome"}, 400

    aluno.nome = dados.get("nome", aluno.nome)
    aluno.idade = dados.get("idade", aluno.idade)
    aluno.data_nascimento = dados.get("data_nascimento", aluno.data_nascimento)
    aluno.nota_primeiro_semestre = dados.get("nota_primeiro_semestre", aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = dados.get("nota_segundo_semestre", aluno.nota_segundo_semestre)
    aluno.media_final = dados.get("media_final", aluno.media_final)

    db.commit()
    db.refresh(aluno)

    return {"message": "Aluno atualizado com sucesso!", "aluno": aluno}, 200

def deletar_aluno(db: Session, idAluno: int):
    aluno = db.query(Alunos).filter(Alunos.id == idAluno).first()
    if not aluno:
        return {"error": "Aluno não encontrado."}, 404

    db.delete(aluno)
    db.commit()
    return {"message": "Aluno removido com sucesso!"}, 200

def resetar_dados(db: Session):
    db.query(Alunos).delete()
    db.commit()
    return {"message": "Dados dos alunos resetados com sucesso!"}, 200