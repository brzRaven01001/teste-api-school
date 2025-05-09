from flask_restx import Api

api = Api(
    version="1.0",
    title="API de Gerenciamento Escolar",
    description="Documentação da API para Alunos, Professores e Turmas",
    doc="/docs",
    mask_swagger=False,
    prefix="/api"
)