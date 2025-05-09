from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import db


class Turma(db.Model):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turno = Column(String(15), nullable=False)
    ativo = Column(Boolean)

    professor_id = Column(Integer, ForeignKey('professores.id'))
    professor = relationship('Professor', back_populates='turmas')

    alunos = relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "turno": self.turno,
            "ativo": self.ativo,
            "professor_id": self.professor_id
        }
    
    def to_dict_completo(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "turno": self.turno,
            "ativo": self.ativo,
            "professor_id": self.professor_id,
            "alunos": [{"id": aluno.id, "nome": aluno.nome} for aluno in self.alunos]
        }