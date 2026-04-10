from flask import Blueprint, render_template, redirect, url_for, request, session
from models.tarefas import Tarefa
from utils.func import login_required
from utils.database import db

tarefa_blueprint = Blueprint('tarefa', __name__)

@tarefa_blueprint.route("/tarefa", methods=['POST'])
@login_required
def adicionar_tarefa():
    if request.method == 'POST':
        nome_tarefa       = request.form.get('nome_tarefa')
        prioridade_tarefa = int(request.form.get('prioridade_tarefa'))
        id_usuario        = session['id_usuario']
        if nome_tarefa and prioridade_tarefa and id_usuario:
            Tarefa.insert_tarefa(id_usuario, nome_tarefa, prioridade_tarefa)

    return redirect(url_for('dashboard'))


@tarefa_blueprint.route("/tarefa/<int:id_tarefa>", methods=['PUT'])
@login_required
def editar_tarefa(id_tarefa):
    novo_nome_tarefa       = request.form.get('nome')
    nova_prioridade_tarefa = int(request.form.get('prioridade'))

    if not novo_nome_tarefa or not nova_prioridade_tarefa:
        return {
            'status': 'erro',
            'msg'   : 'Dados da tarefa não foram recebidos'
        }, 400

    tarefa = Tarefa.select_one_tarefa(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        Tarefa.update_tarefa(
            id_tarefa,
            novo_nome_tarefa,
            nova_prioridade_tarefa
        )

    return {
        "status": "ok",
        "url"   : url_for('dashboard')
    }, 200


@tarefa_blueprint.route("/tarefa/<int:id_tarefa>", methods=['DELETE'])
@login_required
def deletar_tarefa(id_tarefa):
    tarefa = Tarefa.select_one_tarefa(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        Tarefa.delete_tarefa(id_tarefa)

    return {
        "status": "ok",
        "url"   : url_for('dashboard')
    }, 200


@tarefa_blueprint.route('/tarefa/concluir_tarefa/<int:id_tarefa>', methods=['PUT'])
@login_required
def concluir_tarefa(id_tarefa):
    tarefa = Tarefa.select_one_tarefa(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        Tarefa.update_tarefa(
            id_tarefa        = id_tarefa,
            tarefa_concluida = not tarefa.concluida
        )
        return {
            'status': 'ok',
            'msg'   : 'Status da tarefa atualizado com sucesso.'
        }, 204

    return {
        'status': 'erro',
        'msg'   : 'Acesso não autorizado.'
    }, 403