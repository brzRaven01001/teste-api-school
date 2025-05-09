from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config import db

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
            "data_nascimento": self.data_nascimento,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "turma_id": self.turma_id
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
            "turma": [{"id": self.turma.id,
                "nome": self.turma.nome,
                "turno": self.turma.turno,
                "ativo": self.turma.ativo,
                "professor": {
                    "id": self.turma.professor.id,
                    "nome": self.turma.professor.nome
                } if self.turma and self.turma.professor else None
                }]
        }