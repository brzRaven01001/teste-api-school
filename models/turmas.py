from sqlalchemy import Column, Integer, String, Table, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import db
from models.alunos import aluno_turma

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turno = Column(String(15), nullable=False)
    ativo = Column(Boolean)

    professor_id = Column(Integer, ForeignKey('professores.id'))
    professor = relationship('Professor', back_populates='turmas')

    alunos = relationship('Aluno', secondary=aluno_turma, back_populates='turmas')

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
            "professor_nome": self.professor.nome if self.professor else None,
            "alunos": [{"id": aluno.id, "nome": aluno.nome} for aluno in self.alunos]
        }
