from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from config import db

aluno_turma = Table('aluno_turma', db.Model.metadata,
    Column('aluno_id', Integer, ForeignKey('alunos.id'), primary_key=True),
    Column('turma_id', Integer, ForeignKey('turmas.id'), primary_key=True)
)

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(String(20), nullable=False)
    nota_primeiro_semestre = Column(Float)
    nota_segundo_semestre = Column(Float)
    media_final = Column(Float)


    turmas = relationship('Turma', secondary=aluno_turma, back_populates='alunos')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "turma_id": [turma.id for turma in self.turmas]
        }
    
    def to_dict_completo(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final,
            "turma": [{"id": turma.id,
                        "nome": turma.nome,
                        "turno": turma.turno,
                        "ativo": turma.ativo,
                        "professor_id": turma.professor_id} for turma in self.turmas]
        }