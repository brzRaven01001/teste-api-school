from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(String(20), nullable=False)
    nota_primeiro_semestre = Column(Float)
    nota_segundo_semestre = Column(Float)
    media_final = Column(Float)

    turma_id = Column(Integer, ForeignKey('turmas.id'))
    turma = relationship('Turma', back_populates='alunos')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final,
            "turma_id": self.turma_id
        }

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
            "turmas": [turma.id for turma in self.turmas]
        }

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
            "professor_id": self.professor_id,
            "alunos": [aluno.id for aluno in self.alunos]
        }
