from flask_restx import Namespace, Resource, fields
from flask import request
from models import professores
from database import db


professores_bp = Namespace('professores', description='Operações relacionadas a professores')


professor_model = professores_bp.model('ProfessorInput', {
    'id': fields.Integer(readonly=True, description='ID do professor'),
    'nome': fields.String(required=True, description='Nome do professor'),
    'idade': fields.Integer(description='Idade do professor'),
    'data_nascimento': fields.String(description='Data de nascimento do professor'),
    'disciplina': fields.String(description='Disciplina do professor'),
    'salario': fields.Float(description='Salário do professor')
})


professor_output = professores_bp.model('ProfessorOutput', {
    'id': fields.Integer(readonly=True, description='ID do professor'),
    'nome': fields.String(description='Nome do professor'),
    'idade': fields.Integer(description='Idade do professor'),
    'data_nascimento': fields.String(description='Data de nascimento do professor'),
    'disciplina': fields.String(description='Disciplina do professor'),
    'salario': fields.Float(description='Salário do professor'),
    'turmas': fields.List(fields.Nested(professores_bp.model('Turma', {
        'id': fields.Integer(description='ID da turma'),
        'nome': fields.String(description='Nome da turma'),
        'turno': fields.String(description='Turno da turma'),
        'ativo': fields.Boolean(description='Status da turma')
    })))
})

@professores_bp.route('/listar')
class ListarProfessores(Resource):
    def get(self):
        """
        Lista todos os professores cadastrados
        """
        return professores.listar_professores(db.session), 200

@professores_bp.route('/filtrar/<int:idProfessor>')
class FiltrarProfessor(Resource):
    @professores_bp.marshal_with(professor_output)
    def get(self, idProfessor):
        """
        Filtra um professor pelo ID
        """
        result = professores.get_professor_by_id(db.session, idProfessor)
        if isinstance(result, tuple):
            return result
        return result

@professores_bp.route('/criar')
class CriarProfessor(Resource):
    @professores_bp.expect(professor_model)
    def post(self):
        """
        Cria um novo professor
        """
        dados = request.json
        result, status = professores.criar_professor(db.session, dados)
        return result, status

@professores_bp.route('/atualizar/<int:idProfessor>')
class AtualizarProfessor(Resource):
    @professores_bp.expect(professor_model)
    def put(self, idProfessor):
        """
        Atualiza os dados de um professor
        """
        dados = request.json
        result, status = professores.atualizar_professor(db.session, idProfessor, dados)
        return result, status

@professores_bp.route('/<int:idProfessor>')
class DeletarProfessor(Resource):
    def delete(self, idProfessor):
        """
        Deleta um professor pelo ID
        """
        result, status = professores.deletar_professor(db.session, idProfessor)
        return result, status

@professores_bp.route('/reseta', methods=['POST', 'DELETE'])
class ResetarProfessores(Resource):
    def post(self):
        """
        Reseta os dados dos professores
        """
        result, status = professores.resetar_dados(db.session)
        return result, status

    def delete(self):
        """
        Reseta os dados dos professores
        """
        result, status = professores.resetar_dados(db.session)
        return result, status
