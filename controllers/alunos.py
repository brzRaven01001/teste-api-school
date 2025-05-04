from flask_restx import Namespace, Resource, fields
from flask import request
from models import alunos
from database import db

alunos_bp = Namespace('alunos', description='Operações relacionadas a alunos')

aluno_model = alunos_bp.model('Aluno', {
    'id': fields.Integer(readonly=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'data_nascimento': fields.String(description='Data de nascimento do aluno'),
    'nota_primeiro_semestre': fields.Float(description='Nota do primeiro semestre'),
    'nota_segundo_semestre': fields.Float(description='Nota do segundo semestre'),
    'media_final': fields.Float(description='Média final'),
    'turma_id': fields.Integer(description='ID da turma')
})

aluno_output = alunos_bp.model('AlunoOutput', {
    'id': fields.Integer(readonly=True, description='ID do aluno'),
    'nome': fields.String(description='Nome do aluno'),
    'idade': fields.Integer(description='Idade do aluno'),
    'data_nascimento': fields.String(description='Data de nascimento do aluno'),
    'nota_primeiro_semestre': fields.Float(description='Nota do primeiro semestre'),
    'nota_segundo_semestre': fields.Float(description='Nota do segundo semestre'),
    'media_final': fields.Float(description='Média final'),
    'turma': fields.Nested(alunos_bp.model('TurmaAluno', {
        'id': fields.Integer(description='ID da turma'),
        'nome': fields.String(description='Nome da turma'),
        'turno': fields.String(description='Turno da turma'),
        'ativo': fields.Boolean(description='Status da turma'),
        'professor': fields.Nested(alunos_bp.model('ProfessorTurma', {
            'id': fields.Integer(description='ID do professor'),
            'nome': fields.String(description='Nome do professor')
        }))
    }))
})


@alunos_bp.route('/listar')
class ListarAlunos(Resource):
    def get(self):
        """
        Lista todos os alunos cadastrados
        """
        return alunos.listar_alunos(db.session), 200

@alunos_bp.route('/filtrar/<int:idAluno>')
class FiltrarAluno(Resource):
    def get(self, idAluno):
        """
        Filtra um aluno pelo ID
        """
        return alunos.filtrar_por_id(db.session, idAluno)

@alunos_bp.route('/criar')
class CriarAluno(Resource):
    @alunos_bp.expect(aluno_model)
    def post(self):
        """
        Cria um novo aluno
        """
        dados = request.json
        result, status = alunos.adicionar_aluno(db.session, dados)
        return result, status

@alunos_bp.route('/atualizar/<int:idAluno>')
class AtualizarAluno(Resource):
    @alunos_bp.expect(aluno_model)
    def put(self, idAluno):
        """
        Atualiza os dados de um aluno
        """
        dados = request.json
        result, status = alunos.atualizar_aluno(db.session, idAluno, dados)
        return result, status

@alunos_bp.route('/<int:idAluno>')
class DeletarAluno(Resource):
    def delete(self, idAluno):
        """
        Deleta um aluno pelo ID
        """
        result, status = alunos.deletar_aluno(db.session, idAluno)
        return result, status

@alunos_bp.route('/reseta', methods=['POST', 'DELETE'])
class ResetarAlunos(Resource):
    def post(self):
        """
        Reseta os dados dos alunos
        """
        result, status = alunos.resetar_dados(db.session)
        return result, status

    def delete(self):
        """
        Reseta os dados dos alunos
        """
        result, status = alunos.resetar_dados(db.session)
        return result, status
