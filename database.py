from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from flask_sqlalchemy import SQLAlchemy

class Alunos(db.Model):
    __tablename__ = 'alunos' 
    id = Column (Integer, primary_key=True, index= True)
    nome = Column (String(100), nullable= False)
    idade = Column (Integer, nullable=False)
    data_nascimento = Column (String(20), nullable=False)
    nota_primeiro_semestre = Column (float)
    nota_segundo_semestre = Column (float)
    media_final = Column (float)

class Professores(db.Model):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(String(15), nullable=False)
    disciplina =  Column(String(100))
    salario = Column(float)

class Turmas(db.Model):
    __tablename__ = 'Turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    turno = Column(String(15), nullable=False)
    ativo = Column(bool)