from flask_restx import Namespace, Resource, fields
from controllers.turmas import listar_turmas, criar_turma, filtrar_turma, atualizar_turma, deletar_turma, resetar_dados

turmas_ns = Namespace('turmas', description='Operações relacionadas a turmas')

turma_model = turmas_ns.model('Turma', {
    "nome": fields.String(required=True, description="Nome da turma"),
    "turno": fields.String(required=True, description="Turno da turma (Matutino, Vespertino ou Noturno)"),
    "ativo": fields.Boolean(required=True, description="Status da turma (ativa ou inativa)"),
    "professor_id": fields.Integer(required=True, description="ID do professor associado"),
})

turma_output_model = turmas_ns.model('TurmaOutput', {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
    "turno": fields.String(description="Turno da turma"),
    "ativo": fields.Boolean(description="Status da turma (ativa ou não)"),
    "professor_id": fields.Integer(description="ID do professor responsável pela turma"),
    "alunos": fields.List(fields.Nested(turmas_ns.model('Aluno', {
        "id": fields.Integer(description="ID do aluno"),
        "nome": fields.String(description="Nome do aluno")
    })), description="Lista de alunos da turma")
})


@turmas_ns.route('/listar')
class TurmasResource(Resource):
    @turmas_ns.marshal_with(turma_model, as_list=True)
    def get(self):
        """Listar todas as turmas"""
        return listar_turmas()

@turmas_ns.route('/criar')
class CriarTurmaResource(Resource):
    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model)
    def post(self):
        """Criar uma nova turma"""
        dados = turmas_ns.payload
        return criar_turma(dados)

@turmas_ns.route('/<int:idTurma>')
class TurmaResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, idTurma):
        """Obtém uma turma por ID"""
        return filtrar_turma(idTurma)

    @turmas_ns.expect(turma_model)
    @turmas_ns.marshal_with(turma_output_model)
    def put(self, idTurma):
        """Atualizar informações de uma turma"""
        dados = turmas_ns.payload
        return atualizar_turma(idTurma, dados)

    def delete(self, idTurma):
        """Excluir uma turma"""
        return deletar_turma(idTurma)
    
@turmas_ns.route('/resetar')
class ResetarTurmasResource(Resource):
    def delete(self):
        """Resetar todas as turmas"""
        return resetar_dados()