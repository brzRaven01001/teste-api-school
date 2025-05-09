from flask_restx import Namespace, Resource, fields
from repository.alunos import listar_alunos, adicionar_aluno, filtrar_por_id, atualizar_aluno, deletar_aluno, resetar_alunos

alunos_ns = Namespace('alunos', description='Operações relacionadas a alunos')

aluno_model = alunos_ns.model('AlunoInput', {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma à qual o aluno pertence")
})

aluno_output_model = alunos_ns.model('AlunoOutput', {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "idade": fields.Integer(description="Idade do aluno"),
    "data_nascimento": fields.String(description="Data de nascimento do aluno (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(description="Nota do segundo semestre"),
    "media_final": fields.Float(description="Média final do aluno"),
    "turma": fields.List(fields.Nested(alunos_ns.model('TurmaAluno', {
        "id": fields.Integer(description="ID da turma"),
        "nome": fields.String(description="Nome da turma"),
        "turno": fields.String(description="Turno da turma"),
        "ativo": fields.Boolean(description="Status da turma"),
        "professor": fields.Nested(alunos_ns.model('ProfessorTurma', {
            "id": fields.Integer(description="ID do professor"),
            "nome": fields.String(description="Nome do professor")
        }), description="Professor responsável pela turma", allow_null=True)
    })), description="Turma à qual o aluno pertence")
})




@alunos_ns.route('/listar')
class AlunosResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model, as_list=True)
    def get(self):
        """Listar todos os alunos"""
        return listar_alunos()

@alunos_ns.route('/criar')
class CriarAlunoResource(Resource):
    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model)
    def post(self):
        """Criar um novo aluno"""
        dados = alunos_ns.payload
        return adicionar_aluno(dados)
    
@alunos_ns.route('/<int:idAluno>')
class AlunoResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, idAluno):
        """Obtém um aluno por ID"""
        return filtrar_por_id(idAluno)

    @alunos_ns.expect(aluno_model)
    @alunos_ns.marshal_with(aluno_output_model)
    def put(self, idAluno):
        """Atualizar informações de um aluno"""
        dados = alunos_ns.payload
        return atualizar_aluno(idAluno, dados)

    def delete(self, idAluno):
        """Excluir um aluno"""
        return deletar_aluno(idAluno)
    
@alunos_ns.route('/resetar')
class ResetarAlunosResource(Resource):
    def delete(self):
        """Resetar todos os alunos"""
        return resetar_alunos()