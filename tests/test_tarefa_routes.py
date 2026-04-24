import pytest
from unittest.mock import MagicMock


def test_adicionar_tarefa_com_sucesso(logged_in_client, mock_tarefa):
    mock_tarefa.insert_tarefa.return_value = {'status': 'ok'}

    response = logged_in_client.post('/tarefa', data={
        'nome_tarefa'      : 'Teste Unitário',
        'prioridade_tarefa': '1'
    })

    assert response.status_code == 302
    assert '/dashboard' in response.location

    mock_tarefa.insert_tarefa.assert_called_once_with(1, 'Teste Unitário', 1)


def test_adicionar_tarefa_com_falha(logged_in_client, mock_tarefa):
    mock_tarefa.insert_tarefa.return_value = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados.'
    }

    response = logged_in_client.post('/tarefa', data={
        'nome_tarefa'      : 'Teste Unitário',
        'prioridade_tarefa': '1'
    })

    assert response.status_code == 500
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Erro interno no banco de dados.'

    mock_tarefa.insert_tarefa.assert_called_once_with(1, 'Teste Unitário', 1)


def test_adicionar_tarefa_faltando_dados(logged_in_client):
    response = logged_in_client.post('/tarefa', data={
        'nome_tarefa': 'Teste Unitário'
    })

    assert response.status_code == 400
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Dados da tarefa não foram recebidos'


def test_editar_tarefa_sucesso(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
    mock_tarefa_obj.usuario_proprietario.return_value = True

    mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
    mock_tarefa.update_tarefa.return_value     = {'status': 'ok', 'msg': 'Tarefa atualizada'}

    response = logged_in_client.put('/tarefa/5', data={
        'nome'      : 'Nome Atualizado',
        'prioridade': '2'
    })

    assert response.status_code == 200
    json_data                   = response.get_json()
    assert json_data['status']  == 'ok'
    assert '/dashboard' in json_data['url']

    mock_tarefa.update_tarefa.assert_called_once_with(5, 'Nome Atualizado', 2)


def test_editar_tarefa_com_falha(logged_in_client, mock_tarefa):
    mock_tarefa.update_tarefa.return_value = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados.'
    }

    response = logged_in_client.put('/tarefa/5', data={
        'nome'      : 'Teste Unitário',
        'prioridade': '1'
    })

    assert response.status_code == 500
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Erro interno no banco de dados.'

    mock_tarefa.update_tarefa.assert_called_once_with(5, 'Teste Unitário', 1)


def test_editar_tarefa_nao_autorizado(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
    mock_tarefa_obj.usuario_proprietario.return_value = False
    mock_tarefa.select_one_tarefa.return_value        = mock_tarefa_obj

    response = logged_in_client.put('/tarefa/5', data={
        'nome'      : 'Tentando Hackear',
        'prioridade': '3'
    })

    assert response.status_code == 401
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Essa tarefa não pertence a esse usuário.'


def test_editar_tarefa_faltando_dados(logged_in_client):
    response = logged_in_client.put('/tarefa/5', data={
        'nome': 'Teste Unitário'
    })

    assert response.status_code == 400
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Dados da tarefa não foram recebidos'


def test_deletar_tarefa_sucesso(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock()
    mock_tarefa_obj.usuario_proprietario.return_value = True

    mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
    mock_tarefa.delete_tarefa.return_value     = {'status': 'ok'}

    response = logged_in_client.delete('/tarefa/5')

    assert response.status_code == 200
    json_data                   = response.get_json()
    assert json_data['status']  == 'ok'
    assert json_data['msg']     == 'Tarefa deletada com sucesso.'

    mock_tarefa.delete_tarefa.assert_called_once_with(5)


def test_deletar_tarefa_com_falha(logged_in_client, mock_tarefa):
    mock_tarefa.delete_tarefa.return_value = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados.'
    }

    response = logged_in_client.delete('/tarefa/5')

    assert response.status_code == 500
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Erro interno no banco de dados.'

    mock_tarefa.delete_tarefa.assert_called_once_with(5)


def test_deletar_tarefa_nao_autorizado(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
    mock_tarefa_obj.usuario_proprietario.return_value = False
    mock_tarefa.select_one_tarefa.return_value        = mock_tarefa_obj

    response = logged_in_client.delete('/tarefa/5')

    assert response.status_code == 401
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Essa tarefa não pertence a esse usuário.'


def test_concluir_tarefa_sucesso(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock()
    mock_tarefa_obj.usuario_proprietario.return_value = True
    mock_tarefa_obj.concluida                         = False

    mock_tarefa.select_one_tarefa.return_value = mock_tarefa_obj
    mock_tarefa.update_tarefa.return_value     = {'status': 'ok'}

    response = logged_in_client.put('/tarefa/concluir_tarefa/5')

    assert response.status_code == 200
    json_data                   = response.get_json()
    assert json_data['status']  == 'ok'
    assert json_data['msg']     == 'Status da tarefa atualizado com sucesso.'

    mock_tarefa.update_tarefa.assert_called_once_with(
        id_tarefa        = 5,
        tarefa_concluida = True
    )


def test_concluir_tarefa_com_falha(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock()
    mock_tarefa_obj.usuario_proprietario.return_value = True
    mock_tarefa_obj.concluida                         = False
    mock_tarefa.select_one_tarefa.return_value        = mock_tarefa_obj

    mock_tarefa.update_tarefa.return_value = {
        'status': 'erro',
        'msg'   : 'Erro interno no banco de dados.'
    }

    response = logged_in_client.put('/tarefa/concluir_tarefa/5')

    assert response.status_code == 500
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Erro interno no banco de dados.'

    mock_tarefa.update_tarefa.assert_called_once_with(
        id_tarefa        = 5,
        tarefa_concluida = True
    )


def test_concluir_tarefa_nao_autorizado(logged_in_client, mock_tarefa):
    mock_tarefa_obj                                   = MagicMock() # Tarefa falsa
    mock_tarefa_obj.usuario_proprietario.return_value = False
    mock_tarefa.select_one_tarefa.return_value        = mock_tarefa_obj

    response = logged_in_client.put('/tarefa/concluir_tarefa/5')

    assert response.status_code == 401
    json_data                   = response.get_json()
    assert json_data['status']  == 'erro'
    assert json_data['msg']     == 'Essa tarefa não pertence a esse usuário.'