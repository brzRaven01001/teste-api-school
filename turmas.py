from flask import request, jsonify, render_template, Blueprint
from database import SessionLocal
from models import Turma 

turmas_bp = Blueprint('turmas', __name__)


@turmas_bp.route('/', methods=['POST'])
def adicionar_turma():
    try:
        data = request.json
        session = SessionLocal()

        nova_turma = Turma(
            nome=data['nome'],  
            semestre=data['semestre'],  
            quantidade_alunos=data['quantidade_alunos'] 
        )

        session.add(nova_turma)
        session.commit()
        session.close()

        return jsonify({'message': 'Turma adicionada com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': 'Erro ao adicionar turma.', 'details': str(e)}), 500
    


@turmas_bp.route('/listar', methods=['GET'])
def listar_turmas():
    try:
        session = SessionLocal()
        turmas = session.query(Turma).all()  
        session.close()

        turmas_lista = []
        for turma in turmas:
            turmas_lista.append({
                'id': turma.id,
                'nome': turma.nome,
                'semestre': turma.semestre,
                'quantidade_alunos': turma.quantidade_alunos
            })

        return jsonify({'turmas': turmas_lista})
    except Exception as e:
        return jsonify({'error': 'Erro ao listar turmas.', 'details': str(e)}), 500

    
@turmas_bp.route('/atualizar', methods=['PUT'])
def atualizar_turmas():
    try:
        data = request.json
        session = SessionLocal()

        turma = session.query(Turma).filter(Turma.id == turma_id).first()

        if turma:
            turma.nome = data.get('nome')
            turma.semestre = data.get ('semestre')
            turma.quantidade_alunos = data.get('quantidade_alunos')

            session.commit()
            session.close()

            return jsonify({'message': 'Turma atualizada!'}),200
        else:
            session.close()
            return jsonify({'error': 'Turma não encontrada'}),404
    except Exception as e:
        return jsonify ({'error': 'Erro ao atualizar turma', 'details': str(e)}), 500


@turmas_bp.route('/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    try:
        session = SessionLocal()

        turma = session.query(Turma).filter(Turma.id == turma_id).first()

        if turma:
            session.delete(turma)
            session.commit()
            session.close()

            return jsonify({'message': 'Turma deletada!'}), 200
        else:
            session.close()
            return jsonify({'error': 'Turma não encontrada.'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar turma.', 'details': str(e)}), 500