from sqlalchemy.orm import Session
from database import Professores

def listar_professores(db: Session):
    return db.query(Professores).all()

def get_professor_by_id(db: Session, idProfessor: int):
    professor = db.query(Professores).filter(Professores.id == idProfessor).first()
    if professor:
        return professor
    return {"error": "Professor não encontrado"}, 404

def criar_professor(db: Session, dados: dict):
    if not dados.get("nome"):
        return {"error": "Nome é obrigatório."}, 400

    professor_existente = db.query(Professores).filter(Professores.id == dados.get("id")).first()
    if professor_existente:
        return {"error": "ID já utilizado."}, 400

    novo_professor = Professores(
        id=dados.get("id"),
        nome=dados["nome"],
        idade=dados.get("idade"),
        data_nascimento=dados.get("data_nascimento"),
        disciplina=dados.get("disciplina"),
        salario=dados.get("salario")
    )

    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return {"message": "Professor cadastrado!", "professor": novo_professor}, 201

def atualizar_professor(db: Session, idProfessor: int, dados: dict):
    professor = db.query(Professores).filter(Professores.id == idProfessor).first()
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

    return {"message": "Professor atualizado!", "professor": professor}, 200

def deletar_professor(db: Session, idProfessor: int):
    professor = db.query(Professores).filter(Professores.id == idProfessor).first()
    if not professor:
        return {"error": "Professor não encontrado."}, 404

    db.delete(professor)
    db.commit()

    return {"message": "Professor removido!"}, 200

def resetar_dados(db: Session):
    db.query(Professores).delete()
    db.commit()
    return {"message": "Dados resetados!"}, 200