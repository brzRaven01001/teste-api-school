from models.professores import db, Professor
from models.turmas import db, Turma
from sqlalchemy.orm import Session

def listar_professores(db: Session):
    professores = db.query(Professor).all()
    return [professor.to_dict() for professor in professores]

def get_professor_by_id(db: Session, idProfessor: int):
    professor = db.query(Professor).filter(Professor.id == idProfessor).first()
    if professor:
        return professor.to_dict_completo()
    return {"error": "Professor não encontrado"}, 404

def criar_professor(db: Session, dados: dict):
    if not dados.get("nome"):
        return {"error": "Nome é obrigatório."}, 400

    if dados.get("id"):
        professor_existente = db.query(Professor).filter(Professor.id == dados.get("id")).first()
        if professor_existente:
            return {"error": "ID já utilizado."}, 400

    novo_professor = Professor(
        id=dados.get("id"),
        nome=dados["nome"],
        idade=dados.get("idade"),
        data_nascimento=dados.get("data_nascimento"),
        disciplina=dados.get("disciplina"),
        salario=dados.get("salario")
    )

    turma_ids = dados.get("turma_ids")
    if turma_ids:
        turmas = db.query(Turma).filter(Turma.id.in_(turma_ids)).all()
        if len(turmas) != len(turma_ids):
            return {"error": "Uma ou mais turmas não encontradas."}, 400
        novo_professor.turmas = turmas

    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return {
        "message": "Professor cadastrado com sucesso!",
        "professor": novo_professor.to_dict()
    }, 201

def atualizar_professor(db: Session, idProfessor: int, dados: dict):
    professor = db.query(Professor).filter(Professor.id == idProfessor).first()
    if not professor:
        return {"error": "Professor não encontrado."}, 404

    if "nome" not in dados or not dados["nome"]:
        return {"error": "Professor sem nome"}, 400

    professor.nome = dados.get("nome", professor.nome)
    professor.idade = dados.get("idade", professor.idade)
    professor.data_nascimento = dados.get("data_nascimento", professor.data_nascimento)
    professor.disciplina = dados.get("disciplina", professor.disciplina)
    professor.salario = dados.get("salario", professor.salario)

    db.commit()
    db.refresh(professor)

    return {"message": "Professor atualizado com sucesso!", "professor": professor.to_dict()}, 200

def deletar_professor(db: Session, idProfessor: int):
    professor = db.query(Professor).filter(Professor.id == idProfessor).first()
    if not professor:
        return {"error": "Professor não encontrado."}, 404

    db.delete(professor)
    db.commit()

    return {"message": "Professor removido com sucesso!"}, 200

def resetar_dados(db: Session):
    db.query(Professor).delete()
    db.commit()
    return {"message": "Dados resetados com sucesso!"}, 200