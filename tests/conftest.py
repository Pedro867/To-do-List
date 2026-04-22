import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Configura o client de testes do Flask."""
    app.config['TESTING'] = True

    # Cria o client de testes
    with app.test_client() as client:
        # Precisamos de um contexto de aplicação para rodar url_for, etc.
        with app.app_context():
            yield client


@pytest.fixture
def logged_in_client(client):
    """Retorna um client já com um usuário logado na sessão."""
    with client.session_transaction() as session_mock:
        session_mock['id_usuario'] = 1
    yield client


@pytest.fixture
def mock_tarefa():
    """Mocka a classe Tarefa para isolar os testes das rotas de banco de dados."""
    with patch('routes.tarefa_routes.Tarefa') as mock:
        yield mock
