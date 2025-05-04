from flask_restx import Namespace, Resource, fields
from flask import request
from models import turmas
from database import db
from controllers.professores import professor_output

# Definindo o namespace para 'turmas'
turmas_bp = Namespace('turmas', description='Operações relacionadas a turmas')

# Modelo de entrada (usado para criação e atualização)
turma_model = turmas_bp.model('Turma', {
    'id': fields.Integer(readonly=True, description='ID da turma'),
    'nome': fields.String(required=True, description='Nome da turma'),
    'turno': fields.String(required=True, description='Turno da turma'),
    'ativo': fields.Boolean(description='Status de ativação da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável')
})

# Modelo de saída (usado apenas para filtro)
turma_output = turmas_bp.model('TurmaOutput', {
    'id': fields.Integer(readonly=True, description='ID da turma'),
    'nome': fields.String(description='Nome da turma'),
    'turno': fields.String(description='Turno da turma'),
    'ativo': fields.Boolean(description='Status de ativação da turma'),
    'aluno': fields.Nested({
        'id': fields.Integer(description='ID do aluno'),
        'nome': fields.String(description='Nome do aluno')
    })
})

# Endpoint para listar as turmas
@turmas_bp.route('/listar')
class ListarTurmas(Resource):
    def get(self):
        """
        Lista todas as turmas cadastradas
        """
        return turmas.listar_turmas(db.session), 200

# Endpoint para filtrar turma por ID
@turmas_bp.route('/filtrar/<int:idTurma>')
class FiltrarTurma(Resource):
    @turmas_bp.marshal_with(turma_output)
    def get(self, idTurma):
        """
        Filtra uma turma pelo ID
        """
        return turmas.filtrar_por_id(db.session, idTurma)

# Endpoint para criar uma turma
@turmas_bp.route('/criar')
class CriarTurma(Resource):
    @turmas_bp.expect(turma_model)
    def post(self):
        """
        Cria uma nova turma
        """
        dados = request.json
        nova_turma, status = turmas.adicionar_turma(db.session, dados)
        return nova_turma, status

# Endpoint para atualizar os dados de uma turma
@turmas_bp.route('/atualizar/<int:idTurma>')
class AtualizarTurma(Resource):
    @turmas_bp.expect(turma_model)
    def put(self, idTurma):
        """
        Atualiza os dados de uma turma
        """
        dados = request.json
        turma_atualizada, status = turmas.atualizar_turma(db.session, idTurma, dados)
        return turma_atualizada, status

# Endpoint para deletar uma turma
@turmas_bp.route('/<int:turma_id>')
class DeletarTurma(Resource):
    def delete(self, turma_id):
        """
        Deleta uma turma pelo ID
        """
        result, status = turmas.deletar_turma(db.session, turma_id)
        return result, status

# Endpoint para resetar os dados das turmas
@turmas_bp.route('/reseta', methods=['POST', 'DELETE'])
class ResetarTurmas(Resource):
    def post(self):
        """
        Reseta os dados das turmas
        """
        result, status = turmas.resetar_turmas(db.session)
        return result, status

    def delete(self):
        """
        Reseta os dados das turmas
        """
        result, status = turmas.resetar_turmas(db.session)
        return result, status
