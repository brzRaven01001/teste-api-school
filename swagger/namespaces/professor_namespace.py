from flask_restx import Namespace, Resource, fields
from controllers.professores import listar_professores, criar_professor, get_professor_by_id, atualizar_professor, deletar_professor, resetar_dados

professores_ns = Namespace('professores', description='Operações relacionadas a professores')

professor_model = professores_ns.model('Professor', {
    "nome": fields.String(required=True, description="Nome do professor"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "idade": fields.Integer(description="Idade do professor"),
    "disciplina": fields.String(description="Disciplina que o professor leciona"),
    "salario": fields.Float(description="Salário do professor")
})

professor_output_model = professores_ns.model('ProfessorOutput', {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "disciplina": fields.String(description="Disciplina que o professor leciona"),
    "salario": fields.Float(description="Salário do professor"),
    "turmas": fields.List(fields.Nested(professores_ns.model('Turma', {
        "id": fields.Integer(description="ID da turma"),
        "nome": fields.String(description="Nome da turma"),
        "turno": fields.String(description="Turno da turma"),
        "ativo": fields.Boolean(description="Status da turma (ativa ou não)")
    })), description="Lista de turmas que o professor leciona")
})

@professores_ns.route('/listar')
class ProfessoresResource(Resource):
    @professores_ns.marshal_with(professor_model, as_list=True)
    def get(self):
        """Listar todos os professores"""
        return listar_professores()

    
@professores_ns.route('/criar')
class CriarProfessorResource(Resource):
    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model)
    def post(self):
        """Criar um novo professor"""
        dados = professores_ns.payload
        return criar_professor(dados)

@professores_ns.route('/<int:idProfessor>')
class ProfessorResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, idProfessor):
        """Obtém um professor por ID"""
        return get_professor_by_id(idProfessor)

    @professores_ns.expect(professor_model)
    @professores_ns.marshal_with(professor_output_model)
    def put(self, idProfessor):
        """Atualizar informações de um professor"""
        dados = professores_ns.payload
        return atualizar_professor(idProfessor, dados)

    def delete(self, idProfessor):
        """Excluir um professor"""
        return deletar_professor(idProfessor)

@professores_ns.route('/resetar')
class ResetarProfessoresResource(Resource):
    def delete(self):
        """Resetar todos os professores"""
        return resetar_dados()