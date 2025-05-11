from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import db


class Professor(db.Model):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(String(15), nullable=False)
    disciplina = Column(String(100))
    salario = Column(Float)

    turmas =  relationship('Turma', back_populates='professor', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "disciplina": self.disciplina,
            "salario": self.salario,
        }

    def to_dict_completo(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "disciplina": self.disciplina,
            "salario": self.salario,
            "turmas": [{
                "id": turma.id,
                "nome": turma.nome,
                "turno": turma.turno,
                "ativo": turma.ativo
            }
            for turma in self.turmas]
        }
