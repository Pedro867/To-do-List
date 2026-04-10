from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from models.usuarios import Usuario
from utils.func import login_required

usuario_blueprint = Blueprint('usuario', __name__)

@usuario_blueprint.route("/users", methods=['GET'])
@login_required
def listar_usuarios():
    id_usuario = request.args.get('id_usuario')
    lista_adm  = request.args.get('lista_adm', 'true').lower() == 'true'

    if not id_usuario:
        return jsonify({
            'status': 'erro',
            'msg'   : 'O ID do usuário é obrigatório.'
        }), 400

    usuario_logado = Usuario.select_one_user(id_usuario)
    if not usuario_logado.adm:
        return jsonify({
            'status': 'erro',
            'msg'   : 'Acesso negado: apenas administradores podem listar usuários.'
        }), 403

    retorno = Usuario.select_all_user(lista_adm)
    if retorno.get('status') != 'ok':
        return jsonify(retorno), 500

    lista_json = []
    for user in retorno.get('list_usuarios'):
        lista_json.append({
            'id'           : user.id,
            'nome'         : user.nome,
            'email'        : user.email,
            'total_tarefas': len(user.tarefas)
        })

    return jsonify(lista_json)