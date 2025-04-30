from database import db, Turma
from sqlalchemy.orm import Session

def listar_turmas(db: Session):
    turmas = db.query(Turma).all()
    return [turma.to_dict() for turma in turmas]

def adicionar_turma(db: Session, dados: dict):
    if not dados.get("nome") or not dados.get("turno"):
        return {"error": "Nome e turno são obrigatórios."}, 400

    nova_turma = Turma(
        nome=dados["nome"],
        turno=dados["turno"],
        ativo=bool(dados.get("ativo", True))
    )

    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    return {"message": "Turma criada com sucesso!", "turma": nova_turma.to_dict()}, 201

def filtrar_por_id(db: Session, idTurma: int):
    turma = db.query(Turma).filter(Turma.id == idTurma).first()
    if turma:
        return turma.to_dict_completo()
    return {"error": "Turma não encontrada."}, 404

def atualizar_turma(db: Session, idTurma: int, dados: dict):
    turma = db.query(Turma).filter(Turma.id == idTurma).first()
    if not turma:
        return {"error": "Turma não encontrada."}, 404

    if not dados.get("nome"):
        return {"error": "Turma sem nome"}, 400

    turma.nome = dados.get("nome", turma.nome)
    turma.turno = dados.get("turno", turma.turno)
    turma.ativo = dados.get("ativo", turma.ativo)

    db.commit()
    db.refresh(turma)
    return {"message": "Turma atualizada com sucesso!", "turma": turma.to_dict()}, 200

def deletar_turma(db: Session, idTurma: int):
    turma = db.query(Turma).filter(Turma.id == idTurma).first()
    if not turma:
        return {"error": "Turma não encontrada."}, 404

    db.delete(turma)
    db.commit()
    return {"message": "Turma removida com sucesso!"}, 200

def resetar_turmas(db: Session):
    db.query(Turma).delete()
    db.commit()
    return {"message": "Dados das turmas resetados com sucesso!"}, 200