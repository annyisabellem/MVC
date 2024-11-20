from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    dados = request.json
    try:
        nova_atividade = atividade_model.criar_atividade(
            id_disciplina=dados['id_disciplina'],
            enunciado=dados['enunciado'],
            respostas=dados.get('respostas', [])
        )
        return jsonify({'message': 'Atividade criada com sucesso!', 'atividade': nova_atividade}), 201
    except KeyError as e:
        return jsonify({'error': f'Campo obrigatório ausente: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@atividade_bp.route('/<int:idAtividade>',methods=['PUT'])
def atualizar_atividade(idAtividade):
    data = request.json
    try:
        atividade_atualizada = atividade_model.atualizar_atividade(
            idAtividade,
            id_disciplina = data.get('id_diciplina'),
            enunciado = data.get('enunciado'),
            respostas = data.get('respostas')
        )
        return jsonify(atividade_atualizada),200
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404