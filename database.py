from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean

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

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final
        }

class Professores(db.Model):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(String(15), nullable=False)
    disciplina = Column(String(100))
    salario = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "disciplina": self.disciplina,
            "salario": self.salario
        }

class Turmas(db.Model):
    __tablename__ = 'Turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turno = Column(String(15), nullable=False)
    ativo = Column(Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "turno": self.turno,
            "ativo": self.ativo
        }
