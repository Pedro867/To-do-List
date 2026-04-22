import pytest
from app import app
from unittest.mock import patch, MagicMock

def test_adicionar_tarefa_com_sucesso(client):
    with patch('routes.tarefa_routes.Tarefa') as mock_tarefa:
        mock_tarefa.insert_tarefa.return_value = {'status': 'ok'}

        with client.session_transaction() as session_mock:
            session_mock['id_usuario'] = 1

        response = client.post('/tarefa', data={
            'nome_tarefa'      : 'Teste Unitário',
            'prioridade_tarefa': '1'
        })

        assert response.status_code == 302
        assert '/dashboard' in response.location

        mock_tarefa.insert_tarefa.assert_called_once_with(1, 'Teste Unitário', 1)


def test_adicionar_tarefa_faltando_dados(client):
    with client.session_transaction() as session_mock:
        session_mock['id_usuario'] = 1

    response = client.post('/tarefa', data={
        'nome_tarefa': 'Teste Unitário'
    })

    assert response.status_code == 400
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Dados da tarefa não foram recebidos'


def test_editar_tarefa_sucesso(client):
    with patch('routes.tarefa_routes.Tarefa') as mock_tarefa:
        mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
        mock_tarefa_obj.usuario_proprietario.return_value = True

        mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
        mock_tarefa.update_tarefa.return_value     = {'status': 'ok', 'msg': 'Tarefa atualizada'}

        with client.session_transaction() as session_mock:
            session_mock['id_usuario'] = 1

        response = client.put('/tarefa/5', data={
            'nome'      : 'Nome Atualizado',
            'prioridade': '2'
        })

        assert response.status_code == 200
        json_data                   = response.get_json()
        assert json_data['status']  == 'ok'
        assert '/dashboard' in json_data['url']

        mock_tarefa.update_tarefa.assert_called_once_with(5, 'Nome Atualizado', 2)


def test_editar_tarefa_nao_autorizado(client):
    with patch('routes.tarefa_routes.Tarefa') as mock_tarefa:
        mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
        mock_tarefa_obj.usuario_proprietario.return_value = False
        mock_tarefa.select_one_tarefa.return_value        = mock_tarefa_obj

        with client.session_transaction() as session_mock:
            session_mock['id_usuario'] = 1

        response = client.put('/tarefa/5', data={
            'nome'      : 'Tentando Hackear',
            'prioridade': '3'
        })

        assert response.status_code == 401
        json_data                   = response.get_json()
        assert json_data['status']  == 'erro'
        assert json_data['msg']     == 'Essa tarefa não pertence a esse usuário.'


def test_deletar_tarefa_sucesso(client):
    with patch('routes.tarefa_routes.Tarefa') as mock_tarefa:
        mock_tarefa_obj                                   = MagicMock()
        mock_tarefa_obj.usuario_proprietario.return_value = True

        mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
        mock_tarefa.delete_tarefa.return_value     = {'status': 'ok'}

        with client.session_transaction() as session_mock:
            session_mock['id_usuario'] = 1

        response = client.delete('/tarefa/5')

        assert response.status_code == 200
        json_data                   = response.get_json()
        assert json_data['status']  == 'ok'
        assert json_data['msg']     == 'Tarefa deletada com sucesso.'

        mock_tarefa.delete_tarefa.assert_called_once_with(5)


def test_concluir_tarefa_sucesso(client):
    with patch('routes.tarefa_routes.Tarefa') as mock_tarefa:
        mock_tarefa_obj                                   = MagicMock()
        mock_tarefa_obj.usuario_proprietario.return_value = True
        mock_tarefa_obj.concluida                         = False

        mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
        mock_tarefa.update_tarefa.return_value     = {'status': 'ok'}

        with client.session_transaction() as session_mock:
            session_mock['id_usuario'] = 1

        response = client.put('/tarefa/concluir_tarefa/5')

        assert response.status_code == 200
        json_data                   = response.get_json()
        assert json_data['status']  == 'ok'
        assert json_data['msg']     == 'Status da tarefa atualizado com sucesso.'

        mock_tarefa.update_tarefa.assert_called_once_with(
            id_tarefa        = 5,
            tarefa_concluida = True
        )
