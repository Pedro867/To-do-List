from flask import Blueprint, render_template, redirect, url_for, request, session
from models.tarefas import Tarefa
from utils.func import login_required
from utils.database import db

tarefa_blueprint = Blueprint('tarefa', __name__)

@tarefa_blueprint.route("/tarefa/add", methods=['POST'])
@login_required
def adicionar_tarefa():
    if request.method == 'POST':
        nome_tarefa = request.form.get('nome_tarefa')
        id_usuario  = session['id_usuario']
        if nome_tarefa and id_usuario:
            nova_tarefa = Tarefa(nome_tarefa=nome_tarefa, id_usuario=id_usuario, prioridade_tarefa=2)
            db.session.add(nova_tarefa)
            db.session.commit()

    return redirect(url_for('dashboard'))


@tarefa_blueprint.route("/tarefa/edi/<int:id_tarefa>", methods=['POST'])
@login_required
def editar_tarefa(id_tarefa):
    novo_nome_tarefa       = request.form.get('nome')
    nova_prioridade_tarefa = int(request.form.get('prioridade'))
    tarefa                 = Tarefa.select_one_tarefa(id_tarefa)

    if not novo_nome_tarefa or not nova_prioridade_tarefa:
        return {
            'status': 'erro',
            'msg'   : 'Dados da tarefa não foram recebidos'
        }, 400

    if tarefa.id_usuario == session.get('id_usuario'):
        tarefa.nome_tarefa       = novo_nome_tarefa
        tarefa.prioridade_tarefa = nova_prioridade_tarefa
        db.session.commit()

    return redirect(url_for('dashboard'))


@tarefa_blueprint.route("/tarefa/<int:id_tarefa>", methods=['DELETE'])
@login_required
def deletar_tarefa(id_tarefa):
    tarefa = Tarefa.select_one_tarefa(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        db.session.delete(tarefa)
        db.session.commit()

    return redirect(url_for('dashboard'))


@tarefa_blueprint.route('/tarefa/concluir/<int:id_tarefa>', methods=['GET'])
@login_required
def concluir(id_tarefa):
    tarefa = Tarefa.select_one_tarefa(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        tarefa.concluida = not tarefa.concluida
        db.session.commit()
        return '', 204
    return {
        'status': 'erro',
        'msg'   : 'Acesso não autorizado.'
    }, 403