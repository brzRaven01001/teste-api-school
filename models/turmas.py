from database import Base
from database import Turmas
from sqlalchemy.orm import Session

def listar_turmas(db: Session):
    return db.query(Turmas).all()

def adicionar_turma(db: Session, nome: str, turno: str, ativo: bool):
    nova_turma = Turmas(nome=nome, turno=turno, ativo=ativo)
    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    return nova_turma

def filtrar_por_id(db: Session, turma_id: int):
    return db.query(Turmas).filter(Turmas.id == turma_id).first()

def atualizar_turma(db: Session, turma_id: int, nome=None, turno=None, ativo=None):
    turma = db.query(Turmas).filter(Turmas.id == turma_id).first()
    if not turma:
        return {"error": "Turma não encontrada."}, 404

    if nome is not None:
        turma.nome = nome
    if turno is not None:
        turma.turno = turno
    if ativo is not None:
        turma.ativo = ativo

    db.commit()
    db.refresh(turma)
    return {"message": "Turma atualizada!", "turma": turma}, 200

def deletar_turma(db: Session, turma_id: int):
    turma = db.query(Turmas).filter(Turmas.id == turma_id).first()
    if not turma:
        return {"error": "Turma não encontrada."}, 404

    db.delete(turma)
    db.commit()
    return {"message": "Turma removida!"}, 200

def resetar_turmas(db: Session):
    db.query(Turmas).delete()
    db.commit()
    return {"message": "Todas as turmas foram apagadas,!"}, 200